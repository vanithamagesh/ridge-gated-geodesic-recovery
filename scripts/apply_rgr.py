"""Apply RGR or RGR-J to the probability map of any network.

    python scripts/apply_rgr.py --prob 01_prob.npy --fov 01_mask.gif --out 01_rgrj.png
    python scripts/apply_rgr.py --prob 01_prob.npy --fov 01_mask.gif --out 01_rgr.png --method rgr
    python scripts/apply_rgr.py --prob 01_prob.npy --fov 01_mask.gif --out 01.png --k 1.703      # other resolution

The probability map may be a .npy array in [0, 1] or an 8-bit image. RGR and RGR-J read only the probability map.
The photograph is needed only for the photograph-ridge gate (--method photo-ridge --image 01_test.tif), the
alternative compared in the paper."""
import argparse, sys
from pathlib import Path
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rgr import ridge_from_probability, ridge_map, rgr, gap_join, rgr_p, threshold

ap = argparse.ArgumentParser()
ap.add_argument("--prob", required=True); ap.add_argument("--fov"); ap.add_argument("--out", required=True)
ap.add_argument("--image", help="photograph, only for --method photo-ridge")
ap.add_argument("--method", choices=["rgr-j", "rgr", "rgr-paths", "photo-ridge"], default="rgr-j")
ap.add_argument("--tp", type=float, default=0.25); ap.add_argument("--tv", type=float, default=0.05)
ap.add_argument("--k", type=float, default=1.0, help="resolution factor relative to DRIVE (CHASE_DB1 1.703, STARE 1.186, FIVES 3.728)")
a = ap.parse_args()

prob = np.load(a.prob).astype(np.float32) if a.prob.endswith(".npy") else np.asarray(Image.open(a.prob).convert("L"), np.float32) / 255.0
fov = np.asarray(Image.open(a.fov).convert("L")) > 0 if a.fov else np.ones(prob.shape, bool)
dl = int(round(8 * a.k))
if a.method == "photo-ridge":
    assert a.image, "--method photo-ridge needs --image"
    ridge = ridge_map(np.asarray(Image.open(a.image).convert("RGB")), fov, a.k)
else:
    ridge = ridge_from_probability(prob, fov, a.k)
mask = rgr(prob, fov, ridge, a.tp, a.tv, dl)
if a.method == "rgr-j": mask = gap_join(prob, fov, mask, a.k)
elif a.method == "rgr-paths": mask = rgr_p(prob, fov, ridge, a.tp, a.tv, dl, rho=dl, base=mask)
seed = threshold(prob, fov)
print(f"threshold 0.5: {int(seed.sum())} pixels; {a.method}: {int((mask & ~seed).sum())} pixels added")
Image.fromarray(mask.astype(np.uint8) * 255).save(a.out)
