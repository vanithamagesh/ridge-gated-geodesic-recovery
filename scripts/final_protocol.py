# -*- coding: utf-8 -*-
"""
final_protocol.py (RGR_final_protocol_v1_5)  -  one frozen protocol for the remaining analyses. No network is trained.

What it does, with the parameters of the paper left untouched (tau_p 0.25, tau_v 0.05, delta 8k, rho 8k, theta 0.3, tau_min 0.10):

  1. Scale factor k from the TRAINING field-of-view masks alone, beside the factor of the paper (training + test masks).
  2. Four-way path ablation on identical probability maps: 0.5 threshold, paths applied directly to the 0.5 mask,
     RGR, and RGR followed by paths (RGR-P); plus RGR without its probability gate.
     New in v1_1: a geometric reconnection control on the 0.5 mask (same end points, window and thickening as path
     completion, but each end point is joined to the nearest fragment by a straight line), with and without a
     45-degree direction rule. It is modelled on the gap-filling rule of Dulau et al. (ICCV Workshops 2023).
     New in v1_2: the ridge evidence is isolated. The probability gate of RGR is swept (0.45 to 0.15) with the ridge
     gate (a) from the photograph, as in the paper, (b) switched off and (c) computed from the probability map instead
     of the photograph; seed, distance limit and connectivity stay fixed. RGR is compared with (b) and (c) at its own
     precision, with bootstrap intervals from the same network outputs.
     New in v1_3: the reconstruction with the ridge taken from the probability map is run as a full procedure
     (RGR-M: scores, bridges, margins), followed by straight joining with the direction rule (RGR-M + joining) or by
     minimal-cost paths; its ridge gate is swept for the sensitivity analysis; the four DRIVE validation images are
     analysed as their own subset; and the run time of each step is recorded. All settings stay those of the paper.
     New in v1_5 (shorter FIVES part; nothing already finished is computed again): the 160 held-out FIVES photographs get
     RGR-M and RGR-M with straight joining only (no minimal-cost paths after RGR-M, no further ridge-gate sweep), the
     FIVES check with the scale factor from training masks keeps the procedures it already has, the photograph ridge is
     computed only where a missing result needs it, and the 40 FIVES photographs of the paper are analysed first.
     New in v1_4 (same analysis as v1_3): the prepared FIVES photographs are saved to Drive once, so a restart after a
     disconnect restores them in about two minutes instead of preparing them again for twenty.
     DRIVE, CHASE_DB1 and STARE use the probability maps already on Drive (all seeds found).
  3. FIVES: probability maps are exported with the three saved networks (inference only) for all 200 official test
     photographs. The 40 photographs of the paper and the 160 photographs never used before are analysed separately;
     the 160 use the training-only scale factor.

Everything is resumable: finished probability maps and finished per-image results are kept, so the script can be
started again after a disconnect and continues where it stopped. Results of v1_0 and v1_1 in the same folder are reused:
only what is new in this version is computed for photographs that an earlier version already finished.

Typical call (Colab):
    python RGR_final_protocol_v1_5.py --drive-out /content/drive/MyDrive/TVR_revision --repo /content/rgr_repo
Results: <drive-out>/final_protocol_v1_0/  (tables as CSV, all_results.json, RGR_final_protocol_results_v1_5.zip)

Names in this script and in its result tables, and the names used in the paper:
    rgrm, "RGR-M (ridge from the probability map)"         ->  RGR
    rgrm_join, "RGR-M, then straight joining ..."           ->  RGR-J
    rgr, "RGR" (ridge from the photograph)                  ->  photograph-ridge gate
    rgr_p, "RGR-P"                                          ->  photograph-ridge gate with minimal-cost paths
    rgrm_paths                                              ->  RGR with minimal-cost paths
    geo_on_seed / geo_free_on_seed                          ->  straight joining on the 0.5 mask, with / without the direction rule
    paths_on_seed                                           ->  minimal-cost paths on the 0.5 mask
"""
import argparse, csv, json, multiprocessing as mp, os, re, shutil, subprocess, sys, time, zipfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import numpy as np
from scipy import ndimage as ndi
from skimage.morphology import skeletonize
from skimage.draw import line as straight_line
from skimage.filters import frangi

ap = argparse.ArgumentParser()
ap.add_argument("--drive-out", type=Path, required=True, help="folder of the earlier run: contains probs/, models/ and fives.rar")
ap.add_argument("--repo", type=Path, help="clone of github.com/vanithamagesh/ridge-gated-geodesic-recovery")
ap.add_argument("--work", type=Path, default=Path("/content/work"), help="local scratch folder (datasets are prepared here)")
ap.add_argument("--out", type=Path, help="result folder (default: <drive-out>/final_protocol_v1_0)")
ap.add_argument("--datasets", nargs="+", default=["drive", "chase", "stare", "fives"])
ap.add_argument("--seeds", type=int, nargs="+", default=[7, 11, 23])
ap.add_argument("--archs", nargs="+", default=["unet", "attunet", "unetpp"])
ap.add_argument("--boot", type=int, default=10000)
ap.add_argument("--workers", type=int, default=0, help="parallel processes for the per-image analysis (0 = all CPU cores)")
ap.add_argument("--device", default=None)
ap.add_argument("--fives-archive", type=Path, help="FIVES archive (default: <drive-out>/fives.rar or fives.zip)")
ap.add_argument("--fives-raw", type=Path, help="FIVES already extracted (folder that contains train/ and test/)")
ap.add_argument("--fives-paper-per-category", type=int, default=10, help="test photographs per category used in the paper")
ap.add_argument("--fives-train-per-category", type=int, default=25, help="training photographs per category used in the paper")
ap.add_argument("--skip-export", action="store_true", help="do not export FIVES maps (use the ones already saved)")
ap.add_argument("--tables-only", action="store_true")
a = ap.parse_args()
OUT = a.out or (a.drive_out / "final_protocol_v1_0"); OUT.mkdir(parents=True, exist_ok=True); a.work.mkdir(parents=True, exist_ok=True)
t0 = time.time()
def log(*x): print(f"[{(time.time() - t0) / 60:6.1f} min]", *x, flush=True)

here = Path(__file__).resolve().parent
ROOT = a.repo or (here.parent if (here.parent / "rgr").exists() else here if (here / "rgr").exists() else Path.cwd())
assert (ROOT / "rgr").exists(), f"rgr package not found under {ROOT}; pass --repo <folder of the cloned repository>"
sys.path.insert(0, str(ROOT))
from rgr.recovery import threshold, rgr, rgr_p, B3, _endpoints
from rgr.metrics import counts
from rgr.data import load_eval, discover, read_bin, read_rgb, fov_diameter, prepare_chase, prepare_stare, prepare_fives, DRIVE_VALID

DS_NAME = {"drive": "DRIVE", "chase": "CHASE_DB1", "stare": "STARE", "fives": "FIVES"}
NET_NAME = {"unet": "U-Net", "attunet": "Attention U-Net", "unetpp": "U-Net++"}
PROCS = ("threshold", "paths_on_seed", "geo_on_seed", "geo_free_on_seed", "rgr", "rgr_p", "rgr_no_pgate", "rgrm", "rgrm_join", "rgrm_paths")
MAP_TV = (0.02, 0.10, 0.20)                                  # further ridge gates of the map-ridge sensitivity sweep (0.05 is the gate of the paper)
PROC_NAME = {"threshold": "0.5 threshold", "paths_on_seed": "Paths on the 0.5 mask", "rgr": "RGR", "rgr_p": "RGR-P (RGR, then paths)", "rgr_no_pgate": "RGR without the probability gate",
             "geo_on_seed": "Geometric joining on the 0.5 mask, direction within 45 degrees", "geo_free_on_seed": "Geometric joining on the 0.5 mask, no direction rule",
             "rgrm": "RGR-M (ridge from the probability map)", "rgrm_join": "RGR-M, then straight joining with the direction rule", "rgrm_paths": "RGR-M, then minimal-cost paths"}
