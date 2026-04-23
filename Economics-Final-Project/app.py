"""ECON 3916 — Oil Shock Radar Streamlit dashboard.

Predicts large WTI crude oil moves (|daily return| > 2%) from AI-GPR
indicators, VIX, and live NYT headline sentiment. Runs with:
    streamlit run app.py
"""

import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix,
)

from nyt_sentiment import (
    fetch_nyt_headlines, compute_daily_sentiment, format_headline_html,
)
from live_predictor import LivePredictor

try:
    import yfinance as yf
    _YF = True
except Exception:
    _YF = False

warnings.filterwarnings("ignore")

import joblib
features = ['gpr_ai_lag1', 'gpr_oil_lag1', 'gpr_aer_lag1', 'vix_lag1', 
            'wti_return_lag1', 'gpr_change_5d', 'wti_return_lag5', 'vix_change_5d']
joblib.dump(features, 'feature_names.pkl')
joblib.dump(best_pipe, 'model_bigmove_1d.pkl')

st.set_page_config(page_title="Oil Shock Radar", layout="wide", page_icon="🛢️")
sns.set_style("whitegrid")


# ---------------------------------------------------------------------------
# Cached loaders
# ---------------------------------------------------------------------------

@st.cache_resource
def load_predictor():
    """Instantiate LivePredictor once per session."""
    try:
        return LivePredictor()
    except FileNotFoundError as e:
        st.error(f"Required file missing: {e}")
        st.stop()


@st.cache_data(show_spinner=False)
def load_test_predictions():
    """Compute probabilities + actuals over the 2024-2026 test window."""
    pred = load_predictor()
    df = pred._df.copy()
    df["wti_return"] = df["wti_price"].pct_change()
    df["target_bigmove_1d"] = (df["wti_return"].abs().shift(-1) > 0.02).astype(int)
    df = df.dropna(subset=pred.features + ["target_bigmove_1d"])
    test = df[df.index >= "2024-01-01"]
    X_test = test[pred.features]
    probs = pred.model.predict_proba(X_test)[:, 1]
    return X_test.index, probs, test["target_bigmove_1d"].astype(int).values


@st.cache_data(ttl=600, show_spinner=False)
def cached_headlines():
    """Fetch NYT RSS + daily sentiment; 10-minute TTL."""
    h = fetch_nyt_headlines()
    s = compute_daily_sentiment(h)
    return h, s


@st.cache_data(ttl=300, show_spinner=False)
def cached_market():
    """Pull live WTI + VIX via yfinance; 5-minute TTL. Returns (None, None)
    if yfinance is unavailable or the call fails."""
    if not _YF:
        return None, None
    try:
        wti = yf.download("CL=F", period="10d", progress=False, auto_adjust=True)
        vix = yf.download("^VIX", period="10d", progress=False, auto_adjust=True)
        wti_c = wti["Close"].squeeze() if "Close" in wti.columns else wti.iloc[:, 0]
        vix_c = vix["Close"].squeeze() if "Close" in vix.columns else vix.iloc[:, 0]
        wti_c = pd.Series(wti_c).dropna()
        vix_c = pd.Series(vix_c).dropna()
        if len(wti_c) < 6 or len(vix_c) < 6:
            return None, None
        return wti_c, vix_c
    except Exception:
        return None, None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def apply_market_update(latest, wti, vix):
    """Override VIX/WTI features from live yfinance series."""
    f = dict(latest)
    vl, v5 = float(vix.iloc[-1]), float(vix.iloc[-6])
    wl, wp, w5 = float(wti.iloc[-1]), float(wti.iloc[-2]), float(wti.iloc[-6])
    f["vix_lag1"] = vl
    f["vix_change_5d"] = vl - v5
    f["wti_return_lag1"] = (wl / wp) - 1.0
    f["wti_return_lag5"] = (wl / w5) - 1.0
    return f, wl, vl


def show_pred_tile(col, label, prob, sub, threshold):
    """Render a prediction metric tile with color-coded alert below."""
    with col:
        st.metric(label, f"{prob:.1%}",
                  delta=f"{(prob - threshold) * 100:+.1f} pp vs threshold")
        st.caption(sub)
        if prob >= threshold:
            st.error("🚨 Elevated risk")
        else:
            st.success("✅ Normal conditions")


# ---------------------------------------------------------------------------
# Load once per session
# ---------------------------------------------------------------------------

predictor = load_predictor()
test_dates, test_probs, test_actuals = load_test_predictions()


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

st.sidebar.header("Model Settings")
threshold = st.sidebar.slider(
    "Risk Sensitivity", min_value=0.20, max_value=0.60, value=0.35, step=0.05,
)
st.sidebar.caption(
    "Lower = more alerts (catches more big-move days, more false alarms). "
    "Higher = fewer alerts (higher precision)."
)
st.sidebar.divider()

