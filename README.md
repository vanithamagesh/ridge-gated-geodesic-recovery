# Thin retinal vessel recovery with ridge-gated reconstruction and gap joining

Code and results for the manuscript *Thin retinal vessel recovery with ridge-gated reconstruction and gap joining* (V. Vanitha, under review).

Segmentation networks often give thin retinal vessels a probability just below 0.5, so thresholding the probability map breaks faint branches into fragments. The two stages in this repository work on the probability map after inference. They need no training, no network weights and no photograph.

**RGR (ridge-gated reconstruction)** adds back a pixel that the 0.5 threshold removed only when three conditions hold:

1. the network gives it a probability of at least τp = 0.25;
2. the probability map forms a ridge there: the Frangi vesselness of the probability map (bright ridges, scales 1, 1.5 and 2 pixels, divided by its 99th percentile in the field of view) is at least τv = 0.05;
3. it lies within δ = 8 pixels of the thresholded mask.

The candidates are grown from the thresholded mask by geodesic reconstruction, so every added pixel is connected to a vessel that the network already found.

**RGR-J (gap joining)** links the fragments that RGR leaves apart. From every end point of the skeleton of the RGR mask, a straight segment is drawn to the nearest pixel of another fragment inside a square window of half-width ρ = 8 pixels. The segment is kept only when it deviates by at most 45° from the direction of the branch, estimated from the skeleton pixels of the same fragment within 5 pixels of the end point, and when it lies inside the field of view. Kept segments are widened where P ≥ 0.10 and the mask is grown again from the seed.

All lengths are given at DRIVE resolution. For another dataset they are multiplied by k, the ratio of its median field-of-view diameter to that of DRIVE (CHASE_DB1 1.703, STARE 1.186, FIVES 3.728).

## Installation

```
git clone https://github.com/vanithamagesh/ridge-gated-geodesic-recovery.git
cd ridge-gated-geodesic-recovery
pip install -r requirements.txt
```

## Using RGR and RGR-J with your own network

```python
from rgr import rgr_j

mask_rgr, mask_rgrj = rgr_j(prob, fov)          # prob: probability map in [0, 1]; fov: boolean field-of-view mask
mask_rgr, mask_rgrj = rgr_j(prob, fov, k=1.703) # images at another resolution
```

The individual steps are also available:

```python
from rgr import ridge_from_probability, rgr, gap_join

ridge = ridge_from_probability(prob, fov, k)
mask = rgr(prob, fov, ridge, tp=0.25, tv=0.05, dl=round(8 * k))
mask_j = gap_join(prob, fov, mask, k)
```

From the command line:

```
python scripts/apply_rgr.py --prob 01_prob.npy --fov 01_mask.gif --out 01_rgrj.png              # RGR-J
python scripts/apply_rgr.py --prob 01_prob.npy --fov 01_mask.gif --out 01_rgr.png --method rgr  # RGR only
python scripts/apply_rgr.py --prob 01_prob.npy --fov 01_mask.gif --out 01.png --k 1.703         # other resolution
```

The probability map may be a `.npy` array in [0, 1] or an 8-bit image. Two alternatives compared in the paper are also available: `--method photo-ridge --image 01_test.tif` computes the ridge from the green channel of the photograph instead of the probability map, and `--method rgr-paths` replaces the straight segments by minimal-cost paths.

## Repository layout

| Path | Contents |
|---|---|
| `rgr/recovery.py` | `ridge_from_probability`, `rgr`, `gap_join`, `rgr_j`; the photograph ridge `ridge_map`, minimal-cost paths `rgr_p`, and the threshold, hysteresis and closing baselines |
| `rgr/baselines.py` | Dual-threshold iteration as released with FR-UNet, dense conditional random field, threshold selection |
| `rgr/data.py` | DRIVE, CHASE_DB1, STARE and FIVES preparation, second observers, thin-vessel reference structures |
| `rgr/networks.py`, `rgr/train_light.py` | U-Net, Attention U-Net and U-Net++ with the training loop and test-time averaging |
| `rgr/metrics.py`, `rgr/measures.py` | Dice, precision, recall, thin-centreline recall, clDice, fragments, vessel measurements |
| `rgr/bridges.py` | Classification of every bridge between fragments against the reference |
| `scripts/run_all.py` | Data preparation, training and export of the probability maps |
| `scripts/final_protocol.py` | The frozen analysis of the paper on the stored probability maps: every procedure, margins at equal precision with bootstrap intervals, bridges, FIVES by diagnosis, scale factor, ridge-source and ridge-gate sweeps, run times |
| `scripts/component_analyses.py` | Gate shares, component ablation, recall by vessel radius, vessel measurements and second-observer rescoring (seed 7) |
| `scripts/apply_rgr.py` | RGR or RGR-J on the probability map of any network |
| `scripts/run_analysis.py`, `make_tables.py`, `make_figures.py`, `ablation.py` | Analyses of the earlier version of the manuscript (photograph ridge, path completion, conservative gate) |
| `weights/` | The six seed-7 networks for DRIVE and CHASE_DB1 |
| `results/final_protocol/` | Result tables (CSV) and `all_results.json` of the frozen analysis |
| `results/component_analyses/` | `component_analyses.json` |