OLD_PROCS = ("threshold", "paths_on_seed", "geo_on_seed", "geo_free_on_seed", "rgr", "rgr_p", "rgr_no_pgate")          # procedures that need no map ridge
LIGHT_PROCS = OLD_PROCS + ("rgrm", "rgrm_join")                                                                    # held-out FIVES photographs
PHOTO_PROCS = ("paths_on_seed", "rgr", "rgr_p", "rgr_no_pgate")                                                    # procedures that read the photograph ridge
BRIDGE_PROCS = ("paths_on_seed", "geo_on_seed", "geo_free_on_seed", "rgr", "rgr_p", "rgrm", "rgrm_join", "rgrm_paths")
CLASSES = ("correct", "mixed", "shortcut", "offset", "unannotated")
GATES = (0.45, 0.40, 0.35, 0.30, 0.25, 0.20, 0.15)          # probability gates of the ridge-evidence sweep; 0.25 is the gate of the paper
RIDGE_VARIANTS = {"photo": "ridge from the photograph (RGR)", "none": "ridge gate switched off", "prob": "ridge from the probability map"}
SUMK = ("tp", "fp", "fn", "c_tp", "c_n", "comp", "sp", "sp_y", "sy", "sy_p")
GRID = {ds: [round(float(t), 2) for t in np.arange(0.30, 0.701, 0.05 if ds == "fives" else 0.02)] for ds in DS_NAME}
# values of the earlier re-analysis on the 40 FIVES photographs (same saved networks): gain of RGR and RGR-P over the 0.5 threshold, bridges
FIVES_REF = {"unet": (3.8859, 4.5032, 1750, 4786), "attunet": (3.8491, 4.4603, 1349, 4077), "unetpp": (4.0067, 4.6159, 1448, 3811)}


def sh(cmd, check=True):
    log("$", cmd); return subprocess.run(cmd, shell=True, check=check)


# ------------------------------------------------------------------ ridge evidence
def ridge_from_probability(prob, fov, k=1.0):
    """The ridge filter of the paper (same scales and normalisation) applied to the probability map instead of the green channel."""
    r = frangi(prob.astype(np.float32), sigmas=[1 * k, 1.5 * k, 2 * k], black_ridges=False)
    return np.clip(r / max(float(np.percentile(r[fov], 99)), 1e-12), 0, 1)


# ------------------------------------------------------------------ geometric reconnection control
def geo_paths(prob, fov, K, rho, base, tp_min=0.10, max_angle=45.0):
    """Same end points, search window, thickening and regrowth as path completion; the path itself is a straight line
    from the end point to the nearest pixel of another fragment, kept when it deviates from the direction of the
    branch at the end point by at most max_angle degrees (180 = no direction rule)."""
    m = base.copy(); lab, _ = ndi.label(m, B3); sk = skeletonize(m); H, W = m.shape; added = np.zeros_like(m)
    r = max(3, int(round(5 * K))); cmin = np.cos(np.deg2rad(max_angle))
    for (y, x) in _endpoints(sk):
        y0, y1 = max(0, y - rho), min(H, y + rho + 1); x0, x1 = max(0, x - rho), min(W, x + rho + 1)
        own = lab[y, x]; L = lab[y0:y1, x0:x1]; targets = (L > 0) & (L != own)
        if not targets.any(): continue
        ty, tx = np.nonzero(targets); i = int(np.argmin((ty + y0 - y) ** 2 + (tx + x0 - x) ** 2)); ty, tx = int(ty[i] + y0), int(tx[i] + x0)
        a0, a1 = max(0, y - r), min(H, y + r + 1); b0, b1 = max(0, x - r), min(W, x + r + 1)
        by, bx = np.nonzero(sk[a0:a1, b0:b1] & (lab[a0:a1, b0:b1] == own)); by = by + a0; bx = bx + b0
        keep = (by != y) | (bx != x)
        if not keep.any(): continue
        vb = np.array([y - by[keep].mean(), x - bx[keep].mean()]); vl = np.array([ty - y, tx - x], float)
        nb, nl = np.linalg.norm(vb), np.linalg.norm(vl)
        if nb == 0 or nl == 0 or float(vb @ vl) / (nb * nl) < cmin: continue
        ly, lx = straight_line(int(y), int(x), ty, tx)
        if not fov[ly, lx].all(): continue
        added[ly, lx] = True
    if not added.any(): return m
    thick = ndi.binary_dilation(added, B3) & threshold(prob, fov, tp_min)
    return ndi.binary_propagation(threshold(prob, fov), structure=B3, mask=m | added | thick)


# ------------------------------------------------------------------ bridges (rule of the paper and the stricter rule)
def classify_bridges(m, seed, d, window=5.0, near=1.5):
    k = d.get("k", 1.0); y = d["y"]; dy = d["dy"]
    lab_s, _ = ndi.label(seed, B3); lab_a, _ = ndi.label(m & ~seed, B3)
    rw = int(np.ceil(window * k)); rn = max(1, int(np.ceil(near * k))); out = {c: 0 for c in CLASSES}; out.update(n=0, correct_published_rule=0)
    for i, sl in enumerate(ndi.find_objects(lab_a), 1):
        if sl is None: continue
        pad = rw + rn + 2
        s2 = tuple(slice(max(0, s.start - pad), min(n, s.stop + pad)) for s, n in zip(sl, m.shape))
        comp = lab_a[s2] == i; ring = ndi.binary_dilation(comp, B3) & ~comp; ls = lab_s[s2]
        touched = [int(t) for t in np.unique(ls[ring]) if t > 0]
        if len(touched) < 2: continue
        win = ndi.distance_transform_edt(~comp) <= rw; yl = y[s2] & win; lab_y, _ = ndi.label(yl, B3)
        contacts = []
        for t in touched:
            reach = ndi.binary_dilation(ring & (ls == t), B3, iterations=rn)
            contacts.append(set(int(v) for v in np.unique(lab_y[reach & yl]) if v > 0))
        f_ref = float((dy[s2][comp] <= near).mean()); n = len(contacts)
        pairs = [(p, q) for p in range(n) for q in range(p + 1, n)]; joined = [bool(contacts[p] & contacts[q]) for p, q in pairs]
        parent = list(range(n))
        def find(x):
            while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
            return x
        for (p, q), j in zip(pairs, joined):
            if j: parent[find(p)] = find(q)
        groups = len(set(find(x) for x in range(n))); all_on = all(len(c) > 0 for c in contacts)
        old = "unannotated" if not all_on else "shortcut" if not any(joined) else "correct" if f_ref >= 0.5 else "offset"
        new = "unannotated" if not all_on else "shortcut" if not any(joined) else "mixed" if groups > 1 else "correct" if f_ref >= 0.5 else "offset"
        out["n"] += 1; out[new] += 1; out["correct_published_rule"] += old == "correct"
    return out


# ------------------------------------------------------------------ per-image work (runs in worker processes)
def load_map(path):
    path = Path(path)
    return (np.load(path)["p"] if path.suffix == ".npz" else np.load(path)).astype(np.float32)