min_d, max_d = test_dates.min().date(), test_dates.max().date()
date_range = st.sidebar.slider(
    "Historical Chart Range", min_value=min_d, max_value=max_d, value=(min_d, max_d),
)
st.sidebar.divider()
st.sidebar.caption("ECON 3916 | Aahan Desai | Spring 2026")
st.sidebar.caption("Data: AI-GPR Index (Iacoviello & Tong, 2026) + FRED + NYT RSS")


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.title("🛢️ Oil Shock Radar")
st.markdown(
    "Predicting large WTI crude oil price moves (|daily return| > 2%) "
    "using geopolitical risk indicators."
)


# ---------------------------------------------------------------------------
# SECTION 1: Today's Prediction
# ---------------------------------------------------------------------------

st.header("Today's Prediction")
c1, c2, c3 = st.columns(3)

hist = predictor.predict_from_history(threshold=threshold)
show_pred_tile(c1, "Historical Model", hist["probability"],
               f"Based on data through {hist['date']}", threshold)

headlines, summary, live = [], None, None
try:
    headlines, summary = cached_headlines()
    live = predictor.predict_from_headlines(summary, threshold=threshold)
    show_pred_tile(c2, "Live Headline Model", live["probability"],
                   f"Based on {summary['total_headlines']} headlines scanned now",
                   threshold)
except Exception as e:
    with c2:
        st.metric("Live Headline Model", "—")
        st.warning(f"Headline fetch failed: {e}")

wti, vix = cached_market()
market_pred = None
if wti is not None and vix is not None:
    feats_live, wti_price, vix_val = apply_market_update(predictor.latest_features, wti, vix)
    prob_m, _ = predictor._predict(feats_live, threshold)
    market_pred = {"probability": prob_m, "features_used": feats_live,
                   "wti": wti_price, "vix": vix_val}
    show_pred_tile(c3, "Live Market Model", prob_m,
                   f"Using live WTI=${wti_price:.2f}, VIX={vix_val:.1f}", threshold)
else:
    with c3:
        st.metric("Live Market Model", "—")
        st.warning("Live prices unavailable, using last known data")

with st.expander("View feature values"):
    rows = {"Historical": hist["features_used"]}
    if live:
        rows["Live Headlines"] = live["features_used"]
    if market_pred:
        rows["Live Market"] = market_pred["features_used"]
    feat_df = pd.DataFrame(rows).T[predictor.features]
    st.dataframe(feat_df.style.format("{:.3f}"))


# ---------------------------------------------------------------------------
# SECTION 2: Live NYT Headlines
# ---------------------------------------------------------------------------

st.header("📰 Live Geopolitical Headlines")

if summary:
    m1, m2, m3 = st.columns(3)
    m1.metric("Headlines Scanned", summary["total_headlines"])
    m2.metric("Avg Risk Score", f"{summary['avg_risk_score']:.2f}")
    m3.metric("Signal", summary["signal"])

    top10 = sorted(headlines, key=lambda h: h["sentiment"]["risk_score"], reverse=True)[:10]
    for h in top10:
        st.markdown(format_headline_html(h), unsafe_allow_html=True)
    st.caption(
        "Sentiment uses keyword + phrase matching, not semantic understanding. "
        "Review headlines for context."
    )
else:
    st.warning("Headlines unavailable")


# ---------------------------------------------------------------------------
# SECTION 3: What-If Scenario
# ---------------------------------------------------------------------------

st.header("🔧 What-If Scenario")
st.markdown("Adjust inputs to see how the model responds.")

latest = predictor.latest_features


def _slider(col, label, key, lo, hi, step):
    return col.slider(label, min_value=float(lo), max_value=float(hi),
                      value=float(latest[key]), step=float(step), key=f"wi_{key}")


r1 = st.columns(4)
gpr_ai = _slider(r1[0], "GPR AI Level", "gpr_ai_lag1", 50, 500, 1)
gpr_oil = _slider(r1[1], "GPR Oil Level", "gpr_oil_lag1", 0, 500, 1)
gpr_aer = _slider(r1[2], "GPR AER Level", "gpr_aer_lag1", 0, 400, 1)
vix_lag = _slider(r1[3], "VIX Level", "vix_lag1", 10, 80, 0.1)

r2 = st.columns(4)
wti_r1 = _slider(r2[0], "Yesterday's WTI Return", "wti_return_lag1", -0.15, 0.15, 0.001)
gpr_ch = _slider(r2[1], "5-Day GPR Change", "gpr_change_5d", -200, 200, 1)
wti_r5 = _slider(r2[2], "5-Day WTI Return", "wti_return_lag5", -0.30, 0.30, 0.001)
vix_ch = _slider(r2[3], "5-Day VIX Change", "vix_change_5d", -30, 30, 0.1)

