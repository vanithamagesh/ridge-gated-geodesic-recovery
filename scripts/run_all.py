import argparse, json, os, re, shutil, subprocess, sys, time, zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent; ROOT = HERE.parent; sys.path.insert(0, str(ROOT))
ap = argparse.ArgumentParser()
ap.add_argument("--out", type=Path, required=True, help="output folder for data, models, probability maps and results")
ap.add_argument("--work", type=Path, default=Path("work"), help="folder for cloned dataset repositories and archives")
ap.add_argument("--seeds", type=int, nargs="+", default=[7, 11, 23])
ap.add_argument("--skip-fives", action="store_true"); ap.add_argument("--skip-train", action="store_true")
ap.add_argument("--fives-zip", type=Path, help="FIVES archive already downloaded (otherwise downloaded from figshare)")
ap.add_argument("--datasets", nargs="+", default=["drive", "chase", "stare", "fives"], help="datasets to process")
ap.add_argument("--crf-grid", choices=["full", "small"], default="full")
ap.add_argument("--fives-per-category", type=int, default=10, help="FIVES test images per category (A, D, G, N); 50 = the full official test set")
ap.add_argument("--fives-train-per-category", type=int, default=25, help="FIVES training images per category used to train the three networks")
ap.add_argument("--jobs", type=int, default=0, help="parallel worker processes, one (dataset, seed, network) task each; 0 = min(4, CPU cores)")
ap.add_argument("--archs", nargs="+", default=["unet", "attunet", "unetpp"])
ap.add_argument("--analyse", nargs="+", help="datasets to analyse (default: all of --datasets)")
a = ap.parse_args(); a.out.mkdir(parents=True, exist_ok=True); a.work.mkdir(parents=True, exist_ok=True)
t0 = time.time(); log = lambda *x: print(f"[{(time.time() - t0) / 60:6.1f} min]", *x, flush=True)
PY = sys.executable
DATA = a.out / "data"; DATA.mkdir(exist_ok=True)


def sh(cmd, check=True, **kw):
    log("$", cmd); return subprocess.run(cmd, shell=True, check=check, **kw)


JOBS = a.jobs if a.jobs > 0 else max(1, min(4, os.cpu_count() or 1))
LOGS = a.out / "logs"; LOGS.mkdir(exist_ok=True)


def run_pool(jobs, n):
    if n <= 1 or len(jobs) <= 1:
        for name, cmd in jobs: sh(cmd)
        return
    log(f"{len(jobs)} jobs, {n} in parallel: " + ", ".join(name for name, _ in jobs))
    pending = list(jobs); running = {}; failed = []; done = 0; last_report = time.time()
    while pending or running:
        while pending and len(running) < n:
            name, cmd = pending.pop(0); f = open(LOGS / f"{name}.txt", "a")
            running[name] = (subprocess.Popen(cmd, shell=True, stdout=f, stderr=subprocess.STDOUT), f, time.time())
            log(f"started {name}")
        for name in list(running):
            proc, f, t1 = running[name]
            if proc.poll() is None: continue
            f.close(); del running[name]; done += 1
            tail = (LOGS / f"{name}.txt").read_text().strip().splitlines()[-2:]
            log(f"finished {name} in {(time.time() - t1) / 60:.1f} min, exit {proc.returncode} ({done}/{len(jobs)} done): " + " | ".join(t[-120:] for t in tail))
            if proc.returncode != 0: failed.append(name)
        if running and time.time() - last_report > 300:
            last_report = time.time()
            for name, (proc, f, t1) in running.items():
                lines = (LOGS / f"{name}.txt").read_text().strip().splitlines()
                log(f"  {name} ({(time.time() - t1) / 60:.0f} min): {lines[-1][-110:] if lines else 'starting'}")
        time.sleep(10)
    if failed: raise SystemExit(f"failed jobs: {failed} (see {LOGS})")


def clone(url, dst):
    if not Path(dst).exists(): sh(f"git clone -q --depth 1 {url} {dst}")
    return Path(dst)


from rgr.data import prepare_chase, prepare_stare, prepare_fives, add_second_observer, discover, STARE_TEST

sgl = clone("https://github.com/SHI-Labs/SGL-Retinal-Vessel-Segmentation", a.work / "sgl")
ddn = clone("https://github.com/sraashis/deepdyn", a.work / "deepdyn")
roots = {}
DRIVE_ROOT = sgl / "dataset"; roots["drive"] = DRIVE_ROOT
roots["chase"] = prepare_chase(sgl / "dataset", DATA / "chase")
if not any((DATA / "chase" / "DRIVET" / "VE2").glob("*")):
    add_second_observer(DATA / "chase", "test", {p.case: ddn / "data" / "CHASEDB" / "manual" / f"Image_{p.case}_2ndHO.png"
                                                  for p in discover(DATA / "chase", "test")})