def image_task(task):
    ds, root, case, K, runs, split = task
    todo = []; need_rf = False
    for r in runs:
        old = None; need, tv = r[4], r[5]
        if Path(r[3]).exists():
            try: old = json.load(open(r[3]))
            except Exception: old = None
        if old is None or any(n not in old["procedures"] for n in need) or "ridge_sweep" not in old or (tv and "map_tv_sweep" not in old):
            todo.append((r, old))
            need_rf = need_rf or old is None or "ridge_sweep" not in old or any(n in PHOTO_PROCS and n not in old["procedures"] for n in need)
    if not todo: return case, 0, 0.0
    t1 = time.time()
    d = load_eval(Path(root), split, cases={case}, k=K, with_rf=need_rf)[0]
    DL = int(round(8 * K)); RHO = int(round(8 * K)); ridge = (d["rfk"] if K != 1.0 else d["rf"]) if need_rf else None; f, y = d["f"], d["y"]
    for (arch, seed, mpath, rpath, need, tv_need), old in todo:
        p = load_map(mpath); s = threshold(p, f); memo = {}; secs = {}
        def rpm():
            if "rp" not in memo:
                tq = time.time(); memo["rp"] = ridge_from_probability(p, f, K); secs["ridge_map_filter"] = time.time() - tq
            return memo["rp"]
        def rgrm_mask():
            if "m" not in memo:
                r_ = rpm(); tq = time.time(); memo["m"] = rgr(p, f, r_, tp=0.25, tv=0.05, dl=DL); secs["reconstruction"] = time.time() - tq
            return memo["m"]
        def rgrm_join_mask():
            b_ = rgrm_mask(); tq = time.time(); m_ = geo_paths(p, f, K, RHO, b_); secs["joining"] = time.time() - tq; return m_
        make = {"rgrm": rgrm_mask, "rgrm_join": rgrm_join_mask, "rgrm_paths": lambda: rgr_p(p, f, rpm(), 0.25, 0.05, DL, RHO, 0.3),"threshold": lambda: s,
                "paths_on_seed": lambda: rgr_p(p, f, ridge, 0.25, 0.05, DL, RHO, 0.3, base=s),
                "geo_on_seed": lambda: geo_paths(p, f, K, RHO, s),
                "geo_free_on_seed": lambda: geo_paths(p, f, K, RHO, s, max_angle=180.0),
                "rgr": lambda: rgr(p, f, ridge, tp=0.25, tv=0.05, dl=DL),
                "rgr_p": lambda: rgr_p(p, f, ridge, 0.25, 0.05, DL, RHO, 0.3),
                "rgr_no_pgate": lambda: rgr(p, f, ridge, tp=0.0, tv=0.05, dl=DL)}
        row = old or dict(case=case, k=K, procedures={}, bridges={}, sweep=[])
        for n in need:
            if n in row["procedures"]: continue
            m = make[n](); row["procedures"][n] = counts(m, d, s)
            if n in BRIDGE_PROCS: row["bridges"][n] = classify_bridges(m, s, d)
        if "ridge_sweep" not in row:
            rp = rpm(); rs = {}
            for name, kw in (("photo", dict(ridge=ridge)), ("none", dict(ridge=ridge, use_ridge=False)), ("prob", dict(ridge=rp))):
                rs[name] = []
                for g in GATES:
                    m = rgr(p, f, kw["ridge"], tp=g, tv=0.05, dl=DL, use_ridge=kw.get("use_ridge", True))
                    rs[name].append([int((m & y).sum()), int((m & ~y & f).sum()), int((m & d["centre"]).sum()), int(ndi.label(m, B3)[1])])
            row["ridge_sweep"] = rs
        if tv_need and "map_tv_sweep" not in row:
            rp = rpm(); ms = {}
            for tv in MAP_TV:
                ms[f"{tv:.2f}"] = []
                for g in GATES:
                    m = rgr(p, f, rp, tp=g, tv=tv, dl=DL)
                    ms[f"{tv:.2f}"].append([int((m & y).sum()), int((m & ~y & f).sum()), int((m & d["centre"]).sum()), int(ndi.label(m, B3)[1])])
            row["map_tv_sweep"] = ms
        if secs: row.setdefault("seconds", {}).update(secs)
        if not row["sweep"]:
            for t in GRID[ds]:
                m = threshold(p, f, t); row["sweep"].append([int((m & y).sum()), int((m & ~y & f).sum()), int((m & d["centre"]).sum())])
        Path(rpath).parent.mkdir(parents=True, exist_ok=True); tmp = str(rpath) + ".tmp"
        json.dump(row, open(tmp, "w"), default=int); os.replace(tmp, rpath)
    return case, len(todo), time.time() - t1


# ------------------------------------------------------------------ data
def clone(url, dst):
    if not Path(dst).exists(): sh(f"git clone -q --depth 1 {url} {dst}")
    return Path(dst)


def prepare_roots():
    roots = {}
    sgl = clone("https://github.com/SHI-Labs/SGL-Retinal-Vessel-Segmentation", a.work / "sgl"); roots["drive"] = sgl / "dataset"
    if "chase" in a.datasets:
        r = a.drive_out / "data" / "chase"
        roots["chase"] = r if (r / "DRIVET" / "HR").exists() else prepare_chase(sgl / "dataset", a.work / "data" / "chase")
    if "stare" in a.datasets:
        r = a.drive_out / "data" / "stare"
        if (r / "DRIVET" / "HR").exists(): roots["stare"] = r
        else:
            ddn = clone("https://github.com/sraashis/deepdyn", a.work / "deepdyn"); roots["stare"] = prepare_stare(ddn / "data" / "STARE", a.work / "data" / "stare")
    if "fives" in a.datasets:
        full = a.work / "fives_full"; cache = a.drive_out / "fives_prepared_cache_v1.tar"
        if not (full / ".prepared").exists() and cache.exists():
            log(f"FIVES: restoring the prepared photographs from Drive ({cache.stat().st_size / 1e9:.2f} GB, about two minutes)")
            try:
                shutil.rmtree(full, ignore_errors=True); sh(f"tar -xf '{cache}' -C '{a.work}'")
            except Exception as exc:
                log("restore failed; the photographs are prepared again:", exc); shutil.rmtree(full, ignore_errors=True)
        if not (full / ".prepared").exists():
            raw = a.fives_raw
            if raw is None:
                fz = a.fives_archive or next((q for q in (a.drive_out / "fives.rar", a.drive_out / "fives.zip") if q.exists()), None)
                assert fz is not None and fz.exists(), f"FIVES archive not found in {a.drive_out} (expected fives.rar); pass --fives-archive"
                raw = a.work / "fives_raw"
                if not (raw / ".extracted").exists():
                    log(f"FIVES: extracting {fz.name} ({fz.stat().st_size / 1e9:.2f} GB)")
                    shutil.rmtree(raw, ignore_errors=True); raw.mkdir(parents=True)
                    if open(fz, "rb").read(4) == b"Rar!":
                        if subprocess.run("command -v unrar > /dev/null && command -v 7z > /dev/null", shell=True).returncode != 0:
                            sh("(apt-get -qq update && apt-get -qq install -y unrar p7zip-full p7zip-rar) > /dev/null 2>&1", check=False)
                        sh(f"unrar x -idq -o+ '{fz}' '{raw}/' || 7z x -y -o'{raw}' '{fz}' > /dev/null")
                    else:
                        zipfile.ZipFile(fz).extractall(raw)
                    for inner in list(raw.rglob("*.zip")): zipfile.ZipFile(inner).extractall(inner.parent); inner.unlink()
                    (raw / ".extracted").write_text("ok\n")
            log("FIVES: preparing the training photographs of the paper and all 200 official test photographs")
            shutil.rmtree(full, ignore_errors=True)
            prepare_fives(raw, full, a.fives_train_per_category, None)
            (full / ".prepared").write_text(f"{len(discover(full, 'test'))} test photographs\n")
            try:
                tmp = cache.with_name(cache.name + ".tmp"); sh(f"tar -cf '{tmp}' -C '{a.work}' fives_full"); os.replace(tmp, cache)
                log("FIVES: prepared photographs saved to Drive; a restart will now skip this step")
            except Exception as exc:
                log("could not save the prepared photographs to Drive (the run continues):", exc)
        roots["fives"] = full
    return {k: v for k, v in roots.items() if k in a.datasets or k == "drive"}


