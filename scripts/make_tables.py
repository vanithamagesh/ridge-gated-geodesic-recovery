import argparse, csv, json
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import numpy as np

ap = argparse.ArgumentParser(); ap.add_argument("--rev", type=Path, required=True); ap.add_argument("--out", type=Path, required=True)
ap.add_argument("--main-seed", type=int, default=7)
a = ap.parse_args(); a.out.mkdir(parents=True, exist_ok=True)
R = [json.load(open(f)) for f in sorted(a.rev.glob("*.json"))]
DS = {"drive": "DRIVE", "chase": "CHASE_DB1", "stare": "STARE", "fives": "FIVES"}
NET = {"unet": "U-Net", "attunet": "Attention U-Net", "unetpp": "U-Net++"}
PROC = [("threshold_0.5", "Threshold 0.5"), ("threshold_selected", "Threshold selected on validation"), ("threshold_0.25", "Threshold 0.25"),
        ("hysteresis_0.25", "Hysteresis 0.25"), ("dti_described_0.3", "DTI as described (0.5 to 0.3)"), ("dti_released_0.3", "DTI as released (0.5, 0.3)"),
        ("dense_crf", "Dense CRF"), ("closing_3x3", "Closing 3 x 3"), ("rgr", "RGR"), ("rgr_on_selected", "RGR on the selected threshold"),
        ("dice_safe_rgr", "Conservative-gate RGR"), ("rgr_p", "RGR-P"), ("rgr_p_selected", "RGR-P, setting re-selected per run"), ("rgr_p_recall", "RGR-P, recall-oriented")]
VLAB = {"rgr": "RGR", "dice_safe_rgr": "Conservative-gate RGR", "rgr_p": "RGR-P", "rgr_p_selected": "RGR-P, setting re-selected per run", "rgr_p_recall": "RGR-P, recall-oriented"}
order = lambda r: (list(DS).index(r["dataset"]), list(NET).index(r["arch"]), r["seed"])
R.sort(key=order)
main = [r for r in R if r["seed"] == a.main_seed]


def pct(x, nd=1):
    q = Decimal(1).scaleb(-nd)
    return str(Decimal(repr(float(x) * 100)).quantize(q, rounding=ROUND_HALF_UP))


def f4(x): return f"{x:.4f}"


