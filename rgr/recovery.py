import numpy as np
from scipy import ndimage as ndi
from skimage.filters import frangi
from skimage.graph import MCP_Geometric
from skimage.morphology import closing, skeletonize

B3 = np.ones((3, 3), bool)
N8 = np.ones((3, 3), int)
DICE_SAFE_GATES = (0.45, 0.40, 0.35, 0.30, 0.25, 0.20, 0.15)


def ridge_map(image, fov, k=1.0):
    g = image[..., 1].astype(np.float32) / 255
    r = frangi(g, sigmas=[1 * k, 1.5 * k, 2 * k], black_ridges=True)
    return np.clip(r / max(float(np.percentile(r[fov], 99)), 1e-12), 0, 1)


def threshold(prob, fov, tau=0.5):
    return (prob >= tau) & fov


def hysteresis(prob, fov, low, high=0.5):
    seed = threshold(prob, fov, high)
    return ndi.binary_propagation(seed, structure=B3, mask=seed | threshold(prob, fov, low))


def closing3(prob, fov):
    return closing(threshold(prob, fov), B3) & fov


def rgr(prob, fov, ridge, tp=0.25, tv=0.05, dl=8, use_ridge=True, use_distance=True, use_connectivity=True):
    seed = threshold(prob, fov)
    cand = threshold(prob, fov, tp)
    if use_ridge: cand &= ridge >= tv
    if use_distance: cand &= ndi.distance_transform_edt(~seed) <= dl
    if not use_connectivity: return seed | cand
    return ndi.binary_propagation(seed, structure=B3, mask=seed | cand)


def dice_safe_rgr(prob, fov, ridge, tv=0.05, dl=8, gates=DICE_SAFE_GATES, return_gate=False):
    seed = threshold(prob, fov)
    d_hat = 2 * prob[seed].sum() / (seed.sum() + prob[fov].sum())
    best, chosen = seed, None
    for tp in gates:
        m = rgr(prob, fov, ridge, tp=tp, tv=tv, dl=dl)
        added = m & ~seed
        if added.sum() == 0 or prob[added].mean() > d_hat / 2:
            best, chosen = m, tp
        else:
            break
    return (best, chosen) if return_gate else best


def _endpoints(sk):
    nb = ndi.convolve(sk.astype(int), N8, mode="constant") - sk
    return np.argwhere(sk & (nb == 1))


def rgr_p(prob, fov, ridge, tp=0.25, tv=0.05, dl=8, rho=8, theta=0.3, tp_min=0.10, base=None):
    m = rgr(prob, fov, ridge, tp=tp, tv=tv, dl=dl) if base is None else base.copy()
    s = np.maximum(np.minimum(prob / 0.5, 1.0), ridge); s[~fov] = 0
    cost = (1.0 - s).astype(np.float64) + 1e-3
    lab, _ = ndi.label(m, B3); sk = skeletonize(m); H, W = m.shape
    added = np.zeros_like(m)
    for (y, x) in _endpoints(sk):
        y0, y1 = max(0, y - rho), min(H, y + rho + 1); x0, x1 = max(0, x - rho), min(W, x + rho + 1)
        sub = cost[y0:y1, x0:x1].copy(); sub[~fov[y0:y1, x0:x1]] = np.inf
        own = lab[y, x]; L = lab[y0:y1, x0:x1]
        targets = (L > 0) & (L != own)
        if not targets.any(): continue
        mcp = MCP_Geometric(sub, fully_connected=True)
        cum, _ = mcp.find_costs([(y - y0, x - x0)])
        cum = np.where(targets, cum, np.inf)
        if not np.isfinite(cum).any(): continue
        ty, tx = np.unravel_index(int(np.argmin(cum)), cum.shape)
        path = mcp.traceback((ty, tx))
        if len(path) < 2: continue
        mean_cost = float(np.mean([sub[py, px] for py, px in path]))
        if mean_cost > theta: continue
        for py, px in path: added[y0 + py, x0 + px] = True
    if not added.any(): return m
    thick = ndi.binary_dilation(added, B3) & threshold(prob, fov, tp_min)
    out = m | added | thick
    return ndi.binary_propagation(threshold(prob, fov), structure=B3, mask=out)


def resolution_factor(fov_diameters_target, fov_diameters_drive):
    return float(np.median(fov_diameters_target) / np.median(fov_diameters_drive))


def fov_diameter(fov):
    return 2 * np.sqrt(fov.sum() / np.pi)
