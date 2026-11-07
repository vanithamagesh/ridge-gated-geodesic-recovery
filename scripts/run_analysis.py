import argparse, json, sys, time
from pathlib import Path
import numpy as np
from scipy.stats import wilcoxon

ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from rgr.recovery import threshold, hysteresis, closing3, rgr, rgr_p, dice_safe_rgr, DICE_SAFE_GATES
from rgr.metrics import counts, aggregate, per_image, admissible
from rgr.data import load_eval, median_fov_diameter, stare_pathology, DRIVE_VALID
from rgr.baselines import dti_released, select_threshold, rgr_seeded, dense_crf
from rgr.measures import (extra_counts, pooled_extra, vessel_measures, measurement_errors, bootstrap_ci, holm,
                          ece, reliability, HistogramBinning, Isotonic)
from rgr.bridges import classify_bridges, summarise, optic_disc, rescore_unannotated
from rgr.analysis import dice_rule, gate_choice, missed_thin, observer2, dice_safe

ap = argparse.ArgumentParser()
ap.add_argument("--dataset", required=True); ap.add_argument("--root", type=Path, required=True)
ap.add_argument("--drive-root", type=Path, required=True, help="DRIVE folder: validation images for thresholds and calibration")
ap.add_argument("--probs", type=Path, required=True); ap.add_argument("--out", type=Path, required=True)
ap.add_argument("--seeds", type=int, nargs="+", default=[7]); ap.add_argument("--archs", nargs="+", default=["unet", "attunet", "unetpp"])
ap.add_argument("--pathology", type=Path, help="STARE all-mg-codes.txt")
ap.add_argument("--no-crf", action="store_true"); ap.add_argument("--boot", type=int, default=10000)
ap.add_argument("--crf-grid", choices=["full", "small"], default="full", help="small: two CRF settings only")
ap.add_argument("--fast", action="store_true", help="coarser sweeps (step 0.05) and downstream measurements for four procedures only (FIVES)")
a = ap.parse_args(); a.out.mkdir(parents=True, exist_ok=True); t0 = time.time()
log = lambda *x: print(f"[{time.time() - t0:6.0f} s]", *x, flush=True)

CRF = not a.no_crf

K = 1.0 if a.dataset == "drive" else median_fov_diameter(a.root) / median_fov_diameter(a.drive_root)
DL = int(round(8 * K)); RK = "rfk" if K != 1.0 else "rf"
path = stare_pathology(a.pathology) if a.pathology else None
test = load_eval(a.root, "test", k=K, pathology=path)
val = load_eval(a.drive_root, "train", cases=DRIVE_VALID)
log(f"{a.dataset}: {len(test)} test images, k = {K:.4f}, distance limit {DL} px")
for d in test: d["od"] = optic_disc(d["img"], d["f"], d["y"], K)
P = lambda arch, seed, D, ds=None: [np.load(a.probs / f"{ds or a.dataset}_{arch}_s{seed}_{d['case']}.npy").astype(np.float32) for d in D]


MEASURED = ("threshold_0.5", "rgr", "dice_safe_rgr", "hysteresis_0.25")


def run(fn, probs, D, name):
    rows, xrows, meas = [], [], []
    with_meas = (not a.fast) or name in MEASURED
    for p, d in zip(probs, D):
        m = fn(p, d); seed = threshold(p, d["f"])
        rows.append(counts(m, d, seed)); xrows.append(extra_counts(m, d))
        if with_meas:
            if "ref_meas" not in d: d["ref_meas"] = vessel_measures(d["y"], d["f"], d["k"])
            meas.append(measurement_errors(vessel_measures(m, d["f"], d["k"]), d["ref_meas"]))
    r = aggregate(rows); r.update(pooled_extra(xrows))
    if meas:
        r["measurements"] = {k: dict(mean_error=float(np.mean([e[k] for e in meas])), mean_abs_error=float(np.mean([abs(e[k]) for e in meas]))) for k in meas[0]}
        r["per_image_measurements"] = meas
    return r, rows


