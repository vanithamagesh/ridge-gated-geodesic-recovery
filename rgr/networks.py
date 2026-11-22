import copy, random, time
import numpy as np, torch, torch.nn as nn, torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

from .data import load_pair, features


def blk(i, o):
    return nn.Sequential(nn.Conv2d(i, o, 3, padding=1, bias=False), nn.BatchNorm2d(o), nn.ReLU(inplace=True),
                         nn.Conv2d(o, o, 3, padding=1, bias=False), nn.BatchNorm2d(o), nn.ReLU(inplace=True))


def _pad(x):
    H, W = x.shape[-2:]
    return F.pad(x, (0, (-W) % 16, 0, (-H) % 16), mode="reflect"), H, W


class AttGate(nn.Module):
    def __init__(self, cx, cg, ci):
        super().__init__()
        self.wx = nn.Sequential(nn.Conv2d(cx, ci, 1, bias=False), nn.BatchNorm2d(ci))
        self.wg = nn.Sequential(nn.Conv2d(cg, ci, 1, bias=False), nn.BatchNorm2d(ci))
        self.psi = nn.Sequential(nn.Conv2d(ci, 1, 1), nn.BatchNorm2d(1), nn.Sigmoid())

    def forward(self, x, g):
        return x * self.psi(F.relu(self.wx(x) + self.wg(g)))


