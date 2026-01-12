# Global Purchasing Power Parity Analysis via the Big Mac Index

## Objective
To empirically test the **Law of One Price** by using the Big Mac Index to evaluate whether exchange rates correctly reflect relative price levels across countries.

## Methodology
- Collected raw Big Mac price data across countries using **The Economist’s 2015 Big Mac Index**, manually structured into Python dictionaries.  
- Calculated **implied Purchasing Power Parity (PPP) exchange rates** by comparing local Big Mac prices to the U.S. benchmark price.  
- Computed **currency misalignment** by comparing implied PPP exchange rates to observed market exchange rates.  
- Quantified the degree of **overvaluation or undervaluation** of each currency relative to the U.S. dollar.

## Key Findings
- The majority of currencies in the sample were **undervalued relative to the U.S. dollar**, indicating that Big Macs were cheaper abroad when converted at prevailing market exchange rates.  
- **Russia, South Africa, Indonesia, and Egypt** exhibited the largest **undervaluations**, suggesting substantial deviations from PPP and highlighting the role of lower labor costs, domestic pricing structures, and limited arbitrage.  
- Major Asian economies such as **China, Hong Kong, Japan, and South Korea** were also undervalued, though to a lesser extent, reflecting persistent price level differences despite integration into global trade.  
- **Argentina, Mexico, and the Philippines** showed moderate undervaluation, consistent with macroeconomic instability, capital controls, or inflation differentials affecting exchange rate alignment.  
- Currencies in advanced economies such as the **Euro Area, Australia, and Britain** were close to parity but still slightly undervalued, suggesting partial convergence toward PPP without full price equalization.  
- In contrast, **Norway** stood out as significantly **overvalued**, implying that domestic prices were substantially higher than U.S. price levels, likely due to high wages, strong purchasing power, and non-tradable costs.  
- **Brazil** also displayed mild overvaluation, diverging from the broader pattern of emerging-market undervaluation.  
- Overall, the results demonstrate that while PPP provides a useful long-run benchmark, **short-run exchange rates are heavily influenced by structural factors, market frictions, and non-tradable goods**, limiting the effectiveness of pure arbitrage in equalizing prices globally.