for seed in a.seeds:
    for arch in a.archs:
        f_out = a.out / f"{a.dataset}_{arch}_s{seed}.json"
        if f_out.exists(): log(f"skip {f_out.name} (exists)"); continue
        PT = P(arch, seed, test); PV = P(arch, seed, val, "drive")
        res = dict(dataset=a.dataset, arch=arch, seed=seed, k=K, dl=DL, cases=[d["case"] for d in test])
        t_sel, dice_sel = select_threshold(PV, val); res["selected_threshold"] = dict(threshold=t_sel, validation_dice=dice_sel)
        R = lambda **kw: (lambda p, d: rgr(p, d["f"], d[RK], **{**dict(tp=0.25, tv=0.05, dl=DL), **kw}))
        M = {"threshold_0.5": lambda p, d: threshold(p, d["f"]),
             "threshold_selected": lambda p, d: threshold(p, d["f"], t_sel),
             "threshold_0.25": lambda p, d: threshold(p, d["f"], 0.25),
             "hysteresis_0.25": lambda p, d: hysteresis(p, d["f"], 0.25),
             "dti_described_0.3": lambda p, d: hysteresis(p, d["f"], 0.3),
             "dti_released_0.3": lambda p, d: dti_released(p, d["f"], 0.5, 0.3),
             "closing_3x3": lambda p, d: closing3(p, d["f"]),
             "rgr": R(), "dice_safe_rgr": lambda p, d: dice_safe_rgr(p, d["f"], d[RK], 0.05, DL)}
        M["rgr_on_selected"] = lambda p, d: rgr_seeded(p, d["f"], d[RK], t_sel, 0.25, 0.05, DL)
        base_v = aggregate([counts(threshold(p, d["f"]), d, threshold(p, d["f"])) for p, d in zip(PV, val)])
        pres = []
        for cfg in [dict(R=R, theta=th) for R in (8, 12, 16) for th in (0.3, 0.4, 0.5, 0.6)]:
            r = aggregate([counts(rgr_p(p, d["f"], d["rf"], 0.25, 0.05, 8, cfg["R"], cfg["theta"]), d, threshold(p, d["f"])) for p, d in zip(PV, val)])
            pres.append((cfg, r))
        def pick(eps):
            adm = [(c, r) for c, r in pres if admissible(r, base_v, eps)]
            if adm: c, r = max(adm, key=lambda z: z[1]["thin_centre"]); return c, r, "admissible"
            c, r = max(pres, key=lambda z: z[1]["dice"]); return c, r, "max_dice"
        cp, rp, howp = pick(0.005); cq, rq, howq = pick(1.0)
        FIXED = dict(R=8, theta=0.3)
        res["rgr_p_setting"] = {"rgr_p": dict(**FIXED, rule="fixed"),
                                "rgr_p_selected": dict(**cp, rule=howp, validation_dice=rp["dice"], validation_thin_centre=rp["thin_centre"]),
                                "rgr_p_recall": dict(**cq, rule=howq, validation_dice=rq["dice"], validation_thin_centre=rq["thin_centre"])}
        log(f"{arch} s{seed} RGR-P: fixed {FIXED}; re-selected conservative {cp} ({howp}), recall-oriented {cq} ({howq})")
        M["rgr_p"] = lambda p, d, c=FIXED: rgr_p(p, d["f"], d[RK], 0.25, 0.05, DL, int(round(c["R"] * K)), c["theta"])
        M["rgr_p_selected"] = lambda p, d, c=cp: rgr_p(p, d["f"], d[RK], 0.25, 0.05, DL, int(round(c["R"] * K)), c["theta"])
        M["rgr_p_recall"] = lambda p, d, c=cq: rgr_p(p, d["f"], d[RK], 0.25, 0.05, DL, int(round(c["R"] * K)), c["theta"])
        if CRF:
            grid = ([dict(w_gauss=g, w_bil=w, sxy_bil=sx, srgb=sr) for g in (0.0, 0.5) for w in (0.25, 0.5, 1.0, 2.0, 4.0) for sx in (2.0, 4.0) for sr in (5.0, 15.0)]
                    if a.crf_grid == "full" else [dict(w_gauss=0.0, w_bil=0.25, sxy_bil=2.0, srgb=5.0), dict(w_gauss=0.0, w_bil=1.0, sxy_bil=2.0, srgb=15.0)])
            res["crf_grid"] = a.crf_grid
            best_adm = best_dice = None
            for cfg in grid:
                fn = lambda p, d, c=cfg: dense_crf(p, d["img"], d["f"], w_gauss=c["w_gauss"], w_bil=c["w_bil"], sxy_bil=c["sxy_bil"], srgb=c["srgb"])
                r = aggregate([counts(fn(p, d), d, threshold(p, d["f"])) for p, d in zip(PV, val)])
                if admissible(r, base_v) and (best_adm is None or r["thin_centre"] > best_adm[0]["thin_centre"]): best_adm = (r, cfg)
                if best_dice is None or r["dice"] > best_dice[0]["dice"]: best_dice = (r, cfg)
            r_sel, cfg = best_adm if best_adm else best_dice
            res["crf_setting"] = dict(**cfg, rule="eq25" if best_adm else "max_dice", validation_dice=r_sel["dice"], validation_thin_centre=r_sel["thin_centre"])
            log(f"{arch} s{seed} CRF setting {cfg} by {'the selection rule' if best_adm else 'max Dice'}")
            M["dense_crf"] = lambda p, d, c=cfg: dense_crf(p, d["img"], d["f"], w_gauss=c["w_gauss"], w_bil=c["w_bil"], sxy_bil=c["sxy_bil"] * (K if K > 1 else 1), srgb=c["srgb"])
        res["procedures"], rows = {}, {}
        for name, fn in M.items():
            r, rw = run(fn, PT, test, name); res["procedures"][name] = r; rows[name] = rw
            log(f"{arch} s{seed} {name:22} dice {r['dice']:.4f} prec {r['precision']:.4f} tc {r['thin_centre']:.4f} cl {r['cldice']:.4f} "
                f"frag {r['components']:.1f} b0err {r['betti0_error']:.1f} b1err {r['betti1_error']:.1f} skF1 {r['skeleton_f1']:.4f}")
        sweep = {}
        st = 0.05 if a.fast else 0.02
        for name, mk, grid in (("threshold", lambda t: (lambda p, d: threshold(p, d["f"], t)), np.round(np.arange(0.30, 0.71, st), 2)),
                               ("hysteresis", lambda t: (lambda p, d: hysteresis(p, d["f"], t)), np.round(np.arange(0.20, 0.50, st), 2)),
                               ("dti_released", lambda t: (lambda p, d: dti_released(p, d["f"], 0.5, t)), np.round(np.arange(0.20, 0.50, st), 2)),
                               ("rgr", lambda t: R(tp=t), (0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45))):
            sweep[name] = []
            for t in grid:
                rr = aggregate([counts(mk(float(t))(p, d), d, threshold(p, d["f"])) for p, d in zip(PT, test)])
                sweep[name].append(dict(t=float(t), **{x: rr[x] for x in ("precision", "thin_centre", "dice", "cldice", "components")}))
        v = res["procedures"]["rgr"]; eq = {}
        for name in ("threshold", "hysteresis", "dti_released"):
            c = sorted(sweep[name], key=lambda z: z["precision"])
            eq[name] = {x: float(np.interp(v["precision"], [z["precision"] for z in c], [z[x] for z in c])) for x in ("thin_centre", "dice", "cldice", "components")}
        eq["rgr"] = {x: v[x] for x in ("thin_centre", "dice", "cldice", "components", "precision")}
        res["sweep"], res["equal_precision"] = sweep, eq
        log(f"{arch} s{seed} equal precision: tc rgr {v['thin_centre']:.4f} thr {eq['threshold']['thin_centre']:.4f} hyst {eq['hysteresis']['thin_centre']:.4f}; "
            f"clDice rgr {v['cldice']:.4f} thr {eq['threshold']['cldice']:.4f}; frag rgr {v['components']:.1f} thr {eq['threshold']['components']:.1f}")
        res["bridges"], res["dice_rule"], res["gate_choice"], res["missed_thin"], res["observer2"] = {}, {}, [], [], {}
        for name in ("rgr", "dice_safe_rgr", "rgr_p", "rgr_p_selected", "rgr_p_recall"):
            allb = []; rules = []; obs = []
            for p, d in zip(PT, test):
                m = M[name](p, d); seed_m = threshold(p, d["f"])
                bs = rescore_unannotated(classify_bridges(m, seed_m, d, od=d["od"]), m, seed_m, d); allb += [dict(case=d["case"], **b) for b in bs]
                rules.append(dice_rule(p, d, m))
                o = observer2(m, seed_m, d)
                if o: obs.append(o)
            res["bridges"][name] = dict(summary=summarise(allb), bridges=allb)
            res["dice_rule"][name] = rules
            if obs: res["observer2"][name] = obs
            s = res["bridges"][name]["summary"]["all"]
            agree = sum(r["predicted_rise"] == r["observed_rise"] for r in rules if r["added"])
            log(f"{arch} s{seed} {name}: {s['n']} bridges, correct {s['correct']} shortcut {s['shortcut']} offset {s['offset']} unannotated {s['unannotated']}; "
                f"Dice rule right on {agree}/{sum(1 for r in rules if r['added'])} images")
        for p, d in zip(PT, test):
            res["gate_choice"].append(gate_choice(p, d, d[RK], 0.05, DL)); res["missed_thin"].append(missed_thin(p, d))
        if res["observer2"]:
            yv = np.concatenate([d["y2"][d["f"]] for d in test]); y1 = np.concatenate([d["y"][d["f"]] for d in test])
            c1 = np.concatenate([d["centre"][d["f"]] for d in test])
            res["observer2"]["human"] = dict(dice_obs2_vs_obs1=float(2 * (yv & y1).sum() / (yv.sum() + y1.sum())),
                                              thin_centre_recall_obs2=float((yv & c1).sum() / c1.sum()),
                                              precision_obs2=float((yv & y1).sum() / yv.sum()))
        pv = np.concatenate([p[d["f"]] for p, d in zip(PV, val)]); yvv = np.concatenate([d["y"][d["f"]] for d in val])
        pt = np.concatenate([p[d["f"]] for p, d in zip(PT, test)]); yt = np.concatenate([d["y"][d["f"]] for d in test])
        res["calibration"] = dict(ece_test=ece(pt, yt), reliability_test=reliability(pt, yt), ece_validation=ece(pv, yvv))
        for cname, cal in (("histogram_binning", HistogramBinning(15).fit(pv, yvv)), ("isotonic", Isotonic().fit(pv, yvv))):
            qt = [cal(p) for p in PT]
            rows_c = []; rules = []
            for p, q, d in zip(PT, qt, test):
                m, g = dice_safe(p, d["f"], d[RK], 0.05, DL, DICE_SAFE_GATES, q=q)
                rows_c.append(counts(m, d, threshold(p, d["f"]))); rules.append(dice_rule(p, d, m, q=q))
            r = aggregate(rows_c); r["ece_test_recalibrated"] = ece(np.concatenate([q[d["f"]] for q, d in zip(qt, test)]), yt)
            r["dice_rule"] = rules
            res["calibration"][f"dice_safe_{cname}"] = {k: r[k] for k in ("dice", "precision", "thin_centre", "cldice", "components", "ece_test_recalibrated", "dice_rule")}
            log(f"{arch} s{seed} conservative gate with {cname}: dice {r['dice']:.4f} tc {r['thin_centre']:.4f} ECE {r['ece_test_recalibrated']:.4f}")
        base = rows["threshold_0.5"]; res["bootstrap"] = {}; pvals = {}
        for name in ("rgr", "dice_safe_rgr", "rgr_p", "rgr_p_selected", "rgr_p_recall", "hysteresis_0.25", "threshold_0.25", "dti_released_0.3", "threshold_selected", "rgr_on_selected") + (("dense_crf",) if CRF else ()):
            rw = rows[name]; n = len(rw); bo = {}
            for key, fn in (("thin_centre", lambda idx, R_: sum(R_[i]["c_tp"] for i in idx) / sum(R_[i]["c_n"] for i in idx)),
                            ("dice", lambda idx, R_: 2 * sum(R_[i]["tp"] for i in idx) / sum(2 * R_[i]["tp"] + R_[i]["fp"] + R_[i]["fn"] for i in idx)),
                            ("precision", lambda idx, R_: sum(R_[i]["tp"] for i in idx) / max(sum(R_[i]["tp"] + R_[i]["fp"] for i in idx), 1)),
                            ("components", lambda idx, R_: np.mean([R_[i]["comp"] for i in idx]))):
                est, lo, hi = bootstrap_ci(lambda idx: 100 * (fn(idx, rw) - fn(idx, base)) if key != "components" else fn(idx, rw) - fn(idx, base), n, a.boot, seed=0)
                bo[key] = dict(gain=est, ci_low=lo, ci_high=hi)
            res["bootstrap"][name] = bo
            for key in ("tc", "dice"):
                diff = per_image(rw, key) - per_image(base, key)
                pvals[f"{name}:{key}"] = float(wilcoxon(diff).pvalue) if np.any(diff) else 1.0
        adj = holm(list(pvals.values()))
        res["wilcoxon"] = {k: dict(p=p, p_holm=q) for (k, p), q in zip(pvals.items(), adj)}
        b = res["bootstrap"]["rgr"]
        log(f"{arch} s{seed} RGR gains: tc {b['thin_centre']['gain']:+.2f} [{b['thin_centre']['ci_low']:+.2f}, {b['thin_centre']['ci_high']:+.2f}] "
            f"dice {b['dice']['gain']:+.2f} [{b['dice']['ci_low']:+.2f}, {b['dice']['ci_high']:+.2f}] pp")
        json.dump(res, open(f_out, "w"), default=float)
        log(f"written {f_out}")
log("done")