roots["stare"] = prepare_stare(ddn / "data" / "STARE", DATA / "stare")
log("DRIVE, CHASE_DB1 (with observer 2) and STARE (with observer 2) ready")

ve2 = DATA / "drive_obs2"
if not ve2.exists():
    try:
        import kagglehub
        p = Path(kagglehub.dataset_download("andrewmvd/drive-digital-retinal-images-for-vessel-extraction"))
        files = {m.group(1): f for f in p.rglob("*manual2*") for m in [re.match(r"(\d\d)_manual2", f.name)] if m}
        if len(files) < 20: raise FileNotFoundError(f"only {len(files)} manual2 files found under {p}")
        ve2.mkdir(); [shutil.copy(f, ve2 / f.name) for f in files.values()]
        log(f"DRIVE second observer: {len(files)} files")
    except Exception as exc:
        log(f"DRIVE second observer not available ({exc}); the observer-2 analysis is done on CHASE_DB1 and STARE only")
if ve2.exists():
    d2 = sgl / "dataset" / "DRIVET" / "VE2"
    if not d2.exists(): add_second_observer(sgl / "dataset", "test", {f.name[:2]: f for f in ve2.glob("*manual2*")})

codes = DATA / "all-mg-codes.txt"
if not codes.exists():
    try: sh(f"curl -sSf --max-time 60 -o {codes} https://cecas.clemson.edu/~ahoover/stare/diagnoses/all-mg-codes.txt")
    except Exception:
        normal = {"0077", "0081", "0082", "0162", "0163", "0235", "0236", "0239", "0240", "0255"}
        codes.write_text("".join(f"im{i} {'Normal' if i in normal else 'Pathology (fallback list)'}\n" for i in sorted(normal | set(STARE_TEST) | {"0001", "0002", "0003", "0004", "0005", "0044", "0139", "0291", "0319", "0324"})))
        log("STARE diagnosis file not reachable; using the standard normal/pathological partition")

FIVES_LOCAL = a.work / "fives"; FIVES_DATA = FIVES_LOCAL / "data"; FIVES_OUT = FIVES_LOCAL / "out"
if not a.skip_fives and "fives" in a.datasets:
    fz = a.fives_zip or next((q for q in (a.out / "fives.rar", a.out / "fives.zip") if q.exists()), a.out / "fives.rar")
    is_rar = lambda q: q.exists() and open(q, "rb").read(4) == b"Rar!"
    is_archive = lambda q: q.exists() and (zipfile.is_zipfile(q) or is_rar(q))
    n_test = 4 * a.fives_per_category

    def fetch_fives(fz):
        if is_archive(fz): return fz
        fz.unlink(missing_ok=True)
        try:
            import urllib.request
            with urllib.request.urlopen("https://api.figshare.com/v2/articles/19688169/files", timeout=60) as r: files = json.load(r)
            f0 = max(files, key=lambda f: f["size"]); fz = fz.with_suffix(Path(f0["name"]).suffix or ".rar")
            log(f"FIVES: downloading {f0['name']} ({f0['size'] / 1e9:.2f} GB) from figshare")
            sh(f"curl -L --fail --retry 3 -C - -o {fz} '{f0['download_url']}'", check=False)
        except Exception as exc:
            log(f"FIVES download failed ({exc})")
        if is_archive(fz): return fz
        fz.unlink(missing_ok=True); return None

    def extract_fives(fz, raw):
        log(f"FIVES: extracting {fz.name} ({fz.stat().st_size / 1e9:.2f} GB)")
        shutil.rmtree(raw, ignore_errors=True); raw.mkdir(parents=True)
        if is_rar(fz):
            if sh("command -v unrar > /dev/null && command -v 7z > /dev/null", check=False).returncode != 0:
                sh("(apt-get -qq update && apt-get -qq install -y unrar p7zip-full p7zip-rar) > /dev/null 2>&1", check=False)
            sh(f"unrar x -idq -o+ '{fz}' '{raw}/' || 7z x -y -o'{raw}' '{fz}' > /dev/null")
        else:
            zipfile.ZipFile(fz).extractall(raw)
        for inner in list(raw.rglob("*.zip")): zipfile.ZipFile(inner).extractall(inner.parent); inner.unlink()
        (raw / ".extracted").write_text("ok\n")

    if not ((FIVES_DATA / "DRIVET" / "HR").exists() and len(list((FIVES_DATA / "DRIVET" / "HR").glob("*"))) == n_test):
        fa = fetch_fives(fz)
        if fa is None:
            try:
                import kagglehub
                kr = Path(kagglehub.dataset_download("nikitamanaenkov/fundus-image-dataset-for-vessel-segmentation"))
                log(f"FIVES: Kaggle copy at {kr}")
                prepare_fives(kr, FIVES_DATA, a.fives_train_per_category, a.fives_per_category)
                log(f"FIVES ready: {4 * a.fives_train_per_category} training and {n_test} test images (lowest numbers of each category)")
            except Exception as exc:
                log(f"FIVES not available ({exc!r}): download the archive from https://figshare.com/articles/figure/19688169 by hand, save it as {a.out / 'fives.rar'} and run again (or use --skip-fives)")
        else:
            raw = a.work / "fives_raw"
            try:
                if not (raw / ".extracted").exists(): extract_fives(fa, raw)
                prepare_fives(raw, FIVES_DATA, a.fives_train_per_category, a.fives_per_category)
                log(f"FIVES ready: {4 * a.fives_train_per_category} training and {n_test} test images (lowest numbers of each category)")
            except Exception as exc:
                log(f"FIVES preparation failed ({exc!r}); folders under {raw}:")
                for q in sorted(d for d in raw.rglob("*") if d.is_dir())[:30]: log(f"  {q.relative_to(raw)}")
    if (FIVES_DATA / "DRIVET" / "HR").exists(): roots["fives"] = FIVES_DATA

