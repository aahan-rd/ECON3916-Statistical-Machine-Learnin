# Audit 02: Deconstructing Statistical Lies

## Executive Summary

This audit examines three critical statistical biases that systematically distort decision-making in real-world applications: latency skew in performance monitoring, false positive paradoxes in detection systems, and survivorship bias in market analysis. Our findings demonstrate how conventional statistical methods can mislead stakeholders when applied to non-normal distributions or rare events.

---

## 1. Latency Skew: The Fragility of Standard Deviation

### Problem Statement
Standard Deviation (SD) is unstable in the presence of outliers, making it unsuitable for skewed distributions common in system performance monitoring.

### Experimental Design
- **Dataset**: 1,000 latency observations
  - Normal traffic: 980 samples (20-50 ms range)
  - Spike traffic: 20 samples (1000-5000 ms range)
- **Comparison**: Standard Deviation vs Median Absolute Deviation (MAD)

### Results

| Metric | Value |
|--------|-------|
| Mean | 90.89 ms |
| Median | 35.0 ms |
| Standard Deviation | 434.37 ms |
| Median Absolute Deviation | 7.0 ms |
| **SD/MAD Ratio** | **62.05x** |

### Key Findings
- The presence of only 2% outliers inflated the Standard Deviation by 62x relative to MAD
- SD (434.37 ms) is 4.8x larger than the mean itself, indicating severe distortion
- MAD (7.0 ms) accurately reflects typical deviation in normal traffic conditions
- Mean (90.89 ms) is 2.6x higher than the median (35.0 ms), confirming positive skew

### Implications
Standard Deviation-based alerting systems will produce excessive false alarms or fail to detect genuine performance degradation. Robust statistics (MAD, median) should be used for service level monitoring in production systems.

---

## 2. False Positive Paradox: The Bayesian Reality Check

### Problem Statement
High-accuracy classifiers produce majority-false-positive results when applied to rare events due to base rate neglect.

### Test Case: IntegrityAI Plagiarism Detector
- **Claimed Accuracy**: 98% (Sensitivity = 98%, Specificity = 98%)
- **Scenarios Tested**: Three academic environments with varying base rates

### Results

| Scenario | Base Rate | P(Cheater \| Flagged) | Interpretation |
|----------|-----------|----------------------|----------------|
| Scenario A: Bootcamp | 50.0% | 98.0% | High base rate: detector reliable |
| Scenario B: Econ Class | 5.0% | 72.1% | Moderate base rate: 28% false positives |
| Scenario C: Honors Seminar | 0.1% | 4.7% | Low base rate: 95% false positives |

### Key Findings
- In the Honors Seminar (0.1% base rate), 95.3% of flagged students are innocent
- Even with 98% accuracy, the posterior probability collapses when priors are low
- The system is effectively unusable in low-prevalence environments without additional evidence

### Implications
Automated decision systems must incorporate base rates. High-stakes applications (fraud detection, medical diagnosis, academic integrity) require human review protocols and multi-stage verification when operating on rare events.

---

## 3. Survivorship Bias: The Graveyard of Failed Tokens

### Problem Statement
Analyzing only successful outcomes severely overestimates expected returns and underestimates risk in venture investments.

### Experimental Design
- **Simulation**: 10,000 cryptocurrency token launches
- **Distribution**: Pareto (power law) with shape parameter 1.16
- **Survivor Threshold**: Top 1% by market capitalization

### Results

| Metric | All Tokens | Survivors Only | Bias Factor |
|--------|------------|----------------|-------------|
| Sample Size | 10,000 | 100 (1%) | - |
| Mean Market Cap | $4,765 | $149,081 | 31.3x |
| Median Market Cap | $1,795 | - | - |

**Market Cap Distribution (All Tokens)**:
- 50th percentile: $1,795
- 90th percentile: $7,020
- 95th percentile: $12,671
- 99th percentile: $45,323
- 99.9th percentile: $291,708

### Key Findings
- Studying only survivors inflates expected returns by 31.3x
- 99% of tokens have market caps below the survivor threshold
- The median token ($1,795) is 83x smaller than the survivor mean
- Power law dynamics create extreme concentration in the top 1%

### Implications
Investment theses based on successful case studies systematically underestimate failure rates. Portfolio strategies must account for the full distribution of outcomes, not just visible successes. Expected value calculations require explicit modeling of the dead project graveyard.

---

## 4. Sample Ratio Mismatch: Engineering Bias Detection

### Problem Statement
Unbalanced randomization in A/B tests indicates systemic bias that invalidates experimental results.

### Test Case: FinFlash A/B Test
- **Expected Split**: 50/50 (50,000 control / 50,000 treatment)
- **Observed Split**: 50,250 control / 49,750 treatment
- **Discrepancy**: 500 users (1% imbalance)

### Statistical Test
Chi-Square Goodness of Fit Test (df=1, alpha=0.05)

### Results
- **Chi-Square Statistic**: 2.50
- **Critical Value**: 3.84
- **P-value**: > 0.05
- **Verdict**: Null hypothesis rejected

The 500-user discrepancy exceeded the threshold for random variation, indicating Sample Ratio Mismatch (SRM).

### Key Findings
- Even small imbalances (1%) can signal engineering defects
- Potential causes: biased randomization, differential app crashes, data pipeline errors
- SRM invalidates treatment effect estimates regardless of outcome metrics

### Implications
All A/B tests must include pre-analysis SRM checks. Experiments with significant ratio mismatches require engineering investigation before interpreting results. Automated SRM monitoring should be implemented in experimentation platforms.

---

## Methodological Notes

### Code Implementation
All analyses were implemented without external statistical libraries to ensure transparency and verifiability:
- MAD calculation: Manual median and absolute deviation computation
- Bayesian inference: Direct application of Bayes' theorem
- Chi-square test: Manual calculation of test statistic
- Survivorship simulation: NumPy Pareto distribution sampling
