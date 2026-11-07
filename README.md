# Ridge-gated geodesic recovery of thin retinal vessels

Code, trained models and results for the manuscript *Training-Free Ridge-Gated Geodesic Recovery of Thin Retinal Vessels Undetected by Deep Segmentation Networks* (V. Vanitha, under review).

Segmentation networks often give thin retinal vessels a probability just below 0.5, so thresholding breaks faint branches into fragments. The two stages here work on the probability map and the photograph after inference. They need no training and no access to the network.

**RGR (ridge-gated geodesic recovery)** adds back a pixel that the 0.5 threshold removed only when three conditions hold:

1. the network gives it a probability of at least τp = 0.25;
2. the raw green channel shows a vessel-like ridge there (normalised Frangi response at least τv = 0.05);
3. it lies within δ = 8 pixels of the thresholded mask.

The accepted pixels are grown from the thresholded mask by geodesic reconstruction, so every added pixel is connected to a vessel the network already found.

**RGR-P (path completion)** joins the fragments that RGR leaves apart. From every end point of the skeleton of the RGR mask, the minimal-cost path to another fragment within a square window of half-width ρ = 8 pixels is traced on the cost 1 − max(min(P/0.5, 1), ridge) + 0.001. A path is accepted when its mean cost is at most θ = 0.3; accepted paths are thickened where P ≥ 0.10 and the mask is grown again from the seed.

**Conservative-gate RGR** (`dice_safe_rgr` in the code) lowers the probability gate from 0.45 in steps of 0.05 while the precision of the added pixels, estimated from the probabilities, stays above half of the estimated Dice of the mask.

All lengths are given at DRIVE resolution. For another dataset they are multiplied by k, the ratio of its median field-of-view diameter to that of DRIVE (CHASE_DB1 1.703, STARE 1.186, FIVES 3.728).

## Repository layout

| Path | Contents |
|---|---|
| `rgr/recovery.py` | `ridge_map`, `rgr`, `rgr_p`, `dice_safe_rgr`, and the threshold, hysteresis and closing baselines |
| `rgr/baselines.py` | Dual-threshold iteration as released with FR-UNet, dense conditional random field, threshold selection |
| `rgr/data.py` | DRIVE, CHASE_DB1, STARE and FIVES preparation, second observers, thin-vessel reference structures |
| `rgr/networks.py` | U-Net, Attention U-Net and U-Net++ with the training loop and test-time averaging |
| `rgr/train_light.py` | Memory-light training for the 2048 × 2048 FIVES photographs |
| `rgr/metrics.py` | Pooled Dice, precision, recall, thin-centreline recall, clDice, fragment count |
| `rgr/measures.py` | Topology and skeleton scores, vessel measurements, bootstrap, Holm adjustment, calibration |
| `rgr/bridges.py` | Classification of every bridge between fragments against the reference |
| `rgr/analysis.py` | Dice condition per image, gate choice, missed thin-vessel pixels, second-observer rescoring |
| `scripts/run_all.py` | The complete study: data, networks, probability maps and every analysis |
| `scripts/export_probs.py` | Trains or loads a network and writes its probability maps |
| `scripts/run_analysis.py` | All analyses of one dataset from saved probability maps |
| `scripts/make_tables.py` | Tables from the result files |
| `scripts/make_figures.py` | Figures from the result files (600 dpi) |
| `scripts/ablation.py` | Ablation of the three gates of RGR |
| `scripts/apply_rgr.py` | RGR, RGR-P or the conservative gate on the probability map of any network |
| `weights/` | The six seed-7 networks for DRIVE and CHASE_DB1 |
| `results/json/` | One result file per dataset, network and training seed (30 files) |
| `results/tables/` | All tables of the paper and the supplement, as CSV and Markdown |
| `results/figures/` | The result figures of the paper and the supplement |

## Installation

```
git clone https://github.com/vanithamagesh/ridge-gated-geodesic-recovery.git
cd ridge-gated-geodesic-recovery
pip install -r requirements.txt
```

