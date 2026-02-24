# Recovering Experimental Truths via Propensity Score Matching

## Project Overview

This project demonstrates how causal structure can be recovered from observational data by explicitly modeling and correcting for selection bias using Propensity Score Matching (PSM).

Using the observational subset of the Lalonde dataset, I reconstructed the experimental benchmark by neutralizing systematic differences between treated and control groups.

---

## Objective

To correct the failure of naïve observational inference by modeling treatment selection mechanisms and recovering an unbiased estimate of the causal effect of job training on earnings.

---

## Methodology

- **Diagnosed Selection Bias**
  - Identified severe imbalance between treated and control groups in the observational sample.
  - Demonstrated that naïve difference-in-means estimates were substantially biased.

- **Modeled Treatment Assignment**
  - Estimated propensity scores using logistic regression.
  - Modeled the probability of treatment as a function of pre-treatment covariates (e.g., demographics and prior earnings).

- **Constructed Counterfactuals via Matching**
  - Implemented Nearest Neighbor matching based on estimated propensity scores.
  - Matched treated individuals to observational controls with comparable selection likelihood.
  - Reduced covariate imbalance to approximate experimental conditions.

- **Estimated Post-Matching Treatment Effect**
  - Computed the Average Treatment Effect on the Treated (ATT) using matched samples.
  - Evaluated balance diagnostics to confirm bias reduction.

---

## Key Findings

- **Naïve Observational Estimate:** –$15,204 (severely biased and directionally incorrect)
- **Matched Estimate (PSM):** ~+$1,800
- **Experimental Benchmark (True Effect):** ~+$1,795

Propensity Score Matching successfully recovered the experimental truth from observational data that initially suggested the opposite conclusion.

This result illustrates a core principle of applied econometrics:  
When selection mechanisms are explicitly modeled, causal signal can be recovered even in non-randomized environments.

---

## Economic Insight

Observational datasets frequently encode behavioral selection patterns that contaminate naïve inference.  

Propensity Score Matching operationalizes a structural correction by reconstructing a quasi-experimental design from non-experimental data. In production analytics environments, this approach provides a disciplined alternative to raw correlation analysis — reducing the risk of policy errors, capital misallocation, and algorithmic bias.

This lab reinforces that credible causal inference is not about more data — it is about better design.
