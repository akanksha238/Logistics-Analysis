# Data Collection, Cleaning, and Preprocessing for Logistics Analysis

**Week 2 Task — Data Science Internship**
**Dataset:** Regional E-Commerce Logistics Orders & Shipment Records

> The formatted Word version of this report is available as a project deliverable
> ([`Week2_Data_Cleaning_Preprocessing.docx`](Week2_Data_Cleaning_Preprocessing.docx));
> this Markdown copy lives alongside the code for easy in-repo reference.

## Executive Summary

This report documents the data collection, cleaning, and preprocessing
pipeline for the logistics analytics project, building on the Week 1
strategic plan. It identifies common data quality issues in logistics order
data — missing values, duplicates, outliers, inconsistent formats, and
unscaled numeric features — and explains the technique used to resolve each,
with working Python code.

## 1. Data Collection Simulation

Simulated using a dataset modeled on public sources (Kaggle Supply Chain
Shipment Pricing Data, Online Retail II, Amazon Last Mile Routing Research
Challenge), representing ~500–5,000 order records over 3–6 months, one row
per order, with warehouse, product, delivery location, and timestamp fields.

## 2. Data Cleaning: Common Issues & Techniques

| Issue | Technique | Why |
|---|---|---|
| Missing values | Drop rows missing critical IDs; median-impute non-critical numerics | Preserves integrity of key fields |
| Duplicate records | `drop_duplicates()` on `order_id` | Prevents double-counting in KPIs |
| Inconsistent formats | `pd.to_datetime()` + string normalization | Reliable date arithmetic & grouping |
| Outliers | IQR-based filtering (1.5× IQR) | Robust to skewed operational data |
| Invalid geocoordinates | Range validation + null-island filtering | Protects clustering/routing inputs |
| Unscaled numeric features | Min-Max normalization | Prevents scale bias in distance-based models |

## 3. Methodology Highlights

- **Missing values**: critical fields (IDs, dates, coordinates) → drop; non-critical numerics → median impute (robust to skew).
- **Outliers**: IQR method preferred over std-dev cutoff since logistics metrics are typically right-skewed. Impossible values (negative cost/time) are removed; statistically extreme-but-plausible values are flagged, not deleted.
- **Normalization**: Min-Max scaling applied only to features feeding distance-based models (K-Means clustering); tree-based models (Random Forest) are scale-invariant and skip this step.

## 4. Code

See implementation in [`src/preprocessing.py`](../src/preprocessing.py), which
extends [`src/data_cleaning.py`](../src/data_cleaning.py) with:

- `flag_outliers_iqr()` — IQR-based outlier detection
- `handle_outliers()` — removes impossible values, flags statistical outliers
- `normalize_features()` — Min-Max scaling for distance-based models
- `preprocess()` — full pipeline entry point

Pipeline order: `data_cleaning.py` → `preprocessing.py` → `demand_forecasting.py` / `zone_clustering.py`

## 5. Reflection

Data quality directly determines the reliability of every downstream KPI and
model in this project. Undetected duplicates inflate demand forecasts and
distort Cost per Delivery; unhandled missing coordinates corrupt route
optimization; unnormalized features bias K-Means clustering toward whichever
feature has the largest numeric range. A rigorous preprocessing pipeline is a
prerequisite for trustworthy logistics analytics.
