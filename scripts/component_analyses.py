"""Analyses of the paper that need the photographs and references, computed from the stored seed-7 probability maps:

  gates       share of missed thin-vessel and background pixels accepted on the four DRIVE validation images (Fig. 3)
  ablation    RGR with one component removed, with the margin over a threshold sweep at equal precision (Fig. 8, Table S8)
  radius      recall gain by vessel radius, share of correct additions on thin vessels, distance of false additions (Fig. 5)
  measures    error of vessel measurements against the reference (Table 7)
  observer2   share of false additions that lie on second-observer vessels (CHASE_DB1, STARE)

    python scripts/component_analyses.py --probs outputs/probs --drive-root work/sgl/dataset \
        --chase-root outputs/data/chase --stare-root outputs/data/stare --out outputs/component_analyses
"""
import argparse, json, sys
from pathlib import Path
import numpy as np
from scipy import ndimage as ndi

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rgr import ridge_from_probability, ridge_map, rgr, gap_join, threshold, hysteresis
from rgr.recovery import B3
from rgr.data import load_eval
from rgr.measures import vessel_measures, measurement_errors

ap = argparse.ArgumentParser()
ap.add_argument("--probs", type=Path, required=True); ap.add_argument("--out", type=Path, required=True)
ap.add_argument("--drive-root", type=Path); ap.add_argument("--chase-root", type=Path); ap.add_argument("--stare-root", type=Path)
ap.add_argument("--seed", type=int, default=7)
a = ap.parse_args(); a.out.mkdir(parents=True, exist_ok=True)
K = {"drive": 1.0, "chase": 1.7030142191255204, "stare": 1.186063452949269}
ROOT = {d: r for d, r in (("drive", a.drive_root), ("chase", a.chase_root), ("stare", a.stare_root)) if r}
ARCHS = ("unet", "attunet", "unetpp"); VALID = {"22", "27", "34", "39"}
def prob(ds, arch, case): return np.load(a.probs / f"{ds}_{arch}_s{a.seed}_{case}.npy").astype(np.float32)
def masks(p, d):
    k = d["k"]; dl = int(round(8 * k)); f = d["f"]; rp = ridge_from_probability(p, f, k)
    m = dict(seed=threshold(p, f), hyst=hysteresis(p, f, 0.25), photo=rgr(p, f, d["rfk"] if k != 1.0 else d["rf"], 0.25, 0.05, dl), rgr=rgr(p, f, rp, 0.25, 0.05, dl),
             noridge=rgr(p, f, rp, 0.25, 0.05, dl, use_ridge=False), nodist=rgr(p, f, rp, 0.25, 0.05, dl, use_distance=False),
             noconn=rgr(p, f, rp, 0.25, 0.05, dl, use_connectivity=False), nopg=rgr(p, f, rp, 0.0, 0.05, dl))
    m["join"] = gap_join(p, f, m["rgr"], k); return m, rp
OUT = {}
# ---------------------------------------------------------------- gates on the DRIVE validation images
if "drive" in ROOT:
    g = {}
    for arch in ARCHS:
        acc = {}
        for d in load_eval(ROOT["drive"], "train", cases=VALID, k=1.0):
            p = prob("drive", arch, d["case"]); f = d["f"]; seed = p >= 0.5
            zone = f & ~seed & (ndi.distance_transform_edt(~seed) <= 8); rp = ridge_from_probability(p, f, 1.0)
            thin = d["y"] & (d["lr"] <= 2); bg = ~d["y"]
            for src, r, use in (("ridge off", rp, False), ("photograph ridge", d["rf"], True), ("probability-map ridge", rp, True)):
                add = rgr(p, f, r, 0.25, 0.05, 8, use_ridge=use) & ~seed & zone
                for cls, c in (("thin", thin), ("background", bg)):
                    t = acc.setdefault(f"{src}|{cls}", [0, 0]); t[0] += int((add & c).sum()); t[1] += int((zone & c).sum())
        g[arch] = {key: 100 * v[0] / v[1] for key, v in acc.items()}
    OUT["gates_drive_validation_percent"] = g