class UNet(nn.Module):
    def __init__(self, c=16, attention=False):
        super().__init__()
        ch = [c, 2 * c, 4 * c, 8 * c]
        self.e = nn.ModuleList([blk(4, ch[0]), blk(ch[0], ch[1]), blk(ch[1], ch[2]), blk(ch[2], ch[3])]); self.b = blk(ch[3], 16 * c)
        self.u = nn.ModuleList([nn.ConvTranspose2d(16 * c, ch[3], 2, 2), nn.ConvTranspose2d(ch[3], ch[2], 2, 2),
                                nn.ConvTranspose2d(ch[2], ch[1], 2, 2), nn.ConvTranspose2d(ch[1], ch[0], 2, 2)])
        self.d = nn.ModuleList([blk(2 * ch[3], ch[3]), blk(2 * ch[2], ch[2]), blk(2 * ch[1], ch[1]), blk(2 * ch[0], ch[0])])
        self.att = nn.ModuleList([AttGate(k, k, max(k // 2, 8)) for k in reversed(ch)]) if attention else None
        self.h = nn.Conv2d(c, 1, 1)

    def forward(self, x):
        x, H, W = _pad(x); sk = []
        for e in self.e: x = e(x); sk.append(x); x = F.max_pool2d(x, 2)
        x = self.b(x)
        for i, (u, d, k) in enumerate(zip(self.u, self.d, reversed(sk))):
            g = u(x)
            if self.att is not None: k = self.att[i](k, g)
            x = d(torch.cat([g, k], 1))
        return {"logits": self.h(x)[..., :H, :W]}


class UNetPP(nn.Module):
    def __init__(self, c=16):
        super().__init__()
        ch = [c, 2 * c, 4 * c, 8 * c, 16 * c]
        self.x = nn.ModuleDict()
        for i in range(5): self.x[f"{i}_0"] = blk(4 if i == 0 else ch[i - 1], ch[i])
        for j in range(1, 5):
            for i in range(5 - j): self.x[f"{i}_{j}"] = blk(ch[i] * j + ch[i + 1], ch[i])
        self.h = nn.Conv2d(c, 1, 1)

    def forward(self, x):
        x, H, W = _pad(x); X = {}
        up = lambda t: F.interpolate(t, scale_factor=2, mode="bilinear", align_corners=False)
        for i in range(5): X[(i, 0)] = self.x[f"{i}_0"](x if i == 0 else F.max_pool2d(X[(i - 1, 0)], 2))
        for j in range(1, 5):
            for i in range(5 - j):
                X[(i, j)] = self.x[f"{i}_{j}"](torch.cat([X[(i, k)] for k in range(j)] + [up(X[(i + 1, j - 1)])], 1))
        return {"logits": self.h(X[(0, 4)])[..., :H, :W]}


ARCH = {"unet": lambda: UNet(), "attunet": lambda: UNet(attention=True), "unetpp": lambda: UNetPP()}
NAME = {"unet": "U-Net", "attunet": "Attention U-Net", "unetpp": "U-Net++"}


def _erode(x):
    return torch.minimum(-F.max_pool2d(-x, (3, 1), 1, (1, 0)), -F.max_pool2d(-x, (1, 3), 1, (0, 1)))


def soft_skeleton(x, iterations=10):
    skeleton = F.relu(x - F.max_pool2d(_erode(x), 3, 1, 1))
    for _ in range(iterations):
        x = _erode(x); delta = F.relu(x - F.max_pool2d(_erode(x), 3, 1, 1))
        skeleton = skeleton + F.relu(delta - skeleton * delta)
    return skeleton


class PatchDataset(Dataset):
    def __init__(self, pairs, steps, batch, patch, seed):
        self.rng, self.n, self.patch, self.items = random.Random(seed), steps * batch, patch, []
        with torch.no_grad():
            for pair in pairs:
                image, target, fov = load_pair(pair)
                skeleton = soft_skeleton(torch.from_numpy(target)[None, None])[0, 0].numpy()
                pts = [np.argwhere((skeleton > 0.1) & (fov > 0)), np.argwhere((target > 0) & (fov > 0)), np.argwhere(fov > 0)]
                self.items.append((features(image), target, fov, pts))

    def __len__(self):
        return self.n

    def __getitem__(self, _):
        image, target, fov, coords = self.rng.choice(self.items)
        h, w = target.shape
        pts = coords[0 if self.rng.random() < 0.35 else 1 if self.rng.random() < 0.54 else 2]
        pts = pts if len(pts) else coords[-1]
        cy, cx = pts[self.rng.randrange(len(pts))]
        top = min(max(int(cy) - self.rng.randrange(self.patch), 0), h - self.patch)
        left = min(max(int(cx) - self.rng.randrange(self.patch), 0), w - self.patch)
        arr = [a[top:top + self.patch, left:left + self.patch] for a in (image, target, fov)]
        rot = self.rng.randrange(4); arr = [np.rot90(a, rot) for a in arr]
        if self.rng.random() < 0.5: arr = [a[:, ::-1] for a in arr]
        if self.rng.random() < 0.5: arr = [a[::-1] for a in arr]
        arr[0] = np.clip(arr[0] * self.rng.uniform(0.85, 1.15) + self.rng.uniform(-0.08, 0.08), -1, 1)
        image, target, fov = arr
        t = lambda a: torch.from_numpy(np.ascontiguousarray(a[None])).float()
        return torch.from_numpy(np.ascontiguousarray(image.transpose(2, 0, 1))).float(), t(target), t(fov)


def _masked_mean(x, v):
    return (x * v).sum() / v.sum().clamp_min(1)


def _soft_dice(p, y, v):
    dims = (1, 2, 3)
    return 1 - ((2 * (p * y * v).sum(dims) + 1) / ((p * v).sum(dims) + (y * v).sum(dims) + 1)).mean()


def train(arch, pairs, out, steps=4000, device="cpu", seed=7):
    torch.manual_seed(seed); np.random.seed(seed); random.seed(seed)
    m = ARCH[arch]().to(device); ema = copy.deepcopy(m).eval()
    print(f"  {NAME[arch]}: {sum(p.numel() for p in m.parameters()):,} parameters", flush=True)
    dl = DataLoader(PatchDataset(pairs, steps, 4, 128, seed), batch_size=4, num_workers=0)
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
        if step % 500 == 0: print(f"  {NAME[arch]} step {step}/{steps} loss {loss.item():.4f} ({time.time() - t0:.0f}s)", flush=True)
    torch.save(ema.state_dict(), out)


def load(arch, path, device="cpu"):
    m = ARCH[arch](); m.load_state_dict(torch.load(path, map_location="cpu", weights_only=True)); return m.to(device).eval()


@torch.inference_mode()
def predict(model, image, device="cpu", tta=True):
    x = torch.from_numpy(features(image).transpose(2, 0, 1)).float().unsqueeze(0).to(device)
    views = [()] if not tta else [(), (-1,), (-2,), (-2, -1)]
    ps = [torch.flip(model(torch.flip(x, v) if v else x)["logits"].sigmoid(), v) if v else model(x)["logits"].sigmoid() for v in views]
    return torch.stack(ps).mean(0)[0, 0].cpu().numpy()