def fives_split(root):
    """Cases of the paper (lowest numbers of each category) and the remaining held-out cases."""
    by = {}
    for p in discover(root, "test"):
        m = re.match(r"(\d+)([ADGN])$", p.case); by.setdefault(m.group(2), []).append(p.case)
    paper = sorted(c for cat in by for c in sorted(by[cat])[:a.fives_paper_per_category])
    held = sorted(c for cat in by for c in sorted(by[cat])[a.fives_paper_per_category:])
    return paper, held


def diam(root, split, cases=None):
    return [fov_diameter(read_bin(p.fov)) for p in discover(root, split) if cases is None or p.case in cases]


# ------------------------------------------------------------------ FIVES probability maps (inference only)
def export_fives(root, cases):
    import torch
    from rgr import networks as nets
    device = a.device or ("cuda" if torch.cuda.is_available() else "cpu")
    pdir = OUT / "probs_fives"; pdir.mkdir(exist_ok=True)
    pairs = {p.case: p for p in discover(root, "test")}
    def predict(model, img):
        try:
            return nets.predict(model, img, device)
        except torch.OutOfMemoryError:
            torch.cuda.empty_cache(); H, W, _ = img.shape; T, O = 1024, 128
            acc = np.zeros((H, W), np.float32); cnt = np.zeros((H, W), np.float32)
            for y0 in range(0, H, T - O):
                for x0 in range(0, W, T - O):
                    y1, x1 = min(H, y0 + T), min(W, x0 + T)
                    acc[y0:y1, x0:x1] += nets.predict(model, np.ascontiguousarray(img[y0:y1, x0:x1]), device); cnt[y0:y1, x0:x1] += 1
            return acc / cnt
    for arch in a.archs:
        todo = [c for c in cases if not (pdir / f"fives_{arch}_s7_{c}.npz").exists()]
        if not todo: log(f"FIVES maps, {NET_NAME[arch]}: all {len(cases)} present"); continue
        w = a.drive_out / "models" / f"{arch}_fives_s7.pt"
        assert w.exists(), f"weight file not found: {w}. This script does not train; put the saved FIVES weights there."
        if device == "cpu": log("no GPU: exporting on the CPU is slow (choose Runtime > Change runtime type > T4 GPU)")
        model = nets.load(arch, w, device); t1 = time.time()
        for i, c in enumerate(todo, 1):
            p = predict(model, read_rgb(pairs[c].image)).astype(np.float16)
            tmp = pdir / f"fives_{arch}_s7_{c}.tmp.npz"; np.savez_compressed(tmp, p=p); os.replace(tmp, pdir / f"fives_{arch}_s7_{c}.npz")
            if i % 20 == 0 or i == len(todo): log(f"FIVES maps, {NET_NAME[arch]}: {i}/{len(todo)} ({(time.time() - t1) / i:.1f} s per photograph)")
        del model
        if device.startswith("cuda"): torch.cuda.empty_cache()
    return pdir


# ------------------------------------------------------------------ statistics from the per-image rows
def unit_sums(rows, groups, proc):
    return np.array([[sum(rows[i]["procedures"][proc][k] for i in g) for k in SUMK] + [len(g)] for g in groups], float)


def stats(S):
    tp, fp, fn, ctp, cn, comp, sp, spy, sy, syp, n = (S[..., j] for j in range(11))
    tprec = spy / np.maximum(sp, 1); tsens = syp / np.maximum(sy, 1)
    return np.stack([100 * tp / np.maximum(tp + fp, 1), 100 * ctp / np.maximum(cn, 1), 100 * 2 * tp / np.maximum(2 * tp + fp + fn, 1), comp / np.maximum(n, 1),
                     100 * 2 * tprec * tsens / np.maximum(tprec + tsens, 1e-12), 100 * tp / np.maximum(tp + fn, 1)], -1)
STAT = ("precision", "thin_centre", "dice", "fragments", "cldice", "recall")


