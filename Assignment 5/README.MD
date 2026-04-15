# ASSIGNMENT 5 + PHASE 4: THE SOVEREIGN RISK ENGINE
## Complete Implementation Guide (Phases 1-4)

---

## TABLE OF CONTENTS

1. [Overview](#overview)
2. [File Structure](#file-structure)
3. [Phase 1: Regularization (Labs 15-16)](#phase-1-regularization)
4. [Phase 2: Classification (Lab 17)](#phase-2-classification)
5. [Phase 3: Evaluation (Lab 18)](#phase-3-evaluation)
6. [Phase 4: AI Context Engineering (P.R.I.M.E. Framework)](#phase-4-ai-context-engineering)
7. [Setup & Execution](#setup--execution)
8. [Expected Outputs](#expected-outputs)
9. [Troubleshooting](#troubleshooting)

---

## OVERVIEW

This is a complete quantitative macroeconomic early warning system for the IMF. You're building a logistic regression classifier to predict sovereign growth crises using World Bank Development Indicators, then validating it through regularization diagnostics, classification metrics, and cost-sensitive optimization.

**Core Question:** Which emerging-market economies will experience sustained economic contraction (growth < 0%) within the next 5 years?

**Output:** A binary crisis classifier that the IMF can deploy quarterly to allocate emergency assessment missions and lending resources.

**Data Source:** Live download from World Bank API (no CSV files needed)

**Total Runtime:** 5-10 minutes depending on approach

---

## FILE STRUCTURE

```
outputs/
├── 00_START_HERE.txt                    ← Read this first
├── README.md                            ← Quick navigation
├── assignment_5_complete.py             ← All code (Phases 1-3) unified script
├── QUICK_REFERENCE_CELLS.md             ← 13 cells for cell-by-cell execution
├── ASSIGNMENT_5_CELL_GUIDE.md           ← What each cell does + deliverables
├── MASTER_INDEX.md                      ← Complete reference
├── CHEAT_SHEET.md                       ← One-page summary (print this!)
├── RESPONSES_CLEAN.txt                  ← Phase 1-3 written responses
├── PHASE_4_PRIME_PROMPTS.md             ← LLM prompts for Task 4.1 & 4.2
├── TASK_4_1_RESPONSE.txt                ← Bootstrap stability response
├── TASK_4_2_RESPONSE.txt                ← Cost optimization response
└── (this file)                          ← Detailed implementation guide
```

---

## PHASE 1: REGULARIZATION

**Labs Assessed:** Lab 15 (Bias-Variance Tradeoff) + Lab 16 (Ridge/Lasso)

**Objective:** Diagnose OLS overfitting and demonstrate how regularization fixes it.

### Step 1.1: OLS Baseline (Cell 4)

**What it does:**
- Fits OLS LinearRegression on continuous GDP growth outcome
- Computes training R² and test R²
- Calculates p/n ratio (predictors / observations)
- Measures the R² gap (overfitting severity)

**Data flow:**
```
X_train_scaled (84 × 25) → LinearRegression.fit() → OLS coefficients
                            → predict on test → R² scores
```

**Key metrics:**
- Train R²: Should be high (~0.6-0.8)
- Test R²: Should be much lower or negative (proof of overfitting)
- p/n ratio: ~0.3-0.5 (high)
- R² gap: Should be large (>0.4)

**Written response required:** Explain why p/n ratio causes overfitting using bias, variance, degrees of freedom.

---

### Step 1.2: Ridge & Lasso Regularization (Cell 5)

**What it does:**
- Fits RidgeCV with 5-fold cross-validation
- Fits LassoCV with 5-fold cross-validation
- Compares OLS vs Ridge vs Lasso on 6 metrics
- Creates model comparison table

**Data flow:**
```
X_train_scaled → RidgeCV(alphas=logspace(-2,3,50), cv=5) → Ridge model
                                                          ↓
                                                    CV-selected λ*
                                                    Test R² improvement

X_train_scaled → LassoCV(alphas=logspace(-2,3,50), cv=5) → Lasso model
                                                          ↓
                                                    CV-selected λ*
                                                    Non-zero predictors
                                                    Test R² improvement
```

**Model Comparison Table (6 columns):**
- Method: OLS, Ridge, Lasso
- λ*: CV-selected regularization parameter
- Non-zero Predictors: How many features kept (Ridge keeps all, Lasso selects)
- Training R²: Fit quality on training data
- Test R²: Generalization quality (the real test)
- Test RMSE: Prediction error magnitude

**Expected results:**
- Ridge test R²: Better than OLS
- Lasso test R²: Best of the three
- Lasso non-zero: ~8-12 out of 25 (80% reduction)

**Written response required:** Recommend one method for IMF operations, explain bias-variance tradeoff.

---

### Step 1.3: Lasso Path (Cell 6)

**What it does:**
- Computes full Lasso path (coefficients across all λ values)
- Plots coefficient trajectories vs log(λ)
- Identifies first predictor to enter model
- Shows which variables are retained at CV-selected λ*

**Data flow:**
```
X_train_scaled → lasso_path(alphas=logspace(3,-4,100)) → coefficient matrix
                                                        (25 × 100)
                                                        ↓
                            Plot: lines colored by non-zero status
                            Vertical line at CV λ*
                            Identify first entry (highest λ)
```

**Plot specifications:**
- X-axis: log₁₀(λ) from 3 to -4
- Y-axis: Coefficient values
- Blue lines: Predictors with non-zero coef at CV λ*
- Gray lines: Predictors zeroed at CV λ*
- Red dashed vertical: CV-selected λ* marker

**Key insight:** Variables that enter earliest (highest λ) are strongest unconditional predictors.

**Written response required:** Explain conditional predictive redundancy. Why does Lasso zeroing a variable NOT mean it's unimportant?

---

## PHASE 2: CLASSIFICATION

**Lab Assessed:** Lab 17 (Logistic Regression)

**Objective:** Build a binary classifier for crisis prediction. Show why LPM fails and logistic regression succeeds.

### Step 2.1: Linear Probability Model Failure (Cell 7)

**What it does:**
- Fits OLS on binary crisis outcome (crisis = 1 if growth < 0, else 0)
- Uses only Lasso-selected features from Phase 1
- Checks how many predictions fall outside [0,1]
- Demonstrates fundamental impossibility of LPM

**Data flow:**
```
Lasso-selected features (84 × 8-12) + binary crisis labels
    ↓
LinearRegression.fit() on {0, 1} outcome
    ↓
Predict probabilities
    ↓
Count: predictions < 0 and > 1
```

**Expected violations:**
- Some predictions will be negative (e.g., -0.15)
- Some will exceed 1 (e.g., 1.23)
- Typically 5-20% of test set violates bounds

**Why this fails:** Probabilities must satisfy axioms of probability theory. A "-12% chance of crisis" is logically incoherent.

**Written response required:** Explain why invalid probabilities are fundamental, not cosmetic.

---

### Step 2.2: Logistic Regression (Cell 8)

**What it does:**
- Fits LogisticRegression on binary crisis outcome
- Extracts coefficients β and intercept β₀
- Computes odds ratios: OR = exp(β)
- Verifies all probabilities fall in [0,1]
- Creates odds ratios table sorted by magnitude

**Data flow:**
```
Lasso-selected features (84 × 8-12) + binary crisis labels
    ↓
LogisticRegression(max_iter=10000).fit()
    ↓
Extract coefficients β and intercept β₀
    ↓
Compute OR = exp(β) for each predictor
    ↓
Sort by |OR| and display
    ↓
Verify: all predict_proba()[:,1] in [0, 1] ✓
```

**Odds Ratios Table (3 columns):**
- Predictor name
- β (Coefficient)
- OR (Odds Ratio = exp(β))

**Interpretation of OR:**
- OR = 1.50: 1 std increase in X → odds of crisis multiply by 1.50 (50% increase)
- OR = 0.80: 1 std increase in X → odds of crisis multiply by 0.80 (20% decrease, protective)
- OR > 1: Risk factor
- OR < 1: Protective factor

**Expected results:**
- All predicted probabilities in [0.01, 0.99] range
- Mix of risk factors (OR > 1) and protective factors (OR < 1)

**Written response required:** Interpret the strongest OR predictor in plain English for IMF briefing.

---

### Step 2.3: LPM vs. Logistic Visualization (Cell 9)

**What it does:**
- Creates side-by-side comparison plots
- Uses strongest predictor (from odds ratios) on x-axis
- Left panel: LPM with impossible regions shaded orange
- Right panel: Logistic sigmoid curve bounded [0,1]
- Scatters actual crisis outcomes (0/1) on both

**Plot specifications:**

**LEFT PANEL (LPM):**
- Orange shaded region P < 0 (below x-axis)
- Orange shaded region P > 1 (above y=1)
- Red line: LPM linear fit
- Blue scatter: Actual crisis outcomes
- Reference lines at P = 0 and P = 1

**RIGHT PANEL (Logistic):**
- Green sigmoid curve (stays between 0 and 1)
- Blue scatter: Actual crisis outcomes
- Reference lines at P = 0 and P = 1

**Both panels:**
- X-axis: Strongest predictor (standardized)
- Y-axis: Predicted probability of crisis

**Key visual insight:** LPM line shoots off the probability scale; logistic curve bounded naturally by sigmoid shape.

---

## PHASE 3: EVALUATION

**Lab Assessed:** Lab 18 (Confusion Matrix, ROC/PR Curves, Threshold Optimization)

**Objective:** Evaluate classifier performance using imbalanced-data appropriate metrics. Optimize threshold for operational constraints.

### Step 3.1: Accuracy Paradox (Cell 10)

**What it does:**
- Calculates accuracy and recall of naïve baseline (always predict "no crisis")
- Calculates accuracy and recall of logistic regression at τ = 0.5
- Computes crisis base rate in test set
- Shows why accuracy misleads in imbalanced data

**Data flow:**
```
y_crisis_test (36 binary labels)
    ↓
Baseline model: y_pred = [0, 0, 0, ..., 0] (all zeros)
    ↓
Accuracy = (correct predictions) / 36
Recall = (caught crises) / (total crises) = 0%
    ↓
Logistic model: y_pred = (y_test_prob_logit >= 0.5).astype(int)
    ↓
Accuracy = (correct predictions) / 36
Recall = (caught crises) / (total crises)
    ↓
Compare accuracies (baseline surprisingly high!)
```

**Expected numbers:**
- Base rate: ~20-30% (crises rare)
- Baseline accuracy: ~70-80% (base rate illusion)
- Baseline recall: 0% (catches no crises)
- Logistic accuracy: ~75-85% (only marginally better)
- Logistic recall: 60-80% (actually useful for early warning)

**Written response required:** Explain accuracy paradox: why high accuracy can be misleading in imbalanced data.

---

### Step 3.2: Confusion Matrix & Classification Report (Cell 11)

**What it does:**
- Computes confusion matrix at default threshold τ = 0.5
- Displays as heatmap with ConfusionMatrixDisplay
- Generates sklearn classification_report
- Extracts and prints TP, FN, FP, TN counts

**Data flow:**
```
y_crisis_test (true labels) vs y_pred (predictions at τ=0.5)
    ↓
confusion_matrix(y_crisis_test, y_pred, labels=[0, 1])
    ↓
Returns: [[TN, FP], [FN, TP]]
    ↓
Plot as heatmap
Print classification_report with precision, recall, F1 per class
```

**Confusion Matrix (2×2):**
```
              Predicted No   Predicted Yes
Actual No     TN            FP
Actual Yes    FN            TP
```

**Classification Report (per class):**
- Precision: TP / (TP + FP) = "when we predict crisis, how often right?"
- Recall: TP / (TP + FN) = "of all actual crises, how many do we catch?"
- F1-score: Harmonic mean of precision and recall
- Support: Number of samples in each class

**Expected numbers (at τ=0.5):**
- TP: 3-8 (caught some crises)
- FN: 1-5 (missed some crises)
- FP: 3-10 (false alarms)
- TN: 20-28 (correct non-crisis calls)

**Written response required:** Explain cost asymmetry (FN >> FP in cost). Which metric matters more?

---

### Step 3.3: ROC & Precision-Recall Curves (Cell 12)

**What it does:**
- Computes ROC curve (TPR vs FPR across all thresholds)
- Computes Precision-Recall curve (Precision vs Recall across all thresholds)
- Plots side-by-side
- Calculates ROC-AUC and PR-AUC metrics

**Data flow:**
```
y_crisis_test (true labels) vs y_test_prob_logit (probabilities 0-1)
    ↓
fpr, tpr, _ = roc_curve(y_crisis_test, y_test_prob_logit)
roc_auc = auc(fpr, tpr)
    ↓
precision, recall, _ = precision_recall_curve(y_crisis_test, y_test_prob_logit)
pr_auc = auc(recall, precision)
    ↓
Plot both curves side-by-side
```

**ROC Curve (Left Panel):**
- X-axis: False Positive Rate (FPR) = FP / (FP + TN)
- Y-axis: True Positive Rate (TPR) = TP / (TP + FN)
- Black diagonal: Random classifier (50% accuracy)
- Blue curve: Your logistic regression
- Legend: ROC-AUC value

**Precision-Recall Curve (Right Panel):**
- X-axis: Recall = TP / (TP + FN)
- Y-axis: Precision = TP / (TP + FP)
- Gray horizontal line: Baseline precision = crisis base rate
- Green curve: Your logistic regression
- Legend: PR-AUC value

**Expected values:**
- ROC-AUC: 0.75-0.90 (good classifier)
- PR-AUC: 0.50-0.75 (honest about imbalance)
- ROC-AUC >> PR-AUC (always true in imbalanced data)

**Why ROC-AUC is inflated:** FPR denominator is all non-crises (abundant), so even mediocre models have low FPR, making ROC curve artificially high.

**Why PR-AUC is honest:** Only cares about the minority class (crises); penalizes false alarms directly through precision.

**Written response required:** Explain why ROC-AUC >> PR-AUC. Which curve is more informative for IMF?

---

### Step 3.4: Threshold Analysis (Cell 13)

**What it does:**
- Sweeps probability thresholds τ from 0.01 to 0.99 in 0.01 steps
- For each τ:
  - Counts countries flagged (probability ≥ τ)
  - Computes Precision, Recall, F1
- Finds capacity-constrained threshold (≤5 countries flagged)
- Finds F1-optimal threshold (maximizes F1)
- Plots Precision, Recall, F1 vs τ
- Writes final memo to Division Chief

**Data flow:**
```
y_test_prob_logit (36 probabilities)
    ↓
FOR τ in [0.01, 0.02, ..., 0.99]:
    y_pred = (y_test_prob_logit >= τ)
    num_flagged = sum(y_pred)
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    f1 = 2 * (precision * recall) / (precision + recall)
    ↓
    Store results
    ↓
    
Find capacity_tau: lowest τ where num_flagged ≤ 5
Find f1_tau: τ that maximizes F1
    ↓
Plot Precision (red), Recall (green), F1 (blue) vs τ
Mark capacity_tau (orange dashed vertical line)
Mark f1_tau (purple dashed vertical line)
```

**Threshold Tradeoff:**
- Low τ (aggressive): Catch more crises (high recall), more false alarms (low precision)
- High τ (conservative): Few false alarms (high precision), miss crises (low recall)

**Capacity-constrained threshold:**
- Definition: Lowest τ that flags ≤ 5 countries per quarter
- Respects operational constraint (5-mission emergency capacity)
- Recall: How many crises actually caught
- Trade-off: Some crises missed to stay within budget

**F1-optimal threshold:**
- Definition: τ that maximizes F1 = 2(precision × recall)/(precision + recall)
- Balances precision and recall equally
- Ignores operational constraints and cost asymmetry
- May flag more countries than IMF can assess

**Expected results:**
- Capacity-constrained τ: ~0.35-0.60 (medium confidence)
- F1-optimal τ: Often different from capacity-constrained
- Recall at capacity τ: ~50-75% (realistic expectation)

**Final memo requirements:**
- State threshold recommendation
- Report recall achieved
- Explain in operational terms ("catch X of Y crises, miss Z")
- Acknowledge explicit tradeoff

---

## PHASE 4: AI CONTEXT ENGINEERING

**Framework:** P.R.I.M.E. (Prep, Request, Iterate, Mechanism Check, Evaluate)

**Objective:** Use LLMs to generate advanced diagnostics that extend Phase 1-3 analysis.

### Task 4.1: Bootstrap Feature Selection Stability (LLM-Generated)

**What it does:**
- Runs 200 bootstrap resamples of training data
- Fits LassoCV on each resample
- Records which predictors selected (non-zero coef) in each sample
- Computes selection frequency for each predictor
- Creates horizontal bar chart ranking by stability

**Data flow:**
```
X_train_scaled (84 × 25) + y_cont_train
    ↓
FOR i in 1:200:
    Bootstrap resample with replacement → X_boot, y_boot
    LassoCV(alphas=logspace(-2,3,50), cv=5).fit(X_boot, y_boot)
    Record non-zero coefficients
    ↓
    
Compute selection_frequency[predictor] = count / 200
    ↓
Plot horizontal bars sorted by frequency
Add reference lines at 50% and 80%
```

**How to generate code:**
1. Copy the P.R.I.M.E. prompt from PHASE_4_PRIME_PROMPTS.md (Task 4.1 section)
2. Paste into Claude, ChatGPT, or other LLM
3. LLM generates Python code
4. Copy generated code into Colab cell
5. Run with your X_train_scaled, y_cont_train, feature_names

**Expected output:**
- Horizontal bar chart with predictors sorted by selection frequency
- Stability categories:
  - Stable: >80% selected (core economic signals)
  - Moderate: 50-80% selected (important but correlated)
  - Fragile: <50% selected (redundant with other indicators)
- Table with frequencies and categories

**Interpretation:**
- High frequency: Predictor is unconditional signal, independent of sample
- Low frequency: Predictor is conditionally redundant, swaps with correlates in bootstrap samples
- Shows which pairs of WDI indicators measure similar phenomena

**Written response (2-3 sentences):**
Identify stable predictors (>80%), fragile predictors (<50%). Explain what selection instability reveals about correlation structure of WDI indicators.

---

### Task 4.2: Cost-Sensitive Threshold Optimization (LLM-Generated)

**What it does:**
- Sweeps probability thresholds τ from 0.01 to 0.99
- At each τ, computes expected cost:
  - FN cost: $50 billion per missed crisis (contagion damage)
  - FP cost: $2 million per false alarm (staff time + credibility)
  - Total = FN × $50B + FP × $2M
- Plots cost curve
- Identifies cost-minimizing threshold
- Compares to F1-optimal and capacity-constrained from Phase 3

**Data flow:**
```
y_crisis_test (true labels) + y_test_prob_logit (predicted probabilities)
    ↓
FOR τ in [0.01, 0.02, ..., 0.99]:
    y_pred = (y_test_prob_logit >= τ)
    Compute confusion matrix: TP, FN, FP, TN
    total_cost = FN × $50_000_000_000 + FP × $2_000_000
    ↓
Plot cost vs τ
Mark minimum cost point
```

**How to generate code:**
1. Copy the P.R.I.M.E. prompt from PHASE_4_PRIME_PROMPTS.md (Task 4.2 section)
2. Paste into Claude, ChatGPT, or other LLM
3. LLM generates Python code
4. Copy generated code into Colab cell
5. Run with your y_crisis_test, y_test_prob_logit

**Expected output:**
- Line plot showing expected cost (billions USD) vs threshold
- Cost curve typically U-shaped or increasing
- Red dot marking cost-minimizing threshold
- Table showing threshold, FN, FP, cost for top rows

**Key insight:**
- Cost-minimizing τ will be MUCH LOWER than F1-optimal
- Reason: $50B per FN >> $2M per FP, so system favors recall
- Example from your data: τ = 0.03 (vs F1-optimal might be 0.25)

**Why thresholds differ:**

| Threshold Type | Optimizes | Constraint | Typical τ |
|---|---|---|---|
| F1-optimal | Precision × Recall balance | None | 0.25-0.50 |
| Capacity-constrained | Recall given 5-mission limit | Budget (5 countries/quarter) | 0.35-0.60 |
| Cost-minimizing | Expected financial loss | Cost asymmetry ($50B vs $2M) | 0.01-0.10 |

**Written response (2-3 sentences):**
State cost-minimizing τ and total cost. Explain why it differs from other thresholds (cost asymmetry penalizes FN heavily). Recommend which threshold and why.

---

## SETUP & EXECUTION

### Option 1: Run Everything in One Cell (Fastest)

**Time: 5 minutes**

1. Open Google Colab
2. Create new notebook
3. Open `assignment_5_complete.py` from outputs folder
4. Copy entire file (Ctrl+A, Ctrl+C)
5. Paste into single Colab cell (Ctrl+V)
6. Run cell (Shift+Enter)
7. Wait 2-3 minutes for World Bank API download
8. All outputs appear automatically

**Pros:** Fast, everything in order
**Cons:** Harder to debug if error occurs

---

### Option 2: Run Cell-by-Cell (Recommended for Learning)

**Time: 15 minutes**

1. Open Google Colab
2. Create new notebook
3. Open `QUICK_REFERENCE_CELLS.md` from outputs folder
4. For each CELL 0 through CELL 13:
   - Copy cell code block (between dashed lines)
   - Create new Colab cell
   - Paste code
   - Run (Shift+Enter)
   - Observe outputs before moving to next cell

5. For Phase 4 (Tasks 4.1 and 4.2):
   - Open `PHASE_4_PRIME_PROMPTS.md`
   - Copy Task 4.1 P.R.I.M.E. prompt
   - Paste into Claude/ChatGPT
   - Copy generated code into new Colab cell
   - Run
   - Repeat for Task 4.2

**Pros:** Understand flow, easy to debug, see each transformation
**Cons:** More typing, longer execution

---

### Option 3: Hybrid (Best of Both)

**Time: 20 minutes**

1. Run Option 1 to see final outputs
2. Then run Option 2 to understand reasoning
3. Use guides (ASSIGNMENT_5_CELL_GUIDE.md, MASTER_INDEX.md) to explain each step

---

## EXPECTED OUTPUTS

### Phase 1-3 (13 cells from assignment_5_complete.py):

**7 Plots:**
1. Lasso path: Coefficient trajectories vs log(λ), colored by non-zero status
2. LPM vs Logistic: Side-by-side showing bounded probabilities
3. Confusion matrix: Heatmap showing TP, FN, FP, TN at τ=0.5
4. ROC curve: TPR vs FPR, marked with AUC value
5. Precision-Recall curve: Precision vs Recall, marked with AUC value
6. Threshold analysis: Three lines (Precision, Recall, F1) vs τ, marked thresholds
7. (Plus diagnostic prints and tables)

**3 Tables:**
1. Model comparison: OLS, Ridge, Lasso with 6 metrics each
2. Odds ratios: Predictor names, β coefficients, OR values sorted by magnitude
3. Threshold results: τ, FN, FP, Precision, Recall, F1, cost

**10 Written Responses:**
- Step 1.1: OLS overfitting explanation
- Step 1.2: Regularization recommendation
- Step 1.3: Lasso interpretation (conditional redundancy)
- Step 2.1: LPM failure explanation
- Step 2.2: Odds ratio interpretation
- Step 3.1: Accuracy paradox explanation
- Step 3.2: Cost asymmetry (FN vs FP)
- Step 3.3: ROC vs PR curves
- Step 3.4: Final memo to Division Chief

**1 Final Memo:** Threshold recommendation with recall, tradeoff statement

---

### Phase 4 (2 LLM-generated tasks):

**4 Additional Outputs:**
1. Bootstrap feature stability bar chart (Task 4.1)
2. Feature stability table with categories (Task 4.1)
3. Cost-minimizing threshold line plot (Task 4.2)
4. Cost table with minimum marked (Task 4.2)

**2 Additional Written Responses:**
- Task 4.1: Bootstrap stability interpretation
- Task 4.2: Cost-minimizing recommendation vs other thresholds

---

## DATA SHAPES & DIMENSIONS

```
World Bank API download:
  ~150 countries × 30+ indicators × 7 years

After aggregation (2013-2019 mean):
  ~150 countries × 30 indicators

After cleaning (drop >40% missing):
  ~120-130 countries × 25-30 indicators

After median imputation:
  ~120-130 countries × 25-30 indicators (no NaNs)

Train-test split (70-30):
  Train: ~84 countries × 25-30 features
  Test: ~36 countries × 25-30 features

After Lasso selection:
  Train: ~84 countries × 8-12 features (80% reduction)
  Test: ~36 countries × 8-12 features

Crisis outcome (binary):
  ~20-30% positive class (crises are rare)
  ~70-80% negative class (no crisis)
```

---

## KEY PARAMETERS

**World Bank API:**
- Time period: 2013-2019 (pre-COVID)
- Minimum data completeness: 60% (drop >40% missing)
- Imputation: Median by indicator

**Train-Test Split:**
- Ratio: 70% train, 30% test
- Random state: 42 (reproducibility)
- Stratification: No (regression, not classification)
- Standardization: StandardScaler fit on train only

**Lasso Path:**
- Alpha grid: logspace(-2, 3, 50) for LassoCV
- CV folds: 5
- Path computation: logspace(3, -4, 100) (wider range)

**Logistic Regression:**
- Max iterations: 10000
- Random state: 42

**Bootstrap (Phase 4):**
- Resamples: 200
- Sampling: With replacement
- LassoCV same as original

**Cost Function (Phase 4):**
- Missed crisis (FN): $50 billion
- False alarm (FP): $2 million
- Ratio: 25,000:1

---

## TROUBLESHOOTING

### Error: "World Bank API download fails"
**Cause:** Network timeout or API overload
**Fix:** Rerun Cell 1. The API is idempotent (safe to rerun).
**Alternative:** If fails 3+ times, check internet connection or manually download from https://data.worldbank.org

### Error: "Shape mismatch in Lasso feature selection"
**Cause:** Running Phase 2 before Phase 1 completes
**Fix:** Ensure Cells 1-6 run successfully before Cells 7-9

### Error: "LogisticRegression doesn't converge"
**Cause:** Data quality or regularization too loose
**Fix:** Already handled in code with max_iter=10000. If persists, check feature scaling.

### Plot doesn't appear in Colab
**Cause:** Matplotlib not in interactive mode
**Fix:** Add `%matplotlib inline` at top of first cell

### Wrong number of features in odds ratios table
**Cause:** Lasso-selected features count mismatch
**Fix:** Verify lasso_selected_indices = np.where(np.abs(lasso_cv.coef_) > 1e-10)[0] is correct

### Cost optimization produces unexpected threshold
**Cause:** FP and FN counts at a particular threshold
**Fix:** This is mathematically correct. Verify numbers make sense (e.g., τ=0.03 flags ~36 countries, catches almost all crises)

### P.R.I.M.E. prompt generates code with errors
**Cause:** LLM hallucination or missing context
**Fix:** Feed back error message: "This code has error X. Fix it." Most LLMs self-correct on iteration.

---

## DELIVERABLES CHECKLIST

### Phase 1-3 (required):
- [ ] All 13 cells run without errors
- [ ] 7 plots appear and are readable
- [ ] 3 tables created
- [ ] 10 written responses complete
- [ ] Final memo to Division Chief submitted

### Phase 4 (required):
- [ ] P.R.I.M.E. prompts documented (exact text)
- [ ] Task 4.1 LLM code executed, bootstrap chart appears
- [ ] Task 4.2 LLM code executed, cost curve appears
- [ ] Task 4.1 response (bootstrap stability) written
- [ ] Task 4.2 response (cost minimization) written

### Grading criteria:
- Code runs without errors
- Plots are labeled and readable
- Tables include all required columns
- Written responses show understanding
- Recommendations are justified with data

---

## ADDITIONAL NOTES

**On reproducibility:**
All random seeds set to 42 (numpy.random.seed(42)). Results should be identical across runs if World Bank API returns same data.

**On computational cost:**
- Phases 1-3: ~2-3 minutes (mostly API download)
- Phase 4 Task 4.1: ~1 minute (200 resamples × LassoCV)
- Phase 4 Task 4.2: ~30 seconds (99 threshold sweeps)
- Total: ~5 minutes

**On data privacy:**
All data is public World Bank Development Indicators. No sensitive data involved.

**On threshold recommendations:**
Three valid thresholds:
1. **F1-optimal:** Balances precision/recall statistically
2. **Capacity-constrained:** Respects operational budget (5 missions/quarter)
3. **Cost-minimizing:** Optimizes financial risk ($50B vs $2M)

You can recommend any, but must justify your choice.

---
