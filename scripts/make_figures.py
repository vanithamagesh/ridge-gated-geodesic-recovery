import argparse, json, sys
from collections import defaultdict
from pathlib import Path
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import ndimage as ndi

ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from rgr.recovery import threshold, rgr, rgr_p
from rgr.data import load_eval, median_fov_diameter

plt.rcParams.update({"font.weight": "bold", "axes.labelweight": "bold", "axes.titleweight": "bold", "font.size": 8,
                     "axes.titlesize": 8, "axes.labelsize": 8, "legend.fontsize": 7, "xtick.labelsize": 7, "ytick.labelsize": 7,
                     "figure.dpi": 100, "savefig.dpi": 600, "pdf.fonttype": 42})
DS = {"drive": "DRIVE", "chase": "CHASE_DB1", "stare": "STARE", "fives": "FIVES"}
NET = {"unet": "U-Net", "attunet": "Attention U-Net", "unetpp": "U-Net++"}
COL = {"threshold": "#1f77b4", "hysteresis": "#ff7f0e", "dti_released": "#9467bd", "rgr": "#2ca02c", "dice_safe_rgr": "#17becf"}
LAB = {"threshold": "Global threshold", "hysteresis": "Hysteresis", "dti_released": "DTI (released code)", "rgr": "RGR"}

ap = argparse.ArgumentParser()
ap.add_argument("--rev", type=Path, required=True); ap.add_argument("--probs", type=Path, required=True)
ap.add_argument("--data", type=Path, required=True, help="folder holding drive/, chase/, stare/, fives/")
ap.add_argument("--out", type=Path, required=True); ap.add_argument("--datasets", nargs="+", default=["drive", "chase", "stare"])
ap.add_argument("--seed", type=int, default=7); ap.add_argument("--only", nargs="*", help="figure names to make")
ap.add_argument("--map-datasets", nargs="+", help="datasets whose probability maps are available (example panels and failure cases); default: all")
a = ap.parse_args(); a.out.mkdir(parents=True, exist_ok=True)
R = {(r["dataset"], r["arch"], r["seed"]): r for r in (json.load(open(f)) for f in a.rev.glob("*.json"))}
ALL = {k: v for k, v in R.items()}
main = {k: v for k, v in R.items() if k[2] == a.seed and k[0] in a.datasets}
DSETS = [d for d in DS if any(k[0] == d for k in main)]
MAPSETS = [d for d in DSETS if (a.map_datasets is None or d in a.map_datasets)]
want = lambda name: a.only is None or name in a.only
bold = lambda ax: [t.set_fontweight("bold") for t in ax.get_xticklabels() + ax.get_yticklabels()]
_data = {}


def data(ds):
    if ds not in _data:
        root = a.data / ds; k = 1.0 if ds == "drive" else median_fov_diameter(root) / median_fov_diameter(a.data / "drive")
        _data[ds] = (load_eval(root, "test", k=k), k)
    return _data[ds]


def prob(ds, arch, case): return np.load(a.probs / f"{ds}_{arch}_s{a.seed}_{case}.npy").astype(np.float32)


def save(fig, name):
    fig.savefig(a.out / f"{name}.png", bbox_inches="tight"); plt.close(fig); print("written", name, flush=True)


