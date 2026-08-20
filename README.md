# Logistics Data Analytics — Route Optimization & Inventory Management

A data science project analyzing and improving operations for a mid-size e-commerce
logistics network: **demand forecasting**, **delivery zone segmentation**, and
**route optimization**, built in Python.

This repo implements the roadmap defined in [`docs/Week1_Strategic_Planning.md`](docs/Week1_Strategic_Planning.md)
(Week 1 deliverable: strategic planning and data exploration).

## Project Scenario

A logistics provider operates 5 regional warehouses serving last-mile deliveries
across a metro area via a fleet of 40–60 vehicles. The project targets three
KPIs:

| KPI | Definition | Formula |
|---|---|---|
| On-Time Delivery Rate (OTDR) | % of orders delivered within the promised window | `on_time_orders / total_orders × 100` |
| Inventory Turnover Ratio | Stock efficiency per warehouse | `cogs / average_inventory_value` |
| Cost per Delivery (CPD) | Avg. operational cost per delivery | `total_delivery_cost / num_deliveries` |

## Repository Structure

```
logistics-analytics/
├── data/
│   ├── raw/                # Original, unmodified source data (gitignored)
│   └── processed/          # Cleaned & preprocessed datasets (gitignored)
├── docs/
│   ├── Week1_Strategic_Planning.md / .docx      # Week 1 report
│   └── Week2_Data_Cleaning_Preprocessing.md / .docx   # Week 2 report
├── notebooks/
│   └── 01_eda.ipynb        # Exploratory data analysis
├── src/
│   ├── __init__.py
│   ├── data_cleaning.py    # Load & clean raw order/shipment data
│   ├── preprocessing.py    # Outlier detection & normalization (Week 2)
│   ├── demand_forecasting.py   # Regression-based demand forecasting
│   ├── zone_clustering.py      # K-Means delivery zone segmentation
│   └── route_optimization.py   # VRP-based route planning
├── tests/
│   ├── test_data_cleaning.py
│   └── test_preprocessing.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone and set up the environment

```bash
git clone https://github.com/<your-username>/logistics-analytics.git
cd logistics-analytics
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Add data

Place raw order/shipment CSVs in `data/raw/`. Suggested public sources:

- [Kaggle: Supply Chain Shipment Pricing Data](https://www.kaggle.com/)
- [Kaggle: Online Retail II](https://www.kaggle.com/)
- [Amazon Last Mile Routing Research Challenge](https://registry.opendata.aws/)

### 3. Run the pipeline

```bash
python -m src.data_cleaning
python -m src.preprocessing
python -m src.demand_forecasting
python -m src.zone_clustering
python -m src.route_optimization
```

Or explore interactively via `notebooks/01_eda.ipynb`.

### 4. Run tests

```bash
pytest tests/
```

## Roadmap

- [x] Week 1 — Strategic planning, KPI definition, data research
- [x] Week 2 — Data collection, cleaning & preprocessing pipeline (outlier handling, normalization)
- [ ] Week 3 — Exploratory data analysis
- [ ] Week 4 — Demand forecasting model
- [ ] Week 5 — Zone clustering & route optimization
- [ ] Week 6 — Evaluation, reporting & final presentation

## License

MIT — see [LICENSE](LICENSE).
