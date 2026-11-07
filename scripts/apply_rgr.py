import argparse, sys
from pathlib import Path
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rgr import ridge_map, rgr, rgr_p, dice_safe_rgr, threshold

ap = argparse.ArgumentParser()
ap.add_argument("--image", required=True); ap.add_argument("--prob", required=True); ap.add_argument("--fov")
ap.add_argument("--out", required=True)
ap.add_argument("--method", choices=["rgr", "rgr-p", "conservative"], default="rgr")
ap.add_argument("--tp", type=float, default=0.25); ap.add_argument("--tv", type=float, default=0.05); ap.add_argument("--dl", type=float, default=8)
ap.add_argument("--rho", type=float, default=8); ap.add_argument("--theta", type=float, default=0.3)
ap.add_argument("--k", type=float, default=1.0, help="resolution factor relative to DRIVE; scales the ridge filter, the distance limit and the path radius")
a = ap.parse_args()

image = np.asarray(Image.open(a.image).convert("RGB"))
prob = np.load(a.prob).astype(np.float32) if a.prob.endswith(".npy") else np.asarray(Image.open(a.prob).convert("L"), np.float32) / 255.0
fov = np.asarray(Image.open(a.fov).convert("L")) > 0 if a.fov else np.ones(prob.shape, bool)
ridge = ridge_map(image, fov, a.k); dl = int(round(a.dl * a.k))
if a.method == "conservative":
    mask, gate = dice_safe_rgr(prob, fov, ridge, a.tv, dl, return_gate=True); print("gate:", gate)
elif a.method == "rgr-p":
    mask = rgr_p(prob, fov, ridge, a.tp, a.tv, dl, int(round(a.rho * a.k)), a.theta)
else:
    mask = rgr(prob, fov, ridge, a.tp, a.tv, dl)
seed = threshold(prob, fov)
print(f"threshold 0.5: {int(seed.sum())} pixels; {a.method}: {int((mask & ~seed).sum())} pixels added")
Image.fromarray(mask.astype(np.uint8) * 255).save(a.out)