if want("fig_equal_precision"):
    fig, axes = plt.subplots(3, len(DSETS), figsize=(2.6 * len(DSETS), 6.2), squeeze=False)
    for j, ds in enumerate(DSETS):
        for i, (key, yl) in enumerate((("thin_centre", "Thin-centreline recall"), ("cldice", "clDice"), ("components", "Fragments per image"))):
            ax = axes[i, j]
            for arch, ls in zip(NET, ("-", "--", ":")):
                r = main.get((ds, arch, a.seed))
                if r is None: continue
                for name in ("threshold", "hysteresis", "dti_released", "rgr"):
                    sw = sorted(r["sweep"][name], key=lambda z: z["precision"])
                    ax.plot([z["precision"] for z in sw], [z[key] for z in sw], ls, color=COL[name], lw=1.2,
                            label=LAB[name] if (arch == "unet" and i == 0 and j == 0) else None)
                v = r["procedures"]["rgr"]; t = r["procedures"]["threshold_0.5"]
                ax.plot(v["precision"], v[key], "*", color=COL["rgr"], ms=7, mec="k", mew=0.4); ax.plot(t["precision"], t[key], "D", color="k", ms=3.5)
            ax.set_xlabel("Precision"); ax.set_ylabel(yl); bold(ax)
            if i == 0: ax.set_title(DS[ds])
    axes[0, 0].legend(loc="upper right", frameon=False)
    for i, lab in enumerate("abc"): axes[i, 0].text(-0.28, 1.02, lab, transform=axes[i, 0].transAxes, fontsize=10, fontweight="bold")
    fig.tight_layout(); save(fig, "fig_equal_precision")

if want("fig_operating_point"):
    fig, ax = plt.subplots(figsize=(3.6, 3.0)); mk = {"drive": "o", "chase": "^", "stare": "s", "fives": "P"}; cl = {"drive": "#d62728", "chase": "#1f77b4", "stare": "#2ca02c", "fives": "#8c564b"}
    for (ds, arch, seed), r in sorted(ALL.items()):
        t = r["procedures"]["threshold_0.5"]; v = r["procedures"]["rgr"]
        ax.plot(100 * (t["precision"] - t["recall"]), 100 * (v["dice"] - t["dice"]), mk[ds], color=cl[ds], ms=5, mec="k", mew=0.4, alpha=0.85,
                label=DS[ds] if (arch == "unet" and seed == min(s for d_, a_, s in ALL if d_ == ds)) else None)
    ax.axhline(0, color="k", lw=0.6); ax.axvline(0, color="k", lw=0.6)
    ax.set_xlabel("Precision minus recall of the 0.5 threshold (pp)"); ax.set_ylabel("Dice change under RGR (pp)"); ax.legend(frameon=False); bold(ax)
    fig.tight_layout(); save(fig, "fig_operating_point")

if want("fig_dice_rule"):
    fig, axes = plt.subplots(1, 2, figsize=(6.4, 3.0))
    mk = {"drive": "o", "chase": "^", "stare": "s", "fives": "P"}; cl = {"drive": "#d62728", "chase": "#1f77b4", "stare": "#2ca02c", "fives": "#8c564b"}
    for (ds, arch, _), r in sorted(main.items()):
        for x in r["dice_rule"]["rgr"]:
            if not x["added"]: continue
            axes[0].plot(100 * x["true_precision"], 100 * x["p_hat"], mk[ds], color=cl[ds], ms=4, mec="k", mew=0.3, alpha=0.8, label=DS[ds] if arch == "unet" else None)
            axes[1].plot(100 * x["true_dice"], 100 * x["d_hat"], mk[ds], color=cl[ds], ms=4, mec="k", mew=0.3, alpha=0.8)
    for ax, xl, yl in ((axes[0], "True precision of the additions (%)", "Estimated precision (%)"), (axes[1], "True Dice of the seed (%)", "Estimated Dice (%)")):
        lo, hi = ax.get_xlim(); lo2, hi2 = ax.get_ylim(); m0, m1 = min(lo, lo2), max(hi, hi2)
        ax.plot([m0, m1], [m0, m1], "k--", lw=0.7); ax.set_xlabel(xl); ax.set_ylabel(yl); bold(ax)
    h, l = axes[0].get_legend_handles_labels(); by = dict(zip(l, h)); axes[0].legend(by.values(), by.keys(), frameon=False)
    axes[0].set_title("a  Precision of the added pixels"); axes[1].set_title("b  Dice of the thresholded mask")
    fig.tight_layout(); save(fig, "fig_dice_rule")

