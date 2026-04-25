"""Live predictor: combines the trained big-move model with live NYT headline
sentiment and user what-if overrides. Imported by the Streamlit app.
"""

import os
import joblib
import numpy as np
import pandas as pd

from nyt_sentiment import fetch_nyt_headlines, compute_daily_sentiment

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _load_csv(path, val_col=None, val_name=None):
    """Read a FRED-style CSV with a date column and one value column.
    Returns a DataFrame indexed by date with the value column renamed."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Required data file not found: {path}")
    df = pd.read_csv(path, parse_dates=[0], na_values='.')
    df.rename(columns={df.columns[0]: 'date'}, inplace=True)
    if val_col is not None and val_name is not None:
        df.rename(columns={df.columns[val_col]: val_name}, inplace=True)
    df.set_index('date', inplace=True)
    return df


class LivePredictor:
    """Load the trained big-move model plus the three history CSVs, compute
    the latest feature values, and expose three prediction modes:
    history, live headlines, and user what-if overrides."""

    def __init__(self,
                 model_path=os.path.join(BASE_DIR, 'model_bigmove_1d.pkl'),
                 features_path=os.path.join(BASE_DIR, 'feature_names.pkl'),
                 gpr_csv=os.path.join(BASE_DIR, 'ai_gpr_data_daily.csv'),
                 wti_csv=os.path.join(BASE_DIR, 'DCOILWTICO.csv'),
                 vix_csv=os.path.join(BASE_DIR, 'VIXCLS.csv')):
        """Load model + CSVs, merge, and cache the latest feature row."""
        for path in (model_path, features_path, gpr_csv, wti_csv, vix_csv):
            if not os.path.exists(path):
                raise FileNotFoundError(f"Required file not found: {path}")
        self.model = joblib.load(model_path)
        self.features = joblib.load(features_path)

        df_gpr = _load_csv(gpr_csv)
        df_wti = _load_csv(wti_csv, val_col=1, val_name='wti_price')
        df_vix = _load_csv(vix_csv, val_col=1, val_name='vix')
        df = df_gpr.join([df_wti, df_vix], how='inner').astype(float)
        df = df.dropna().sort_index()

        df['gpr_ai_lag1'] = df['GPR_AI'].shift(1)
        df['gpr_oil_lag1'] = df['GPR_OIL'].shift(1)
        df['gpr_aer_lag1'] = df['GPR_AER'].shift(1)
        df['vix_lag1'] = df['vix'].shift(1)
        df['wti_return_lag1'] = df['wti_price'].pct_change().shift(1)
        df['gpr_change_5d'] = df['GPR_AI'].shift(1) - df['GPR_AI'].shift(6)
        df['wti_return_lag5'] = df['wti_price'].pct_change(5).shift(1)
        df['vix_change_5d'] = df['vix'].diff(5).shift(1)
        df = df.dropna(subset=self.features)

        self.latest_date = df.index[-1]
        self.latest_features = {f: float(df.iloc[-1][f]) for f in self.features}
        self._df = df

    def _predict(self, features_dict, threshold):
        """Run the model on one feature row. Returns (probability, label)."""
        X = pd.DataFrame([[features_dict[f] for f in self.features]], columns=self.features)
        prob = float(self.model.predict_proba(X)[0, 1])
        label = 'BIG MOVE LIKELY' if prob >= threshold else 'NORMAL CONDITIONS'
        return prob, label

    def predict_from_history(self, threshold=0.35):
        """Predict using the most recent historical feature row from the CSVs."""
        prob, label = self._predict(self.latest_features, threshold)
        return {
            'date': str(self.latest_date.date()),
            'probability': prob,
            'prediction': label,
            'features_used': dict(self.latest_features),
            'threshold': threshold,
            'source': 'history',
        }

    def predict_from_headlines(self, headlines_summary, threshold=0.35):
        """Replace the four GPR-derived features with headline-derived estimates
        while keeping VIX and WTI features at their latest historical values."""
        proxy = headlines_summary['headline_gpr_proxy']
        oil_pct = headlines_summary['oil_related_pct']
        feats = dict(self.latest_features)
        feats['gpr_ai_lag1'] = proxy
        feats['gpr_oil_lag1'] = proxy * oil_pct / 100.0
        feats['gpr_aer_lag1'] = proxy * 0.8
        feats['gpr_change_5d'] = proxy - self.latest_features['gpr_ai_lag1']
        # vix_lag1, wti_return_lag1, wti_return_lag5, vix_change_5d: kept from history
        prob, label = self._predict(feats, threshold)
        return {
            'date': str(self.latest_date.date()),
            'probability': prob,
            'prediction': label,
            'features_used': feats,
            'threshold': threshold,
            'headline_gpr_proxy': proxy,
            'source': 'live_headlines',
        }

    def predict_combined(self, headlines_summary, wti_series, vix_series, threshold=0.35):
        """Combine live NYT headline GPR proxies with live yfinance VIX/WTI
        so all 8 features use the freshest available data."""
        proxy = headlines_summary['headline_gpr_proxy']
        oil_pct = headlines_summary['oil_related_pct']

        vl, v5 = float(vix_series.iloc[-1]), float(vix_series.iloc[-6])
        wl, wp, w5 = float(wti_series.iloc[-1]), float(wti_series.iloc[-2]), float(wti_series.iloc[-6])

        feats = dict(self.latest_features)
        feats['gpr_ai_lag1'] = proxy
        feats['gpr_oil_lag1'] = proxy * oil_pct / 100.0
        feats['gpr_aer_lag1'] = proxy * 0.8
        feats['gpr_change_5d'] = proxy - self.latest_features['gpr_ai_lag1']
        feats['vix_lag1'] = vl
        feats['vix_change_5d'] = vl - v5
        feats['wti_return_lag1'] = (wl / wp) - 1.0
        feats['wti_return_lag5'] = (wl / w5) - 1.0

        prob, label = self._predict(feats, threshold)
        return {
            'date': str(self.latest_date.date()),
            'probability': prob,
            'prediction': label,
            'features_used': feats,
            'threshold': threshold,
            'headline_gpr_proxy': proxy,
            'wti_last': wl,
            'vix_last': vl,
            'source': 'combined',
        }

    def predict_whatif(self, feature_overrides, threshold=0.35):
        """Override any subset of features with user-supplied values; fill
        the rest from the latest historical row."""
        unknown = set(feature_overrides) - set(self.features)
        if unknown:
            raise KeyError(f"Unknown feature(s): {sorted(unknown)}")
        feats = dict(self.latest_features)
        feats.update(feature_overrides)
        prob, label = self._predict(feats, threshold)
        return {
            'date': str(self.latest_date.date()),
            'probability': prob,
            'prediction': label,
            'features_used': feats,
            'threshold': threshold,
            'overrides': dict(feature_overrides),
            'source': 'what_if',
        }


if __name__ == '__main__':
    try:
        predictor = LivePredictor()
    except FileNotFoundError as e:
        print(f"Setup error: {e}")
        print("Run the notebook's 'Save Model' cell first to create model_bigmove_1d.pkl.")
        raise SystemExit(1)

    hist = predictor.predict_from_history(threshold=0.35)
    print("=== Historical Prediction ===")
    print(f"Date: {hist['date']} | Prob: {hist['probability']:.3f} | {hist['prediction']}")

    print("\n=== Live Headline Prediction ===")
    live = None
    try:
        headlines = fetch_nyt_headlines()
        summary = compute_daily_sentiment(headlines)
        print(f"Fetched {summary['total_headlines']} headlines | signal: {summary['signal']}")
        print(f"Headline GPR proxy: {summary['headline_gpr_proxy']:.1f} | oil%: {summary['oil_related_pct']:.1f}")
        live = predictor.predict_from_headlines(summary, threshold=0.35)
        print(f"Prob: {live['probability']:.3f} | {live['prediction']}")
    except Exception as e:
        print(f"Live fetch failed: {e}")

    whatif = predictor.predict_whatif({'vix_lag1': 40.0, 'gpr_ai_lag1': 300.0}, threshold=0.35)
    print("\n=== What-If Scenario (VIX=40, GPR_AI=300) ===")
    print(f"Prob: {whatif['probability']:.3f} | {whatif['prediction']}")

    print("\n=== Side-by-Side Comparison ===")
    print(f"{'Source':<22} {'Prob':>8}  {'Decision':<22}")
    print("-" * 54)
    print(f"{'History':<22} {hist['probability']:>8.3f}  {hist['prediction']:<22}")
    if live:
        print(f"{'Live Headlines':<22} {live['probability']:>8.3f}  {live['prediction']:<22}")
    print(f"{'What-If VIX=40 GPR=300':<22} {whatif['probability']:>8.3f}  {whatif['prediction']:<22}")
