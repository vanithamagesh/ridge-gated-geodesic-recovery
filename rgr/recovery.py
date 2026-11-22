import numpy as np
from scipy import ndimage as ndi
from skimage.filters import frangi
from skimage.graph import MCP_Geometric
from skimage.draw import line as straight_line
from skimage.morphology import closing, skeletonize

B3 = np.ones((3, 3), bool)
N8 = np.ones((3, 3), int)
DICE_SAFE_GATES = (0.45, 0.40, 0.35, 0.30, 0.25, 0.20, 0.15)


def ridge_from_probability(prob, fov, k=1.0):
    """Ridge evidence of the paper: Frangi vesselness of the probability map itself (bright ridges),
    scales 1k, 1.5k and 2k, divided by its 99th percentile inside the field of view and clipped at 1."""
    r = frangi(prob.astype(np.float32), sigmas=[1 * k, 1.5 * k, 2 * k], black_ridges=False)
    return np.clip(r / max(float(np.percentile(r[fov], 99)), 1e-12), 0, 1)


def ridge_map(image, fov, k=1.0):
    """Alternative ridge evidence compared in the paper (photograph-ridge gate): Frangi vesselness of the green
    channel of the photograph (dark ridges), with the same scales and normalisation."""
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
    """Ridge-gated reconstruction. Pass ridge=ridge_from_probability(prob, fov, k) for RGR as in the paper,
    or ridge=ridge_map(image, fov, k) for the photograph-ridge gate."""
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


def gap_join(prob, fov, base, k=1.0, rho=None, phi_deg=45.0, r_dir=None, tp_min=0.10):
    """Gap joining of RGR-J. From every skeleton end point e of base, a straight segment is drawn to the nearest pixel
    of another fragment inside a square window of half-width rho (8k). It is kept when it lies inside the field of
    view and deviates from the branch direction by at most phi_deg; the branch direction points from the mean of the
    skeleton pixels of the same fragment within r_dir (5k) towards e. Kept segments are widened where P >= tp_min
    and the mask is regrown from the 0.5 seed."""
    rho = int(round(8 * k)) if rho is None else int(rho)
    r = max(3, int(round(5 * k))) if r_dir is None else int(r_dir)
    cos_min = np.cos(np.radians(phi_deg))
    m = base.copy(); lab, _ = ndi.label(m, B3); sk = skeletonize(m); H, W = m.shape
    added = np.zeros_like(m)
    for (y, x) in _endpoints(sk):
        own = lab[y, x]
        y0, y1 = max(0, y - rho), min(H, y + rho + 1); x0, x1 = max(0, x - rho), min(W, x + rho + 1)
        ty, tx = np.nonzero((lab[y0:y1, x0:x1] > 0) & (lab[y0:y1, x0:x1] != own))
        if ty.size == 0: continue
        ty = ty + y0; tx = tx + x0; i = int(np.argmin((ty - y) ** 2 + (tx - x) ** 2)); t = np.array([ty[i], tx[i]], float)
        a0, a1 = max(0, y - r), min(H, y + r + 1); b0, b1 = max(0, x - r), min(W, x + r + 1)
        sy, sx = np.nonzero(sk[a0:a1, b0:b1] & (lab[a0:a1, b0:b1] == own))
        pts = np.stack([sy + a0, sx + b0], 1); pts = pts[(pts[:, 0] != y) | (pts[:, 1] != x)]
        if len(pts) == 0: continue
        d = np.array([y, x], float) - pts.mean(0); v = t - np.array([y, x], float)
        nd, nv = np.linalg.norm(d), np.linalg.norm(v)
        if nd == 0 or nv == 0 or float(d @ v) / (nd * nv) < cos_min: continue
        ly, lx = straight_line(int(y), int(x), int(t[0]), int(t[1]))
        if not fov[ly, lx].all(): continue
        added[ly, lx] = True
    if not added.any(): return m
    thick = ndi.binary_dilation(added, B3) & threshold(prob, fov, tp_min)
    return ndi.binary_propagation(threshold(prob, fov), structure=B3, mask=m | added | thick)


def rgr_j(prob, fov, k=1.0, tp=0.25, tv=0.05, dl=None):
    """RGR followed by gap joining, with the settings of the paper. Returns (RGR mask, RGR-J mask)."""
    dl = int(round(8 * k)) if dl is None else int(dl)
    m = rgr(prob, fov, ridge_from_probability(prob, fov, k), tp=tp, tv=tv, dl=dl)
    return m, gap_join(prob, fov, m, k)


def resolution_factor(fov_diameters_target, fov_diameters_drive):
    return float(np.median(fov_diameters_target) / np.median(fov_diameters_drive))


def fov_diameter(fov):
    return 2 * np.sqrt(fov.sum() / np.pi)