if want("fig_gate"):
    fig, axes = plt.subplots(1, len(DSETS), figsize=(2.4 * len(DSETS), 2.6), squeeze=False)
    G = [0.45, 0.40, 0.35, 0.30, 0.25, 0.20, 0.15]; pos = {g: i for i, g in enumerate(G)}; pos[None] = len(G)
    for j, ds in enumerate(DSETS):
        ax = axes[0, j]; M = np.zeros((len(G) + 1, len(G) + 1), int)
        for arch in NET:
            r = main.get((ds, arch, a.seed))
            if r is None: continue
            for x in r["gate_choice"]: M[pos[x["optimum"]], pos[x["chosen"]]] += 1
        ax.imshow(M, cmap="Blues", origin="lower")
        for i_ in range(M.shape[0]):
            for j_ in range(M.shape[1]):
                if M[i_, j_]: ax.text(j_, i_, str(M[i_, j_]), ha="center", va="center", fontsize=6, fontweight="bold", color="k" if M[i_, j_] < M.max() * 0.6 else "w")
        lab = [f"{g:.2f}" for g in G] + ["none"]
        ax.set_xticks(range(len(lab))); ax.set_xticklabels(lab, rotation=90); ax.set_yticks(range(len(lab))); ax.set_yticklabels(lab)
        ax.set_xlabel("Gate chosen by the conservative-gate rule"); ax.set_title(DS[ds]); bold(ax)
        if j == 0: ax.set_ylabel("Gate with the highest true Dice")
    fig.tight_layout(); save(fig, "fig_gate")

if want("fig_measurements"):
    keys = (("density", "Vessel density (pp)"), ("length", "Centreline length (%)"), ("branch_points", "Branch points (%)"), ("end_points", "End points (%)"), ("fractal_dimension", "Fractal dimension"))
    fig, axes = plt.subplots(1, len(keys), figsize=(2.0 * len(keys), 2.6))
    procs = (("threshold_0.5", "T0.5", "#7f7f7f"), ("rgr", "RGR", COL["rgr"]), ("dice_safe_rgr", "Cons. gate", COL["dice_safe_rgr"]), ("hysteresis_0.25", "Hyst.", COL["hysteresis"]))
    for ax, (key, yl) in zip(axes, keys):
        x = 0; ticks = []; tl = []
        for ds in DSETS:
            vals = defaultdict(list)
            for arch in NET:
                r = main.get((ds, arch, a.seed))
                if r is None: continue
                for pk, _, _ in procs: vals[pk] += [e[key] for e in r["procedures"][pk]["per_image_measurements"]]
            for i, (pk, pl, c) in enumerate(procs):
                v = np.array(vals[pk]); ax.bar(x + i * 0.2, np.mean(np.abs(v)), 0.18, color=c, label=pl if (ds == DSETS[0]) else None)
                ax.errorbar(x + i * 0.2, np.mean(np.abs(v)), yerr=np.std(np.abs(v)) / np.sqrt(len(v)), color="k", lw=0.6, capsize=1.5)
            ticks.append(x + 0.3); tl.append(DS[ds]); x += 1.1
        ax.set_xticks(ticks); ax.set_xticklabels(tl, rotation=20); ax.set_ylabel("Mean absolute error: " + yl); bold(ax)
    axes[0].legend(frameon=False, fontsize=6); fig.tight_layout(); save(fig, "fig_measurements")

if want("fig_missed"):
    fig, ax = plt.subplots(figsize=(3.6, 2.6)); edges = np.arange(0, 0.501, 0.05); w = 0.05 / (len(DSETS) + 1)
    for j, ds in enumerate(DSETS):
        H = np.sum([x["hist_near"] for arch in NET if (ds, arch, a.seed) in main for x in main[(ds, arch, a.seed)]["missed_thin"]], 0)
        ax.bar(edges[:-1] + w * (j + 0.5), 100 * H / H.sum(), w, label=DS[ds])
    ax.axvline(0.25, color="k", ls="--", lw=0.8); ax.set_xlabel("Network probability of missed thin-vessel pixels"); ax.set_ylabel("Share of pixels (%)"); ax.legend(frameon=False); bold(ax)
    fig.tight_layout(); save(fig, "fig_missed")

