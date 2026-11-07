import gzip, re
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from skimage.morphology import skeletonize

from .recovery import ridge_map, fov_diameter

STARE_TEST = ("0162", "0163", "0235", "0236", "0239", "0240", "0255", "0291", "0319", "0324")
STARE_TRAIN = ("0001", "0002", "0003", "0004", "0005", "0044", "0077", "0081", "0082", "0139")
DRIVE_VALID = {"22", "27", "34", "39"}
EXTS = ("tif", "png", "jpg", "ppm")


class Pair:
    def __init__(self, case, image, mask, fov, mask2=None):
        self.case, self.image, self.mask, self.fov, self.mask2 = case, image, mask, fov, mask2


def discover(root, split):
    folder = Path(root) / ("DRIVE" if split == "train" else "DRIVET")
    out = []
    for ext in EXTS:
        for im in sorted((folder / "HR").glob(f"*.{ext}")):
            case = im.name.split("_")[0]
            m2 = folder / "VE2" / f"{case}_manual2.gif"
            out.append(Pair(case, im, folder / "VE" / f"{case}_manual1.gif", folder / "mask" / f"{case}_mask.gif",
                            m2 if m2.exists() else None))
    if not out: raise ValueError(f"no {split} images under {folder}")
    return sorted(out, key=lambda p: p.case)


def read_rgb(path):
    return np.asarray(Image.open(path).convert("RGB"), dtype=np.uint8)


def read_bin(path):
    return np.asarray(Image.open(path).convert("L")) > 127


def red_fov(rgb):
    fov = ndi.binary_fill_holes(ndi.binary_opening(rgb[..., 0] > 20, iterations=3))
    lab, _ = ndi.label(fov); fov = lab == (np.argmax(np.bincount(lab.ravel())[1:]) + 1)
    return ndi.binary_erosion(fov, iterations=2)


def _save(out, split, case, rgb, gt, fov, gt2=None, ext="tif"):
    d = Path(out) / ("DRIVE" if split == "train" else "DRIVET")
    for sub in ("HR", "VE", "mask") + (("VE2",) if gt2 is not None else ()): (d / sub).mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgb).save(d / "HR" / f"{case}_training.{ext}")
    Image.fromarray(gt.astype(np.uint8) * 255).save(d / "VE" / f"{case}_manual1.gif")
    Image.fromarray(fov.astype(np.uint8) * 255).save(d / "mask" / f"{case}_mask.gif")
    if gt2 is not None: Image.fromarray(gt2.astype(np.uint8) * 255).save(d / "VE2" / f"{case}_manual2.gif")


def _open_maybe_gz(path):
    path = Path(path)
    if path.suffix == ".gz":
        with gzip.open(path, "rb") as f: return Image.open(f).copy()
    return Image.open(path)


def _find(folder, pattern):
    hits = [p for p in Path(folder).rglob("*") if re.search(pattern, p.name, re.I)]
    return hits[0] if hits else None


def load_pair(pair):
    image = np.asarray(Image.open(pair.image).convert("RGB"), dtype=np.uint8)
    target = (np.asarray(Image.open(pair.mask).convert("L")) > 0).astype(np.float32)
    fov = (np.asarray(Image.open(pair.fov).convert("L")) > 0).astype(np.float32)
    return image, target, fov


def features(image):
    green = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(image[..., 1])
    x = np.concatenate([image, green[..., None]], axis=2).astype(np.float32) / 255.0
    return x * 2.0 - 1.0


def prepare_chase(sgl_dataset: Path, out: Path):
    out = Path(out)
    if (out / "DRIVET" / "HR").exists() and len(list((out / "DRIVET" / "HR").glob("*.tif"))) == 8:
        return out
    for s, d in (("CHASE", "DRIVE"), ("CHASET", "DRIVET")):
        for sub in ("HR", "VE", "mask"): (out / d / sub).mkdir(parents=True, exist_ok=True)
        for f in sorted((Path(sgl_dataset) / s / "HR").glob("*.jpg")):
            case = f.stem.split("_")[1]
            im = Image.open(f).convert("RGB"); a = np.asarray(im)
            fov = ndi.binary_fill_holes(ndi.binary_opening(a[..., 0] > 20, iterations=3))
            lab, _ = ndi.label(fov); fov = lab == (np.argmax(np.bincount(lab.ravel())[1:]) + 1)
            fov = ndi.binary_erosion(fov, iterations=2)
            im.save(out / d / "HR" / f"{case}_training.tif")
            gt = np.asarray(Image.open(Path(sgl_dataset) / s / "VE" / f"Image_{case}_1stHO.png").convert("L")) > 127
            Image.fromarray(gt.astype(np.uint8) * 255).save(out / d / "VE" / f"{case}_manual1.gif")
            Image.fromarray(fov.astype(np.uint8) * 255).save(out / d / "mask" / f"{case}_mask.gif")
    return out


