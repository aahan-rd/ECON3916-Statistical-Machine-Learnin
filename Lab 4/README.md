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
- Sets y-axis limit to focus on the main mass of the data.

**Learning objective:** sanity-check anomaly labels visually and see where the algorithm is “drawing the boundary”.

### 6) Robust vs non-robust summaries: mean/median vs MAD
- Splits the dataset into:
  - “Normal” (`outlier_iso == False`)
  - “Outlier” (`outlier_iso == True`)
- For each group and for metrics `MedInc` and `MedHouseVal`, computes:
  - Mean
  - Median
  - Standard deviation
  - **MAD** (Median Absolute Deviation) using `scipy.stats.median_abs_deviation(..., scale="normal")`
- Adds an “inequality wedge” statistic:
  - `Mean - Median`
- Plots income distributions for normal vs outlier districts side-by-side.

**Learning objective:** see how tails / outliers change the mean much more than the median, and why MAD can be a better dispersion measure in heavy-tailed settings.

## Dependencies / libraries used

- `pandas`, `numpy`
- `seaborn`, `matplotlib`
- `scikit-learn`:
  - `fetch_california_housing`
  - `IsolationForest`
- `scipy`:
  - `median_abs_deviation`

## Data files referenced

- No local CSVs required.
- Dataset is fetched from scikit-learn: `fetch_california_housing(as_frame=True)`.

## How to run

Open the notebook and run all cells in Jupyter / VS Code / Colab:

- `Lab 4/Lab_4_Descriptive_Statistics_—_Robustness_in_a_Skewed_World_.ipynb`
