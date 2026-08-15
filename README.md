# Graphene-THz-ML-Surrogate

Physics-informed ML surrogate & inverse design engine for graphene-based terahertz absorbers (pure Python, zero dependencies)

## Overview

This repository contains a standalone, pure-Python machine-learning pipeline for the rapid forward and inverse design of graphene-based plasmonic absorbers in the terahertz (THz) band.

Instead of running time-consuming full-wave FDTD simulations (CST / COMSOL), this framework:

1. Generates physics-validated datasets from closed-form analytical circuit models (transmission-line + RLC equivalents, derived in my Ph.D. thesis),
2. Trains KNN-based forward surrogates that predict absorption spectra in milliseconds (single-layer test R2 = 0.92; dual-layer R2 = 0.89),
3. Runs KNN inverse-design engines that, given a target Lorentzian resonance, predict optimal fabrication parameters in ~30 ms, replacing the brute-force nested-loop optimization of the thesis (Sec. 4.7.3.1).

## Background (Ph.D. thesis foundation)

The analytical models implemented here are taken directly from my Ph.D. thesis on graphene THz metasurfaces:

- Single-layer disk absorber: closed-form RLC + transmission-line model (Thesis Eqs. 4-148 to 4-158), validated against full-wave FDTD (Thesis Fig. 4-61).
- Dual-layer disk absorber: cascaded transmission-line model (Thesis Eqs. 4-159 to 4-177), broadband response FBW ~153% in the thesis (Fig. 4-63).
- Tri-layer disk absorber: cascaded transmission-line model (Thesis Eqs. 4-181 to 4-207).
- Ultra-broadband ribbon+disk absorber: eigenmode-based analytical model (Thesis Eqs. 4-131 to 4-147).

### The problem solved

In the thesis (Sec. 4.7.3.1), the dielectric thicknesses (d1, d2, d3) of the tri-layer absorber were optimized with exhaustive grid search (three nested for-loops) maximizing mean absorption over 0.8-2.2 THz. This brute-force approach scales poorly with parameter count.

This ML pipeline replaces hours of brute-force search with a ~30 ms KNN inverse-design inference.

## Repository contents

Single-layer pipeline (3-D parameter space: d, tau, alpha):

- absorber.py : analytical forward model (Eqs. 4-148 to 4-158), pure Python, no dependencies
- dataset.py : generates 1000 physics-validated samples (random sampling over d, tau, alpha)
- train_knn.py : KNN forward surrogate, test R2 = 0.92
- inverse_design.py : inverse design, target spectrum -> optimal (d, tau, alpha) in ~30 ms

Dual-layer pipeline (5-D parameter space: d1, d2, alpha1, alpha2, tau):

- absorber_2layer.py : dual-layer cascaded transmission-line model (Eqs. 4-159 to 4-177), with the corrected form of Eq. 4-174 (consistent with Eqs. 4-144 and 4-86)
- optimize_2layer.py : cost-function optimization over (d1, d2, alpha1, alpha2) maximizing mean absorption over 0.45-3.4 THz (Sec. 4.7.3.1 method); best: d1=15um, d2=15um, a1=2.5, a2=1.4 -> FBW ~95%
- dataset_2layer.py : dual-layer dataset generator (1000 samples, 5-D space, 50 frequency points)
- train_knn_2layer.py : KNN forward surrogate for dual-layer, test R2 = 0.89
- inverse_design_2layer.py : KNN inverse design for dual-layer (5-D space, <50 ms)

## How to run

No installation required (standard library only):

    python absorber.py              # single-layer analytical model + text plot
    python dataset.py               # single-layer dataset (1000 x 50 spectrum)
    python train_knn.py             # single-layer KNN surrogate (R2 = 0.92)
    python inverse_design.py        # single-layer inverse design (target @ 1.2 THz)

    python absorber_2layer.py       # dual-layer analytical model
    python optimize_2layer.py       # dual-layer cost-function optimization
    python dataset_2layer.py        # dual-layer dataset (1000 x 50 spectrum)
    python train_knn_2layer.py      # dual-layer KNN surrogate (R2 = 0.89)
    python inverse_design_2layer.py # dual-layer inverse design (target @ 2.0 THz)

## Example outputs

Single-layer inverse design (target: perfect absorption peak at 1.20 THz):

    Optimal fabrication parameters predicted:
       -> Dielectric thickness (d) = 34.7 um
       -> Relaxation time (tau)    = 0.349 ps
       -> Matching coefficient (alpha) = 1.30
    Inference time: 31.7 ms

Dual-layer inverse design (target: broadband Lorentzian peak at 2.0 THz):

    Optimal fabrication parameters predicted:
       -> Dielectric thickness 1 (d1) = 14.0 um
       -> Dielectric thickness 2 (d2) = 13.2 um
       -> Matching coeff 1 (alpha1)   = 2.41
       -> Matching coeff 2 (alpha2)   = 1.47
       -> Relaxation time (tau)       = 0.220 ps
    Inference time: 30.3 ms

## Documented model-development notes

- Initial neural-surrogate attempts (from-scratch backprop) suffered from sigmoid output saturation (vanishing gradients on sharp Lorentzian peaks) and dying ReLUs in deeper nets without advanced optimizers; switching to a KNN baseline resolved both and set the performance benchmark (R2 = 0.92 / 0.89).
- Dual-layer re-implementation revealed a trade-off between the low-frequency edge and the mid-band Fabry-Perot dip; cost-function optimization (Sec. 4.7.3.1 method) filled the dip (FBW 80% -> 95%).

## Roadmap

- [x] Port single-layer model (Eqs. 4-148 to 4-158) + full ML pipeline
- [x] Port dual-layer model (Eqs. 4-159 to 4-177) + cost-function optimization + full ML pipeline
- [ ] Port tri-layer model (Eqs. 4-181 to 4-207) + smart optimization of (d1, d2, d3)
- [ ] Archive datasets on Zenodo (DOI) and add citation

## Contact

Nastaran Korani
Ph.D. in THz Graphene Photonics
Open to remote computational research collaborations and R&D contractor roles.
Email: [nastarankorani7597@gmail.com] | LinkedIn: [https://www.linkedin.com/in/nastaran-korani-b55a68249/]