if want("fig_calibration"):
    fig, axes = plt.subplots(1, len(DSETS), figsize=(2.5 * len(DSETS), 2.7), squeeze=False)
    for j, ds in enumerate(DSETS):
        ax = axes[0, j]; ax.plot([0, 1], [0, 1], "k--", lw=0.7); ax.axvspan(0.15, 0.5, color="0.92")
        for arch, c in zip(NET, ("#1f77b4", "#ff7f0e", "#2ca02c")):
            r = main.get((ds, arch, a.seed))
            if r is None: continue
            rel = [b for b in r["calibration"]["reliability_test"] if b["n"]]
            ax.plot([b["mean_p"] for b in rel], [b["frac"] for b in rel], "o-", color=c, ms=3, lw=1, label=f"{NET[arch]} (ECE {r['calibration']['ece_test']:.3f})")
        ax.set_xlabel("Mean predicted probability"); ax.set_ylabel("Observed vessel fraction"); ax.set_title(DS[ds]); bold(ax)
        ax.legend(frameon=False, loc="lower right", fontsize=6)
    fig.tight_layout(); save(fig, "fig_calibration")

if want("fig_condition"):
    mk = {"drive": ("o", "#d62728"), "chase": ("^", "#1f77b4"), "stare": ("s", "#2ca02c"), "fives": ("P", "#8c564b")}
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.3))
    for ax, var, title in zip(axes, ("rgr", "rgr_p"), ("RGR", "RGR-P")):
        for (ds, arch, seed), r in sorted(ALL.items(), key=lambda z: (list(DS).index(z[0][0]), list(NET).index(z[0][1]))):
            if seed != a.seed: continue
            m, c = mk[ds]
            x = [100 * (e["true_precision"] - e["true_dice"] / 2) for e in r["dice_rule"][var]]; y = [100 * e["dice_change"] for e in r["dice_rule"][var]]
            ax.plot(x, y, m, color=c, ms=4, mec="k", mew=0.3, alpha=0.8, label=DS[ds] if arch == "unet" else None)
        ax.axhline(0, color="k", lw=0.8); ax.axvline(0, color="k", lw=0.8); ax.set_title(title)
        ax.set_xlabel("Precision of the additions minus D/2 (pp)"); ax.set_ylabel("Dice change (pp)"); bold(ax)
    axes[0].legend(frameon=False, fontsize=7)
    fig.text(0.01, 0.98, "a", fontsize=10, fontweight="bold", va="top"); fig.text(0.51, 0.98, "b", fontsize=10, fontweight="bold", va="top")
    fig.tight_layout(); save(fig, "fig_condition")

if want("fig_paths") and "drive" in MAPSETS:
    D, _ = data("drive"); best = None
    for d in D:
        p = prob("drive", "unet", d["case"])
        seed = threshold(p, d["f"]); m = rgr(p, d["f"], d["rfk"], 0.25, 0.05, 8); mp = rgr_p(p, d["f"], d["rfk"], 0.25, 0.05, 8, 8, 0.3, base=m)
        paths = mp & ~m
        if not paths.any(): continue
        inner = ndi.distance_transform_edt(d["f"]) > 60
        sc = ndi.uniform_filter((paths & d["y"]).astype(float), 80) * 6400 * inner
        sc *= (ndi.uniform_filter(seed.astype(float), 80) < 0.25)
        yy, xx = np.unravel_index(int(np.argmax(sc)), sc.shape)
        if best is None or sc[yy, xx] > best[0]: best = (sc[yy, xx], d, p, seed, m, mp, yy, xx)
    _, d, p, seed, m, mp, cy, cx = best
    H, W = seed.shape; sl = (slice(max(0, cy - 40), min(H, cy + 40)), slice(max(0, cx - 40), min(W, cx + 40)))

    def paint(mask):
        img = np.zeros(mask[sl].shape + (3,)); y = d["y"][sl]
        img[y] = (0.45, 0.45, 0.45); img[mask[sl] & y] = (1, 1, 1); img[mask[sl] & ~y] = (1, 0.55, 0)
        return img
    fig, axes = plt.subplots(1, 6, figsize=(7.2, 1.45))
    img = paint(m); add = (mp & ~m)[sl]; y = d["y"][sl]; img[add & y] = (0, 0.8, 0); img[add & ~y] = (0.9, 0, 0.9)
    panels = [("Photograph", d["img"][sl]), ("Probability", p[sl]), ("Seed (0.5)", paint(seed)), ("RGR", paint(m)), ("RGR-P", paint(mp)), ("Paths added", img)]
    for ax, (t, im) in zip(axes, panels):
        ax.imshow(im, cmap="gray" if im.ndim == 2 else None, vmin=0, vmax=1, interpolation="nearest"); ax.set_title(t, fontsize=7); ax.set_xticks([]); ax.set_yticks([])
    fig.text(0.5, -0.06, f"DRIVE test image {d['case']}, U-Net. Grey: reference; white: mask on the reference; orange: mask off the reference; green and magenta: path pixels on and off the reference.", ha="center", fontsize=6, fontweight="bold")
    fig.tight_layout(); save(fig, "fig_paths")

