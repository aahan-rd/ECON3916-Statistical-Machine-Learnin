# 🤖 AI Capex Diagnostic Modeling

## 📌 Objective

To diagnose and correct structural failures in an OLS regression model predicting AI software revenue by addressing heteroscedasticity and multicollinearity, and restoring valid statistical inference through robust estimation techniques.

---

## ⚙️ Methodology

- **Data Structuring & Exploration**
  - Analyzed 2026 Nvidia AI capital expenditure and deployment dataset  
  - Conducted exploratory data analysis to understand scaling behavior across investment tiers  

- **Baseline OLS Estimation**
  - Built a multivariate regression model to estimate the relationship between capital expenditure, deployment metrics, and AI software revenue  
  - Evaluated coefficient estimates and initial statistical significance  

- **Heteroscedasticity Diagnostics**
  - Examined residual plots to detect non-constant variance  
  - Identified systematic variance expansion at higher levels of capital expenditure  

- **Multicollinearity Assessment**
  - Measured predictor interdependence using **Variance Inflation Factor (VIF)**  
  - Evaluated redundancy across deployment-related variables  

- **Robust Inference Correction**
  - Applied **HC3 (heteroscedasticity-consistent) robust standard errors**  
  - Re-estimated model to correct biased inference caused by heteroscedasticity  

---

## 🔍 Key Findings

- Detected **severe heteroscedasticity**, with residual variance increasing significantly at higher capital expenditure levels  
- Observed that naive OLS produced **artificially low p-values**, overstating statistical confidence  
- Application of **HC3 robust estimators** appropriately widened standard errors, correcting inference bias  
- Revealed the **true statistical significance** of AI deployment metrics, providing a more reliable basis for economic interpretation  

---

## 🧠 Conclusion

This project underscores the importance of rigorous diagnostic testing in econometric modeling, particularly in high-growth, high-variance sectors like AI infrastructure. By correcting for structural violations, the analysis ensures that statistical conclusions reflect genuine economic relationships rather than artifacts of model misspecification.
