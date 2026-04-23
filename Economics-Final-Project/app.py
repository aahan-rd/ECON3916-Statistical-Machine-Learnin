"""ECON 3916 — Oil Shock Radar Streamlit dashboard.

Loads the trained big-move model from model_bigmove_1d.pkl and renders
a four-section dashboard: live ticker bar, today's predictions, live
geopolitical headlines, what-if scenario, and historical performance.

Run locally:  streamlit run app.py
"""

import warnings
from email.utils import parsedate_to_datetime

try:
    from zoneinfo import ZoneInfo
    _NY_TZ = ZoneInfo("America/New_York")
except Exception:
    from datetime import timezone, timedelta
    _NY_TZ = timezone(timedelta(hours=-4))

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix,
)

from nyt_sentiment import fetch_nyt_headlines, compute_daily_sentiment
from live_predictor import LivePredictor

try:
    import yfinance as yf
    _YF = True
except Exception:
    _YF = False

warnings.filterwarnings("ignore")

st.set_page_config(page_title="Oil Shock Radar", layout="wide", page_icon="🛢️")
sns.set_style("whitegrid")

# Load-only. The .pkl files are committed to the repo; never rebuild here.
model = joblib.load("model_bigmove_1d.pkl")
features = joblib.load("feature_names.pkl")

# --- Custom CSS (dark-mode compatible via rgba accents) ---
st.markdown("""
<style>
[data-testid="stMetricValue"] { font-size: 28px; font-weight: 700; }
[data-testid="stMetricLabel"] { font-size: 13px; opacity: 0.8; }
.block-container { padding-top: 2rem; }
.ticker-cell {
    padding: 12px 16px; border-radius: 10px;
    background: rgba(128,128,128,0.08);
    border: 1px solid rgba(128,128,128,0.18);
    height: 100%;
}
.ticker-label {
    font-size: 11px; opacity: 0.7; text-transform: uppercase;
    letter-spacing: 0.8px; margin-bottom: 4px;
}
.ticker-num { font-size: 28px; font-weight: 700; line-height: 1.15; }
.ticker-sub { font-size: 12.5px; opacity: 0.75; margin-top: 3px; }
.delta-up { color: #27ae60; }
.delta-dn { color: #e74c3c; }
.signal-low  { color: #27ae60; font-weight: 700; }
.signal-mod  { color: #e67e22; font-weight: 700; }
.signal-elev { color: #c0392b; font-weight: 700; }
.as-of { font-size: 13px; opacity: 0.7; margin: -6px 0 18px 0; }
.headline-card {
    padding: 12px 16px; margin: 8px 0; border-radius: 8px; border-left: 4px solid;
}
.headline-card h4 { margin: 0 0 6px 0; font-size: 15px; font-weight: 600; }
.headline-card .meta {
    font-size: 11px; opacity: 0.7; margin-bottom: 6px;
    text-transform: uppercase; letter-spacing: 0.3px;
}
.badge {
    display: inline-block; padding: 2px 9px; margin: 2px 4px 2px 0;
    border-radius: 12px; font-size: 10.5px; font-weight: 600;
}
.badge-neg { background: rgba(192,57,43,0.18); color: #c0392b; }
.badge-pos { background: rgba(39,174,96,0.18); color: #1f7a1f; }
.badge-oil { background: rgba(44,90,160,0.18); color: #2c5aa0; }
</style>
""", unsafe_allow_html=True)
# --- Cached loaders ---
@st.cache_resource
def load_predictor():
    """LivePredictor instance (loads model + CSVs once per session)."""
    try:
        return LivePredictor()
    except FileNotFoundError as e:
        st.error(f"Required file missing: {e}")
        st.stop()
@st.cache_data(show_spinner=False)
def load_test_predictions():
    """Probabilities + actuals over the 2024-2026 test window."""
    pred = load_predictor()
    df = pred._df.copy()
    df["wti_return"] = df["wti_price"].pct_change()
    df["target_bigmove_1d"] = (df["wti_return"].abs().shift(-1) > 0.02).astype(int)
    df = df.dropna(subset=pred.features + ["target_bigmove_1d"])
    test = df[df.index >= "2024-01-01"]
    probs = pred.model.predict_proba(test[pred.features])[:, 1]
    return test.index, probs, test["target_bigmove_1d"].astype(int).values
