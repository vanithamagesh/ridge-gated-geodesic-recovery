import numpy as np
from scipy import ndimage as ndi

from .recovery import threshold, B3


def dti_released(prob, fov, high=0.5, low=0.3):
    img = (np.clip(prob, 0, 1) * 255).astype(np.uint8)
    g = img >= high * 255
    cand = (img < high * 255) & (img >= low * 255) & fov
    strong = g.copy()
    H, W = g.shape
    z = np.zeros(W, bool)
    for i in range(H):
        c = cand[i]
        if not c.any(): continue
        v = (g[i - 1] if i > 0 else z) | (strong[i + 1] if i < H - 1 else z)
        trig = v.copy(); trig[1:] |= v[:-1]; trig[:-1] |= v[1:]
        row = strong[i]; trig[1:] |= row[:-1]; trig[:-1] |= row[1:]
        t = trig & c
        edges = np.flatnonzero(np.diff(np.r_[0, c.view(np.int8), 0]))
        for s, e in zip(edges[::2], edges[1::2]):
            seg = t[s:e]
            if seg.any(): g[i, s + int(seg.argmax()):e] = True
    return g & fov


def select_threshold(prob_list, data_list, grid=None):
    grid = np.round(np.arange(0.30, 0.701, 0.01), 2) if grid is None else grid
    best = None
    for t in grid:
        tp = fp = fn = 0
        for p, d in zip(prob_list, data_list):
            m = threshold(p, d["f"], t); y = d["y"]
            tp += (m & y).sum(); fp += (m & ~y & d["f"]).sum(); fn += (~m & y).sum()
        dice = 2 * tp / (2 * tp + fp + fn)
        if best is None or dice > best[1]: best = (float(t), float(dice))
    return best


def dense_crf(prob, image, fov, w_gauss=0.0, sxy_gauss=1.0, w_bil=1.0, sxy_bil=3.0, srgb=10.0, iters=5, trunc=2.5):
    import torch
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    p = np.clip(prob.astype(np.float32), 1e-5, 1 - 1e-5)
    U = torch.from_numpy(np.stack([-np.log(1 - p), -np.log(p)])).to(dev)
    I = torch.from_numpy(image.astype(np.float32)).permute(2, 0, 1).to(dev)
    F = torch.from_numpy(fov.astype(np.float32)).to(dev)
    Q = torch.softmax(-U, 0)
    H, W = p.shape
    R = int(np.ceil(trunc * max(sxy_gauss if w_gauss else 0, sxy_bil if w_bil else 0)))
    if R == 0: return (p > 0.5) & fov
    def shifted(x, dy, dx):
        out = torch.zeros_like(x)
        ys, yd = (slice(dy, None), slice(0, H - dy)) if dy >= 0 else (slice(0, H + dy), slice(-dy, None))
        xs, xd = (slice(dx, None), slice(0, W - dx)) if dx >= 0 else (slice(0, W + dx), slice(-dx, None))
        out[..., yd, xd] = x[..., ys, xs]; return out
    with torch.no_grad():
        ker = []; ng = torch.zeros(H, W, device=dev); nb = torch.zeros(H, W, device=dev)
        for dy in range(-R, R + 1):
            for dx in range(-R, R + 1):
                if (dy, dx) == (0, 0): continue
                r2 = dy * dy + dx * dx; Fs = shifted(F, dy, dx)
                kg = float(np.exp(-r2 / (2 * sxy_gauss ** 2))) if (w_gauss and r2 <= (trunc * sxy_gauss) ** 2) else 0.0
                kb = (np.exp(-r2 / (2 * sxy_bil ** 2)) * torch.exp(-((I - shifted(I, dy, dx)) ** 2).sum(0) / (2 * srgb ** 2)) * Fs
                      if (w_bil and r2 <= (trunc * sxy_bil) ** 2) else None)
                if kg: ng += kg * Fs
                if kb is not None: nb += kb
                ker.append((dy, dx, kg, kb))
        ng = ng.clamp_min(1e-6); nb = nb.clamp_min(1e-6)
        for _ in range(iters):
            mg = torch.zeros_like(Q); mb = torch.zeros_like(Q)
            for dy, dx, kg, kb in ker:
                Qs = shifted(Q, dy, dx)
                if kg: mg += kg * Qs
                if kb is not None: mb += kb * Qs
            msg = w_gauss * mg / ng + w_bil * mb / nb
            pair = torch.stack([msg[1], msg[0]])
            Q = torch.softmax(-(U + pair), 0)
        lab = (Q[1] > Q[0]).cpu().numpy()
    return lab & fov


def rgr_seeded(prob, fov, ridge, seed_tau=0.5, tp=0.25, tv=0.05, dl=8):
    seed = threshold(prob, fov, seed_tau)
    cand = threshold(prob, fov, min(tp, seed_tau)) & (ridge >= tv) & (ndi.distance_transform_edt(~seed) <= dl)
    return ndi.binary_propagation(seed, structure=B3, mask=seed | cand)