def summarise(rows, groups, ds, nboot, seed=0):
    C = len(groups); rng = np.random.default_rng(seed); Wb = rng.multinomial(C, np.full(C, 1.0 / C), size=nboot).astype(float); I = np.eye(C)
    HAVE = tuple(p for p in PROCS if all(p in r["procedures"] for r in rows)); has_tv = all("map_tv_sweep" in r for r in rows)
    A = {p: unit_sums(rows, groups, p) for p in HAVE}
    est = {p: stats(A[p].sum(0)) for p in HAVE}; boot = {p: stats(Wb @ A[p]) for p in HAVE}; unit = {p: stats(A[p]) for p in HAVE}
    res = dict(units=C, images=len(rows), procedures={}, contrasts={}, equal_precision={}, bridges={})
    for p in HAVE:
        res["procedures"][p] = {k: float(est[p][j]) for j, k in enumerate(STAT)}
        res["procedures"][p]["added_pixels"] = int(sum(r["procedures"][p]["add_tp"] + r["procedures"][p]["add_fp"] for r in rows))
        res["procedures"][p]["added_on_reference"] = int(sum(r["procedures"][p]["add_tp"] for r in rows))
    for pa, pb in (("paths_on_seed", "threshold"), ("geo_on_seed", "threshold"), ("geo_free_on_seed", "threshold"), ("rgr", "threshold"), ("rgr_p", "threshold"), ("rgr_no_pgate", "threshold"),
                   ("rgr_p", "paths_on_seed"), ("rgr_p", "rgr"), ("rgr", "paths_on_seed"), ("rgr_no_pgate", "rgr"), ("paths_on_seed", "geo_on_seed"), ("paths_on_seed", "geo_free_on_seed"),
                   ("rgrm", "threshold"), ("rgrm_join", "threshold"), ("rgrm_paths", "threshold"), ("rgrm", "rgr"), ("rgrm_join", "rgrm"), ("rgrm_join", "geo_on_seed"), ("rgrm_join", "rgr_p"), ("rgrm_join", "rgrm_paths"), ("rgrm", "paths_on_seed")):
        if pa not in HAVE or pb not in HAVE: continue
        e = est[pa] - est[pb]; b = boot[pa] - boot[pb]; u = unit[pa] - unit[pb]; c = {}
        for j, k in enumerate(STAT):
            c[k] = dict(diff=float(e[j]), lo=float(np.quantile(b[:, j], 0.025)), hi=float(np.quantile(b[:, j], 0.975)),
                        units_positive=int((u[:, j] > 0).sum()), units_negative=int((u[:, j] < 0).sum()), units=C)
        res["contrasts"][f"{pa}-{pb}"] = c
    # margin over the global threshold at equal precision
    T = np.array([[[sum(rows[i]["sweep"][t][j] for i in g) for j in range(3)] + [sum(rows[i]["procedures"]["threshold"]["c_n"] for i in g)] for g in groups]
                  for t in range(len(GRID[ds]))], float)                         # thresholds x units x (tp, fp, c_tp, c_n)
    def curve(w):
        s = np.tensordot(T, w, axes=([1], [0]))
        pr = 100 * s[:, 0] / np.maximum(s[:, 0] + s[:, 1], 1); tc = 100 * s[:, 2] / np.maximum(s[:, 3], 1); o = np.argsort(pr)
        return pr[o], tc[o]
    for p in ("paths_on_seed", "geo_on_seed", "geo_free_on_seed", "rgr", "rgr_p", "rgr_no_pgate", "rgrm", "rgrm_join", "rgrm_paths"):
        if p not in HAVE: continue
        def one(w, v):
            pr, tc = curve(w); return v[1] - float(np.interp(v[0], pr, tc)), not (pr[0] <= v[0] <= pr[-1])
        e, outside = one(np.ones(C), est[p]); V = np.array([one(Wb[i], boot[p][i])[0] for i in range(nboot)]); per = [one(I[c], unit[p][c])[0] for c in range(C)]
        res["equal_precision"][p] = dict(diff=float(e), lo=float(np.quantile(V, 0.025)), hi=float(np.quantile(V, 0.975)), units_positive=int(sum(x > 0 for x in per)),
                                         units=C, outside_sweep=bool(outside), share_resamples_positive=float((V > 0).mean()))
    for p in BRIDGE_PROCS:
        if p in HAVE: res["bridges"][p] = {k: int(sum(r["bridges"][p][k] for r in rows)) for k in ("n", "correct_published_rule") + CLASSES}
    # ridge evidence: RGR against the same rule with the ridge gate off, or taken from the probability map, at the precision of RGR
    res["ridge"] = {}; res["rgrm_vs"] = {}; res["map_tv_curves"] = {}
    res["seconds"] = {k: float(np.mean([r["seconds"][k] for r in rows if k in r.get("seconds", {})])) for k in ("ridge_map_filter", "reconstruction", "joining") if any(k in r.get("seconds", {}) for r in rows)}
    seedU = np.array([[sum(rows[i]["procedures"]["threshold"][k] for i in g) for k in ("tp", "fp", "c_tp", "comp")] for g in groups], float)      # units x 4
    cnU = np.array([sum(rows[i]["procedures"]["threshold"]["c_n"] for i in g) for g in groups], float); nU = np.array([len(g) for g in groups], float)
    for var in ("none", "prob", "photo") + (tuple(f"tv{tv:.2f}" for tv in MAP_TV) if has_tv else ()):
        src = (lambda i, gi, j, var=var: rows[i]["map_tv_sweep"][var[2:]][gi][j]) if var.startswith("tv") else (lambda i, gi, j, var=var: rows[i]["ridge_sweep"][var][gi][j])
        V = np.array([[[sum(src(i, gi, j) for i in g) for j in range(4)] for g in groups] for gi in range(len(GATES))], float)   # gates x units x 4
        V = np.concatenate([seedU[None], V], 0)                                                                                                      # the seed is the point "gate 0.5"
        def one(w):
            s = np.tensordot(V, w, axes=([1], [0])); pr = 100 * s[:, 0] / np.maximum(s[:, 0] + s[:, 1], 1); tc = 100 * s[:, 2] / max(float(cnU @ w), 1); fr = s[:, 3] / max(float(nU @ w), 1)
            o = np.argsort(pr); a = stats((w[:, None] * A["rgr"]).sum(0))
            return a[1] - float(np.interp(a[0], pr[o], tc[o])), a[3] - float(np.interp(a[0], pr[o], fr[o])), not (pr[o][0] <= a[0] <= pr[o][-1])
        e = one(np.ones(C)); Vb = np.array([one(Wb[i])[:2] for i in range(nboot)]); per = np.array([one(I[c])[:2] for c in range(C)])
        # every gate of this variant against the global threshold at equal precision
        cur = []
        for gi, gate in enumerate(GATES):
            def og(w, gi=gi):
                sv = V[gi + 1].T @ w; prg = 100 * sv[0] / max(sv[0] + sv[1], 1); tcg = 100 * sv[2] / max(float(cnU @ w), 1)
                pr_t, tc_t = curve(w); return tcg - float(np.interp(prg, pr_t, tc_t)), prg, tcg, sv[3] / max(float(nU @ w), 1), not (pr_t[0] <= prg <= pr_t[-1])
            eg = og(np.ones(C)); bg = np.array([og(Wb[i])[0] for i in range(0, nboot, 5)]); pg = [og(I[c])[0] for c in range(C)]
            cur.append(dict(gate=gate, precision=float(eg[1]), thin_centre=float(eg[2]), fragments=float(eg[3]), margin=dict(diff=float(eg[0]), lo=float(np.quantile(bg, 0.025)), hi=float(np.quantile(bg, 0.975))),
                            units_positive=int(sum(x > 0 for x in pg)), outside_sweep=bool(eg[4])))
        if var.startswith("tv"): res["map_tv_curves"][var[2:]] = cur; continue
        res.setdefault("ridge_curves", {})[var] = cur
        if var in ("none", "photo") and "rgrm" in HAVE:      # RGR-M against the same rule with the ridge off, or with the photograph ridge, at the precision of RGR-M
            def onem(w):
                sm = np.tensordot(V, w, axes=([1], [0])); pr = 100 * sm[:, 0] / np.maximum(sm[:, 0] + sm[:, 1], 1); tc = 100 * sm[:, 2] / max(float(cnU @ w), 1); o = np.argsort(pr); am = stats((w[:, None] * A["rgrm"]).sum(0))
                return am[1] - float(np.interp(am[0], pr[o], tc[o])), not (pr[o][0] <= am[0] <= pr[o][-1])
            em = onem(np.ones(C)); bm = np.array([onem(Wb[i])[0] for i in range(0, nboot, 2)]); pm = [onem(I[c])[0] for c in range(C)]
            res["rgrm_vs"][var] = dict(diff=float(em[0]), lo=float(np.quantile(bm, 0.025)), hi=float(np.quantile(bm, 0.975)), units_positive=int(sum(x > 0 for x in pm)), units=C, outside_sweep=bool(em[1]))
        res["ridge"][var] = dict(diff=float(e[0]), lo=float(np.quantile(Vb[:, 0], 0.025)), hi=float(np.quantile(Vb[:, 0], 0.975)), units_positive=int((per[:, 0] > 0).sum()), units=C, outside_sweep=bool(e[2]),
                                 fragments=dict(diff=float(e[1]), lo=float(np.quantile(Vb[:, 1], 0.025)), hi=float(np.quantile(Vb[:, 1], 0.975))))
    return res


def ci(c, f="{:+.2f}"): return f"{f.format(c['diff'])} [{f.format(c['lo'])}, {f.format(c['hi'])}]"