## Using RGR with your own network

```python
from rgr import ridge_map, rgr, rgr_p, dice_safe_rgr

ridge = ridge_map(image, fov)                 # image: RGB uint8, fov: boolean mask
mask = rgr(prob, fov, ridge)                  # prob: probability map in [0, 1]
mask_p = rgr_p(prob, fov, ridge)              # RGR followed by path completion
mask_c = dice_safe_rgr(prob, fov, ridge)      # conservative gate
```

For images at another resolution, compute the ridge map with `ridge_map(image, fov, k)` and pass `dl=round(8 * k)` and `rho=round(8 * k)`.

From the command line:

```
python scripts/apply_rgr.py --image 01_test.tif --prob 01_prob.npy --fov 01_mask.gif --out 01_rgr.png
python scripts/apply_rgr.py --image 01_test.tif --prob 01_prob.npy --fov 01_mask.gif --out 01_rgrp.png --method rgr-p
python scripts/apply_rgr.py --image 01_test.tif --prob 01_prob.npy --fov 01_mask.gif --out 01_cons.png --method conservative
python scripts/apply_rgr.py ... --k 1.703
```

The probability map may be a `.npy` array in [0, 1] or an 8-bit image.

## Reproducing the paper

```
python scripts/run_all.py --out outputs
python scripts/make_tables.py --rev outputs/json --out outputs/tables
python scripts/make_figures.py --rev outputs/json --probs outputs/probs --data outputs/data --out outputs/figures
python scripts/ablation.py --data outputs/data --probs outputs/probs --out outputs/tables/T_ablation.csv
```

`run_all.py` downloads the data, trains the networks that are not in `weights/`, writes the probability maps and runs every analysis. DRIVE and CHASE_DB1 come from the SGL repository, STARE and the CHASE_DB1 second observer from the deepdyn repository, and FIVES from figshare (article 19688169). The FIVES archive is a RAR file and needs `unrar` or `7z`. The DRIVE second observer is read from a Kaggle copy of DRIVE when `kagglehub` is installed and configured; without it the second-observer analysis covers CHASE_DB1 and STARE, as in the paper. The STARE pathology flags come from the STARE diagnosis list; when the list cannot be downloaded, the standard split into ten normal and ten pathological images is used. The published results flag test images 0291, 0319 and 0324 as pathological.

Every step skips what is already in `--out`, so an interrupted run continues where it stopped. A GPU is recommended. Useful options:

| Option | Effect |
|---|---|
| `--datasets drive chase stare` | Process a subset of the datasets |
| `--seeds 7` | Train and analyse one seed only (default 7, 11 and 23) |
| `--skip-fives` | Leave out FIVES |
| `--fives-zip PATH` | Use a FIVES archive that is already downloaded |
| `--jobs N` | Number of parallel tasks |

The result files of a run are written to `outputs/json/` and have the same format as `results/json/`. The seed-7 networks for DRIVE and CHASE_DB1 are taken from `weights/`; all other networks are trained with the configuration below. The published files were computed from GPU probability maps. GPU and CPU inference differ in a few pixels of the maps; for DRIVE U-Net, a CPU rerun selects the same settings and differs from the published file by at most 0.00002 in Dice, 0.00014 in thin-centreline recall and 0.25 in fragments per image.

## Protocol

