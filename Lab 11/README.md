# 📊 Data Wrangling & Engineering Pipeline

## 📌 Objective

To transform a structurally inconsistent and incomplete dataset into a statistically robust foundation for econometric modeling through systematic feature engineering and principled handling of missing data.

---

## ⚙️ Methodology

- **Data Ingestion & Audit**
  - Imported and inspected `messy_hr_economics.csv` to assess data quality, structural inconsistencies, and feature distributions

- **Missingness Diagnostics**
  - Utilized visualization tools to map patterns of missing data
  - Identified missingness mechanisms consistent with **Missing At Random (MAR)** assumptions

- **Imputation Strategy**
  - Applied context-aware imputation techniques to preserve statistical integrity without introducing bias

- **Categorical Encoding**
  - Addressed categorical variables using encoding techniques suited for econometric modeling
  - Prevented **perfect multicollinearity (Dummy Variable Trap)** by explicitly defining and dropping a reference category

- **High-Cardinality Feature Engineering**
  - Compressed geographically granular variables using **Target Encoding**
  - Retained predictive signal while reducing dimensionality and noise

- **Feature Structuring for Econometric Models**
  - Prepared a clean, model-ready dataset compatible with regression-based frameworks (e.g., OLS)

---

## 🔍 Key Findings

- Successfully diagnosed and handled **non-random missingness structures**, ensuring valid downstream inference  
- Eliminated risks of **multicollinearity** through disciplined encoding practices and reference class selection  
- Achieved efficient dimensionality reduction in **high-cardinality features** without sacrificing informational value  
- Delivered a **clean, structured dataset** optimized for econometric modeling and causal analysis  

---

## 🧠 Conclusion

This pipeline demonstrates that rigorous data preparation is not a preliminary step, but a core component of econometric analysis. By aligning data engineering practices with statistical theory, the project ensures that subsequent modeling is both interpretable and methodologically sound.
