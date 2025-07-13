# Multimessenger App - Analysis Module

## Overview
This repository is part of a **Multimessenger App** designed to analyze data from different astronomical sources. In multimessenger astronomy, signals from various messengers—such as gravitational waves, radio waves, and electromagnetic waves—are combined to gain a more comprehensive understanding of astrophysical phenomena.

In multi-messenger astronomy, signals from different astrophysical messengers (e.g., gravitational waves and radio waves) provide complementary insights into the same cosmic events. This repository enables joint inference by:

- Performing parameter estimation from gravitational wave data using Dingo-BNS, a machine learning framework that provides fast, accurate inference for binary neutron star (BNS) mergers.

- Performing light curve fitting using afterglowpy to estimate viewing angle and luminosity distance from off-axis jet observations.

- Conducting overlap analysis by comparing posterior distributions (e.g., $\theta_{\rm obs}$ and $d_L$) from both modalities, helping to reduce degeneracies and improve cosmological measurements, such as the Hubble constant ($H_0$).

## Repository Structure
```
MMA_MultimessengerAnalysis/
├── ParameterEstimation/    # Inference using Dingo-BNS on gravitational wave data
├── OverlapAnalysis/        # Scripts for overlapping GW and EM posteriors (e.g., DL and theta_obs)
└── README.md
```

## MMA Module Purpose
This module streamlines joint GW–EM inference by integrating outputs from gravitational wave parameter estimation and radio afterglow modeling. A key goal is to illustrate how joint constraints can improve the measurement of cosmological parameters like the Hubble constant ($H_0$). Specifically:

- Dingo-BNS provides posteriors on $d_L$ and $\theta_{\rm view}$ from GW observations.
- Afterglowpy-based radio fitting reduces parameter degeneracy by constraining jet orientation and energy.
- The overlap analysis aligns posteriors from both sources to quantify combined inference capabilities.

## Getting Started
Each subfolder (e.g., ParameterEstimation/, OverlapAnalysis/) includes example scripts and configuration files to reproduce the analyses.

To run a full end-to-end joint analysis:

1. Run GW parameter estimation using ParameterEstimation/dingo_inference.py.
2. Fit the radio afterglow using afterglowpy scripts from your corresponding Radio module.
3. Perform joint comparison in OverlapAnalysis/ using corner plots or KDE-based contours.

## Related Projects
This repo focuses on performing joint analysis between gravitational and radio wave data. For gravitational wave and radio wave analysis, please visit [Gravitational Wave Analysis Repo](https://github.com/parth7stark/MMA_GravitationalWave/tree/main) and [Radio Wave Analysis Repo](https://github.com/parth7stark/MMA_RadioWave/tree/main). Together, these repositories work within the multimessenger framework to capture and analyze various cosmic events.