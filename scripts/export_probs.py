import argparse, shutil, sys, time
from pathlib import Path
import numpy as np, torch

ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from rgr import networks as nets
from rgr.data import discover, read_rgb, DRIVE_VALID

ap = argparse.ArgumentParser()
ap.add_argument("--dataset", required=True, choices=["drive", "chase", "stare", "fives"])
ap.add_argument("--root", type=Path, required=True)
ap.add_argument("--out", type=Path, required=True)
ap.add_argument("--seeds", type=int, nargs="+", default=[7])
ap.add_argument("--archs", nargs="+", default=["unet", "attunet", "unetpp"])
ap.add_argument("--weights", type=Path, help="folder with the seed-7 weights (<arch>_<dataset>.pt)")
ap.add_argument("--steps", type=int, default=4000)
ap.add_argument("--light-train", action="store_true", help="memory-light training for large photographs (FIVES)")
ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
a = ap.parse_args()
(a.out / "probs").mkdir(parents=True, exist_ok=True); (a.out / "models").mkdir(parents=True, exist_ok=True)


def predict(model, img):
    try:
        return nets.predict(model, img, a.device)
    except torch.OutOfMemoryError:
        torch.cuda.empty_cache(); H, W, _ = img.shape; T, O = 1024, 128
        acc = np.zeros((H, W), np.float32); cnt = np.zeros((H, W), np.float32)
        for y0 in range(0, H, T - O):
            for x0 in range(0, W, T - O):
                y1, x1 = min(H, y0 + T), min(W, x0 + T)
                acc[y0:y1, x0:x1] += nets.predict(model, np.ascontiguousarray(img[y0:y1, x0:x1]), a.device)
                cnt[y0:y1, x0:x1] += 1
        return acc / cnt


test = discover(a.root, "test"); train = discover(a.root, "train")
val = [p for p in train if a.dataset == "drive" and p.case in DRIVE_VALID]
fit = [p for p in train if not (a.dataset == "drive" and p.case in DRIVE_VALID)]
for seed in a.seeds:
    for arch in a.archs:
        f = a.out / "models" / f"{arch}_{a.dataset}_s{seed}.pt"
        rel = a.weights / f"{arch}_{a.dataset}.pt" if a.weights else None
        if not f.exists() and seed == 7 and rel is not None and rel.exists(): shutil.copy(rel, f)
        if not f.exists():
            print(f"[train] {nets.NAME[arch]} on {a.dataset}, seed {seed}, {len(fit)} images", flush=True)
            t0 = time.time()
            if a.light_train:
                from rgr.train_light import train_light
                train_light(arch, fit, f, a.steps, a.device, seed=seed, log=lambda *x: print(*x, flush=True))
            else:
                nets.train(arch, fit, f, a.steps, a.device, seed=seed)
            print(f"  trained in {time.time() - t0:.0f} s", flush=True)
        model = None
        for p in test + val:
            g = a.out / "probs" / f"{a.dataset}_{arch}_s{seed}_{p.case}.npy"
            if g.exists(): continue
            if model is None: model = nets.load(arch, f, a.device)
            np.save(g, predict(model, read_rgb(p.image)).astype(np.float16 if a.dataset == "fives" else np.float32))
        print(f"[maps] {a.dataset} {arch} seed {seed}: {len(test)} test" + (f" + {len(val)} validation" if val else ""), flush=True)
        if a.device.startswith("cuda"): torch.cuda.empty_cache()
