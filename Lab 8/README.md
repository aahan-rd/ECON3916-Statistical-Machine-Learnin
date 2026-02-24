# Hypothesis Testing & Causal Evidence Architecture

## The Epistemology of Falsification: Hypothesis Testing on the Lalonde Dataset

---

## Project Overview

This project operationalizes the scientific method in a causal inference setting.  
Rather than focusing purely on estimation, I structured the analysis around **falsification** — testing whether the observed earnings lift from job training could plausibly arise under a null model of no causal effect.

Using the Lalonde (1986) randomized experimental dataset, I adjudicated between competing narratives of causality through formal statistical contradiction.

---

## Objective

The objective was to pivot from point estimation toward **evidence adjudication**:

- Move beyond “What is the estimated effect?”
- Ask instead: “Can the null hypothesis of no treatment effect survive structured statistical attack?”

The Average Treatment Effect (ATE) was treated not as a number to compute, but as a claim to stress-test.

---

## Technical Approach

### Parametric Inference (Signal-to-Noise Architecture)

- Estimated the ATE via difference in means.
- Applied Welch’s T-Test (via SciPy) to account for unequal variances.
- Interpreted the T-statistic as a signal-to-noise ratio.
- Explicitly controlled for Type I error (α = 0.05).

### Non-Parametric Validation (Distribution-Free Testing)

- Conducted a 10,000-resample permutation test.
- Simulated a counterfactual world in which treatment assignment was meaningless.
- Compared empirical p-values against the parametric test to validate robustness under non-normal earnings distributions.

### Epistemic Framing

- Treated p-values as measures of contradiction against the null — not truth metrics.
- Interpreted rejection as structured falsification rather than confirmation.

---

## Key Findings

- Observed Average Treatment Effect: **~$1,795 increase in real earnings (1978)**
- Welch’s T-Test indicated statistical significance at α = 0.05.
- Permutation testing corroborated the parametric inference.

The null hypothesis of no treatment effect was rejected via statistical contradiction.  
Results were consistent across both parametric and non-parametric frameworks.

---

## Business Insight

Rigorous hypothesis testing serves as the **Safety Valve of the Algorithmic Economy**.

In data-rich environments, patterns are easy to manufacture. Without disciplined falsification:

- Spurious correlations masquerade as product insights.
- A/B tests devolve into p-hacking.
- Optimization systems overfit noise.

Hypothesis testing introduces structured skepticism. By controlling Type I errors and validating results across inferential frameworks, we prevent data grubbing and protect signal integrity.

In production-scale systems, this discipline safeguards capital allocation, product strategy, and user trust.

---

# Concept Extension: Return-Aware Experimentation

In industry environments such as Netflix, experimentation is not governed solely by the academic convention of *p < 0.05*. Instead, firms apply **Return-Aware Experimentation** — aligning statistical thresholds with expected business value.

Under this framework:

- A statistically significant result may not justify deployment if expected ROI is low.
- A result that does not meet the 0.05 threshold may still be deployed if upside potential is asymmetric and downside risk is bounded.

Decision thresholds are business parameters, not scientific constants.

Where academia optimizes for error control in abstract inference, production systems optimize for expected utility under uncertainty. Significance levels become adjustable levers in a broader capital allocation architecture.
