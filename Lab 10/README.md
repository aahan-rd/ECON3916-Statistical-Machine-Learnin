# 📈 Detecting Spurious Correlation & Multicollinearity in Macroeconomic Data

## 📌 Project Overview

This project investigates the risks of **spurious correlation** and **multicollinearity** in macroeconomic time-series data using the FRED (Federal Reserve Economic Data) API. The goal is to demonstrate how naive analysis of raw economic indicators can lead to misleading conclusions, and how proper statistical techniques can uncover more reliable relationships.

---

## 🎯 Objective

To identify and correct misleading correlations in macroeconomic data by:
- Visualizing relationships in raw (non-stationary) time-series data  
- Quantifying multicollinearity using statistical diagnostics  
- Transforming data to achieve stationarity  
- Mapping structurally meaningful relationships  

---

## ⚙️ Methodology

### 1. Data Collection
- Retrieved macroeconomic indicators (e.g., GDP, CPI, unemployment) using the **FRED API**
- Structured and cleaned data using **pandas**

---

### 2. Exploratory Analysis & Correlation Traps
- Visualized relationships in raw level data using **seaborn**
- Identified **spurious correlations** driven by shared trends rather than causal relationships

---

### 3. Multicollinearity Diagnostics
- Applied **Variance Inflation Factor (VIF)** using `statsmodels`
- Quantified redundancy among predictors
- Highlighted instability in regression coefficients caused by highly correlated variables

---

### 4. Stationarity Transformation
- Converted variables into **Year-over-Year (YoY) growth rates**
- Reduced trend-driven noise and improved interpretability
- Enabled more meaningful statistical comparisons

---

### 5. Structural Analysis
- Used **Directed Acyclic Graphs (DAGs)** to represent underlying causal relationships
- Distinguished between correlation and plausible economic causation

---

## 📊 Tools & Technologies

- **Python**
- **pandas** — Data manipulation  
- **seaborn / matplotlib** — Visualization  
- **statsmodels** — Statistical diagnostics (VIF)  
- **FRED API** — Data sourcing  

---

## 🔍 Key Takeaways

- Raw macroeconomic time-series data often produce **misleading correlations** due to shared upward trends  
- **Multicollinearity inflates model variance**, reducing interpretability and reliability  
- Transforming data into **growth rates** mitigates non-stationarity issues  
- **DAG-based reasoning** provides a clearer framework for understanding causal structure  

---

## 🧠 Conclusion

This project highlights the importance of moving beyond surface-level correlations in economic data analysis. By combining statistical diagnostics with structural reasoning, it demonstrates a more robust approach to building interpretable and reliable models in macroeconomic contexts.
