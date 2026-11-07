import time
import numpy as np
from scipy import ndimage as ndi
from scipy.stats import wilcoxon
from skimage.morphology import skeletonize

from .recovery import threshold, B3


def counts(m, d, m0):
    y, f = d["y"], d["f"]; spk = skeletonize(m); add = m & ~m0; dd = d["dy"][add & ~y]
    c = dict(tp=(m & y).sum(), fp=(m & ~y & f).sum(), fn=(~m & y).sum(), thin_tp=(m & d["thin"]).sum(), thin_n=d["thin"].sum(),
             c_tp=(m & d["centre"]).sum(), c_n=d["centre"].sum(), sp=spk.sum(), sp_y=(spk & y).sum(), sy=d["sk"].sum(),
             sy_p=(d["sk"] & m).sum(), comp=ndi.label(m, B3)[1], comp_ref=ndi.label(y, B3)[1],
             add_tp=(add & y).sum(), add_fp=(add & ~y).sum(), add_thin=(add & d["thin"]).sum(), add_c=(add & d["centre"]).sum(),
             fp_d1=(dd <= 1.5).sum(), fp_d2=((dd > 1.5) & (dd <= 3)).sum(), fp_d3=((dd > 3) & (dd <= 5)).sum(), fp_d4=(dd > 5).sum())
    for lo, hi, n in ((0, 1, "r1"), (1, 2, "r2"), (2, 3, "r3"), (3, 99, "r4")):
        b = y & (d["lr"] > lo) & (d["lr"] <= hi); c[n + "_tp"] = (m & b).sum(); c[n + "_n"] = b.sum()
    return {k: int(v) for k, v in c.items()}


def aggregate(rows):
    s = {k: sum(r[k] for r in rows) for k in rows[0]}
    tp, fp, fn = s["tp"], s["fp"], s["fn"]; tprec, tsens = s["sp_y"] / max(s["sp"], 1), s["sy_p"] / max(s["sy"], 1)
    o = dict(dice=2 * tp / (2 * tp + fp + fn), iou=tp / (tp + fp + fn), precision=tp / max(tp + fp, 1), recall=tp / (tp + fn),
             thin_region=s["thin_tp"] / s["thin_n"], thin_centre=s["c_tp"] / s["c_n"],
             cldice=2 * tprec * tsens / max(tprec + tsens, 1e-12), components=s["comp"] / len(rows), comp_ref=s["comp_ref"] / len(rows))
    for n in ("r1", "r2", "r3", "r4"): o[n] = s[n + "_tp"] / max(s[n + "_n"], 1)
    for k in ("add_tp", "add_fp", "add_thin", "add_c", "fp_d1", "fp_d2", "fp_d3", "fp_d4"): o[k] = s[k]
    return o


def evaluate(probs, data, fn):
    rows = []; t0 = time.time()
    for p, d in zip(probs, data): rows.append(counts(fn(p, d), d, threshold(p, d["f"])))
    r = aggregate(rows); r["sec_per_image"] = (time.time() - t0) / len(data)
    return r, rows


def per_image(rows, key):
    if key == "tc": return np.array([x["c_tp"] / x["c_n"] for x in rows])
    return np.array([2 * x["tp"] / (2 * x["tp"] + x["fp"] + x["fn"]) for x in rows])


def paired_test(rows_a, rows_b):
    out = {}
    for key in ("tc", "dice"):
        diff = per_image(rows_a, key) - per_image(rows_b, key)
        out[key + "_improved"] = int((diff > 0).sum()); out[key + "_n"] = len(diff)
        out[key + "_p"] = float(wilcoxon(diff).pvalue) if np.any(diff) else 1.0
    return out


def admissible(r, base, eps=0.005):
    return r["dice"] >= base["dice"] and base["precision"] - r["precision"] <= eps
