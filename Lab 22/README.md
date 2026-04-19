# Clustering World Economies with K-Means & PCA

**Objective:** To uncover latent structural similarities among global economies using unsupervised machine learning, moving beyond traditional univariate GDP-based classifications to capture multi-dimensional development indicators.

## Methodology
* **Data Acquisition:** Extracted 10 macro-development indicators for approximately 160 nations using the World Bank API (`wbgapi`).
* **Preprocessing:** Standardized the feature space using `StandardScaler` to ensure proportional weighting across diverse metrics (e.g., life expectancy, mortality rates, and enrollment).
* **Cluster Optimization:** Evaluated spatial partitioning for $K=2$ through $K=10$ utilizing Within-Cluster Sum of Squares (Elbow Method) and Silhouette Score analysis to determine the optimal underlying structure.
* **Modeling:** Deployed K-Means clustering with an aggregate $K=4$ constraint to segment the global economic landscape.
* **Dimensionality Reduction:** Executed Principal Component Analysis (PCA) to project the high-dimensional feature set onto a 2D plane for visual cluster interpretation.
* **Validation & Comparison:** Cross-tabulated algorithmic cluster assignments against established World Bank income classifications to assess heuristic alignment. 
* **Pipeline Extension:** Validated the robustness and generalization of the spatial clustering architecture by applying the identical model flow to California housing census tract data.

## Key Findings
* **Optimal Topology:** Silhouette and inertia diagnostics indicated $K=4$ as an effective partition point, distinguishing distinct tiers of global infrastructural and economic development.
* **Classification Alignment:** The K-Means clusters demonstrated strong, yet imperfect, correlation with traditional World Bank income brackets. Mismatches effectively isolated nations whose broader developmental indicators (e.g., health and education constraints) deviate from their raw macroeconomic GDP trajectory.
* **Pipeline Generalizability:** The successful deployment of the same normalization, clustering, and PCA visualization stack on the California housing dataset confirmed the pipeline’s structural versatility for varied geospatial use cases.