## Reproducing the paper

```
python scripts/run_all.py --out outputs --maps-only
python scripts/final_protocol.py --drive-out outputs --repo . --work work --fives-archive fives.rar
python scripts/component_analyses.py --probs outputs/probs --drive-root work/sgl/dataset \
    --chase-root outputs/data/chase --stare-root outputs/data/stare --out outputs/component_analyses
```

`run_all.py` downloads the data, trains the networks that are not in `weights/` and writes the probability maps. DRIVE and CHASE_DB1 come from the SGL repository, STARE and the CHASE_DB1 second observer from the deepdyn repository, and FIVES from figshare (article 19688169); the FIVES archive is a RAR file and needs `unrar` or `7z`. `final_protocol.py` reads the stored maps and the saved FIVES networks, exports the maps of all 200 FIVES test photographs (inference only), and writes every table of the paper and the supplement. It runs on a CPU, skips finished work and continues where it stopped after an interruption. Without `--maps-only`, `run_all.py` also runs the analyses of the earlier version of the manuscript, which used the photograph ridge, path completion and a conservative gate.

The names in the result tables of `final_protocol.py` differ from the paper: `RGR-M` is RGR, `RGR-M, then straight joining with the direction rule` is RGR-J, and `RGR` is the photograph-ridge gate. The full mapping is at the top of the script.

## Protocol

| Item | Setting |
|---|---|
| DRIVE | 20 training images (21 to 40) and 20 test images (01 to 20); training images 22, 27, 34 and 39 form the validation set, and the networks are trained on the other 16 |
| CHASE_DB1 | Images 1 to 20 for training, 21 to 28 (children 11 to 14) for testing |
| STARE | The 20 labelled images, 10 for training and 10 for testing (0162, 0163, 0235, 0236, 0239, 0240, 0255, 0291, 0319, 0324); the Hoover annotation is the reference and the Kouznetsova annotation the second observer |
| FIVES | The 25 lowest-numbered training and the 10 lowest-numbered test photographs of each category (100 and 40); the other 160 official test photographs are held out and were analysed once, after the method was fixed |
| Field of view | Provided for DRIVE, generated from the red channel for the other datasets |
| Reference | The first observer; thin vessels are reference skeleton pixels with a radius of at most 2k pixels |
| Training | 4,000 steps of four 128 × 128 patches, AdamW with cosine decay from 10⁻³ to 2 × 10⁻⁵, 0.75 cross-entropy + 0.25 soft Dice, averaged weights, four flipped views at test time |
| Seeds | 7, 11 and 23 on DRIVE, CHASE_DB1 and STARE; 7 on FIVES |
| Parameters | τp, τv and δ chosen once on the four DRIVE validation images (with the photograph as ridge source) and kept unchanged; ρ = 8 and τmin = 0.10 from the earlier path search; 45° and 5 pixels fixed in advance; transferred to the other datasets with k |
| Equal precision | Global threshold swept from 0.30 to 0.70 on each test set; margin = thin-centreline recall of a procedure minus that of the threshold interpolated at the same precision; 95% percentile bootstrap with 10,000 resamples over photographs (over children on CHASE_DB1) |

## Results

Seed 7, pooled over the test photographs. TCR is thin-centreline recall; fragments are the mean number of eight-connected components per image (reference annotations: 2.85 on DRIVE, 2.13 on CHASE_DB1, 4.70 on STARE, 4.05 on FIVES). The margin is the thin-centreline recall of the procedure minus that of a global threshold at the same precision, in percentage points.