if want("fig_bridges"):
    fig = plt.figure(figsize=(7.2, 5.3)); gs = fig.add_gridspec(2, 1, height_ratios=(1.5, 1), hspace=0.5, top=0.96, bottom=0.10, left=0.07, right=0.98)
    top = gs[0].subgridspec(3, 6, wspace=0.05, hspace=0.6); bot = gs[1].subgridspec(1, len(DSETS), wspace=0.35)
    for i, (cls, members) in enumerate((("correct", ("correct",)), ("unannotated", ("unannotated",)), ("shortcut or offset", ("shortcut", "offset")))):
        picks = []
        for ds in MAPSETS:
            for arch in NET:
                r = main.get((ds, arch, a.seed))
                if r is None: continue
                for b in r["bridges"]["rgr"]["bridges"]:
                    if b["cls"] in members and (b["pixels"] >= 2 or cls != "correct"): picks.append((ds, arch, b))
        rng = np.random.default_rng(3); rng.shuffle(picks); picks = picks[:6]
        for j in range(6):
            ax = fig.add_subplot(top[i, j]); ax.set_xticks([]); ax.set_yticks([])
            if j >= len(picks): ax.axis("off"); continue
            ds, arch, b = picks[j]; D, k = data(ds); d = next(x for x in D if x["case"] == b["case"]); p = prob(ds, arch, b["case"])
            seed = threshold(p, d["f"]); m = rgr(p, d["f"], d["rfk"], 0.25, 0.05, int(round(8 * k))); add = m & ~seed
            Rw = int(round(12 * k)); cy, cx = int(b["cy"]), int(b["cx"]); sl = (slice(max(0, cy - Rw), cy + Rw + 1), slice(max(0, cx - Rw), cx + Rw + 1))
            img = np.zeros(seed[sl].shape + (3,)); y = d["y"][sl]
            img[y] = (0.55, 0.55, 0.55); img[seed[sl]] = (1, 1, 1); img[seed[sl] & y] = (0.78, 0.78, 1.0); img[add[sl] & ~y] = (1, 0.5, 0); img[add[sl] & y] = (0, 0.75, 0)
            ax.imshow(img, interpolation="nearest"); ax.set_title(f"{DS[ds][0]}{b['case']}" + ("" if cls != "shortcut or offset" else f" ({b['cls']})"), fontsize=5.5)
            if j == 0: ax.set_ylabel({"correct": "correct", "unannotated": "unannotated", "shortcut or offset": "shortcut /\noffset"}[cls], fontsize=6.5)
    for j, ds in enumerate(DSETS):
        ax = fig.add_subplot(bot[0, j]); ctx = ("all", "junction", "adjacent", "optic_disc", "none_of_these"); names = ("all", "junction", "adjacent", "optic disc", "other")
        tot = defaultdict(lambda: defaultdict(int))
        for arch in NET:
            r = main.get((ds, arch, a.seed))
            if r is None: continue
            for c in ctx:
                for key, v in r["bridges"]["rgr"]["summary"][c].items(): tot[c][key] += v
        bottom = np.zeros(len(ctx))
        for cls, col in (("correct", "#2ca02c"), ("offset", "#bcbd22"), ("unannotated", "#ff7f0e"), ("shortcut", "#d62728")):
            v = np.array([tot[c][cls] for c in ctx], float); ax.bar(range(len(ctx)), v, 0.7, bottom=bottom, color=col, label=cls); bottom += v
        ax.set_xticks(range(len(ctx))); ax.set_xticklabels(names, rotation=30); ax.set_ylabel("Bridges"); ax.set_title(DS[ds]); bold(ax)
        if j == 0: ax.legend(frameon=False, fontsize=6)
    ya = min(ax.get_position().y0 for ax in fig.axes[:18]); yb = max(ax.get_position().y1 for ax in fig.axes[18:])
    fig.text(0.01, 0.99, "a", fontsize=10, fontweight="bold", va="top"); fig.text(0.01, yb + 0.05, "b", fontsize=10, fontweight="bold", va="top")
    fig.text(0.5, ya - 0.045, "D: DRIVE, C: CHASE_DB1, S: STARE. Grey: reference; white: seed; light blue: seed on reference; green and orange: additions on and off the reference", ha="center", va="center", fontsize=5.5, fontweight="bold")
    save(fig, "fig_bridges")

