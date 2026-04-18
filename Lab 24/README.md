### Causal ML — Double Machine Learning for 401(k) Policy Evaluation
## Objective
Estimate the causal effect of 401(k) eligibility on household net financial assets using modern double/debiased machine learning to reduce regularization and model-selection bias in high-dimensional settings.

## Methodology
Regularization bias demonstration (simulation): Illustrated how naively applying LASSO to a causal regression shrinks the treatment coefficient toward zero under a known data-generating process (TRUE_ATE = 5.0), highlighting the distinction between prediction-optimized and causal-identified estimation.
DoubleML setup (PLR framework): Implemented a Partially Linear Regression (PLR) design to separate the treatment effect from flexible, data-driven controls.
Nuisance estimation with ML: Used Random Forest learners to model the nuisance components (outcome and treatment equations) nonparametrically.
Cross-fitting for debiasing: Applied 5-fold cross-fitting to mitigate overfitting and deliver approximately orthogonalized moment conditions for the ATE.
Policy estimand: Estimated the Average Treatment Effect (ATE) of 401(k) eligibility on net financial assets using the PLR/DML estimator.
Heterogeneity analysis: Computed Conditional Average Treatment Effects (CATEs) by income quartile to assess distributional differences in the policy impact.
Visualization: Plotted subgroup CATE point estimates with confidence intervals to communicate heterogeneity transparently.

## Key Findings
Average treatment effect (ATE): 401(k) eligibility increased net financial assets by approximately $[FILL IN ATE] (units consistent with the dataset).
Heterogeneity by income: The estimated effect varied across income quartiles, with the largest gains observed in [FILL IN quartile(s)] and smaller (or statistically weaker) effects in [FILL IN quartile(s)].
Core takeaway: Compared with naive regularized regression, the DoubleML PLR approach provides a more credible causal estimate by insulating the target parameter from shrinkage and leveraging flexible ML controls, while the CATE results suggest meaningful distributional differences in how eligibility translates into asset accumulation.
(Update the bracketed fields with your reported ATE and the direction/magnitude of CATE differences across quartiles.)