for name in ("drive", "fives"):
    if name in roots and not (DATA / name).exists(): (DATA / name).symlink_to(Path(roots[name]).resolve(), target_is_directory=True)
roots = {k: v for k, v in roots.items() if k in a.datasets}
if not a.skip_train:
    jobs = [(f"export_{ds}_s{seed}_{arch}", f"{PY} {HERE / 'export_probs.py'} --dataset {ds} --root {root} --out {a.out} --seeds {seed} --archs {arch} --weights {ROOT / 'weights'}")
            for ds, root in roots.items() if ds != "fives" for seed in a.seeds for arch in a.archs]
    run_pool(jobs, JOBS)
    if "fives" in roots:
        (FIVES_OUT / "models").mkdir(parents=True, exist_ok=True)
        for f in (a.out / "models").glob("*_fives_*.pt"): shutil.copy(f, FIVES_OUT / "models" / f.name)
        sh(f"{PY} {HERE / 'export_probs.py'} --dataset fives --root {roots['fives']} --out {FIVES_OUT} --seeds 7 --light-train")
        (a.out / "models").mkdir(exist_ok=True)
        for f in (FIVES_OUT / "models").glob("*.pt"): shutil.copy(f, a.out / "models" / f.name)
    log("all probability maps exported")

analyse = [d for d in roots if d in (a.analyse or roots)]
jobs = []
for ds in analyse:
    if ds == "fives": continue
    extra = f"--pathology {codes}" if ds == "stare" else ""
    for seed in a.seeds:
        for arch in a.archs:
            jobs.append((f"analysis_{ds}_s{seed}_{arch}", f"{PY} {HERE / 'run_analysis.py'} --dataset {ds} --root {roots[ds]} --drive-root {DRIVE_ROOT} --probs {a.out / 'probs'} "
                         f"--out {a.out / 'json'} --seeds {seed} --archs {arch} --crf-grid {a.crf_grid} {extra}"))
run_pool(jobs, JOBS)
if "fives" in analyse:
    probs = FIVES_OUT / "probs"; probs.mkdir(parents=True, exist_ok=True)
    for f in (a.out / "probs").glob("drive_*_s7_*.npy"): shutil.copy(f, probs / f.name)
    sh(f"{PY} {HERE / 'run_analysis.py'} --dataset fives --root {roots['fives']} --drive-root {DRIVE_ROOT} --probs {probs} "
       f"--out {a.out / 'json'} --seeds 7 --crf-grid {a.crf_grid} --fast --no-crf")

z = a.out / f"results_{time.strftime('%Y%m%d_%H%M')}.zip"
with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
    for f in sorted((a.out / "json").glob("*.json")): zf.write(f, f"json/{f.name}")
    for f in sorted((a.out / "json").glob("*.txt")): zf.write(f, f"json/{f.name}")
log(f"done: {z}")
