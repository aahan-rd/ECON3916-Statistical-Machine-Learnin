# NY Fed Yield Curve Recession Model Replication

## Objective
Replicate the Federal Reserve Bank of New York’s yield curve recession model by estimating recession probabilities 12 months ahead using a logistic regression on FRED macroeconomic data.

## Methodology
- Collected FRED series T10Y3M (10-Year minus 3-Month Treasury yield spread) and USREC (NBER recession indicator) spanning 1970–present.
- Resampled the daily yield spread to month-end frequency and applied a 12-month lag to align with the forecast horizon.
- Fit a Linear Probability Model to demonstrate out-of-bounds predictions and motivate a logistic specification.
- Estimated a logistic regression using scikit-learn and computed odds ratios with 95% confidence intervals via statsmodels.
- Generated a monthly recession probability time series and evaluated model behavior around the 2022–2024 inversion episode.
- Applied time-series cross-validation (TimeSeriesSplit) for a structured out-of-sample check.

## Key Findings
The Linear Probability Model produced logically invalid probabilities (below 0 and above 1) on real data, while the logistic model delivered a bounded S-curve with interpretable odds ratios. The yield spread coefficient implied substantially lower recession odds as the curve steepens, and the estimated 95% confidence interval supported statistical significance. The model’s probability series flagged elevated risk during the 2022–2024 inversion despite no NBER recession, underscoring that probabilistic forecasts quantify risk rather than guarantee outcomes.