def prepare_stare(raw, out):
    out = Path(out)
    if (out / "DRIVET" / "HR").exists() and len(list((out / "DRIVET" / "HR").glob("*"))) == 10: return out
    for split, ids in (("train", STARE_TRAIN), ("test", STARE_TEST)):
        for i in ids:
            im = _find(raw, rf"^im{i}\.ppm(\.gz)?$"); ah = _find(raw, rf"^im{i}\.ah\.p[pg]m(\.gz)?$")
            vk = _find(raw, rf"^im{i}\.vk\.p[pg]m(\.gz)?$")
            if im is None or ah is None: raise FileNotFoundError(f"STARE im{i} or its ah label not found under {raw}")
            rgb = np.asarray(_open_maybe_gz(im).convert("RGB"), dtype=np.uint8)
            gt = np.asarray(_open_maybe_gz(ah).convert("L")) > 127
            gt2 = np.asarray(_open_maybe_gz(vk).convert("L")) > 127 if vk is not None else None
            _save(out, split, i, rgb, gt, red_fov(rgb), gt2)
    return out


def stare_pathology(codes_file):
    flags = {}
    for line in Path(codes_file).read_text(errors="ignore").splitlines():
        m = re.match(r"\s*im(\d{4})\s+(.*)", line)
        if m: flags[m.group(1)] = "normal" not in m.group(2).lower()
    return flags


def add_second_observer(root, split, files):
    d = Path(root) / ("DRIVE" if split == "train" else "DRIVET") / "VE2"; d.mkdir(parents=True, exist_ok=True)
    for case, path in files.items():
        Image.fromarray(read_bin(path).astype(np.uint8) * 255).save(d / f"{case}_manual2.gif")


def prepare_fives(raw, out, train_per_category=None, test_per_category=None):
    out = Path(out)
    n_test = 200 if test_per_category is None else 4 * test_per_category
    if (out / "DRIVET" / "HR").exists() and len(list((out / "DRIVET" / "HR").glob("*"))) == n_test: return out
    for split, per_cat in (("train", train_per_category), ("test", test_per_category)):
        base = next(p for p in Path(raw).rglob("*") if p.is_dir() and p.name.lower() == split)
        ims = sorted(p for p in base.rglob("*.png") if "original" in str(p.parent).lower())
        if per_cat is not None:
            by = {}
            for im in ims:
                m = re.match(r"(\d+)_([ADGN])", im.stem)
                if m: by.setdefault(m.group(2), []).append((int(m.group(1)), im))
            ims = [im for cat in sorted(by) for _, im in sorted(by[cat])[:per_cat]]
        for im in ims:
            gtp = next((q for q in base.rglob(im.name) if q != im and "original" not in str(q.parent).lower()), None)
            if gtp is None: raise FileNotFoundError(f"FIVES label for {im.name} not found")
            n, cat = re.match(r"(\d+)_([ADGN])", im.stem).groups()
            rgb = read_rgb(im)
            _save(out, split, f"{int(n):04d}{cat}", rgb, read_bin(gtp), red_fov(rgb), ext="png")
    return out


def load_case(p):
    rgb = read_rgb(p.image); f = read_bin(p.fov); y = read_bin(p.mask) & f
    y2 = (read_bin(p.mask2) & f) if p.mask2 is not None else None
    return rgb, y, f, y2


def median_fov_diameter(root):
    return float(np.median([fov_diameter(read_bin(p.fov)) for s in ("train", "test") for p in discover(root, s)]))


def load_eval(root, split, cases=None, k=1.0, pathology=None, with_rf=True):
    out = []
    for p in discover(root, split):
        if cases and p.case not in cases: continue
        im, y, f, y2 = load_case(p)
        sk = skeletonize(y); rad = ndi.distance_transform_edt(y)
        _, idx = ndi.distance_transform_edt(~sk, return_indices=True)
        lr = rad[tuple(idx)]; lr[~y] = 0
        d = dict(case=p.case, img=im, f=f, y=y, y2=y2, k=k, sk=sk, lr=(lr / k).astype(np.float32), centre=sk & (rad <= 2 * k) & f,
                 thin=y & (lr <= 2 * k), dy=(ndi.distance_transform_edt(~y) / k).astype(np.float32),
                 pathology=bool(pathology.get(p.case, False)) if pathology else (p.case[-1] in "ADG" if re.match(r"\d{4}[ADGN]$", p.case) else False))
        if with_rf:
            d["rf"] = ridge_map(im, f)
            d["rfk"] = ridge_map(im, f, k) if k != 1.0 else d["rf"]
        out.append(d)
    return out
