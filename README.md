# ECON 3916: Statistical & Machine Learning for Economics

**Northeastern University | Spring 2026 | Aahan Desai**

This repository is my complete body of work for ECON 3916, spanning 25 labs, 4 assignments, a full econometrics research paper, a capstone final project, and a portfolio website. The course follows a concept-extension philosophy: each lab begins with a foundational econometric idea (OLS, hypothesis testing, causal inference) and extends it with a modern ML technique (regularization, cross-validation, tree ensembles, NLP). The result is a curriculum that treats prediction and explanation as complementary, not competing, goals.

---

## Capstone: Oil Shock Radar

**Predicting WTI Crude Oil Volatility from Geopolitical Risk**
[Live Dashboard](https://livenews-oil-shock-radar.streamlit.app)

### What it does

A Streamlit dashboard that predicts whether tomorrow's WTI crude oil price will move more than 2% in either direction, using geopolitical risk indices, market volatility (VIX), and live NYT headlines.

### Why volatility instead of direction

The first attempt tried directional prediction (will oil go up or down tomorrow?) and flatlined at AUC ~0.53, barely better than a coin flip. This makes economic sense: public geopolitical news gets priced into oil markets within minutes, so yesterday's headlines have almost no predictive power over tomorrow's *direction*. But they do carry information about tomorrow's *magnitude*. A trader doesn't need to know "oil goes up"; they need to know "expect chaos today, size your positions accordingly." The pivot to volatility prediction (binary: >2% absolute daily return) reached AUC ~0.60 and is far more actionable for risk management.

### The custom bigram sentiment scorer

Standard unigram sentiment analysis fails catastrophically on geopolitical headlines. "End the war" and "start the war" both contain "war" and get the same negative score, despite meaning opposite things. For a model tracking the Strait of Hormuz, this distinction is existential: "strait reopened" and "strait closed" are not the same headline.

The solution is a two-pass phrase-aware scorer (`nyt_sentiment.py`):

1. **Pass 1 (phrases, weight=2):** 44 positive and 42 negative bigram/trigram patterns are matched first, with regex allowing up to 2 intervening words (so "end the Iran war" still matches the "end war" pattern). Matched text is *removed* from the headline before Pass 2 to prevent double-counting.

2. **Pass 2 (single words, weight=1):** Remaining text is scored against curated positive, negative, and uncertainty word lists. Because phrases were already extracted, "end the war" scores as one positive phrase (+2), not as one positive phrase (+2) plus one negative word "war" (+1).

This matters because the official AI-GPR geopolitical risk index updates monthly, but crises break daily. The bigram scorer generates a real-time GPR proxy from NYT RSS feeds (`headline_gpr_proxy = 100 + avg_risk_score x 50`), bridging the gap between monthly index releases and the model's need for daily signals.

### Modeling decisions

- **8 lagged features:** All features use yesterday's data or earlier to prevent look-ahead bias. The feature set combines three signal families: geopolitical risk (GPR_AI, GPR_OIL, GPR_AER, 5-day GPR change), market volatility (VIX, 5-day VIX change), and oil momentum (1-day and 5-day WTI returns).
- **Gradient boosting over logistic regression:** Oil markets don't respond linearly to geopolitical risk. A GPR jump from 100 to 120 is qualitatively different from 400 to 420 (already in crisis). Tree ensembles capture these nonlinear interactions automatically, and the feature importances remain interpretable. Logistic regression was tested as a baseline and achieved comparable AUC (~0.60) but without the interaction effects.
- **Balanced class weights over SMOTE:** With 33% big-move days and 67% normal days, the minority class needed upweighting. SMOTE was rejected because synthetic oversampling on time-series data creates correlated duplicates that inflate cross-validation scores. Balanced sample weights during boosting are more reliable.
- **Threshold at 0.35 (not 0.50):** At 0.35, the model catches 89% of actual big-move days but has only 32% precision. At 0.50, precision rises to 60% but recall drops to 14%. The default favors recall because in risk management, missing a real crisis is far more expensive than a false alarm.
- **Test window includes March 2026 Hormuz escalation:** The model trained on 1990-2023 data and was tested on 2024-2026, which includes a genuine out-of-sample geopolitical shock (GPR_OIL hit an all-time high of 3,539). The model captured the shift, with probability climbing from ~55% to 80-92% during the crisis peak.

### Three prediction modes

The dashboard offers Historical (latest CSV data), Live Headline (NYT RSS + bigram scorer overriding GPR features), and Combined (headlines + yfinance live market quotes). A what-if scenario tab lets users manually set all 8 features to explore edge cases.

---

## Econometrics Research Paper: The Cost of Stepping Back

**Human Capital Depreciation vs. Household Facilitation in Female Labor Supply**

### Research question

Does motherhood reduce women's wages because stepping out of the workforce erodes human capital (depreciation), or does a higher-earning husband buffer that penalty by enabling more flexible work arrangements (facilitation)?

### Why this framing

Most wage gap research estimates a single "motherhood penalty" coefficient. This paper instead pits two competing mechanisms against each other in a horse-race regression: an interaction between young children and labor market experience (D1: depreciation) and an interaction between young children and husband's wage (D2: facilitation). If D1 is negative and significant, experience returns decay for mothers. If D2 is positive and significant, higher household income offsets the penalty.

### Data and methodology

The Mroz (1987) dataset (753 married women, 428 in the labor force) was analyzed using OLS with HC1 heteroscedasticity-robust standard errors, justified by a Breusch-Pagan test rejecting homoscedasticity at p=0.01. Log-wage transformation was applied because raw wages are heavily right-skewed, and log-transformation yields approximate normality and percentage-change coefficient interpretation.

### Key findings

Neither mechanism reached statistical significance. The kids-times-experience interaction (D1) was positive but insignificant (p=0.52), meaning no evidence that experience returns decay for mothers. The kids-times-husband-wage interaction (D2) was negative and insignificant (p=0.40), meaning no evidence that household income buffers the penalty. Education (10.1% per year) and experience (1.7% per year) remained the dominant wage determinants across all specifications.

### Why the null result is informative

The paper argues the null likely reflects an omitted variable: occupational flexibility. Mothers may self-select into lower-paying but more flexible jobs, a mechanism that would bias the depreciation coefficient downward (making it appear less negative than the true effect). The cross-sectional Mroz data cannot capture this sorting, which requires panel data with occupation-switching information. The husband's wage correlation (2.3%, p=0.03) likely reflects assortative mating rather than a causal household production effect.

---

## Portfolio Website

**[Live Site](https://aahan-desai.vercel.app)**

A single-page portfolio built with Next.js 16, React 19, TypeScript, Tailwind CSS, and Framer Motion. Deployed on Vercel. Built during Lab 25 (AI Literacy) using Claude Code CLI to practice AI-assisted development and prompt engineering for code generation.

The site showcases professional experience (Bevi, CENTA, Graphene AI), technical projects (including Oil Shock Radar and the Mroz econometric paper from this course), skills across ML/data/product, wildlife photography and conservation work, and the AeroNU rocketry project. Design uses a dark charcoal palette with copper accents, Playfair Display and DM Sans typography, and a subtle grain overlay. A Ken Burns animation on the hero section uses the user's own wildlife photography.

---

## Lab Progression

The labs follow a deliberate arc: foundational statistics, then causal inference, then ML methods, then advanced applications. Each lab begins with an economic question, not a technique.

### Foundations (Labs 1-5)

| Lab | Topic | Core Idea |
|-----|-------|-----------|
| 1 | **Global PPP via the Big Mac Index** | Tests the Law of One Price empirically. Calculates implied PPP exchange rates and quantifies currency misalignment across countries. |
| 2 | **The Illusion of Growth (FRED)** | Deflates nominal U.S. wages for inflation and composition effects. Reveals the 2020 "Pandemic Paradox" where apparent wage surges were statistical artifacts from low-wage workers exiting the labor force, not structural gains. |
| 3 | **Statistical Foundations** | Core statistical computing and data manipulation. |
| 4 | **Robust Descriptive Statistics** | Demonstrates how the mean misleads in skewed distributions (California Housing). Compares IQR-based outlier detection with Isolation Forest, and contrasts non-robust (mean, SD) vs. robust (median, MAD) summaries. |
| 5 | **Probability as Prediction Engine** | Law of Large Numbers, Monty Hall conditional probability, and Monte Carlo revenue risk simulation for SaaS forecasting. Connects probability distributions to business decision-making. |

### Causal Inference & Estimation (Labs 7-14)

| Lab | Topic | Core Idea |
|-----|-------|-----------|
| 7 | **Estimation: Formulas to Bootstrapping** | Moves from closed-form standard errors to simulation-based inference. Constructs bootstrap confidence intervals and empirical sampling distributions through resampling. |
| 8 | **Hypothesis Testing & Falsification** | Operationalizes the scientific method on the Lalonde experimental dataset. Combines parametric (Welch's T-Test) with non-parametric (permutation testing) to adjudicate whether job training earnings lift is real or noise. |
| 9 | **Propensity Score Matching** | Recovers causal structure from observational data by correcting selection bias. Nearest-neighbor matching on logistic propensity scores transforms severely biased observational estimates into estimates matching the experimental benchmark. |
| 10 | **Spurious Correlation & Multicollinearity** | Investigates misleading correlations in macroeconomic time-series (FRED). Quantifies multicollinearity with VIF, transforms to stationarity via YoY growth rates, and uses DAGs for causal reasoning. |
| 11 | **Data Wrangling Pipeline** | Context-aware imputation, categorical encoding, preventing the dummy variable trap, and high-cardinality feature engineering with Target Encoding. |
| 12 | **Building the Prediction Engine** | Deploys a multivariate OLS model for real estate valuation. Implements train-test framework and evaluates out-of-sample RMSE in dollar terms, bridging econometric explanation with practical prediction. |
| 13 | **Dimensionality & the FWL Theorem** | Hedonic pricing model validated by the Frisch-Waugh-Lovell theorem. Demonstrates Omitted Variable Bias through intentional exclusion experiments and verifies that residualized regression produces exact coefficient equivalence with the full model. |
| 14 | **When OLS Fails (AI Capex Diagnostics)** | Diagnoses heteroscedasticity and multicollinearity in AI infrastructure capital expenditure data. Applies HC3 robust standard errors to restore valid inference. |

### Machine Learning Methods (Labs 15-19)

| Lab | Topic | Core Idea |
|-----|-------|-----------|
| 15 | **The Polynomial Trap (Bias-Variance)** | Systematic polynomial regression on synthetic and Ames Housing data. Shows why training error misleads for model selection and how cross-validation identifies optimal complexity. |
| 16 | **Regularization (Ridge & Lasso)** | Compares Ridge and Lasso against unregularized OLS. Cross-validation for lambda selection. Demonstrates Lasso's automatic feature selection and how regularization improves out-of-sample generalization. |
| 17 | **Logistic Regression** | Explains why Linear Probability Models produce invalid predictions outside [0,1]. Fits logistic regression with interpretable odds ratios and the sigmoid's natural probability bounding. |
| 18 | **Fraud Detection & Evaluation Metrics** | Evaluates logistic regression on severely imbalanced data. Moves beyond accuracy to confusion matrices, ROC-AUC, PR-AUC, and cost-sensitive threshold optimization under operational constraints (max daily investigations). Deploys an interactive Streamlit dashboard. |
| 19 | **Random Forests** | Compares Decision Tree, Ridge, and Random Forest on California Housing. Tunes via GridSearchCV. Extracts Mean Decrease Impurity and permutation importance. Visualizes partial dependence plots showing non-linear feature effects. |

### Advanced Applications (Labs 22-25)

| Lab | Topic | Core Idea |
|-----|-------|-----------|
| 22 | **Clustering World Economies (K-Means & PCA)** | Unsupervised learning on 10 World Bank macro-development indicators. Elbow Method and Silhouette Analysis select K=4. PCA for 2D visualization. Compares algorithmic clusters against traditional World Bank income classifications. |
| 23 | **FedSpeak NLP on FOMC Minutes** | TF-IDF document-term matrix on Federal Reserve meeting minutes. Loughran-McDonald financial sentiment lexicon. PCA + K-Means identifies distinct communication "regimes." Reveals structural regime change post-COVID with elevated uncertainty language. |
| 24 | **Causal ML: Double Machine Learning** | Estimates the causal effect of 401(k) eligibility on household net financial assets using double/debiased ML. Demonstrates how naive LASSO shrinks treatment coefficients toward zero, motivating the Partially Linear Regression design with Random Forest nuisance learners and 5-fold cross-fitting. Estimates CATEs by income quartile. |
| 25 | **AI Literacy & Portfolio Deployment** | Builds the portfolio website using Claude Code CLI. Practices prompt engineering for code generation. Deploys a live Next.js application via Vercel. |

---

## Assignments

| Assignment | Topic | Core Idea |
|------------|-------|-----------|
| 2 | **Deconstructing Statistical Lies** | Four biases: latency skew (SD inflates 62x vs. MAD with outliers), the false positive paradox (98% accurate classifiers yield 95% false positives in low-prevalence settings), survivorship bias (analyzing only successful crypto tokens inflates expected returns 31x), and sample ratio mismatch detection in A/B tests. |
| 3 | **The Causal Architecture** | Bootstrap CI for skewed medians, permutation testing for A/B experiments, and propensity score matching on real e-commerce data with Love plots showing covariate imbalance reduction. |
| 5 | **The Sovereign Risk Engine** | Four-phase IMF early warning system. Phase 1: regularization diagnostics (OLS vs Ridge vs Lasso). Phase 2: LPM failure vs logistic regression. Phase 3: accuracy paradox, confusion matrix, ROC/PR curves, threshold optimization. Phase 4: bootstrap feature stability and cost-sensitive thresholds. Predicts sovereign growth crises in emerging markets using World Bank indicators. |

---

## Tech Stack

- **Python**, **Pandas**, **NumPy**, **Scikit-learn**, **Statsmodels**
- **Streamlit** (dashboards for Labs 18, Final Project)
- **Next.js / React / TypeScript / Tailwind CSS** (portfolio site)
- **Google Colab** (lab notebooks)
- **FRED API**, **World Bank API**, **yfinance**, **NYT RSS** (data sources)
- **Vercel** (deployment)