# ================================================================== main
SUBSETS = []          # dicts: key, label, ds, root, cases, K, ktag, seeds
if not a.tables_only:
    roots = prepare_roots()
    d_drive_all = diam(roots["drive"], "train") + diam(roots["drive"], "test"); d_drive_train = diam(roots["drive"], "train")
    scale = []
    for ds in [x for x in ("drive", "chase", "stare", "fives") if x in roots and x in a.datasets]:
        root = roots[ds]
        if ds == "fives":
            paper, held = fives_split(root); test_cases = set(paper)
            assert len(paper) + len(held) == len(discover(root, "test"))
        else:
            paper = [p.case for p in discover(root, "test")]; held = []; test_cases = None
        d_tr = diam(root, "train"); d_te = diam(root, "test", test_cases)
        k_paper = 1.0 if ds == "drive" else float(np.median(d_tr + d_te) / np.median(d_drive_all))
        k_train = 1.0 if ds == "drive" else float(np.median(d_tr) / np.median(d_drive_train))
        differ = abs(k_paper - k_train) > 5e-5
        scale.append(dict(dataset=ds, train_masks=len(d_tr), test_masks=len(d_te), k_paper=k_paper, k_train=k_train,
                          px_paper=int(round(8 * k_paper)), px_train=int(round(8 * k_train)), differ=bool(differ)))
        log(f"{DS_NAME[ds]}: k = {k_paper:.4f} with training and test masks (paper), {k_train:.4f} with training masks alone; distance limit {int(round(8 * k_paper))} and {int(round(8 * k_train))} px")
        FULL = dict(need=list(PROCS), tv=True)
        SUBSETS.append(dict(key=ds, label=DS_NAME[ds] + (f", {len(paper)} test photographs of the paper" if ds == "fives" else ""), ds=ds, root=str(root), cases=paper, K=k_paper, ktag="paper",
                            seeds=[7] if ds == "fives" else a.seeds, **FULL))
        if ds == "drive":
            SUBSETS.append(dict(key="drive_val", label="DRIVE, four validation images", ds=ds, root=str(root), cases=sorted(DRIVE_VALID), K=1.0, ktag="paper", seeds=a.seeds, split="train", **FULL))
        if differ and ds != "fives":
            SUBSETS.append(dict(key=ds + "_ktrain", label=DS_NAME[ds] + ", scale factor from training masks alone", ds=ds, root=str(root), cases=paper, K=k_train, ktag="train", seeds=[7], **FULL))
        if ds == "fives":
            if differ: SUBSETS.append(dict(key="fives_ktrain", label=f"FIVES, {len(paper)} test photographs of the paper, scale factor from training masks alone", ds=ds, root=str(root), cases=paper, K=k_train, ktag="train", seeds=[7], need=list(OLD_PROCS), tv=False))
            if held: SUBSETS.append(dict(key="fives_heldout", label=f"FIVES, {len(held)} held-out test photographs", ds=ds, root=str(root), cases=held, K=k_train, ktag="train", seeds=[7], need=list(LIGHT_PROCS), tv=False))
            if not a.skip_export: export_fives(root, paper + held)
    json.dump(dict(scale=scale, subsets=SUBSETS), open(OUT / "protocol.json", "w"), indent=1)

    # ---- per-image analysis, resumable
    def map_path(ds, arch, seed, case):
        return (OUT / "probs_fives" / f"fives_{arch}_s{seed}_{case}.npz") if ds == "fives" else (a.drive_out / "probs" / f"{ds}_{arch}_s{seed}_{case}.npy")
    def row_path(sub, arch, seed, case): return OUT / "rows" / f"{sub['ds']}_k{sub['ktag']}" / f"{sub['ds']}_{arch}_s{seed}_{case}.json"
    def row_complete(f, sub):
        if not f.exists(): return False
        try:
            row = json.load(open(f)); return all(n in row["procedures"] for n in sub["need"]) and "ridge_sweep" in row and (not sub["tv"] or "map_tv_sweep" in row)
        except Exception: return False
    tasks = {}
    for sub in SUBSETS:
        for seed in sub["seeds"]:
            for arch in a.archs:
                missing = [c for c in sub["cases"] if not map_path(sub["ds"], arch, seed, c).exists()]
                if missing: log(f"skip {sub['label']} {NET_NAME[arch]} seed {seed}: {len(missing)} probability maps not found (first: {map_path(sub['ds'], arch, seed, missing[0])})"); continue
                for c in sub["cases"]:
                    if not row_complete(row_path(sub, arch, seed, c), sub):
                        tasks.setdefault((sub["ds"], sub["root"], c, sub["K"], sub.get("split", "test")), []).append((arch, seed, str(map_path(sub["ds"], arch, seed, c)), str(row_path(sub, arch, seed, c)), tuple(sub["need"]), bool(sub["tv"])))
    order = {"drive": 0, "chase": 1, "stare": 2, "fives": 3}
    kind_of = lambda t: (t[0], "all procedures" if t[4][0][5] else "short list")          # photographs of one kind take about the same time
    tasks = sorted(((ds, root, c, K, runs, split) for (ds, root, c, K, split), runs in tasks.items()), key=lambda t: (order[t[0]], not t[4][0][5], t[3], t[2]))
    n_runs = sum(len(t[4]) for t in tasks)
    if tasks:
        W = a.workers if a.workers > 0 else (os.cpu_count() or 1)
        log(f"per-image analysis: {len(tasks)} photographs, {n_runs} photograph-network results to compute, {W} worker processes")
        left = {}; spent = {}
        for t in tasks: left[kind_of(t)] = left.get(kind_of(t), 0) + 1
        for kd, nk in left.items(): log(f"  {nk} photographs: {DS_NAME[kd[0]]}, {kd[1]}")
        done = 0; t1 = time.time()
        if W == 1:
            it = ((t, image_task(t)) for t in tasks)
        else:
            ex = ProcessPoolExecutor(max_workers=W, mp_context=mp.get_context("fork")); futs = {ex.submit(image_task, t): t for t in tasks}; it = ((futs[f], f.result()) for f in as_completed(futs))
        for i, (t, (case, n, sec)) in enumerate(it, 1):
            done += n; kd = kind_of(t); left[kd] -= 1; spent.setdefault(kd, []).append(sec)
            # minutes left: for every kind of photograph, the mean time of those already finished (or of all finished ones while none of that kind is)
            every = np.mean([x for v in spent.values() for x in v]); busy = (time.time() - t1) * W / max(sum(sum(v) for v in spent.values()), 1e-9)
            eta = sum(nk * (np.mean(spent[k_]) if k_ in spent else every) for k_, nk in left.items()) * max(busy, 1.0) / W / 60
            if t[0] == "fives" or i % max(1, len(tasks) // 40) == 0 or i == len(tasks):
                log(f"  {i}/{len(tasks)} photographs ({case}, {sec:.0f} s), {done}/{n_runs} results; about {eta:.0f} min left")
    else:
        log("per-image analysis: nothing left to compute")
else:
    P = json.load(open(OUT / "protocol.json")); scale = P["scale"]; SUBSETS = P["subsets"]
    def row_path(sub, arch, seed, case): return OUT / "rows" / f"{sub['ds']}_k{sub['ktag']}" / f"{sub['ds']}_{arch}_s{seed}_{case}.json"

# ------------------------------------------------------------------ aggregation and tables
log("statistics and tables")
RES = []
for sub in SUBSETS:
    ds = sub["ds"]; cases = sub["cases"]
    unit_of = (lambda c: c[:-1] if c[-1] in "LR" else c) if ds == "chase" else (lambda c: c)
    names = sorted(set(unit_of(c) for c in cases)); groups = [[i for i, c in enumerate(cases) if unit_of(c) == n] for n in names]
    for seed in sub["seeds"]:
        for arch in a.archs:
            fs = [row_path(sub, arch, seed, c) for c in cases]
            if not all(f.exists() for f in fs): continue
            rows = [json.load(open(f)) for f in fs]
            need = sub.get("need", PROCS); tv = sub.get("tv", True)
            if not all(n in row["procedures"] for row in rows for n in need) or not all("ridge_sweep" in row and (not tv or "map_tv_sweep" in row) for row in rows): log(f"skip {sub['label']} {NET_NAME[arch]} seed {seed}: results of an older version, run again without --tables-only"); continue
            r = summarise(rows, groups, ds, a.boot); r.update(subset=sub["key"], label=sub["label"], dataset=ds, arch=arch, seed=seed, k=sub["K"], k_source=sub["ktag"],
                                                               unit="child (both eyes)" if ds == "chase" else "photograph")
            if ds == "fives":
                r["by_diagnosis"] = {}
                for cat in "ADGN":
                    idx = [i for i, c in enumerate(cases) if c.endswith(cat)]
                    if idx: r["by_diagnosis"][cat] = summarise([rows[i] for i in idx], [[j] for j in range(len(idx))], ds, min(a.boot, 2000))
            RES.append(r)
            g = r["contrasts"]; e = r["equal_precision"]
            log(f"{sub['label']} | {NET_NAME[arch]} s{seed}: TCR gain paths {ci(g['paths_on_seed-threshold']['thin_centre'])}, RGR {ci(g['rgr-threshold']['thin_centre'])}, RGR-P {ci(g['rgr_p-threshold']['thin_centre'])}; "
                f"margin at equal precision paths {ci(e['paths_on_seed'])}, RGR {ci(e['rgr'])}, RGR-P {ci(e['rgr_p'])}")
            if "rgrm_join" in r["procedures"]: log(f"   RGR-M: TCR gain {ci(g['rgrm-threshold']['thin_centre'])}, precision {ci(g['rgrm-threshold']['precision'])}, margin at equal precision {ci(e['rgrm'])} ({e['rgrm']['units_positive']}/{r['units']} units); with joining: margin {ci(e['rgrm_join'])}, "
                f"bridges {r['bridges']['rgrm_join']['n']} ({100 * r['bridges']['rgrm_join']['correct_published_rule'] / max(r['bridges']['rgrm_join']['n'], 1):.1f}% correct)")
            log(f"   ridge evidence, TCR of RGR minus the variant at equal precision: ridge off {ci(r['ridge']['none'])} ({r['ridge']['none']['units_positive']}/{r['units']} units), "
                f"ridge from the probability map {ci(r['ridge']['prob'])} ({r['ridge']['prob']['units_positive']}/{r['units']} units)")
            if False and sub["key"] == "fives" and arch in FIVES_REF and len(cases) == 40:
                ref = FIVES_REF[arch]
                log(f"   check against the earlier run: RGR gain {g['rgr-threshold']['thin_centre']['diff']:+.2f} (earlier {ref[0]:+.2f}), RGR-P gain {g['rgr_p-threshold']['thin_centre']['diff']:+.2f} (earlier {ref[1]:+.2f}), "
                    f"bridges {r['bridges']['rgr']['n']} and {r['bridges']['rgr_p']['n']} (earlier {ref[2]} and {ref[3]})")
json.dump(dict(scale=scale, results=RES), open(OUT / "all_results.json", "w"), default=float)

DSN = lambda r: r["label"]
with open(OUT / "T1_scale_factor.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["Dataset", "Training masks", "Test masks", "k, training and test masks (paper)", "k, training masks alone", "Distance limit and path window (px), paper", "Same, training masks alone", "Factors differ beyond 0.00005"])
    for s in scale: w.writerow([DS_NAME[s["dataset"]], s["train_masks"], s["test_masks"], f"{s['k_paper']:.4f}", f"{s['k_train']:.4f}", s["px_paper"], s["px_train"], "yes" if s["differ"] else "no"])
with open(OUT / "T2_procedures.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["Data", "k", "Seed", "Network", "Procedure", "Precision (%)", "Recall (%)", "TCR (%)", "Dice (%)", "clDice (%)", "Fragments per image", "Added pixels",
                                    "TCR change against the 0.5 threshold (pp) [95% CI]", "Precision change (pp) [95% CI]", "Dice change (pp) [95% CI]", "Fragment change [95% CI]",
                                    "Margin over the global threshold at equal precision, TCR (pp) [95% CI]", "Units with positive margin", "Precision outside the sweep"])
    for r in RES:
        for p in PROCS:
            if p not in r["procedures"]: continue
            x = r["procedures"][p]; c = r["contrasts"].get(f"{p}-threshold"); e = r["equal_precision"].get(p)
            w.writerow([DSN(r), f"{r['k']:.4f}", r["seed"], NET_NAME[r["arch"]], PROC_NAME[p], f"{x['precision']:.2f}", f"{x['recall']:.2f}", f"{x['thin_centre']:.2f}", f"{x['dice']:.2f}", f"{x['cldice']:.2f}",
                        f"{x['fragments']:.1f}", x["added_pixels"]] + ([ci(c["thin_centre"]), ci(c["precision"]), ci(c["dice"]), ci(c["fragments"], "{:+.1f}")] if c else ["-"] * 4)
                       + ([ci(e), f"{e['units_positive']}/{e['units']}", "yes" if e["outside_sweep"] else "no"] if e else ["-"] * 3))
LAB = {"rgr_p-paths_on_seed": "RGR-P minus paths on the 0.5 mask", "rgr_p-rgr": "RGR-P minus RGR", "rgr-paths_on_seed": "RGR minus paths on the 0.5 mask", "rgr_no_pgate-rgr": "RGR without the probability gate minus RGR",
       "paths_on_seed-geo_on_seed": "Paths on the 0.5 mask minus geometric joining with the direction rule", "paths_on_seed-geo_free_on_seed": "Paths on the 0.5 mask minus geometric joining without a direction rule",
       "rgrm-rgr": "RGR-M minus RGR (photograph ridge)", "rgrm_join-rgrm": "RGR-M with joining minus RGR-M", "rgrm_join-geo_on_seed": "RGR-M with joining minus joining on the 0.5 mask", "rgrm_join-rgr_p": "RGR-M with joining minus RGR-P",
       "rgrm_join-rgrm_paths": "RGR-M with straight joining minus RGR-M with minimal-cost paths", "rgrm-paths_on_seed": "RGR-M minus paths on the 0.5 mask"}
with open(OUT / "T3_contrasts.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["Data", "Seed", "Network", "Difference", "Unit", "Units", "TCR (pp) [95% CI]", "Precision (pp) [95% CI]", "Dice (pp) [95% CI]", "Fragments per image [95% CI]", "Units with higher TCR", "Units with fewer fragments"])
    for r in RES:
        for key, name in LAB.items():
            if key not in r["contrasts"]: continue
            c = r["contrasts"][key]
            w.writerow([DSN(r), r["seed"], NET_NAME[r["arch"]], name, r["unit"], r["units"], ci(c["thin_centre"]), ci(c["precision"]), ci(c["dice"]), ci(c["fragments"], "{:+.1f}"),
                        f"{c['thin_centre']['units_positive']}/{r['units']}", f"{c['fragments']['units_negative']}/{r['units']}"])
def bridge_row(head, b):
    n = max(b["n"], 1); pc = lambda k: f"{b[k]} ({100 * b[k] / n:.1f})"
    return head + [b["n"], pc("correct_published_rule"), pc("correct"), b["mixed"], pc("shortcut"), b["offset"], pc("unannotated")]
BH = ["Bridges", "Correct, rule of the paper (%)", "Correct, stricter rule (%)", "Mixed", "Shortcut (%)", "Offset", "Unannotated (%)"]
with open(OUT / "T4_bridges.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["Data", "Seed", "Network", "Procedure"] + BH)
    pooled = {}
    for r in RES:
        for p in BRIDGE_PROCS:
            if p not in r["bridges"]: continue
            w.writerow(bridge_row([DSN(r), r["seed"], NET_NAME[r["arch"]], PROC_NAME[p]], r["bridges"][p]))
            q = pooled.setdefault((DSN(r), r["seed"], p), {})
            for k, v in r["bridges"][p].items(): q[k] = q.get(k, 0) + v
    for (lab, seed, p), b in pooled.items(): w.writerow(bridge_row([lab, seed, "three networks pooled", PROC_NAME[p]], b))
CAT = {"A": "Age-related macular degeneration", "D": "Diabetic retinopathy", "G": "Glaucoma", "N": "Normal"}
with open(OUT / "T5_fives_by_diagnosis.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["Data", "Diagnosis", "Photographs", "Network", "Procedure", "Precision (%)", "TCR (%)", "Dice (%)", "Fragments per image", "TCR change against the 0.5 threshold (pp) [95% CI]",
                                    "Precision change (pp) [95% CI]", "Dice change (pp) [95% CI]"] + BH)
    for r in RES:
        for cat, s in r.get("by_diagnosis", {}).items():
            for p in ("threshold", "paths_on_seed", "geo_on_seed", "rgr", "rgr_p", "rgrm", "rgrm_join"):
                if p not in s["procedures"]: continue
                x = s["procedures"][p]; c = s["contrasts"].get(f"{p}-threshold"); b = s["bridges"].get(p)
                w.writerow(bridge_row([DSN(r), CAT[cat], s["images"], NET_NAME[r["arch"]], PROC_NAME[p], f"{x['precision']:.2f}", f"{x['thin_centre']:.2f}", f"{x['dice']:.2f}", f"{x['fragments']:.1f}"]
                                      + ([ci(c["thin_centre"]), ci(c["precision"]), ci(c["dice"])] if c else ["-"] * 3), b) if b else
                           [DSN(r), CAT[cat], s["images"], NET_NAME[r["arch"]], PROC_NAME[p], f"{x['precision']:.2f}", f"{x['thin_centre']:.2f}", f"{x['dice']:.2f}", f"{x['fragments']:.1f}"] + ["-"] * 10)
with open(OUT / "T6_effect_of_scale_factor.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["Dataset", "Network", "Procedure", "k (paper)", "k (training masks alone)", "Precision: paper, training-only (%)", "TCR: paper, training-only (%)", "Dice: paper, training-only (%)",
                                    "Fragments: paper, training-only", "Largest absolute change (pp)"])
    by = {(r["subset"], r["arch"], r["seed"]): r for r in RES}
    for (sub, arch, seed), r2 in by.items():
        if not sub.endswith("_ktrain"): continue
        r1 = by.get((sub[:-7], arch, seed))
        if r1 is None: continue
        for p in PROCS:
            if p not in r1["procedures"] or p not in r2["procedures"]: continue
            x, z = r1["procedures"][p], r2["procedures"][p]
            w.writerow([DS_NAME[r1["dataset"]], NET_NAME[arch], PROC_NAME[p], f"{r1['k']:.4f}", f"{r2['k']:.4f}"] + [f"{x[k]:.2f}, {z[k]:.2f}" for k in ("precision", "thin_centre", "dice")]
                       + [f"{x['fragments']:.1f}, {z['fragments']:.1f}", f"{max(abs(x[k] - z[k]) for k in ('precision', 'thin_centre', 'dice', 'recall')):.3f}"])
with open(OUT / "T7_ridge_evidence.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["Data", "k", "Seed", "Network", "Unit", "Units", "RGR minus ridge-off RGR at equal precision, TCR (pp) [95% CI]", "Units positive", "Fragments per image [95% CI]", "Precision outside the sweep",
                                    "RGR minus RGR with the ridge from the probability map, TCR (pp) [95% CI]", "Units positive", "Fragments per image [95% CI]", "Precision outside the sweep", "Check: RGR minus its own curve (0 expected)"])
    for r in RES:
        a_, b_, c_ = r["ridge"]["none"], r["ridge"]["prob"], r["ridge"]["photo"]
        w.writerow([DSN(r), f"{r['k']:.4f}", r["seed"], NET_NAME[r["arch"]], r["unit"], r["units"], ci(a_), f"{a_['units_positive']}/{a_['units']}", ci(a_["fragments"], "{:+.1f}"), "yes" if a_["outside_sweep"] else "no",
                    ci(b_), f"{b_['units_positive']}/{b_['units']}", ci(b_["fragments"], "{:+.1f}"), "yes" if b_["outside_sweep"] else "no", f"{c_['diff']:+.3f}"])
