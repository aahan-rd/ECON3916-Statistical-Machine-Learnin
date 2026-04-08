import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    confusion_matrix, roc_curve, roc_auc_score, precision_recall_curve, auc,
    precision_score, recall_score, f1_score
)
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import os

# Check if dataset exists
if not os.path.exists("creditcard.csv"):
    st.error("Dataset file 'creditcard.csv' not found. Please check the file path.")
    st.stop()

data = pd.read_csv("creditcard.csv")

X = data.drop("Class", axis=1)
y = data["Class"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

@st.cache_resource
def train_models(X_train, y_train):
    log_reg = LogisticRegression(solver='liblinear', random_state=42)
    log_reg.fit(X_train, y_train)

    rf_clf = RandomForestClassifier(n_estimators=10, random_state=42)  # Reduced trees for faster training
    rf_clf.fit(X_train, y_train)

    return log_reg, rf_clf

models = train_models(X_train, y_train)


# Cache predictions to speed up slider updates
@st.cache_data
def get_predictions(_models, X_test):
    log_reg, rf_clf = _models
    y_prob_log_reg = log_reg.predict_proba(X_test)[:, 1]
    y_prob_rf = rf_clf.predict_proba(X_test)[:, 1]
    return y_prob_log_reg, y_prob_rf

# Cost metric calculation
def calculate_cost(conf_matrix, cost_fn, cost_fp):
    tn, fp, fn, tp = conf_matrix.ravel()
    return fn * cost_fn + fp * cost_fp

# Load your data here (replace with your dataset)
# Example: X_train, X_test, y_train, y_test = load_data()
# Ensure these variables are defined in your notebook before running this script.

# Streamlit app
st.title("Fraud Detection Dashboard")
st.sidebar.header("Threshold Adjustment")

# Sidebar inputs
threshold = st.sidebar.slider("Threshold", 0.01, 0.99, 0.5, 0.01)
cost_fn = st.sidebar.number_input("Cost of False Negative (FN)", min_value=1, value=1000, step=100)
cost_fp = st.sidebar.number_input("Cost of False Positive (FP)", min_value=1, value=100, step=10)

# Train models and get predictions
models = train_models(X_train, y_train)
y_prob_log_reg, y_prob_rf = get_predictions(models, X_test)

# Logistic Regression Panel
st.header("Logistic Regression Evaluation")
y_pred_log_reg = (y_prob_log_reg >= threshold).astype(int)
conf_matrix = confusion_matrix(y_test, y_pred_log_reg)
precision = precision_score(y_test, y_pred_log_reg, zero_division=0)
recall = recall_score(y_test, y_pred_log_reg)
f1 = f1_score(y_test, y_pred_log_reg)
cost = calculate_cost(conf_matrix, cost_fn, cost_fp)

# Display confusion matrix and metrics
st.subheader("Confusion Matrix")
st.write(pd.DataFrame(conf_matrix, columns=["Predicted 0", "Predicted 1"], index=["Actual 0", "Actual 1"]))
st.metric("Precision", f"{precision:.2%}")
st.metric("Recall", f"{recall:.2%}")
st.metric("F1 Score", f"{f1:.2%}")
st.metric("Dollar Cost", f"${cost:,.2f}")

# ROC and PR Curves
st.subheader("ROC and Precision-Recall Curves")
fpr, tpr, _ = roc_curve(y_test, y_prob_log_reg)
roc_auc = roc_auc_score(y_test, y_prob_log_reg)
prec, rec, _ = precision_recall_curve(y_test, y_prob_log_reg)
pr_auc = auc(rec, prec)

fig, ax = plt.subplots(1, 2, figsize=(12, 5))
# ROC Curve
ax[0].plot(fpr, tpr, label=f"ROC-AUC = {roc_auc:.2f}")
ax[0].plot([0, 1], [0, 1], "k--")
ax[0].set_title("ROC Curve")
ax[0].set_xlabel("False Positive Rate")
ax[0].set_ylabel("True Positive Rate")
ax[0].legend()

# Precision-Recall Curve
ax[1].plot(rec, prec, label=f"PR-AUC = {pr_auc:.2f}")
ax[1].set_title("Precision-Recall Curve")
ax[1].set_xlabel("Recall")
ax[1].set_ylabel("Precision")
ax[1].legend()

st.pyplot(fig)

# Random Forest Comparison Panel
st.header("Random Forest Comparison")
fpr_rf, tpr_rf, _ = roc_curve(y_test, y_prob_rf)
roc_auc_rf = roc_auc_score(y_test, y_prob_rf)
prec_rf, rec_rf, _ = precision_recall_curve(y_test, y_prob_rf)
pr_auc_rf = auc(rec_rf, prec_rf)

fig, ax = plt.subplots(1, 2, figsize=(12, 5))
# ROC Curve
ax[0].plot(fpr, tpr, label=f"LogReg ROC-AUC = {roc_auc:.2f}")
ax[0].plot(fpr_rf, tpr_rf, label=f"RF ROC-AUC = {roc_auc_rf:.2f}")
ax[0].plot([0, 1], [0, 1], "k--")
ax[0].set_title("ROC Curve Comparison")
ax[0].set_xlabel("False Positive Rate")
ax[0].set_ylabel("True Positive Rate")
ax[0].legend()

# Precision-Recall Curve
ax[1].plot(rec, prec, label=f"LogReg PR-AUC = {pr_auc:.2f}")
ax[1].plot(rec_rf, prec_rf, label=f"RF PR-AUC = {pr_auc_rf:.2f}")
ax[1].set_title("Precision-Recall Curve Comparison")
ax[1].set_xlabel("Recall")
ax[1].set_ylabel("Precision")
ax[1].legend()

st.pyplot(fig)

# Interpretation
st.sidebar.header("Interpretation")
st.sidebar.write("""
- **Dollar-Cost Curve**: As you adjust the threshold, observe how the cost changes. Lower thresholds flag more transactions, increasing FP costs, while higher thresholds miss frauds, increasing FN costs.
- **Cost-Minimizing Point**: The threshold where the dollar-cost is minimized.
- **F1-Maximizing Point**: The threshold where F1 score is highest, balancing Precision and Recall.
- **PR-AUC vs. ROC-AUC**: PR-AUC is more informative for imbalanced datasets because it focuses on the positive class (fraud) performance.
""")