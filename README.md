# Graphene-THz-ML-Surrogate

Physics-informed ML surrogate & inverse design engine for graphene-based terahertz absorbers (pure Python, zero dependencies)

## Overview

This repository contains a standalone, pure-Python machine-learning pipeline for the rapid forward and inverse design of graphene-based plasmonic absorbers in the terahertz (THz) band.

Instead of running time-consuming full-wave FDTD simulations (CST / COMSOL), this framework:

1. Generates physics-validated datasets from closed-form analytical circuit models (transmission-line + RLC equivalents, derived in my Ph.D. thesis),
2. Trains a KNN-based forward surrogate that predicts absorption spectra in milliseconds (test R2 = 0.92),
3. Runs a KNN inverse-design engine that, given a target Lorentzian resonance, predicts optimal fabrication parameters in ~30 ms, replacing the brute-force nested-loop optimization of the thesis (Sec. 4.7.3.1).
## Background (Ph.D. thesis foundation)

The analytical models implemented here are taken directly from my Ph.D. thesis on graphene THz metasurfaces:

- Single-layer disk absorber: closed-form RLC + transmission-line model (Thesis Eqs. 4-148 to 4-158), validated against full-wave FDTD (Thesis Fig. 4-61).
- Dual- and tri-layer disk absorbers: cascaded transmission-line models (Thesis Eqs. 4-159 to 4-207).
- Ultra-broadband ribbon+disk absorber: eigenmode-based analytical model (Thesis Eqs. 4-131 to 4-147).

### The problem solved

In the thesis (Sec. 4.7.3.1), the dielectric thicknesses (d1, d2, d3) of the tri-layer absorber were optimized with exhaustive grid search (three nested for-loops) maximizing mean absorption over 0.8-2.2 THz. This brute-force approach scales poorly with parameter count.

This ML pipeline replaces hours of brute-force search with a ~30 ms KNN inverse-design inference.
## Repository contents

- absorber.py : analytical forward model (Eqs. 4-148 to 4-158), pure Python, no dependencies
- dataset.py : generates 1000 physics-validated samples (random sampling over d, tau, alpha)
- train_knn.py : KNN forward surrogate, test R2 = 0.92
- inverse_design.py : inverse design, target spectrum -> optimal (d, tau, alpha) in ~30 ms

## How to run

No installation required (standard library only):

    python absorber.py        # analytical forward model + text plot
    python dataset.py         # generate dataset.csv (1000 x 50 spectrum)
    python train_knn.py       # train/evaluate forward surrogate (R2 = 0.92)
    python inverse_design.py  # inverse design demo (target @ 1.2 THz)
    ## Example inverse-design output

    Target: perfect absorption peak at 1.20 THz
    Optimal fabrication parameters predicted:
       -> Dielectric thickness (d) = 34.7 um
       -> Relaxation time (tau)    = 0.349 ps
       -> Matching coefficient (alpha) = 1.30
    Inference time: 31.7 ms

## Roadmap

- [ ] Port dual-layer model (Eqs. 4-159 to 4-177) - in progress
- [ ] Port tri-layer model (Eqs. 4-181 to 4-207) + smart optimization of (d1, d2, d3)
- [ ] Neural surrogate with documented failure analysis (sigmoid saturation, dying ReLU)

## Contact

Nastaran Korani
Ph.D. in THz Graphene Photonics
Open to remote computational research collaborations and R&D contractor roles.
Email: [nastarankorani7597@gmail.com] | LinkedIn: [https://www.linkedin.com/in/nastaran-korani-b55a68249/]
