# ECON3916 — Lab 5: Probability — The Engine of Prediction

This folder contains Lab 5 material for ECON3916, focused on **probability as the foundation of prediction**, with simulations that build intuition for randomness, convergence, conditional probability, and Monte Carlo risk modeling.

## Contents

- `Lab_5_Probability_—_The_Engine_of_Prediction_.ipynb` — notebook with three simulation-based probability examples:
  1) Law of Large Numbers (coin flips)
  2) Monty Hall simulation (switch vs stay)
  3) Monte Carlo revenue risk model (SaaS-style forecasting)

## Overview (What this notebook does)

### 1) The Law of Large Numbers: convergence to the mean
- Simulates repeated **fair coin flips** using NumPy (`0/1` for tails/heads).
- Tracks the cumulative proportion of heads over time:
  - `cumulative_averages = np.cumsum(flips) / np.arange(1, n_flips + 1)`
- Plots the running estimate alongside the theoretical probability of 0.5.

**Learning objective:** see empirically how sample averages stabilize as the number of trials grows.

---

### 2) Conditional probability intuition: Monty Hall
- Simulates the **Monty Hall problem** for many games:
  - randomly places the prize behind one of 3 doors
  - player chooses a door
  - host opens a losing door that is not the chosen door
  - compares outcomes for:
    - **staying** with original choice
    - **switching** to the remaining unopened door
- Prints estimated win rates for both strategies.

**Learning objective:** understand how *information revealed by the host* changes probabilities (switching ≈ 2/3).

---

### 3) Monte Carlo risk modeling: revenue uncertainty (SaaS example)
- Builds a simple revenue model with randomness in:
  - churn rate: `Normal(mean=0.10, sd=0.02)`
  - new sales: `Normal(mean=1.5M, sd=0.5M)`
- Simulates projected net revenue:
  - `net_revenue = base_rev * (1 - churn) + sales`
- Computes and prints:
  - probability of revenue decline (`P(net_revenue < base_rev)`)
  - **Value at Risk (95%)** via the 5th percentile of outcomes
- Plots a histogram of simulated revenues with vertical reference lines:
  - baseline revenue
  - VaR threshold

**Learning objective:** connect probability distributions to **business forecasting** and **risk metrics** using simulation.

## Dependencies / libraries used

- `numpy`
- `matplotlib`

## Data files referenced

- None (all examples are simulated).

## How to run

Open and run all cells in:

- `Lab 5/Lab_5_Probability_—_The_Engine_of_Prediction_.ipynb`
