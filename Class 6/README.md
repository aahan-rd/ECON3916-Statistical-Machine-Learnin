# ECON3916 — Class 6: The Architecture of Bias

This folder contains the notebook for Class 6, which focuses on how **bias can enter a workflow through sampling, splitting, and experimentation mechanics**—even before any “modeling” happens.

## Contents

- `Class_6_The_Architecture_of_Bias_.ipynb` — notebook with examples illustrating sampling bias, stratified splitting, and SRM detection.

## Overview (What this notebook does)

### 1) Load a real dataset + baseline outcome rate
- Loads the **Titanic** dataset via `seaborn.load_dataset("titanic")`.
- Computes:
  - total sample size
  - overall survival rate

### 2) Train/test splitting can introduce sampling bias
- Creates a randomized 80/20 split using a permutation of indices (`np.random.permutation` with a fixed seed).
- Compares survival rates in train vs test.
- Reports a simple “sampling bias” measure as the absolute difference in survival rates:
  - `delta = abs(train_surv - test_surv)`

**Goal:** show that even “random” splits can produce noticeably different distributions/outcome rates in smaller samples.

### 3) Stratified splitting as a mitigation (preserve key distributions)
- Uses `sklearn.model_selection.train_test_split(..., stratify=df["pclass"])`.
- Prints class proportions (`pclass`) in train vs test to show they match closely.

**Goal:** demonstrate how stratification reduces distribution shift in important covariates.

### 4) Sample Ratio Mismatch (SRM) detection for experiments (Chi-square test)
- Illustrates an A/B test assignment check:
  - Observed counts: Control=450, Treatment=550
  - Expected counts: Control=500, Treatment=500
- Runs a **chi-square goodness-of-fit test** (`scipy.stats.chisquare`) to compute:
  - chi-square statistic
  - p-value
- Flags a “critical failure” when the p-value is very small (e.g., `< 0.01`), labeling it as **SRM detected**.

**Goal:** emphasize that if assignment is broken (load balancer / randomizer issues), causal conclusions from the experiment can be invalid—even with perfect downstream analysis.

## Dependencies / libraries used

- `seaborn`, `pandas`, `numpy`
- `scikit-learn` (`train_test_split`)
- `scipy` (`chisquare`)

## Data files referenced

- No local CSVs are required.
- The dataset is loaded directly from Seaborn: `sns.load_dataset("titanic")`.

## Key takeaways

- Bias can appear from **sampling variation** and **dataset splitting choices**.
- **Stratified splits** help maintain comparable distributions across splits.
- In experimentation, always check for **SRM** before interpreting treatment effects.