| Dataset | Network | Threshold 0.5: precision / TCR / fragments | RGR: precision / TCR / fragments | RGR-J: precision / TCR / fragments | Margin of RGR [95% CI] | Margin of RGR-J [95% CI] | Margin of the photograph-ridge gate |
|---|---|---|---|---|---|---|---|
| DRIVE | U-Net | 83.86 / 68.98 / 75.2 | 80.57 / 75.71 / 30.7 | 80.28 / 76.28 / 10.6 | +2.62 [+2.38, +2.86] | +2.87 [+2.59, +3.13] | +0.65 |
|  | Attention U-Net | 83.97 / 69.06 / 68.2 | 80.66 / 75.98 / 26.2 | 80.42 / 76.44 / 8.8 | +2.72 [+2.43, +3.01] | +2.90 [+2.61, +3.19] | +0.69 |
|  | U-Net++ | 83.64 / 69.62 / 55.8 | 80.46 / 76.10 / 23.6 | 80.24 / 76.49 / 8.8 | +2.63 [+2.38, +2.92] | +2.79 [+2.53, +3.09] | +0.69 |
| CHASE_DB1 | U-Net | 78.09 / 68.97 / 71.2 | 75.82 / 74.96 / 43.9 | 75.60 / 75.66 / 22.2 | +3.25 [+2.40, +4.08] | +3.69 [+2.81, +4.58] | +0.59 |
|  | Attention U-Net | 79.09 / 67.43 / 74.2 | 76.91 / 73.64 / 45.1 | 76.64 / 74.45 / 21.4 | +3.45 [+2.80, +4.04] | +3.96 [+3.15, +4.67] | +0.27 |
|  | U-Net++ | 79.00 / 69.19 / 67.4 | 76.74 / 75.08 / 42.1 | 76.50 / 75.86 / 19.2 | +3.05 [+2.49, +3.47] | +3.54 [+3.00, +3.96] | +0.14 |
| STARE | U-Net | 87.37 / 77.72 / 69.6 | 84.61 / 83.21 / 32.7 | 84.37 / 83.83 / 14.2 | +2.20 [+1.74, +2.82] | +2.58 [+2.17, +3.09] | +1.81 |
|  | Attention U-Net | 87.12 / 79.00 / 66.6 | 84.22 / 84.45 / 29.4 | 83.93 / 85.03 / 12.1 | +2.22 [+1.78, +2.76] | +2.50 [+2.09, +2.97] | +1.60 |
|  | U-Net++ | 87.86 / 79.33 / 51.0 | 85.10 / 84.62 / 26.4 | 84.90 / 84.98 / 13.2 | +2.00 [+1.61, +2.52] | +2.15 [+1.79, +2.59] | +1.45 |
| FIVES, 40 photographs | U-Net | 82.05 / 75.00 / 390.4 | 76.85 / 80.86 / 306.3 | 76.53 / 81.82 / 206.2 | +2.15 [+1.94, +2.37] | +2.90 [+2.63, +3.19] | +1.34 |
|  | Attention U-Net | 82.65 / 77.10 / 339.3 | 78.16 / 81.61 / 257.9 | 77.87 / 82.23 / 169.8 | +1.67 [+1.51, +1.84] | +2.12 [+1.94, +2.32] | +1.11 |
|  | U-Net++ | 84.63 / 70.90 / 301.6 | 80.31 / 76.94 / 236.0 | 80.07 / 77.73 / 158.4 | +2.32 [+2.13, +2.53] | +2.93 [+2.70, +3.18] | +1.50 |
| FIVES, 160 held-out photographs | U-Net | 81.00 / 76.21 / 510.4 | 75.43 / 82.47 / 403.8 | 74.98 / 83.40 / 268.8 | +2.23 [+2.10, +2.37] | +2.88 [+2.72, +3.05] | +1.42 |
|  | Attention U-Net | 81.30 / 78.18 / 421.9 | 76.71 / 83.16 / 311.8 | 76.36 / 83.82 / 199.4 | +1.97 [+1.86, +2.09] | +2.42 [+2.30, +2.55] | +1.38 |
|  | U-Net++ | 83.59 / 72.17 / 404.1 | 79.03 / 78.59 / 328.3 | 78.70 / 79.46 / 217.7 | +2.59 [+2.46, +2.73] | +3.21 [+3.06, +3.35] | +1.71 |

Bridges are the added components that join two or more fragments of the thresholded mask, pooled over the three networks. A bridge is correct when it reconnects fragments that the reference joins along the annotated course, a shortcut when it joins vessels that the reference keeps apart, and unannotated when a fragment it touches lies on no reference vessel.

| Dataset | Stage | Bridges | Correct (%) | Shortcut (%) | Unannotated (%) |
|---|---|---|---|---|---|
| DRIVE | RGR | 2,227 | 80.4 | 0.4 | 18.5 |
| DRIVE | RGR-J | 3,154 | 78.4 | 1.3 | 19.5 |
| CHASE_DB1 | RGR | 559 | 72.5 | 0.2 | 25.6 |
| CHASE_DB1 | RGR-J | 1,020 | 68.4 | 1.9 | 27.8 |
| STARE | RGR | 910 | 79.5 | 0.1 | 20.2 |
| STARE | RGR-J | 1,353 | 76.3 | 1.6 | 21.9 |
| FIVES, 40 photographs | RGR | 7,166 | 41.0 | 0.2 | 56.9 |
| FIVES, 40 photographs | RGR-J | 13,965 | 33.6 | 1.6 | 63.4 |
| FIVES, 160 held-out photographs | RGR | 36,196 | 34.4 | 0.2 | 63.6 |
| FIVES, 160 held-out photographs | RGR-J | 71,540 | 26.3 | 1.1 | 71.2 |

Over all 42 runs (three networks; seeds 7, 11 and 23 on DRIVE, CHASE_DB1 and STARE; the DRIVE validation images; the 40 and the 160 FIVES photographs), the 95% interval of the margin lies above zero for RGR and for RGR-J. Every value of the paper and the supplement is in `results/final_protocol/` and `results/component_analyses/`.

## Citation

The citation will be added when the manuscript is published.

## License

MIT License. DRIVE, CHASE_DB1, STARE and FIVES are subject to the terms of their original providers.
