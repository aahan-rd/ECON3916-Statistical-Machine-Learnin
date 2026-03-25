# The Polynomial Trap: Bias-Variance Tradeoff

## Portfolio Summary

This lab explores the fundamental bias-variance tradeoff in predictive modeling through systematic experimentation with polynomial regression. Using both synthetic and real-world data, I demonstrate how model complexity affects generalization performance and why training error alone is a misleading metric for model selection.

### Methodology

I conducted experiments on two datasets: (1) synthetic data generated from a sine function with Gaussian noise (n=50 training, n=200 test), and (2) the Ames Housing dataset (1,460 observations, 80 features). For the synthetic data, I fit polynomial models of degrees 1–15 and evaluated performance using training RMSE, test RMSE, and 5-fold cross-validation. For the housing data, I compared parsimonious feature-selected models against high-dimensional specifications.

### Key Findings

- **Optimal complexity:** Polynomial degrees 3–5 achieved optimal test performance on synthetic data, balancing underfitting and overfitting.
- **CV reliability:** Cross-validation reliably identified the true test-optimal complexity without requiring a held-out set.
- **Real-world application:** On the Ames data, a 5-feature model outperformed the kitchen-sink specification in CV RMSE despite exhibiting lower training R², illustrating the overfitting penalty of excessive complexity.

### Technical Stack

Python, NumPy, scikit-learn (PolynomialFeatures, LinearRegression, cross_val_score), Matplotlib

### Implications

These findings reinforce that model selection should prioritize out-of-sample performance metrics. Cross-validation provides a practical, statistically grounded approach to navigating the bias-variance tradeoff in applied settings.

---

*View the full notebook for interactive visualizations and detailed analysis.*
