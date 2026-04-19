# FedSpeak Analysis — NLP on FOMC Minutes

**Objective:** To systematically quantify shifts in U.S. monetary policy communication over two decades by applying unsupervised machine learning and financial sentiment analysis to Federal Open Market Committee (FOMC) meeting minutes.

## Methodology
* **Text Preprocessing:** Structured raw FOMC transcripts by tokenizing, lemmatizing, parsing out non-alphabetic noise, and removing standard stop words to isolate macroeconomic substance.
* **Feature Engineering:** Constructed a high-dimensional Document-Term Matrix utilizing Term Frequency-Inverse Document Frequency (TF-IDF) scores across both unigrams and bigrams to capture nuanced central bank phrasing.
* **Sentiment Scoring:** Applied the domain-specific Loughran-McDonald financial lexicon to compute precise net sentiment (positive vs. negative) and systemic uncertainty metrics per meeting.
* **Dimensionality Reduction & Clustering:** Deployed Principal Component Analysis (PCA) to compress the sparse TF-IDF feature space, subsequently using K-Means clustering to algorithmically identify distinct structural "regimes" in Fed communication.
* **Time-Series Variation:** Conducted comparative distribution analysis of language patterns prior to and following the exogenous shock of the March 2020 COVID-19 pandemic.

## Key Findings
* **Algorithmic Language Regimes:** Unsupervised K-Means clustering naturally partitioned the minutes into distinct macroeconomic epochs. These text clusters independently tracked major historical transitions, separating "status-quo" baseline periods from acute crisis-management eras (e.g., the Global Financial Crisis). 
* **The Post-COVID Structural Shift:** Statistical distributions revealed a mathematically significant regime change post-March 2020. FedSpeak became structurally more negative and exhibited elevated uncertainty indices compared to the pre-2020 baseline, reflecting the rapid adaptation to unprecedented supply-chain friction, pandemic volatility, and subsequent aggressive tightening cycles.