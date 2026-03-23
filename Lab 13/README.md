# 🧠 The Architecture of Dimensionality: Hedonic Pricing & the FWL Theorem

## 📌 Objective

To implement a multivariate hedonic pricing model and rigorously validate the Frisch-Waugh-Lovell (FWL) theorem by decomposing and isolating variable effects within a high-dimensional real estate valuation framework.

---

## ⚙️ Methodology

- **Data Structuring**
  - Utilized 2026 California real estate data (Zillow synthetic dataset) including key variables such as sale price, property age, and proximity to tech hubs  
  - Prepared dataset for econometric modeling with appropriate variable selection  

- **Baseline OLS Modeling**
  - Estimated a multivariate Ordinary Least Squares (OLS) regression to quantify the relationship between property characteristics and sale price  
  - Interpreted coefficients within a hedonic pricing framework  

- **Omitted Variable Bias (OVB) Experiment**
  - Intentionally excluded a key explanatory variable (distance to tech hubs)  
  - Observed distortion in coefficient estimates, demonstrating how omitted factors bias model interpretation  

- **Frisch-Waugh-Lovell (FWL) Theorem Implementation**
  - Residualized the dependent variable and target independent variable against the omitted covariate  
  - Isolated the **partial effect** by regressing residuals on residuals  
  - Effectively “partialled out” shared covariance to simulate ceteris paribus conditions  

- **Dimensional Decomposition**
  - Compared the FWL-derived coefficient with the full multivariate model  
  - Verified exact equivalence, confirming the theorem computationally  

---

## 🔍 Key Findings

- Identified **severe omitted variable bias**, where excluding proximity to tech hubs incorrectly inflated the estimated effect of property age  
- Demonstrated that multivariate relationships can mask **shared covariance structures**, leading to misleading economic interpretations  
- Successfully validated the **FWL theorem**, showing that partial regression yields identical coefficients to the full model  
- Established a clear computational proof of **algorithmic ceteris paribus**, isolating the true marginal effect of a variable  

---

## 🧠 Conclusion

This project illustrates how econometric modeling is fundamentally about managing dimensionality and isolating signal from confounding structure. By bridging theory and computation, it demonstrates that rigorous decomposition techniques like the FWL theorem are essential for achieving interpretable and causally meaningful estimates in modern data environments.
