# ECON3916 — Lab 4: Descriptive Statistics — Robustness in a Skewed World

This folder contains Lab 4 material for ECON3916, focused on **robust descriptive statistics** and **outlier detection** in settings where data are skewed and/or capped.

## Contents

- `Lab_4_Descriptive_Statistics_—_Robustness_in_a_Skewed_World_.ipynb` — notebook demonstrating skewed outcomes, robust summaries (median/MAD), and outlier detection (IQR vs Isolation Forest).

## Overview (What this notebook does)

### 1) Load a real-world dataset + basic descriptive statistics
- Loads the **California Housing** dataset via:
  - `sklearn.datasets.fetch_california_housing(as_frame=True)`
- Creates a DataFrame (`df = data.frame`)
- Prints a summary (`df["MedHouseVal"].describe()`), emphasizing the distribution of median house values.

### 2) Visualize skew / censoring (the $500k cap)
- Plots a histogram + KDE of `MedHouseVal`:
  - highlights the well-known **upper cap** in this dataset (values capped at 5.0 in $100k units).

**Learning objective:** see why the mean can be misleading in capped / skewed distributions, and why visualization matters.

### 3) Manual outlier flagging using the IQR rule
- Implements an IQR-based outlier flagger:
  - computes Q1, Q3, IQR
  - flags values outside `[Q1 − 1.5*IQR, Q3 + 1.5*IQR]`
- Applies it to `MedInc`:
  - stores results in `df["outlier_iqr"]`
  - prints count of outliers and notes these tend to represent “wealthy” districts.

**Learning objective:** understand the classic IQR method and its interpretability.

### 4) Algorithmic anomaly detection using Isolation Forest
- Fits `sklearn.ensemble.IsolationForest` with:
  - `n_estimators=100`
  - `contamination=0.05`
  - `random_state=42`
- Uses features:
  - `MedInc`, `HouseAge`, `AveRooms`, `AveBedrms`, `Population`
- Produces `df["outlier_iso"]` (True for anomalies), and prints counts.

**Learning objective:** compare a simple rules-based outlier approach to an ML-based anomaly detector.

### 5) Visualize detected anomalies
- Scatter plot of:
  - x = `MedInc`
  - y = `AveRooms`
  - color = `outlier_iso`