@st.cache_data(ttl=600, show_spinner=False)
def cached_headlines():
    h = fetch_nyt_headlines()
    s = compute_daily_sentiment(h)
    return h, s
@st.cache_data(ttl=300, show_spinner=False)
def cached_market():
    """Pull live WTI + VIX via yfinance (5-min TTL)."""
    if not _YF:
        return None, None
    try:
        wti = yf.download("CL=F", period="10d", progress=False, auto_adjust=True)
        vix = yf.download("^VIX", period="10d", progress=False, auto_adjust=True)
        wti_c = (wti["Close"].squeeze() if "Close" in wti.columns else wti.iloc[:, 0]).dropna()
        vix_c = (vix["Close"].squeeze() if "Close" in vix.columns else vix.iloc[:, 0]).dropna()
        if len(wti_c) < 6 or len(vix_c) < 6:
            return None, None
        return wti_c, vix_c
    except Exception:
        return None, None

# --- Helpers ---
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
def latest_data_timestamp(wti, vix, headlines):
    """Pick the newest timestamp across yfinance data and NYT headlines."""
    candidates = []
    for series in (wti, vix):
        if series is not None and len(series):
            ts = pd.Timestamp(series.index[-1])
            if ts.tzinfo is None:
                ts = ts.tz_localize("UTC")
            candidates.append(ts)
    for h in headlines or []:
        pub = h.get("published", "")
        if not pub:
            continue
        try:
            ts = pd.Timestamp(parsedate_to_datetime(pub))
            if ts.tzinfo is None:
                ts = ts.tz_localize("UTC")
            candidates.append(ts)
        except Exception:
            pass
    return max(candidates) if candidates else None
def fmt_as_of(ts):
    """Render 'Wednesday, April 23, 2026 at 12:15 AM EDT' without local clock."""
    if ts is None:
        return "—"
    try:
        ts_ny = ts.tz_convert(_NY_TZ)
    except Exception:
        ts_ny = ts
    day_name = ts_ny.strftime("%A")
    month_name = ts_ny.strftime("%B")
    day = ts_ny.day
    year = ts_ny.year
    hour12 = ts_ny.hour % 12 or 12
    minute = ts_ny.minute
    ampm = "AM" if ts_ny.hour < 12 else "PM"
    tz_abbr = ts_ny.strftime("%Z") or "ET"
    return f"{day_name}, {month_name} {day}, {year} at {hour12}:{minute:02d} {ampm} {tz_abbr}"
def ticker_cell(label, main_html, sub_html=""):
    sub = f'<div class="ticker-sub">{sub_html}</div>' if sub_html else ""
    return (f'<div class="ticker-cell"><div class="ticker-label">{label}</div>'
            f'<div class="ticker-num">{main_html}</div>{sub}</div>')
def arrow_span(pct):
    arrow = "▲" if pct >= 0 else "▼"
    cls = "delta-up" if pct >= 0 else "delta-dn"
    return f'<span class="{cls}">{arrow} {abs(pct):.2f}%</span>'
def signal_html(signal):
    cls = {"LOW": "signal-low", "MODERATE": "signal-mod",
           "ELEVATED RISK": "signal-elev"}.get(signal, "")
    return f'<span class="{cls}">{signal}</span>'
def headline_card_html(h):
    s = h["sentiment"]
    risk, net = s["risk_score"], s["net_sentiment"]
    if risk >= 3:
        bg, border, label = "rgba(192,57,43,0.15)", "#c0392b", "HIGH RISK"
    elif risk >= 1:
        bg, border, label = "rgba(230,126,34,0.15)", "#e67e22", "MODERATE RISK"
    elif net > 0:
        bg, border, label = "rgba(39,174,96,0.15)", "#27ae60", "POSITIVE"
    else:
        bg, border, label = "rgba(149,165,166,0.12)", "#95a5a6", "NEUTRAL"
    title = h.get("title", "").replace("<", "&lt;").replace(">", "&gt;")
    published = h.get("published", "")
    badges = []
    for p in s.get("matched_negative_phrases", []):
        badges.append(f'<span class="badge badge-neg">⚠ {p}</span>')
    for p in s.get("matched_positive_phrases", []):
        badges.append(f'<span class="badge badge-pos">✓ {p}</span>')
    if s["oil_related"]:
        badges.append('<span class="badge badge-oil">oil</span>')
    return (
        f'<div class="headline-card" style="background:{bg};border-left-color:{border};">'
        f'<h4>{title}</h4>'
        f'<div class="meta">{published} · {label}</div>'
        f'<div>{"".join(badges) if badges else "&nbsp;"}</div>'
        f'</div>'
    )
