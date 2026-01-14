# The Illusion of Growth & the Composition Effect  
### Deflating History with FRED

## Objective
To analyze long-run U.S. wage dynamics by correcting nominal wage growth for inflation and labor-market composition effects, and to distinguish genuine real wage growth from statistical artifacts.


## Methodology
- Built a Python-based data pipeline to ingest **live macroeconomic time series** from the Federal Reserve Economic Data (FRED) API.  
- Retrieved nominal wage data (Average Hourly Earnings, AHETPI) and consumer price data to compute **real wages** and evaluate long-term purchasing power trends.  
- Identified a structural anomaly in 2020—commonly interpreted as a wage boom—and tested whether it reflected true labor market strength.  
- Fetched the **Employment Cost Index (ECI)** to control for the **composition effect**, isolating wage changes from shifts in workforce demographics.  
- Used visualization and time-series analysis to compare nominal wages, real wages, and composition-adjusted compensation.


## Key Findings
- Over the period **1964–2025**, nominal wages increased by **+1170.4%**, while real wages rose by **+953.7%**, indicating that **inflation absorbed approximately 216.7% of nominal gains**.  
- Long-run real wage growth has been uneven, with the **best year in 1973 (+1.81%)** and the **worst year in 2008 (–1.77%)**, highlighting the cyclical vulnerability of worker purchasing power.  
- Despite persistent narratives of stagnation, real wages increased by **+24.42% over the last five years**, reaching an **all-time high purchasing power** of **$326.03** in 2025.  
- Periods of near-stagnation remain evident, including **14 consecutive months of real wage growth below 0.5% annually**, underscoring slow diffusion of productivity gains.  
- The apparent wage surge in 2020 represents a **Pandemic Paradox**:  
  - Nominal and real wages spiked as low-wage workers disproportionately exited the labor force.  
  - Composition-adjusted measures (ECI) show no comparable increase, confirming that the observed “wage boom” was **statistical rather than structural**.  
- This analysis demonstrates the **money illusion** and reinforces the necessity of adjusting for inflation and labor composition when interpreting wage data.


## Economic Insight
This project illustrates why macroeconomic narratives based solely on nominal indicators can be misleading. Correcting for both inflation and workforce composition reveals a more accurate picture of wage dynamics—one in which long-run gains exist, but are modest, uneven, and frequently obscured by statistical distortions.

