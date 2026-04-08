# Fraud Detection Model Evaluation — Metrics that Matter

**Objective:**  
To rigorously evaluate a logistic regression classifier on a severely imbalanced dataset by moving beyond aggregate accuracy, utilizing class-specific performance metrics and capacity-constrained threshold analysis to identify a cost-effective, optimal operational point.

**Methodology:**
* **Data Processing & Foundations:** Analyzed the Kaggle Credit Card Fraud Detection dataset comprising 284,807 real-world European transactions with PCA-anonymized features (V1–V28) and a structural class imbalance (0.172% positive fraud rate).
* **Model Training & Baseline Construction:** Trained a Logistic Regression classifier (`scikit-learn`) and benchmarked it against a naive majority-class baseline to empirically demonstrate the accuracy paradox (achieving 99.83% accuracy despite yielding zero fraud recall).
* **Advanced Evaluation Metrics:** Evaluated out-of-sample performance using specialized imbalanced metrics arrays: confusion matrices, ROC-AUC, and Precision-Recall AUC (PR-AUC), isolating the model's true effectiveness on the minority class.
* **Cost-Sensitive Threshold Optimization:** Conducted dynamic threshold analysis to locate the precise F1-maximizing operating boundary, diverging from the naive default probability threshold of 0.5.
* **Operational Constraint Integration:** Simulated real-world business constraints by applying a capacity limit (maximum 500 daily investigations) to dynamically select a risk-adjusted, business-relevant decision threshold.
* **Interactive Dashboard Deployment:** Engineered a real-time Streamlit dashboard (`fraud_dashboard.py`) to systematically compare Logistic Regression vs. Random Forest capabilities and to visualize the marginal dollar-cost impacts of False Positives and False Negatives across varying thresholds.

**Key Findings:**
* **The Accuracy Paradox:** Confirmed mathematically that baseline accuracy is a misleading performance indicator for low-frequency, high-impact anomalies like fraud.
* **Metric Divergence:** While ROC-AUC presented a highly optimistic model view, the PR-AUC provided an operationally grounded, stringent measure of the model's precision-recall trade-off on the positive class.
* **Optimal Operating Bounds:** Shifting the probability threshold incrementally generated stark variances in the true-positive/false-positive mix. The default 0.5 threshold proved sub-optimal for the F1-score.
* **Business-Aligned Risk Management:** Imposing a strict capacity constraint (investigating top instances up to an absolute limit) effectively bridged the gap between raw statistical output and actionable risk-management strategy, minimizing wasted operations while protecting institutional capital.