def alert(prob, threshold):
    if prob >= threshold:
        st.error("🚨 Elevated risk")
    else:
        st.success("✅ Normal conditions")

# --- Load once per session ---
predictor = load_predictor()
test_dates, test_probs, test_actuals = load_test_predictions()
wti, vix = cached_market()
try:
    headlines, summary = cached_headlines()
except Exception:
    headlines, summary = [], None

# --- Sidebar ---
st.sidebar.header("Model Settings")
threshold = st.sidebar.slider("Risk Sensitivity", 0.20, 0.60, 0.35, 0.05)
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
st.sidebar.subheader("Data Sources")
st.sidebar.markdown(
    "- **AI-GPR Index** — Iacoviello & Tong (2026)\n"
    "- **FRED** — WTI crude oil, VIX\n"
    "- **yfinance** — live WTI + VIX\n"
    "- **NYT RSS** — Middle East, World, Energy"
)
st.sidebar.divider()
st.sidebar.caption("ECON 3916 | Aahan Desai | Spring 2026")

# --- Top banner ---
st.title("🛢️ Oil Shock Radar")
st.markdown(
    "Predicting large WTI crude oil price moves using geopolitical risk indicators."
)
ts = latest_data_timestamp(wti, vix, headlines)
st.markdown(f'<div class="as-of">Live as of: <b>{fmt_as_of(ts)}</b></div>',
            unsafe_allow_html=True)

# --- Live market ticker bar ---
tcols = st.columns(4)
if wti is not None and len(wti) >= 2:
    wti_last, wti_prev = float(wti.iloc[-1]), float(wti.iloc[-2])
    tcols[0].markdown(ticker_cell(
        "WTI Crude", f"${wti_last:.2f}",
        arrow_span((wti_last / wti_prev - 1) * 100),
    ), unsafe_allow_html=True)
else:
    tcols[0].markdown(ticker_cell("WTI Crude", "—", "Unavailable"), unsafe_allow_html=True)
if vix is not None and len(vix) >= 2:
    vix_last, vix_prev = float(vix.iloc[-1]), float(vix.iloc[-2])
    tcols[1].markdown(ticker_cell(
        "VIX", f"{vix_last:.2f}",
        arrow_span((vix_last / vix_prev - 1) * 100),
    ), unsafe_allow_html=True)
else:
    tcols[1].markdown(ticker_cell("VIX", "—", "Unavailable"), unsafe_allow_html=True)
gpr_val = predictor.latest_features["gpr_ai_lag1"]
gpr_date = predictor.latest_date.strftime("%b ") + str(predictor.latest_date.day)
tcols[2].markdown(ticker_cell(
    "GPR AI Index", f"{gpr_val:.1f}", f"(as of {gpr_date})"
), unsafe_allow_html=True)
if summary:
    tcols[3].markdown(ticker_cell(
        "Headline Signal", signal_html(summary["signal"]),
        f"{summary['total_headlines']} headlines",
    ), unsafe_allow_html=True)
else:
    tcols[3].markdown(ticker_cell("Headline Signal", "—", "Unavailable"),
                      unsafe_allow_html=True)
st.divider()

# --- SECTION 1: Today's Prediction (2 cols) ---
st.header("Today's Prediction")
c1, c2 = st.columns(2)

live_headline_pred = None
if summary:
    live_headline_pred = predictor.predict_from_headlines(summary, threshold=threshold)
    with c1:
        p = live_headline_pred["probability"]
        st.metric("Live Headline Model", f"{p:.1%}",
                  delta=f"{(p - threshold) * 100:+.1f} pp vs threshold")
        st.caption(f"Based on {summary['total_headlines']} NYT headlines")
        alert(p, threshold)
else:
    with c1:
        st.metric("Live Headline Model", "—")
        st.warning("Headlines unavailable")

live_market_pred = None
if wti is not None and vix is not None:
    feats_live, wti_last, vix_last = apply_market_update(predictor.latest_features, wti, vix)
    prob_m, _ = predictor._predict(feats_live, threshold)
    live_market_pred = {"probability": prob_m, "features_used": feats_live}
    with c2:
        st.metric("Live Market Model", f"{prob_m:.1%}",
                  delta=f"{(prob_m - threshold) * 100:+.1f} pp vs threshold")
        st.caption(f"Using live WTI ${wti_last:.2f} + VIX {vix_last:.2f} + latest GPR")
        alert(prob_m, threshold)
