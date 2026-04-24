# Oil Shock Radar

Predicting large WTI crude oil price moves (|daily return| > 2%) from geopolitical risk indicators, market volatility, and live news sentiment.

**Live dashboard:** https://livenews-oil-shock-radar.streamlit.app

ECON 3916 Statistical Machine Learning — Final Project
Aahan Desai · Northeastern University · Spring 2026

---

## What this is

A binary classifier that flags trading days likely to produce a large WTI crude oil move. Directional prediction (up vs. down) fails at AUC ~0.53 because public geopolitical news is priced in within minutes. Predicting *volatility* (the size of the move, not its sign) works better — following Caldara & Iacoviello (2022), the model reaches AUC ~0.60 on the 2024–2026 test window.

The dashboard extends the static model with two real-time signal streams:

1. **NYT RSS sentiment** — fetches Middle East / World / Energy headlines, scores each with a phrase-aware geopolitical lexicon, and maps the aggregate to a GPR-equivalent value. Captures breaking news before the monthly AI-GPR update reflects it.
2. **yfinance live quotes** — pulls current WTI crude (`CL=F`) and VIX (`^VIX`) prices and recomputes the return / momentum features.

---

## Architecture

| File | Role |
|---|---|
| `app.py` | 4-section Streamlit dashboard (live ticker / today's prediction / headlines / what-if / historical performance) |
| `nyt_sentiment.py` | NYT RSS fetcher + phrase-aware sentiment scorer. Bigram matching (`end the war` beats individual word counts) with flexible word-gap regex |
| `live_predictor.py` | `LivePredictor` class exposing three prediction modes: `predict_from_history`, `predict_from_headlines`, `predict_whatif` |
| `model_bigmove_1d.pkl` | Trained pipeline: `StandardScaler` → `GradientBoostingClassifier` (500 trees, depth 3, lr 0.05, balanced sample weights) |
| `feature_names.pkl` | The 8 feature names in the order the model expects |
| `ai_gpr_data_daily.csv` | AI Geopolitical Risk Index (Iacoviello & Tong, 2026) |
| `DCOILWTICO.csv` | WTI crude oil spot prices from FRED |
| `VIXCLS.csv` | CBOE VIX from FRED |
| `requirements.txt` | Runtime dependencies |
| `3916-final-project-check-point.ipynb` | Full notebook: EDA → feature engineering → target pivot → modeling → recommendation |

---

## Features

The model uses 8 engineered features, all lagged to avoid look-ahead:

- `gpr_ai_lag1`, `gpr_oil_lag1`, `gpr_aer_lag1` — yesterday's AI-GPR indices
- `gpr_change_5d` — 5-day change in GPR_AI (measured through yesterday)
- `vix_lag1`, `vix_change_5d` — yesterday's VIX level + 5-day change
- `wti_return_lag1`, `wti_return_lag5` — 1-day and 5-day WTI returns through yesterday

Top importances in the trained model: `vix_lag1` (~23%), `wti_return_lag5` (~15%), `gpr_aer_lag1` (~13%), `wti_return_lag1` (~13%), `gpr_ai_lag1` (~12%).

---

## Three prediction modes

**Historical Model** — latest feature values from CSV (through March 2026). Baseline reading of geopolitical + market conditions.

**Live Headline Model** — NYT RSS headlines scored with a bigram-aware lexicon. The aggregate risk score maps to a `headline_gpr_proxy = 100 + avg_risk_score × 50`, which substitutes for the AI-GPR features while VIX and WTI features stay from history.

**Live Market Model** — yfinance pulls today's WTI and VIX; the model recomputes returns and VIX change from those quotes, keeping GPR features from the latest CSV.

All three share a user-adjustable classification threshold (0.20–0.60) so the operator can trade precision for recall. At threshold 0.35 the model catches 89% of actual big-move days in the test window at 32% precision; at threshold 0.50 it fires rarely but at 60% precision.

---

## Phrase-aware sentiment

The key design decision in `nyt_sentiment.py`: "end the war" and "start the war" must score differently. A naive unigram counter scores them identically because both contain "war."

The solution:

1. Two phrase lists (`POSITIVE_PHRASES`, `NEGATIVE_PHRASES`), each phrase weighted ±2.
2. Phrase matching uses a flexible regex that allows up to 2 intervening words, so `end war` matches `end the iran war`.
3. Matched spans are *removed* from the text before single-word scoring runs, preventing double-counting.
4. Oil-relevance is checked against the original text so that negative phrases like "oil shock" still flag the headline as oil-related.

Validation on five hand-crafted headlines gives the expected sign every time (including `End the Iran War` → net +1 despite two occurrences of "war").

---

## What-if scenario

All 8 features expose sliders in the dashboard. Example: `VIX = 40, GPR_AI = 300` (Hormuz-level crisis) pushes the probability to ~92%, versus ~55% at April 2026 baseline.

---

## Running locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The `.pkl` files ship with the repo, so there's no retraining step. CSVs are loaded by absolute path (`__file__`-relative), so it works from any working directory.

To regenerate the model from scratch, run the notebook through Part 3.

---

## Data sources

- **AI Geopolitical Risk Index** — Iacoviello & Tong (2026): https://www.matteoiacoviello.com/ai_gpr.html
- **FRED** — Federal Reserve Economic Data: DCOILWTICO (WTI), VIXCLS (VIX)
- **yfinance** — live quotes for `CL=F` and `^VIX`
- **NYT RSS** — Middle East, World, and Energy/Environment feeds (no API key required)

---

## Model card

- **Target:** `target_bigmove_1d` = 1 if `|tomorrow's WTI return| > 2%`, else 0. Class balance ~67/33 in training data.
- **Training window:** 1990-01-10 to 2023-12-29 (7,619 samples)
- **Test window:** 2024-01-04 to 2026-03-31 (478 samples, includes March 2026 Hormuz escalation)
- **Cross-validation:** 5-fold `TimeSeriesSplit` on training data
- **Reported test metrics at threshold 0.35:** Accuracy 38%, AUC 0.59, Precision 0.32, Recall 0.89, F1 0.47
- **Reported test metrics at default threshold 0.50:** Accuracy 71%, AUC 0.60, Precision 0.60, Recall 0.14, F1 0.23

Low accuracy at threshold 0.35 is intentional — the model is tuned for recall on rare events, not overall accuracy on the majority "normal day" class.

---

## Limitations

- AUC ~0.60 means the model gives a meaningful but modest edge. Probabilities should inform attention, not trigger automated trades.
- The test period contains only one major geopolitical shock (Hormuz, March 2026). Performance in a genuinely novel crisis is an extrapolation.
- Sentiment scoring is lexical, not semantic. `format_headline_html` marks matched phrases in the UI so the user can sanity-check what triggered the score.
- GPR indices update at a lower frequency than the dashboard; the live headline proxy is a stopgap, not a replacement for the underlying index.