| Item | Setting |
|---|---|
| DRIVE | 20 training images (21 to 40) and 20 test images (01 to 20); training images 22, 27, 34 and 39 form the validation set, and the networks are trained on the other 16 |
| CHASE_DB1 | Images 1 to 20 for training, 21 to 28 (children 11 to 14) for testing |
| STARE | The 20 labelled images, 10 for training and 10 for testing (0162, 0163, 0235, 0236, 0239, 0240, 0255, 0291, 0319, 0324); the Hoover annotation is the reference and the Kouznetsova annotation the second observer |
| FIVES | Fixed subset of the official split: the 25 lowest-numbered training images and the 10 lowest-numbered test images of each category (100 and 40 images) |
| Field of view | Provided for DRIVE, generated from the red channel for the other datasets |
| Reference | The first observer; thin vessels are reference skeleton pixels with a radius of at most 2k pixels |
| Training | 4,000 steps of four 128 × 128 patches, AdamW with cosine decay from 10⁻³ to 2 × 10⁻⁵, 0.75 cross-entropy + 0.25 soft Dice, averaged weights, four flipped views at test time |
| Seeds | 7, 11 and 23 on DRIVE, CHASE_DB1 and STARE; 7 on FIVES |
| Parameters | Chosen once on the four DRIVE validation images and transferred to the other datasets with k; no test image is used for any choice |

## Results

Seed 7, pooled over the test images. Fragments per image is the mean number of eight-connected components; the reference annotations have 2.85 (DRIVE), 2.13 (CHASE_DB1), 4.70 (STARE) and 4.05 (FIVES).

| Dataset | Network | Procedure | Dice | Precision | Thin-centreline recall | clDice | Fragments per image |
|---|---|---|---|---|---|---|---|
| DRIVE | U-Net | Threshold 0.5 | 0.8253 | 0.8386 | 0.6898 | 0.8263 | 75.2 |
|  |  | RGR | 0.8254 | 0.8316 | 0.7060 | 0.8291 | 61.0 |
|  |  | RGR-P | 0.8237 | 0.8216 | 0.7245 | 0.8336 | 20.6 |
|  | Attention U-Net | Threshold 0.5 | 0.8262 | 0.8397 | 0.6906 | 0.8270 | 68.2 |
|  |  | RGR | 0.8263 | 0.8330 | 0.7067 | 0.8299 | 55.4 |
|  |  | RGR-P | 0.8249 | 0.8239 | 0.7242 | 0.8344 | 17.2 |
|  | U-Net++ | Threshold 0.5 | 0.8274 | 0.8364 | 0.6962 | 0.8282 | 55.8 |
|  |  | RGR | 0.8274 | 0.8298 | 0.7113 | 0.8304 | 45.5 |
|  |  | RGR-P | 0.8259 | 0.8222 | 0.7249 | 0.8334 | 14.2 |
| CHASE_DB1 | U-Net | Threshold 0.5 | 0.8086 | 0.7809 | 0.6897 | 0.8365 | 71.2 |
|  |  | RGR | 0.8021 | 0.7443 | 0.7388 | 0.8413 | 48.9 |
|  |  | RGR-P | 0.8016 | 0.7420 | 0.7442 | 0.8413 | 32.6 |
|  | Attention U-Net | Threshold 0.5 | 0.8101 | 0.7909 | 0.6743 | 0.8343 | 74.2 |
|  |  | RGR | 0.8041 | 0.7532 | 0.7230 | 0.8406 | 51.2 |
|  |  | RGR-P | 0.8043 | 0.7512 | 0.7309 | 0.8425 | 34.8 |
|  | U-Net++ | Threshold 0.5 | 0.8100 | 0.7900 | 0.6919 | 0.8350 | 67.4 |
|  |  | RGR | 0.8045 | 0.7525 | 0.7387 | 0.8399 | 49.0 |
|  |  | RGR-P | 0.8044 | 0.7504 | 0.7457 | 0.8409 | 31.6 |
| STARE | U-Net | Threshold 0.5 | 0.8423 | 0.8737 | 0.7772 | 0.8773 | 69.6 |
|  |  | RGR | 0.8442 | 0.8608 | 0.8118 | 0.8855 | 47.0 |
|  |  | RGR-P | 0.8443 | 0.8561 | 0.8207 | 0.8874 | 24.7 |
|  | Attention U-Net | Threshold 0.5 | 0.8474 | 0.8712 | 0.7900 | 0.8820 | 66.6 |
|  |  | RGR | 0.8480 | 0.8564 | 0.8229 | 0.8887 | 42.9 |
|  |  | RGR-P | 0.8472 | 0.8510 | 0.8323 | 0.8903 | 20.8 |
|  | U-Net++ | Threshold 0.5 | 0.8499 | 0.8786 | 0.7933 | 0.8848 | 51.0 |
|  |  | RGR | 0.8513 | 0.8648 | 0.8249 | 0.8910 | 33.1 |
|  |  | RGR-P | 0.8511 | 0.8621 | 0.8301 | 0.8918 | 19.5 |
| FIVES | U-Net | Threshold 0.5 | 0.8332 | 0.8204 | 0.7501 | 0.8277 | 390.4 |
|  |  | RGR | 0.8239 | 0.7796 | 0.7933 | 0.8117 | 327.9 |
|  |  | RGR-P | 0.8225 | 0.7749 | 0.8001 | 0.8060 | 186.7 |
|  | Attention U-Net | Threshold 0.5 | 0.8440 | 0.8265 | 0.7710 | 0.8384 | 339.4 |
|  |  | RGR | 0.8351 | 0.7910 | 0.8051 | 0.8228 | 295.3 |
|  |  | RGR-P | 0.8334 | 0.7866 | 0.8100 | 0.8168 | 160.7 |
|  | U-Net++ | Threshold 0.5 | 0.8343 | 0.8463 | 0.7089 | 0.8299 | 301.4 |
|  |  | RGR | 0.8312 | 0.8118 | 0.7544 | 0.8221 | 259.4 |
|  |  | RGR-P | 0.8304 | 0.8084 | 0.7601 | 0.8181 | 151.7 |

