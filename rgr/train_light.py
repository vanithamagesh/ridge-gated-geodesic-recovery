import copy, random, time
import cv2, numpy as np, torch, torch.nn as nn, torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from skimage.morphology import skeletonize

from .networks import ARCH, NAME, _masked_mean, _soft_dice
from .data import load_pair


class LightPatchDataset(Dataset):
    def __init__(self, pairs, steps, batch, patch, seed):
        self.rng, self.n, self.patch, self.items = random.Random(seed), steps * batch, patch, []
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        for pair in pairs:
            image, target, fov = load_pair(pair)
            x = np.concatenate([image, clahe.apply(image[..., 1])[..., None]], axis=2)
            y = target > 0; v = fov > 0
            centre = np.argwhere(skeletonize(y) & v).astype(np.int32)
            vessel = np.argwhere(y & v).astype(np.int32)
            self.items.append((x, y, v, centre if len(centre) else vessel, vessel))

    def __len__(self):
        return self.n

    def __getitem__(self, _):
        x, y, v, centre, vessel = self.rng.choice(self.items)
        h, w = y.shape; u = self.rng.random()
        if u < 0.35 and len(centre): cy, cx = centre[self.rng.randrange(len(centre))]
        elif u < 0.70 and len(vessel): cy, cx = vessel[self.rng.randrange(len(vessel))]
        else:
            for _ in range(1000):
                cy, cx = self.rng.randrange(h), self.rng.randrange(w)
                if v[cy, cx]: break
        top = min(max(int(cy) - self.rng.randrange(self.patch), 0), h - self.patch)
        left = min(max(int(cx) - self.rng.randrange(self.patch), 0), w - self.patch)
        sl = (slice(top, top + self.patch), slice(left, left + self.patch))
        arr = [x[sl].astype(np.float32) / 255.0 * 2.0 - 1.0, y[sl].astype(np.float32), v[sl].astype(np.float32)]
        rot = self.rng.randrange(4); arr = [np.rot90(a, rot) for a in arr]
        if self.rng.random() < 0.5: arr = [a[:, ::-1] for a in arr]
        if self.rng.random() < 0.5: arr = [a[::-1] for a in arr]
        arr[0] = np.clip(arr[0] * self.rng.uniform(0.85, 1.15) + self.rng.uniform(-0.08, 0.08), -1, 1)
        image, target, fov = arr
        t = lambda a: torch.from_numpy(np.ascontiguousarray(a[None])).float()
        return torch.from_numpy(np.ascontiguousarray(image.transpose(2, 0, 1))).float(), t(target), t(fov)


def train_light(arch, pairs, out, steps=4000, device="cpu", seed=7, log=print):
    torch.manual_seed(seed); np.random.seed(seed); random.seed(seed)
    m = ARCH[arch]().to(device); ema = copy.deepcopy(m).eval()
    log(f"  {NAME[arch]}: {sum(p.numel() for p in m.parameters()):,} parameters; loading {len(pairs)} images")
    t0 = time.time(); ds = LightPatchDataset(pairs, steps, 4, 128, seed); log(f"  images loaded in {time.time() - t0:.0f} s")
    dl = DataLoader(ds, batch_size=4, num_workers=0)
    opt = torch.optim.AdamW(m.parameters(), lr=1e-3, weight_decay=1e-4)
    sch = torch.optim.lr_scheduler.CosineAnnealingLR(opt, steps, eta_min=2e-5); t0 = time.time()
    for step, (x, y, v) in enumerate(dl, 1):
        x, y, v = x.to(device), y.to(device), v.to(device)
        m.train(); opt.zero_grad(); lo = m(x)["logits"]
        loss = 0.75 * _masked_mean(F.binary_cross_entropy_with_logits(lo, y, reduction="none"), v) + 0.25 * _soft_dice(lo.sigmoid(), y, v)
        loss.backward(); nn.utils.clip_grad_norm_(m.parameters(), 2); opt.step(); sch.step()
        with torch.no_grad():
            dcy = min(.99, 1 - 1 / (step + 1))
            for e, p in zip(ema.parameters(), m.parameters()): e.lerp_(p, 1 - dcy)
            for e, p in zip(ema.buffers(), m.buffers()): e.copy_(p)
        if step % 500 == 0: log(f"  {NAME[arch]} step {step}/{steps} loss {loss.item():.4f} ({time.time() - t0:.0f}s)")
    torch.save(ema.state_dict(), out)