with open(OUT / "T8_ridge_source_by_gate.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["Data", "Seed", "Network", "Ridge gate", "Probability gate", "Precision (%)", "TCR (%)", "Fragments per image", "Precision change against the 0.5 threshold (pp)", "TCR change (pp)",
                                    "Margin over the global threshold at equal precision, TCR (pp) [95% CI]", "Units with positive margin", "Precision outside the sweep"])
    for r in RES:
        t = r["procedures"]["threshold"]
        for var, nm in RIDGE_VARIANTS.items():
            for c in r["ridge_curves"][var]:
                w.writerow([DSN(r), r["seed"], NET_NAME[r["arch"]], nm, f"{c['gate']:.2f}", f"{c['precision']:.2f}", f"{c['thin_centre']:.2f}", f"{c['fragments']:.1f}", f"{c['precision'] - t['precision']:+.2f}", f"{c['thin_centre'] - t['thin_centre']:+.2f}",
                            ci(c["margin"]), f"{c['units_positive']}/{r['units']}", "yes" if c["outside_sweep"] else "no"])
with open(OUT / "T9_map_ridge_sensitivity.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["Data", "Seed", "Network", "Ridge gate (map ridge)", "Probability gate", "Precision (%)", "TCR (%)", "Fragments per image", "Precision change against the 0.5 threshold (pp)", "TCR change (pp)",
                                    "Margin over the global threshold at equal precision, TCR (pp) [95% CI]", "Units with positive margin", "Precision outside the sweep"])
    for r in RES:
        t = r["procedures"]["threshold"]; curves = dict(r["map_tv_curves"]); curves["0.05"] = r["ridge_curves"]["prob"]
        for tv in sorted(curves, key=float):
            for c in curves[tv]:
                w.writerow([DSN(r), r["seed"], NET_NAME[r["arch"]], tv, f"{c['gate']:.2f}", f"{c['precision']:.2f}", f"{c['thin_centre']:.2f}", f"{c['fragments']:.1f}", f"{c['precision'] - t['precision']:+.2f}", f"{c['thin_centre'] - t['thin_centre']:+.2f}",
                            ci(c["margin"]), f"{c['units_positive']}/{r['units']}", "yes" if c["outside_sweep"] else "no"])