Bridges are the added components that join two or more fragments of the thresholded mask, pooled over the three networks. A bridge is correct when it reconnects fragments that the reference joins along the annotated course, and a shortcut when it joins vessels that the reference keeps apart.

| Dataset | Stage | Bridges | Correct (%) | Shortcuts |
|---|---|---|---|---|
| DRIVE | RGR | 742 | 81.4 | 2 |
| DRIVE | RGR-P | 2596 | 78.7 | 33 |
| CHASE_DB1 | RGR | 455 | 74.9 | 2 |
| CHASE_DB1 | RGR-P | 797 | 71.0 | 13 |
| STARE | RGR | 621 | 84.7 | 2 |
| STARE | RGR-P | 1101 | 78.1 | 11 |
| FIVES | RGR | 4563 | 48.4 | 16 |
| FIVES | RGR-P | 14212 | 30.8 | 112 |

The standard deviation over the three training seeds is at most 0.2 percentage points for the thin-centreline gain of RGR and of RGR-P (`results/tables/T_seeds.csv`). Bootstrap intervals and Wilcoxon tests are in `T_boot.csv`, the equal-precision comparison in `T_equal.csv`, the second observer in `T_obs2.csv`, the downstream vessel measurements in `T_measure.csv` and the calibration analysis in `T_calib.csv`.

| Figure | File |
|---|---|
| Figure 5 | `results/figures/fig_paths.png` |
| Figure 7 | `results/figures/fig_equal_precision.png` |
| Figure 8 | `results/figures/fig_bridges.png` |
| Figure 9 | `results/figures/fig_condition.png` |
| Figure 10 | `results/figures/fig_operating_point.png` |
| Figure 13 | `results/figures/fig_failures.png` |
| Figure S4 | `results/figures/fig_dice_rule.png` |
| Figure S5 | `results/figures/fig_gate.png` |
| Figure S6 | `results/figures/fig_calibration.png` |
| Figure S7 | `results/figures/fig_missed.png` |
| Figure S8 | `results/figures/fig_measurements.png` |

## Citation

The citation will be added when the manuscript is published.

## License

MIT License. DRIVE, CHASE_DB1, STARE and FIVES are subject to the terms of their original providers.
