# ECON3916 — Lab 7: Estimation — From Formulas to Bootstrapping

This folder contains Lab 7 material for ECON3916, focused on **statistical estimation** and the shift from closed-form formulas to **simulation-based inference** (bootstrapping).

## Contents

- `Class_7_Estimation_—_From_Formulas_to_Bootstrapping_.ipynb` — notebook covering estimation concepts and bootstrap-based uncertainty quantification.

## Overview (What this notebook is about)

This lab centers on how we estimate unknown quantities from data and how we quantify uncertainty around those estimates.

Topics typically include:

- **Point estimation**
  - Estimating parameters like means, proportions, regression coefficients, etc.
  - Thinking about estimators as random variables (they vary across samples).

- **Sampling variability & standard errors**
  - Why estimates change from sample to sample.
  - How standard errors summarize that variability.

- **From formulas to resampling**
  - When analytic standard-error formulas are available (and when they’re not).
  - Using computational methods to approximate uncertainty.

- **Bootstrap estimation**
  - Resampling the observed data with replacement.
  - Recomputing the estimator many times to build an empirical sampling distribution.
  - Constructing:
    - bootstrap standard errors
    - confidence intervals (e.g., percentile intervals)

## Dependencies / libraries used

Commonly used:
- `numpy`
- `pandas`
- `matplotlib` (and/or `seaborn`)

## Data files referenced

- None listed in this folder (the notebook may generate data or load data inline).

## How to run

Open and run all cells in:

- `Lab 7/Class_7_Estimation_—_From_Formulas_to_Bootstrapping_.ipynb`