def write(name, header, rows, caption):
    with open(a.out / f"{name}.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)
    md.append(f"\n**{name}.** {caption}\n\n| " + " | ".join(header) + " |\n|" + "---|" * len(header) + "\n" + "\n".join("| " + " | ".join(map(str, r)) + " |" for r in rows) + "\n")


md = []
rows = []
for r in main:
    for key, label in PROC:
        p = r["procedures"].get(key)
        if p is None: continue
        rows.append([DS[r["dataset"]], NET[r["arch"]], label, f4(p["dice"]), f4(p["precision"]), f4(p["recall"]), f4(p["thin_centre"]), f4(p["cldice"]),
                     f"{p['components']:.1f}", f"{p['betti0_error']:.1f}", f"{p['betti1_error']:.1f}", f4(p["skeleton_f1"]), f4(p["mcc"]),
                     f4(p["accuracy"]), f4(p["specificity"]), f4(p["sensitivity"])])
write("T_matched", ["Dataset", "Network", "Procedure", "Dice", "Pre", "Rec", "TCR", "clDice", "Frag", "Betti-0 err", "Betti-1 err", "Skel F1", "MCC", "Acc", "Spe", "Sen"], rows,
      "Matched comparison of refinement procedures applied to identical probability maps (seed 7). Frag: components per image; Betti errors: mean absolute difference to the reference per image; Skel F1: skeleton F1 at 2 DRIVE-equivalent pixels.")
rows = []
for r in main:
    e = r["equal_precision"]
    for key, label in (("rgr", "RGR"), ("threshold", "Threshold"), ("hysteresis", "Hysteresis"), ("dti_released", "DTI as released")):
        v = e[key]
        rows.append([DS[r["dataset"]], NET[r["arch"]], label, f4(e["rgr"]["precision"]), f4(v["thin_centre"]), f4(v["dice"]), f4(v["cldice"]), f"{v['components']:.1f}"])
write("T_equal", ["Dataset", "Network", "Procedure", "Precision", "TCR", "Dice", "clDice", "Frag"], rows,
      "Values at the precision of the selected RGR setting; threshold, hysteresis and DTI values are interpolated along their test-set sweeps (retrospective).")
rows = []
for ds in DS:
    for var in ("rgr", "dice_safe_rgr", "rgr_p", "rgr_p_selected", "rgr_p_recall"):
        agg = defaultdict(lambda: defaultdict(int)); n_r = 0
        for r in main:
            if r["dataset"] != ds or var not in r["bridges"]: continue
            n_r += 1
            for ctx, c in r["bridges"][var]["summary"].items():
                for k, v in c.items(): agg[ctx][k] += v
        if not n_r: continue
        for ctx, lab in (("all", "all bridges"), ("junction", "near a junction or crossing"), ("adjacent", "closely adjacent vessels"), ("optic_disc", "optic-disc region"), ("pathology", "images with pathology"), ("none_of_these", "none of these")):
            c = agg[ctx]; n = c["n"]
            if n == 0 and ctx != "all": continue
            o2 = f"{c['unannotated_obs2_vessel']}/{c['unannotated_scored_obs2']}" if c["unannotated_scored_obs2"] else "-"
            rows.append([DS[ds], VLAB[var], lab, n, c["correct"], pct(c["correct"] / max(n, 1)), c["shortcut"], c["offset"], c["unannotated"], o2])
write("T_bridges", ["Dataset", "Variant", "Context", "Bridges", "Correct", "Correct (%)", "Shortcut", "Offset", "Unannotated", "Unannotated on observer-2 vessel"], rows,
      "Reconnection analysis of bridges (added components joining two or more seed fragments), pooled over the three networks (seed 7).")
rows = []
for r in main:
    for var in ("rgr", "dice_safe_rgr"):
        d = [x for x in r["dice_rule"][var] if x["added"]]
        agree = sum(x["predicted_rise"] == x["observed_rise"] for x in d)
        dis = [abs(x["dice_change"]) * 100 for x in d if x["predicted_rise"] != x["observed_rise"]]
        bias_d = np.mean([x["d_hat"] - x["true_dice"] for x in d]) * 100; bias_p = np.mean([x["p_hat"] - x["true_precision"] for x in d]) * 100
        rows.append([DS[r["dataset"]], NET[r["arch"]], "RGR" if var == "rgr" else "Conservative-gate RGR", len(d), agree, sum(x["predicted_rise"] for x in d), sum(x["observed_rise"] for x in d),
                     f"{max(dis):.2f}" if dis else "-", f"{bias_d:+.1f}", f"{bias_p:+.1f}"])
write("T_dicerule", ["Dataset", "Network", "Variant", "Images", "Direction right", "Predicted rise", "Observed rise", "Largest Dice error when wrong (pp)", "Bias of est. Dice (pp)", "Bias of est. precision (pp)"], rows,
      "The reference-free Dice rule (Eqs. S5 and S6) evaluated prospectively: the direction of the Dice change predicted from the probabilities against the observed direction, per image.")
rows = []
for r in main:
    g = r["gate_choice"]; n = len(g)
    same = sum(x["chosen"] == x["optimum"] for x in g)
    within = sum(x["chosen"] is not None and x["optimum"] is not None and abs(x["chosen"] - x["optimum"]) <= 0.051 for x in g) + sum(x["chosen"] is None and x["optimum"] is None for x in g)
    gap = np.mean([x["dice_optimum"] - x["dice_chosen"] for x in g]) * 100
    rose = sum(x["dice_chosen"] > x["dice_seed"] for x in g); fell = sum(x["dice_chosen"] < x["dice_seed"] for x in g)
    rows.append([DS[r["dataset"]], NET[r["arch"]], n, same, within, rose, fell, f"{gap:.2f}", f"{np.mean([x['dice_optimum'] - x['dice_seed'] for x in g]) * 100:.2f}"])
write("T_gate", ["Dataset", "Network", "Images", "Chosen = optimum", "Within one step", "Dice rose", "Dice fell", "Mean Dice left on the table (pp)", "Mean Dice gain of the optimum (pp)"], rows,
      "Gate chosen by the conservative-gate rule per image against the gate that maximises the true Dice of that image (gates 0.45 to 0.15 or no addition).")
rows = []
for r in main:
    for key, label in (("threshold_0.5", "Threshold 0.5"), ("rgr", "RGR"), ("dice_safe_rgr", "Conservative-gate RGR"), ("hysteresis_0.25", "Hysteresis 0.25")):
        m = r["procedures"][key]["measurements"]
        rows.append([DS[r["dataset"]], NET[r["arch"]], label] + [f"{m[q]['mean_error']:+.1f} ({m[q]['mean_abs_error']:.1f})" for q in ("density", "length", "branch_points", "end_points")] +
                    [f"{m['fractal_dimension']['mean_error']:+.3f} ({m['fractal_dimension']['mean_abs_error']:.3f})"])
write("T_measure", ["Dataset", "Network", "Mask", "Density (pp)", "Centreline length (%)", "Branch points (%)", "End points (%)", "Fractal dimension"], rows,
      "Downstream measurements: mean signed error against the reference over test images (mean absolute error in brackets). Branch and end points after removing spurs of at most 5 DRIVE-equivalent pixels.")
def holm(pv):
    pv = np.asarray(pv, float); m = len(pv); order = np.argsort(pv); adj = np.empty(m); run = 0.0
    for rank, i in enumerate(order): run = max(run, min(1.0, (m - rank) * pv[i])); adj[i] = run
    return adj
PROCS_B = (("rgr", "RGR"), ("dice_safe_rgr", "Conservative-gate RGR"), ("rgr_p", "RGR-P"), ("rgr_p_selected", "RGR-P, setting re-selected per run"), ("rgr_p_recall", "RGR-P, recall-oriented"), ("hysteresis_0.25", "Hysteresis 0.25"), ("threshold_selected", "Threshold selected"), ("dense_crf", "Dense CRF"), ("dti_released_0.3", "DTI as released"))
HOLM = {}
for key, _ in PROCS_B:
    for met in ("tc", "dice"):
        rs = [r for r in main if key in r["bootstrap"]]
        for r, q in zip(rs, holm([r["wilcoxon"][f"{key}:{met}"]["p"] for r in rs]) if rs else []): HOLM[(r["dataset"], r["arch"], key, met)] = q
rows = []
for r in main:
    for key, label in PROCS_B:
        b = r["bootstrap"].get(key)
        if b is None: continue
        w = r["wilcoxon"]; ht, hd = HOLM[(r["dataset"], r["arch"], key, "tc")], HOLM[(r["dataset"], r["arch"], key, "dice")]
        rows.append([DS[r["dataset"]], NET[r["arch"]], label,
                     f"{b['thin_centre']['gain']:+.2f} [{b['thin_centre']['ci_low']:+.2f}, {b['thin_centre']['ci_high']:+.2f}]",
                     f"{b['dice']['gain']:+.2f} [{b['dice']['ci_low']:+.2f}, {b['dice']['ci_high']:+.2f}]",
                     f"{b['precision']['gain']:+.2f} [{b['precision']['ci_low']:+.2f}, {b['precision']['ci_high']:+.2f}]",
                     f"{b['components']['gain']:+.1f} [{b['components']['ci_low']:+.1f}, {b['components']['ci_high']:+.1f}]",
                     f"{w[key + ':tc']['p']:.2g} / {ht:.2g}", f"{w[key + ':dice']['p']:.2g} / {hd:.2g}"])
write("T_boot", ["Dataset", "Network", "Procedure", "dTCR (pp) [95% CI]", "dDice (pp) [95% CI]", "dPrecision (pp) [95% CI]", "dFrag [95% CI]", "p TCR (raw / Holm)", "p Dice (raw / Holm)"], rows,
      "Change relative to the 0.5 threshold with bootstrap 95% percentile intervals over images (10,000 resamples) and two-sided Wilcoxon p-values; Holm adjustment over the dataset-network tests of each procedure and measure.")
rows = []
for r in main:
    c = r["calibration"]; p0 = r["procedures"]["dice_safe_rgr"]
    rows.append([DS[r["dataset"]], NET[r["arch"]], "none (published rule)", f"{c['ece_test']:.4f}", f4(p0["dice"]), f4(p0["thin_centre"]), f"{p0['components']:.1f}"])
    for key, label in (("dice_safe_histogram_binning", "histogram binning (15 bins)"), ("dice_safe_isotonic", "isotonic regression")):
        q = c[key]
        rows.append([DS[r["dataset"]], NET[r["arch"]], label, f"{q['ece_test_recalibrated']:.4f}", f4(q["dice"]), f4(q["thin_centre"]), f"{q['components']:.1f}"])
write("T_calib", ["Dataset", "Network", "Recalibration (fitted on 4 DRIVE validation images)", "ECE on test", "Dice", "TCR", "Frag"], rows,
      "Conservative-gate RGR with the estimates of Eq. S5 computed from bin-wise recalibrated probabilities; the gates stay on the network probability.")
rows = []
for r in main:
    o = r.get("observer2") or {}
    if "human" not in o: continue
    h = o["human"]
    for var in ("rgr", "dice_safe_rgr", "rgr_p", "rgr_p_selected", "rgr_p_recall"):
        if var not in o: continue
        s = {k: sum(x[k] for x in o[var]) for k in ("added", "false_obs1", "vessel_obs2", "near_obs2", "true_obs2")}
        rows.append([DS[r["dataset"]], NET[r["arch"]], VLAB[var], pct(h["thin_centre_recall_obs2"]), f4(h["dice_obs2_vs_obs1"]),
                     s["added"], s["false_obs1"], pct(s["vessel_obs2"] / max(s["false_obs1"], 1)), pct(s["near_obs2"] / max(s["false_obs1"], 1)), pct(s["true_obs2"] / max(s["added"], 1))])
if rows:
    write("T_obs2", ["Dataset", "Network", "Variant", "Observer-2 TCR vs observer 1 (%)", "Dice obs2 vs obs1", "Added pixels", "False by observer 1", "Of these: vessel by observer 2 (%)", "Within 1.5 px of observer-2 vessel (%)", "Added pixels on observer-2 vessel (%)"], rows,
          "Second observer: thin-centreline recall of observer 2 against observer 1 (the human ceiling) and the additions of RGR re-scored against observer 2.")
rows = []
for r in main:
    H = np.sum([x["hist_near"] for x in r["missed_thin"]], 0); n = H.sum()
    band = H[5:].sum()
    rows.append([DS[r["dataset"]], NET[r["arch"]], int(n), pct(band / n), pct(H[7:].sum() / n), pct(H[:5].sum() / n)])
write("T_missed", ["Dataset", "Network", "Missed thin-vessel pixels within 8k px of the seed", "p in [0.25, 0.5) (%)", "p in [0.35, 0.5) (%)", "p < 0.25 (%)"], rows,
      "Network probability of reference thin-vessel pixels removed by the 0.5 threshold, within the distance limit of the seed.")
seeds = sorted(set(r["seed"] for r in R))
if len(seeds) > 1:
    rows = []
    for ds in DS:
        for arch in NET:
            rs = [r for r in R if r["dataset"] == ds and r["arch"] == arch]
            if len(rs) < 2: continue
            def ms(fn): v = [fn(r) for r in rs]; return f"{np.mean(v):+.2f} +- {np.std(v):.2f}"
            rows.append([DS[ds], NET[arch], len(rs), ms(lambda r: r["bootstrap"]["rgr"]["thin_centre"]["gain"]), ms(lambda r: r["bootstrap"]["rgr"]["dice"]["gain"]),
                         ms(lambda r: r["bootstrap"]["dice_safe_rgr"]["thin_centre"]["gain"]), ms(lambda r: r["bootstrap"]["dice_safe_rgr"]["dice"]["gain"]),
                         ms(lambda r: r["bootstrap"]["rgr_p"]["thin_centre"]["gain"]) if all("rgr_p" in r["bootstrap"] for r in rs) else "-",
                         ms(lambda r: r["bootstrap"]["rgr_p"]["dice"]["gain"]) if all("rgr_p" in r["bootstrap"] for r in rs) else "-",
                         ms(lambda r: r["bootstrap"]["rgr_p"]["components"]["gain"]) if all("rgr_p" in r["bootstrap"] for r in rs) else "-",
                         ms(lambda r: 100 * (r["equal_precision"]["rgr"]["thin_centre"] - r["equal_precision"]["threshold"]["thin_centre"])),
                         ms(lambda r: 100 * (r["equal_precision"]["rgr"]["cldice"] - r["equal_precision"]["threshold"]["cldice"]))])
    write("T_seeds", ["Dataset", "Network", "Seeds", "RGR dTCR", "RGR dDice", "Conservative gate dTCR", "Conservative gate dDice", "RGR-P dTCR", "RGR-P dDice", "RGR-P dFrag", "Margin TCR at equal precision", "Margin clDice at equal precision"], rows,
          "Mean +- SD over training seeds of the changes relative to the 0.5 threshold (percentage points).")
(a.out / "tables.md").write_text("\n".join(md))
print("written", a.out / "tables.md", "and", len(list(a.out.glob("*.csv"))), "CSV files")