overrides = {
    "gpr_ai_lag1": gpr_ai, "gpr_oil_lag1": gpr_oil, "gpr_aer_lag1": gpr_aer,
    "vix_lag1": vix_lag, "wti_return_lag1": wti_r1,
    "gpr_change_5d": gpr_ch, "wti_return_lag5": wti_r5, "vix_change_5d": vix_ch,
}
whatif = predictor.predict_whatif(overrides, threshold=threshold)

mcol, gcol = st.columns([1, 2])
with mcol:
    st.metric("What-If Probability", f"{whatif['probability']:.1%}",
              delta=f"{(whatif['probability'] - threshold) * 100:+.1f} pp vs threshold")
    if whatif["probability"] >= threshold:
        st.error("🚨 BIG MOVE LIKELY")
    else:
        st.success("✅ NORMAL CONDITIONS")

with gcol:
    hist_means = predictor._df[predictor.features].mean()
    comp = pd.DataFrame(
        {"Scenario": [overrides[f] for f in predictor.features],
         "Historical mean": [hist_means[f] for f in predictor.features]},
        index=predictor.features,
    )
    fig, ax = plt.subplots(figsize=(8, 4))
    comp.plot(kind="barh", ax=ax, color=["#2c7fb8", "#999999"])
    ax.set_xlabel("Feature value")
    ax.set_title("Scenario vs Historical Mean")
    ax.legend(loc="lower right", fontsize=8)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


# ---------------------------------------------------------------------------
# SECTION 4: Historical Performance
# ---------------------------------------------------------------------------

st.header("📊 Historical Model Performance")

date_mask = (test_dates.date >= date_range[0]) & (test_dates.date <= date_range[1])
probs_v = test_probs[date_mask]
actuals_v = test_actuals[date_mask]
dates_v = test_dates[date_mask]

tab1, tab2, tab3 = st.tabs(["Timeline", "Confusion Matrix", "Feature Importance"])

with tab1:
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(dates_v, probs_v, color="steelblue", linewidth=1.2, label="P(big move)")
    big = dates_v[actuals_v == 1]
    norm = dates_v[actuals_v == 0]
    ax.scatter(big, np.ones(len(big)), color="red", s=18, alpha=0.8, label="Actual big-move")
    ax.scatter(norm, np.zeros(len(norm)), color="gray", s=10, alpha=0.4, label="Actual normal")
    ax.axhline(threshold, color="black", linestyle="--", linewidth=1,
               label=f"Threshold={threshold}")
    hormuz_s, hormuz_e = pd.Timestamp("2026-03-01"), pd.Timestamp("2026-03-31")
    if len(dates_v) and dates_v.min() <= hormuz_e and dates_v.max() >= hormuz_s:
        ax.axvspan(max(dates_v.min(), hormuz_s), min(dates_v.max(), hormuz_e),
                   color="red", alpha=0.2, label="Hormuz crisis")
    ax.set_ylim(-0.1, 1.1)
    ax.set_ylabel("Probability / actual")
    ax.set_title("Test-Period Predictions vs Actuals")
    ax.legend(loc="upper left", fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with tab2:
    if len(actuals_v):
        preds = (probs_v >= threshold).astype(int)
        cm = confusion_matrix(actuals_v, preds, labels=[0, 1])
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax,
                    xticklabels=["Normal", "Big Move"],
                    yticklabels=["Normal", "Big Move"])
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        ax.set_title(f"Confusion Matrix @ threshold={threshold}")
        st.pyplot(fig)
        plt.close(fig)

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Accuracy",  f"{accuracy_score(actuals_v, preds):.3f}")
        k2.metric("Precision", f"{precision_score(actuals_v, preds, zero_division=0):.3f}")
        k3.metric("Recall",    f"{recall_score(actuals_v, preds, zero_division=0):.3f}")
        k4.metric("F1",        f"{f1_score(actuals_v, preds, zero_division=0):.3f}")
    else:
        st.info("No data in selected date range.")

with tab3:
    fi = pd.Series(
        predictor.model.named_steps["clf"].feature_importances_,
        index=predictor.features,
    ).sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    fi.plot(kind="barh", ax=ax, color="steelblue")
    ax.set_xlabel("Feature importance (Gini)")
    ax.set_title("Feature Importance — GradBoost (1-Day Big Move)")
    ax.text(
        0.98, 0.02,
        "Predictive importance only.\nDoes not imply causal effect.",
        transform=ax.transAxes, fontsize=9, ha="right", va="bottom",
        style="italic", color="#c0392b",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#fdedec", edgecolor="#e74c3c"),
    )
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