# ---------------------------------------------------------------- per test image
GRID = np.round(np.arange(0.20, 0.701, 0.02), 2)
VAR = ("seed", "hyst", "photo", "rgr", "join", "noridge", "nodist", "noconn", "nopg")
BINS = [(0, 1.0), (1.0, 2.0), (2.0, 3.0), (3.0, 99.0)]; DB = [(0, 1.5), (1.5, 3), (3, 5), (5, 1e9)]
for ds, root in ROOT.items():
    for arch in ARCHS:
        cnt = {v: np.zeros(4) for v in VAR}; sweep = np.zeros((len(GRID), 3)); cn = 0
        rad = {}; meas = {}; obs = [0, 0]; frag = {v: 0 for v in VAR}; n_img = 0
        for d in load_eval(root, "test", k=K[ds]):
            p = prob(ds, arch, d["case"]); f, y, ce = d["f"], d["y"], d["centre"]; m, _ = masks(p, d); n_img += 1; cn += int(ce.sum())
            for i, t in enumerate(GRID):
                mm = (p >= t) & f; sweep[i] += [(mm & y).sum(), (mm & ~y).sum(), (mm & ce).sum()]
            ref = vessel_measures(y, f, K[ds])
            for v in VAR:
                mm = m[v] & f; cnt[v] += [(mm & y).sum(), (mm & ~y).sum(), (mm & ce).sum(), (y & f).sum()]
                frag[v] += ndi.label(mm, B3)[1]
                if v in ("seed", "photo", "rgr", "join", "hyst"):
                    for i, (lo, hi) in enumerate(BINS):
                        b = y & f & (d["lr"] > lo) & (d["lr"] <= hi)
                        t_ = rad.setdefault(f"{v}|recall|{i}", [0, 0]); t_[0] += int((mm & b).sum()); t_[1] += int(b.sum())
                    add = mm & ~m["seed"]; t_ = rad.setdefault(f"{v}|thin_share", [0, 0]); t_[0] += int((add & y & (d["lr"] <= 2)).sum()); t_[1] += int((add & y).sum())
                    fa = add & ~y
                    for i, (lo, hi) in enumerate(DB):
                        t_ = rad.setdefault(f"{v}|false_distance|{i}", [0, 0]); t_[0] += int((fa & (d["dy"] > lo) & (d["dy"] <= hi)).sum()); t_[1] += int(fa.sum())
                    e = measurement_errors(vessel_measures(mm, f, K[ds]), ref)
                    for key in ("density", "length", "branch_points", "end_points", "fractal_dimension"): meas.setdefault(f"{v}|{key}", []).append(float(e[key]))
            if d.get("y2") is not None:
                fa = m["rgr"] & ~m["seed"] & f & ~y; obs[0] += int(fa.sum()); obs[1] += int((fa & d["y2"]).sum())
        pr = 100 * sweep[:, 0] / sweep[:, :2].sum(1); tc = 100 * sweep[:, 2] / cn; o = np.argsort(pr)
        res = {}
        for v in VAR:
            tp, fp, ctp, yy = cnt[v]; pv = 100 * tp / (tp + fp); tv = 100 * ctp / cn
            res[v] = dict(precision=pv, thin_centreline_recall=tv, dice=100 * 2 * tp / (tp + fp + yy), fragments=frag[v] / n_img,
                          margin=float(tv - np.interp(pv, pr[o], tc[o])), outside_sweep=bool(not pr.min() <= pv <= pr.max()))
        OUT[f"{ds}.{arch}"] = dict(procedures=res, radius={k_: 100 * v[0] / max(v[1], 1) for k_, v in rad.items()},
                                   measurement_error={k_: float(np.mean(v)) for k_, v in meas.items()},
                                   false_additions_on_second_observer_percent=(100 * obs[1] / obs[0]) if obs[0] else None)
        r = res["rgr"]; print(f"{ds} {arch}: RGR margin {r['margin']:+.2f}, TCR {r['thin_centreline_recall']:.2f}, precision {r['precision']:.2f}, fragments {r['fragments']:.1f}", flush=True)
json.dump(OUT, open(a.out / "component_analyses.json", "w"), indent=1)
print("written", a.out / "component_analyses.json")
