import numpy as np
from scipy import ndimage as ndi
from skimage.measure import euler_number
from skimage.morphology import skeletonize

from .recovery import B3

N8 = np.ones((3, 3), int)


def betti(m):
    b0 = ndi.label(m, B3)[1]
    return int(b0), int(b0 - euler_number(m, connectivity=2))


def extra_counts(m, d, tol=2.0):
    y, f = d["y"], d["f"]; k = d.get("k", 1.0)
    tp = int((m & y).sum()); fp = int((m & ~y & f).sum()); fn = int((~m & y).sum()); tn = int((~m & ~y & f).sum())
    b0, b1 = betti(m & f)
    if "betti_ref" not in d: d["betti_ref"] = betti(y)
    r0, r1 = d["betti_ref"]
    sp = skeletonize(m & f)
    if "dt_sk" not in d: d["dt_sk"] = ndi.distance_transform_edt(~d["sk"]).astype(np.float32)
    dsp = ndi.distance_transform_edt(~sp) if sp.any() else np.full(m.shape, np.inf)
    t = tol * k
    return dict(tp=tp, fp=fp, fn=fn, tn=tn, b0=b0, b1=b1, b0_ref=r0, b1_ref=r1,
                skp_hit=int((sp & (d["dt_sk"] <= t)).sum()), skp_n=int(sp.sum()),
                sky_hit=int((d["sk"] & (dsp <= t)).sum()), sky_n=int(d["sk"].sum()))


def pooled_extra(rows):
    s = {k: sum(r[k] for r in rows) for k in ("tp", "fp", "fn", "tn", "skp_hit", "skp_n", "sky_hit", "sky_n")}
    tp, fp, fn, tn = (float(s[k]) for k in ("tp", "fp", "fn", "tn"))
    mcc = (tp * tn - fp * fn) / max(np.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)), 1e-12)
    sp, sr = s["skp_hit"] / max(s["skp_n"], 1), s["sky_hit"] / max(s["sky_n"], 1)
    return dict(accuracy=(tp + tn) / (tp + tn + fp + fn), specificity=tn / (tn + fp), sensitivity=tp / (tp + fn), mcc=mcc,
                betti0_error=float(np.mean([abs(r["b0"] - r["b0_ref"]) for r in rows])),
                betti1_error=float(np.mean([abs(r["b1"] - r["b1_ref"]) for r in rows])),
                skeleton_precision=sp, skeleton_recall=sr, skeleton_f1=2 * sp * sr / max(sp + sr, 1e-12))


def skeleton_graph(sk):
    nb = ndi.convolve(sk.astype(int), N8, mode="constant") - sk
    ends = sk & (nb == 1)
    junction = sk & (nb >= 3)
    return int(ends.sum()), int(ndi.label(junction, B3)[1])


def skeleton_length(sk):
    s = sk
    h = s[:, :-1] & s[:, 1:]; v = s[:-1] & s[1:]
    d1 = s[:-1, :-1] & s[1:, 1:]; d2 = s[:-1, 1:] & s[1:, :-1]
    d1 = d1 & ~(s[:-1, 1:] | s[1:, :-1]); d2 = d2 & ~(s[:-1, :-1] | s[1:, 1:])
    return float(h.sum() + v.sum() + np.sqrt(2) * (d1.sum() + d2.sum()))


def fractal_dimension(sk):
    ys, xs = np.nonzero(sk)
    if len(ys) < 10: return float("nan")
    sizes = np.array([2, 4, 8, 16, 32, 64]); n = []
    for s in sizes:
        n.append(len(set(zip((ys // s).tolist(), (xs // s).tolist()))))
    return float(-np.polyfit(np.log(sizes), np.log(n), 1)[0])


def prune_spurs(sk, max_len):
    sk = sk.copy()
    while True:
        nb = ndi.convolve(sk.astype(int), N8, mode="constant") - sk
        ends = sk & (nb == 1); junction = sk & (nb >= 3)
        if not ends.any(): return sk
        body = sk & ~junction
        lab, n = ndi.label(body, B3)
        if n == 0: return sk
        sizes = ndi.sum(body, lab, index=np.arange(1, n + 1))
        has_end = ndi.maximum(ends, lab, index=np.arange(1, n + 1)) > 0
        touches_j = ndi.maximum(ndi.binary_dilation(junction, B3), lab, index=np.arange(1, n + 1)) > 0
        spur = has_end & touches_j & (sizes <= max_len)
        if not spur.any(): return sk
        sk &= ~np.isin(lab, np.flatnonzero(spur) + 1)


def vessel_measures(m, f, k=1.0, spur=5.0):
    m = m & f; sk = skeletonize(m)
    ends_raw, branches_raw = skeleton_graph(sk)
    skp = prune_spurs(sk, int(round(spur * k)))
    ends, branches = skeleton_graph(skp)
    return dict(density=float(m.sum() / f.sum()), length=skeleton_length(sk) / k, branch_points=branches,
                end_points=ends, branch_points_raw=branches_raw, end_points_raw=ends_raw,
                fractal_dimension=fractal_dimension(sk))


def measurement_errors(pred, ref):
    out = {}
    for key in ("length", "branch_points", "end_points", "branch_points_raw", "end_points_raw"):
        out[key] = 100 * (pred[key] - ref[key]) / max(ref[key], 1e-9)
    out["density"] = 100 * (pred["density"] - ref["density"])
    out["fractal_dimension"] = pred["fractal_dimension"] - ref["fractal_dimension"]
    return out


def bootstrap_ci(stat, n, b=10000, seed=0, alpha=0.05):
    rng = np.random.default_rng(seed)
    vals = np.array([stat(rng.integers(0, n, n)) for _ in range(b)])
    return float(stat(np.arange(n))), float(np.quantile(vals, alpha / 2)), float(np.quantile(vals, 1 - alpha / 2))


def holm(pvalues):
    p = np.asarray(pvalues, float); m = len(p); order = np.argsort(p)
    adj = np.empty(m); running = 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * p[i])); adj[i] = running
    return adj.tolist()


def ece(prob, y, bins=10):
    idx = np.minimum((prob * bins).astype(int), bins - 1); e = 0.0
    for b in range(bins):
        s = idx == b
        if s.any(): e += s.mean() * abs(y[s].mean() - prob[s].mean())
    return float(e)


def reliability(prob, y, bins=10):
    idx = np.minimum((prob * bins).astype(int), bins - 1)
    return [dict(lo=b / bins, hi=(b + 1) / bins, n=int((idx == b).sum()),
                 mean_p=float(prob[idx == b].mean()) if (idx == b).any() else None,
                 frac=float(y[idx == b].mean()) if (idx == b).any() else None) for b in range(bins)]


class HistogramBinning:
    def __init__(self, bins=15): self.bins = bins

    def fit(self, p, y):
        idx = np.minimum((p * self.bins).astype(int), self.bins - 1)
        self.v = np.array([y[idx == b].mean() if (idx == b).any() else (b + 0.5) / self.bins for b in range(self.bins)])
        return self

    def __call__(self, p):
        return self.v[np.minimum((p * self.bins).astype(int), self.bins - 1)]


class Isotonic:
    def fit(self, p, y):
        from sklearn.isotonic import IsotonicRegression
        sub = np.random.default_rng(0).choice(len(p), min(len(p), 400000), replace=False)
        self.r = IsotonicRegression(y_min=0, y_max=1, out_of_bounds="clip").fit(p[sub], y[sub].astype(float))
        return self

    def __call__(self, p):
        return self.r.predict(p.ravel()).reshape(p.shape)
