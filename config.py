"""Central configuration: paths and shared constants used across the project."""

from pathlib import Path

# ---- Paths ---------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
OUTPUTS_DIR = ROOT_DIR / "outputs"
CHARTS_DIR = OUTPUTS_DIR / "charts"
DOCS_DIR = ROOT_DIR / "docs"

DATASET_PATH = DATA_DIR / "logistics_dataset.csv"
EDA_SUMMARY_PATH = OUTPUTS_DIR / "eda_summary.txt"

# Ensure directories exist when the package is imported
for _dir in (DATA_DIR, OUTPUTS_DIR, CHARTS_DIR):
    _dir.mkdir(parents=True, exist_ok=True)

# ---- Simulation parameters -------------------------------------------------
RANDOM_SEED = 42
N_RECORDS = 1200
SIMULATION_START_DATE = "2026-01-01"
SIMULATION_DAYS = 181  # ~6 months

REGIONS = ["North", "South", "East", "West", "Central"]
REGION_WEIGHTS = [0.22, 0.20, 0.18, 0.22, 0.18]

TRANSPORT_MODES = ["Road", "Rail", "Air", "Sea"]
MODE_WEIGHTS = [0.55, 0.15, 0.10, 0.20]

CARRIERS = ["Carrier A", "Carrier B", "Carrier C", "Carrier D"]
CARRIER_WEIGHTS = [0.30, 0.28, 0.22, 0.20]

PRODUCT_CATEGORIES = ["Electronics", "Perishables", "Textiles", "Machinery", "Consumer Goods"]
CATEGORY_WEIGHTS = [0.22, 0.15, 0.20, 0.15, 0.28]

MODE_DISTANCE_BASE = {"Road": 450, "Rail": 900, "Air": 1800, "Sea": 3500}
MODE_DISTANCE_SD = {"Road": 200, "Rail": 350, "Air": 700, "Sea": 1200}

CATEGORY_WEIGHT_BASE = {
    "Electronics": 180, "Perishables": 650, "Textiles": 320,
    "Machinery": 1400, "Consumer Goods": 500,
}

MODE_COST_PER_KM_PER_TON = {"Road": 0.09, "Rail": 0.045, "Air": 0.32, "Sea": 0.02}
MODE_BASE_HANDLING_FEE = {"Road": 25, "Rail": 60, "Air": 120, "Sea": 200}

MODE_SPEED_KMPD = {"Road": 550, "Rail": 700, "Air": 4500, "Sea": 550}
MODE_BASE_DAYS = {"Road": 1.0, "Rail": 1.5, "Air": 0.5, "Sea": 3.0}
MODE_PROMISE_DAYS = {"Road": 3.0, "Rail": 4.5, "Air": 1.5, "Sea": 10.0}

MODE_DAMAGE_PROB = {"Road": 0.02, "Rail": 0.015, "Air": 0.01, "Sea": 0.035}

# ---- Chart styling ----------------------------------------------------------
CHART_PALETTE = ["#2E5090", "#4C9F70", "#E8A33D", "#C0504D", "#7B6FA0"]
CHART_DPI = 150