else:
    with c2:
        st.metric("Live Market Model", "—")
        st.warning("Live prices unavailable, using last known data")

with st.expander("View feature values used by each model"):
    rows = {}
    if live_headline_pred:
        rows["Live Headline"] = live_headline_pred["features_used"]
    if live_market_pred:
        rows["Live Market"] = live_market_pred["features_used"]
    if rows:
        st.dataframe(pd.DataFrame(rows).T[predictor.features].style.format("{:.3f}"))
    else:
        st.info("No live predictions available.")

# --- SECTION 2: Live Headlines (card layout) ---
st.header("📰 Live Geopolitical Headlines")

if summary:
    top10 = sorted(headlines, key=lambda h: h["sentiment"]["risk_score"], reverse=True)[:10]
    for h in top10:
        st.markdown(headline_card_html(h), unsafe_allow_html=True)
    st.caption(
        "Sentiment uses keyword + phrase matching, not semantic understanding. "
        "Review headlines for context."
    )
else:
    st.warning("Headlines unavailable")

# --- SECTION 3: What-If Scenario ---
st.header("🔧 What-If Scenario")
st.markdown("Adjust inputs to see how the model responds.")

latest = predictor.latest_features

def _sl(col, label, key, lo, hi, step):
    return col.slider(label, min_value=float(lo), max_value=float(hi),
                      value=float(latest[key]), step=float(step), key=f"wi_{key}")

r1 = st.columns(4)
gpr_ai = _sl(r1[0], "GPR AI Level", "gpr_ai_lag1", 50, 500, 1)
gpr_oil = _sl(r1[1], "GPR Oil Level", "gpr_oil_lag1", 0, 500, 1)
gpr_aer = _sl(r1[2], "GPR AER Level", "gpr_aer_lag1", 0, 400, 1)
vix_lag = _sl(r1[3], "VIX Level", "vix_lag1", 10, 80, 0.1)

r2 = st.columns(4)
wti_r1 = _sl(r2[0], "Yesterday's WTI Return", "wti_return_lag1", -0.15, 0.15, 0.001)
gpr_ch = _sl(r2[1], "5-Day GPR Change", "gpr_change_5d", -200, 200, 1)
wti_r5 = _sl(r2[2], "5-Day WTI Return", "wti_return_lag5", -0.30, 0.30, 0.001)
vix_ch = _sl(r2[3], "5-Day VIX Change", "vix_change_5d", -30, 30, 0.1)

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

# --- SECTION 4: Historical Performance ---
st.header("📊 Historical Model Performance")

tab_hist, tab_time, tab_cm, tab_fi = st.tabs([
    "Latest Historical Prediction", "Timeline", "Confusion Matrix", "Feature Importance",
])

hist = predictor.predict_from_history(threshold=threshold)

with tab_hist:
    st.caption(f"Data through: {hist['date']} (most recent date in the merged CSVs).")
    cA, cB = st.columns([1, 2])
    with cA:
        p = hist["probability"]
        st.metric("Historical Model Probability", f"{p:.1%}",
                  delta=f"{(p - threshold) * 100:+.1f} pp vs threshold")
        alert(p, threshold)
    with cB:
        feat_df = pd.DataFrame(
            {"Value": [hist["features_used"][f] for f in predictor.features]},
            index=predictor.features,
        )
        st.dataframe(feat_df.style.format("{:.3f}"))

date_mask = (test_dates.date >= date_range[0]) & (test_dates.date <= date_range[1])
probs_v = test_probs[date_mask]
actuals_v = test_actuals[date_mask]
dates_v = test_dates[date_mask]

with tab_time:
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

with tab_cm:
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
        k1.metric("Accuracy", f"{accuracy_score(actuals_v, preds):.3f}")
        k2.metric("Precision", f"{precision_score(actuals_v, preds, zero_division=0):.3f}")
        k3.metric("Recall", f"{recall_score(actuals_v, preds, zero_division=0):.3f}")
        k4.metric("F1", f"{f1_score(actuals_v, preds, zero_division=0):.3f}")
    else:
        st.info("No data in selected date range.")

with tab_fi:
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
