import numpy as np
from scipy import ndimage as ndi

from .recovery import B3, fov_diameter

N8 = np.ones((3, 3), int)
CLASSES = ("correct", "shortcut", "offset", "unannotated")


def optic_disc(image, fov, y, k=1.0):
    f = fov.astype(float)
    sm = lambda a, s: ndi.gaussian_filter(a * f, s) / np.maximum(ndi.gaussian_filter(f, s), 1e-3)
    bright = sm(image[..., :2].astype(float).mean(-1), 10 * k)
    thick = y & (ndi.distance_transform_edt(y) >= 2 * k)
    dens = sm(thick.astype(float), 25 * k)
    score = (bright / max(bright[fov].max(), 1e-9)) * (dens / max(dens[fov].max(), 1e-9))
    score[~ndi.binary_erosion(fov, iterations=max(1, int(10 * k)))] = 0
    cy, cx = np.unravel_index(int(np.argmax(score)), score.shape)
    return int(cy), int(cx), float(0.15 * fov_diameter(fov))


def classify_bridges(m, seed, d, window=5.0, near=1.5, od=None):
    k = d.get("k", 1.0); y = d["y"]; dy = d["dy"]
    if "junction" not in d:
        sk = d["sk"]; nb = ndi.convolve(sk.astype(int), N8, mode="constant") - sk
        d["junction"] = sk & (nb >= 3)
    lab_s, _ = ndi.label(seed, B3)
    add = m & ~seed
    lab_a, _ = ndi.label(add, B3)
    rw = int(np.ceil(window * k)); rn = max(1, int(np.ceil(near * k)))
    out = []
    for i, sl in enumerate(ndi.find_objects(lab_a), 1):
        if sl is None: continue
        pad = rw + rn + 2
        s2 = tuple(slice(max(0, s.start - pad), min(n, s.stop + pad)) for s, n in zip(sl, m.shape))
        comp = lab_a[s2] == i
        ring = ndi.binary_dilation(comp, B3) & ~comp
        ls = lab_s[s2]
        touched = [int(t) for t in np.unique(ls[ring]) if t > 0]
        if len(touched) < 2: continue
        win = ndi.distance_transform_edt(~comp) <= rw
        yl = y[s2] & win
        lab_y, ny = ndi.label(yl, B3)
        contacts = []
        for t in touched:
            c = ring & (ls == t)
            reach = ndi.binary_dilation(c, B3, iterations=rn)
            contacts.append(set(int(v) for v in np.unique(lab_y[reach & yl]) if v > 0))
        f_ref = float((dy[s2][comp] <= near).mean())
        shared = any(contacts[a] & contacts[b] for a in range(len(contacts)) for b in range(a + 1, len(contacts)))
        all_on = all(len(c) > 0 for c in contacts)
        if not all_on: cls = "unannotated"
        elif not shared: cls = "shortcut"
        elif f_ref >= 0.5: cls = "correct"
        else: cls = "offset"
        cy, cx = (np.array(np.nonzero(comp)).mean(1) + [s2[0].start, s2[1].start])
        tags = dict(junction=bool((d["junction"][s2] & win).any()), adjacent=bool(ny >= 2),
                    optic_disc=bool(od is not None and np.hypot(cy - od[0], cx - od[1]) <= od[2]),
                    pathology=bool(d.get("pathology", False)))
        out.append(dict(cls=cls, pixels=int(comp.sum()), fragments=len(touched), f_ref=round(f_ref, 3),
                        cy=float(cy), cx=float(cx), **tags))
    return out


def rescore_unannotated(bridges, m, seed, d, near=1.5):
    if d.get("y2") is None: return bridges
    d2 = ndi.distance_transform_edt(~d["y2"]) / d.get("k", 1.0)
    lab_a, _ = ndi.label(m & ~seed, B3)
    for b in bridges:
        if b["cls"] != "unannotated": continue
        lab = lab_a[int(round(b["cy"])), int(round(b["cx"]))]
        comp = lab_a == lab if lab > 0 else None
        if comp is None or not comp.any():
            ys, xs = np.nonzero(lab_a); j = np.argmin((ys - b["cy"]) ** 2 + (xs - b["cx"]) ** 2); comp = lab_a == lab_a[ys[j], xs[j]]
        b["obs2_vessel"] = bool((d2[comp] <= near).mean() >= 0.5)
    return bridges


def summarise(bridges):
    def count(bs):
        c = {k: sum(b["cls"] == k for b in bs) for k in CLASSES}
        c["uncertain"] = c["offset"] + c["unannotated"]; c["n"] = len(bs)
        c["unannotated_obs2_vessel"] = sum(1 for b in bs if b["cls"] == "unannotated" and b.get("obs2_vessel"))
        c["unannotated_scored_obs2"] = sum(1 for b in bs if b["cls"] == "unannotated" and "obs2_vessel" in b)
        return c
    s = {"all": count(bridges)}
    for tag in ("junction", "adjacent", "optic_disc", "pathology"):
        s[tag] = count([b for b in bridges if b[tag]])
    s["none_of_these"] = count([b for b in bridges if not (b["junction"] or b["adjacent"] or b["optic_disc"])])
    return s