if want("fig_failures"):
    rows = []
    for ds in MAPSETS:
        D, k = data(ds); cands = []
        for d in D:
            p = prob(ds, "unet", d["case"]); seed = threshold(p, d["f"]); m = rgr(p, d["f"], d["rfk"], 0.25, 0.05, int(round(8 * k)))
            fa = m & ~seed & ~d["y"] & (d["dy"] > 1.5)
            lab, n = ndi.label(ndi.binary_dilation(fa, iterations=int(round(3 * k))), np.ones((3, 3)))
            if n == 0: continue
            sizes = ndi.sum(fa, lab, index=np.arange(1, n + 1)); top = np.argsort(sizes)[::-1][:2]
            for t in top:
                cy, cx = ndi.center_of_mass(lab == t + 1); cands.append((int(sizes[t]), d, p, seed, m, int(cy), int(cx)))
        cands.sort(key=lambda z: -z[0]); rows.append((ds, k, cands[:3]))
    fig, axes = plt.subplots(len(rows), 6, figsize=(7.2, 1.3 * len(rows) + 0.3), squeeze=False)
    for i, (ds, k, cs) in enumerate(rows):
        for j, (n, d, p, seed, m, cy, cx) in enumerate(cs):
            Rw = int(round(28 * k)); sl = (slice(max(0, cy - Rw), cy + Rw), slice(max(0, cx - Rw), cx + Rw))
            axes[i, 2 * j].imshow(d["img"][sl]); axes[i, 2 * j].set_title(f"{DS[ds]} {d['case']} ({n} px)", fontsize=6)
            img = np.zeros(seed[sl].shape + (3,)); y = d["y"][sl]; add = (m & ~seed)[sl]
            img[seed[sl] & y] = (1, 1, 1); img[seed[sl] & ~y] = (1, 0.5, 0); img[~seed[sl] & y] = (0.8, 0, 0); img[add & y] = (0, 0.75, 0); img[add & ~y] = (1, 0.85, 0)
            axes[i, 2 * j + 1].imshow(img, interpolation="nearest")
        for ax in axes[i]: ax.set_xticks([]); ax.set_yticks([])
    fig.text(0.5, 0.005, "Photograph (left) and masks (right): white seed on vessel, orange seed off vessel, red missed vessel, green correct addition, yellow false addition", ha="center", fontsize=6, fontweight="bold")
    fig.tight_layout(rect=(0, 0.03, 1, 1)); save(fig, "fig_failures")
print("done")
