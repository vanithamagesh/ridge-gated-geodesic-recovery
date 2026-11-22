import argparse, csv, sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from rgr.recovery import threshold, rgr
from rgr.metrics import counts, aggregate
from rgr.data import load_eval, median_fov_diameter

ap = argparse.ArgumentParser()
ap.add_argument("--data", type=Path, required=True, help="folder holding drive/, chase/, stare/, fives/")
ap.add_argument("--probs", type=Path, required=True); ap.add_argument("--out", type=Path, required=True)
ap.add_argument("--datasets", nargs="+", default=["drive", "chase"]); ap.add_argument("--seed", type=int, default=7)
ap.add_argument("--archs", nargs="+", default=["unet", "attunet", "unetpp"])
a = ap.parse_args(); a.out.parent.mkdir(parents=True, exist_ok=True)
DS = {"drive": "DRIVE", "chase": "CHASE_DB1", "stare": "STARE", "fives": "FIVES"}
NET = {"unet": "U-Net", "attunet": "Attention U-Net", "unetpp": "U-Net++"}
VAR = (("RGR (all constraints)", {}), ("Without ridge gate", dict(use_ridge=False)),
       ("Without distance limit", dict(use_distance=False)), ("Without connectivity", dict(use_connectivity=False)))
rows = []
for ds in a.datasets:
    k = 1.0 if ds == "drive" else median_fov_diameter(a.data / ds) / median_fov_diameter(a.data / "drive")
    data = load_eval(a.data / ds, "test", k=k); dl = int(round(8 * k))
    res = {}
    for arch in a.archs:
        probs = [np.load(a.probs / f"{ds}_{arch}_s{a.seed}_{d['case']}.npy").astype(np.float32) for d in data]
        for name, kw in VAR:
            r = aggregate([counts(rgr(p, d["f"], d["rfk"], 0.25, 0.05, dl, **kw), d, threshold(p, d["f"])) for p, d in zip(probs, data)])
            res[(arch, name)] = r
            rows.append([DS[ds], NET[arch], name, f"{r['dice']:.4f}", f"{r['precision']:.4f}", f"{r['thin_centre']:.4f}", f"{r['components']:.1f}"])
            print(*rows[-1], flush=True)
    for name, _ in VAR:
        v = [res[(arch, name)] for arch in a.archs]
        rows.append([DS[ds], "Mean", name] + [f"{np.mean([r[q] for r in v]):.4f}" for q in ("dice", "precision", "thin_centre")] + [f"{np.mean([r['components'] for r in v]):.1f}"])
with open(a.out, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["Dataset", "Network", "Variant", "Dice", "Precision", "TCR", "Frag"]); w.writerows(rows)
print("written", a.out)