with open(OUT / "T10_rgrm_ridge_source_and_time.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["Data", "Seed", "Network", "RGR-M minus ridge-off rule at equal precision, TCR (pp) [95% CI]", "Units positive", "Outside the sweep", "RGR-M minus photograph-ridge rule at equal precision, TCR (pp) [95% CI]", "Units positive", "Outside the sweep",
                                    "Ridge filter on the map (s per image)", "Reconstruction (s per image)", "Joining (s per image)"])
    for r in RES:
        if not r["rgrm_vs"]: continue
        a_, b_ = r["rgrm_vs"]["none"], r["rgrm_vs"]["photo"]; sec = r.get("seconds", {})
        w.writerow([DSN(r), r["seed"], NET_NAME[r["arch"]], ci(a_), f"{a_['units_positive']}/{a_['units']}", "yes" if a_["outside_sweep"] else "no", ci(b_), f"{b_['units_positive']}/{b_['units']}", "yes" if b_["outside_sweep"] else "no"]
                   + [f"{sec[k]:.3f}" if k in sec else "-" for k in ("ridge_map_filter", "reconstruction", "joining")])
zp = OUT / "RGR_final_protocol_results_v1_5.zip"
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(OUT.glob("T*.csv")) + [OUT / "all_results.json", OUT / "protocol.json"]:
        if f.exists(): z.write(f, f"RGR_final_protocol_results_v1_5/{f.name}")
log(f"{len(RES)} runs summarised. Tables and all_results.json are in {OUT}")
log(f"Send back this one file: {zp}")
for s in scale: print(f"  scale factor {DS_NAME[s['dataset']]}: paper {s['k_paper']:.4f}, training masks alone {s['k_train']:.4f}")
