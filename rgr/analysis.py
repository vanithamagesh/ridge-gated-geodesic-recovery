import numpy as np
from scipy import ndimage as ndi

from .recovery import threshold, rgr, DICE_SAFE_GATES


def _dice(m, y, f):
    tp = (m & y).sum(); fp = (m & ~y & f).sum(); fn = (~m & y).sum()
    return 2 * tp / max(2 * tp + fp + fn, 1)


def estimates(q, f, seed, add):
    d_hat = 2 * q[seed].sum() / (seed.sum() + q[f].sum())
    p_hat = float(q[add].mean()) if add.any() else float("nan")
    return float(d_hat), p_hat


def dice_safe(prob, fov, ridge, tv=0.05, dl=8, gates=DICE_SAFE_GATES, q=None):
    q = prob if q is None else q
    seed = threshold(prob, fov)
    d_hat = 2 * q[seed].sum() / (seed.sum() + q[fov].sum())
    best, chosen = seed, None
    for tp in gates:
        m = rgr(prob, fov, ridge, tp=tp, tv=tv, dl=dl); add = m & ~seed
        if add.sum() == 0 or q[add].mean() > d_hat / 2: best, chosen = m, tp
        else: break
    return best, chosen


def dice_rule(prob, d, m, q=None):
    f, y = d["f"], d["y"]; q = prob if q is None else q
    seed = threshold(prob, f); add = m & ~seed
    d_hat, p_hat = estimates(q, f, seed, add)
    D0, D1 = _dice(seed, y, f), _dice(m, y, f)
    n = int(add.sum())
    return dict(case=d["case"], added=n, d_hat=d_hat, p_hat=p_hat, true_dice=float(D0),
                true_precision=float((add & y).sum() / n) if n else float("nan"), dice_change=float(D1 - D0),
                predicted_rise=bool(n and p_hat > d_hat / 2), observed_rise=bool(D1 > D0))


def gate_choice(prob, d, ridge, tv=0.05, dl=8, gates=DICE_SAFE_GATES, q=None):
    f, y = d["f"], d["y"]; seed = threshold(prob, f)
    best_d, best_g = _dice(seed, y, f), None
    per = {}
    for tp in gates:
        dd = _dice(rgr(prob, f, ridge, tp=tp, tv=tv, dl=dl), y, f); per[tp] = float(dd)
        if dd > best_d: best_d, best_g = dd, tp
    _, chosen = dice_safe(prob, f, ridge, tv, dl, gates, q)
    return dict(case=d["case"], chosen=chosen, optimum=best_g, dice_seed=float(_dice(seed, y, f)),
                dice_chosen=per.get(chosen, float(_dice(seed, y, f))) if chosen else float(_dice(seed, y, f)),
                dice_optimum=float(best_d), dice_per_gate=per)


def missed_thin(prob, d, edges=(0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50)):
    f = d["f"]; seed = threshold(prob, f); miss = d["thin"] & ~seed
    near = miss & (ndi.distance_transform_edt(~seed) <= 8 * d.get("k", 1.0))
    h = lambda s: np.histogram(prob[s], bins=edges)[0].astype(int).tolist()
    return dict(case=d["case"], n_missed=int(miss.sum()), n_near=int(near.sum()), hist_all=h(miss), hist_near=h(near))


def observer2(m, seed, d, near=1.5):
    y2 = d["y2"]
    if y2 is None: return None
    add = m & ~seed; false1 = add & ~d["y"]
    d2 = ndi.distance_transform_edt(~y2) / d.get("k", 1.0)
    return dict(case=d["case"], added=int(add.sum()), false_obs1=int(false1.sum()),
                vessel_obs2=int((false1 & y2).sum()), near_obs2=int((false1 & (d2 <= near)).sum()),
                true_obs2=int((add & y2).sum()))
