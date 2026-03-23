# ECON3916 — Assignment 3: The Causal Architecture

This folder contains my Assignment 3 work for ECON3916 (Statistical / Machine Learning), focused on **causal inference thinking** and why “naive” comparisons can mislead when treatment is not randomly assigned.

## Contents

- `Assignment_3_The_Causal_Architecture.ipynb` — Jupyter notebook with simulations and causal estimation workflows.

## Overview (What this notebook does)

This assignment builds intuition for causal inference through a set of worked examples and code-based experiments:

### 1) Skewed outcomes & robust summaries (mean vs median)
- Simulates a highly skewed outcome distribution (e.g., many zeros + exponential “tips”).
- Compares **mean vs median** and uses **bootstrap resampling** to construct a **95% confidence interval for the median**.

### 2) Randomization inference via permutation testing (A/B-style example)
- Generates two groups with different outcome distributions (e.g., control normal vs treatment lognormal).
- Computes an observed difference in means, then uses a **permutation test** to estimate an **empirical p-value**.

### 3) Observational treatment effects & selection bias (propensity score matching)
Using a dataset loaded from `swiftcart_loyalty.csv`, the notebook demonstrates:

- **Naive SDO (simple difference in outcomes)**:
  - Compares mean post-period spend between subscribers and non-subscribers.
  - Highlights how this can be biased because subscribers may differ systematically from non-subscribers.

- **Propensity score estimation (Logistic Regression)**:
  - Fits a logit model to estimate **P(subscriber = 1 | covariates)** using:
    - `pre_spend`
    - `account_age`
    - `support_tickets`

- **Nearest-neighbor matching on the propensity score**:
  - Matches each treated unit (subscriber) to a similar control unit.
  - Estimates the **ATT (Average Treatment Effect on the Treated)** using matched pairs.

- **Covariate balance diagnostics (Standardized Mean Differences + Love Plot)**:
  - Computes SMDs before and after matching.
  - Plots a love plot to visualize balance improvements after matching.

## How to run

1. Open the notebook:
   - `Assignment 3/Assignment_3_The_Causal_Architecture.ipynb`

2. Run all cells in Jupyter / VS Code / Colab.

### Notes
- The notebook reads a file named `swiftcart_loyalty.csv`.
  - If it’s not in the repo (or not in the same working directory), you’ll need to add it or update the path.

## Key takeaway

Causal conclusions require thinking about:
- **what would have happened without treatment (counterfactuals)**,
- **how treatment assignment happens (selection / confounding)**,
- and using tools like **randomization inference** (when applicable) and **propensity score methods** (for observational settings) to reduce bias.
