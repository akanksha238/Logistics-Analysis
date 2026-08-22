"""
Step 2: Exploratory Data Analysis (EDA)

Computes central tendencies, dispersion, distributions, and correlations
for the logistics dataset and writes a text summary to outputs/eda_summary.txt.

Usage:
    python -m src.eda
"""

import pandas as pd

from src import config

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 20)

NUMERIC_COLS = [
    "distance_km", "shipment_weight_kg", "transportation_cost_usd",
    "delivery_time_days", "delay_days", "fuel_surcharge_pct",
    "customer_satisfaction",
]


def load_dataset() -> pd.DataFrame:
    if not config.DATASET_PATH.exists():
        raise FileNotFoundError(
            f"{config.DATASET_PATH} not found. Run `python -m src.simulate_data` first."
        )
    return pd.read_csv(config.DATASET_PATH, parse_dates=["dispatch_date"])


def run_eda(df: pd.DataFrame) -> str:
    """Run the full EDA and return the report as a single string."""
    lines: list[str] = []

    def log(x=""):
        lines.append(str(x))

    log("=" * 70)
    log("1. DATASET OVERVIEW")
    log("=" * 70)
    log(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    log(f"Date range: {df['dispatch_date'].min().date()} to {df['dispatch_date'].max().date()}")
    log("")
    log("Missing values per column:")
    log(df.isna().sum().to_string())

    log("")
    log("=" * 70)
    log("2. CENTRAL TENDENCY & DISPERSION (numeric variables)")
    log("=" * 70)
    desc = df[NUMERIC_COLS].describe().T
    desc["median"] = df[NUMERIC_COLS].median()
    desc["skew"] = df[NUMERIC_COLS].skew()
    log(desc.round(2).to_string())

    log("")
    log("=" * 70)
    log("3. CATEGORICAL DISTRIBUTIONS")
    log("=" * 70)
    for col in ["region", "transport_mode", "carrier", "product_category"]:
        log(f"\n-- {col} --")
        vc = df[col].value_counts()
        pct = (df[col].value_counts(normalize=True) * 100).round(1)
        log(pd.DataFrame({"count": vc, "pct": pct}).to_string())

    log("")
    log("=" * 70)
    log("4. DELAY / SLA PERFORMANCE")
    log("=" * 70)
    overall_delay_rate = df["is_delayed"].mean() * 100
    log(f"Overall on-time-vs-delayed: {overall_delay_rate:.1f}% of shipments delayed")
    log("\nDelay rate by transport mode:")
    log((df.groupby("transport_mode")["is_delayed"].mean() * 100).round(1).to_string())
    log("\nDelay rate by carrier:")
    log((df.groupby("carrier")["is_delayed"].mean() * 100).round(1).to_string())
    log("\nDelay rate: weekday vs weekend dispatch:")
    log((df.groupby("is_weekend")["is_delayed"].mean() * 100).round(1).to_string())
    log("\nAverage delay (days) among delayed shipments, by mode:")
    log(df[df["is_delayed"]].groupby("transport_mode")["delay_days"].mean().round(2).to_string())

    log("")
    log("=" * 70)
    log("5. COST ANALYSIS")
    log("=" * 70)
    log("Average transportation cost by mode:")
    log(df.groupby("transport_mode")["transportation_cost_usd"].mean().round(2).to_string())
    log("\nAverage transportation cost by region:")
    log(df.groupby("region")["transportation_cost_usd"].mean().round(2).to_string())
    log("\nCost per kg by mode (efficiency indicator):")
    cost_per_kg = df["transportation_cost_usd"] / df["shipment_weight_kg"]
    log(df.assign(cost_per_kg=cost_per_kg).groupby("transport_mode")["cost_per_kg"].mean().round(3).to_string())

    log("")
    log("=" * 70)
    log("6. CORRELATION MATRIX")
    log("=" * 70)
    corr = df[NUMERIC_COLS].corr(numeric_only=True)
    log(corr.round(2).to_string())

    log("")
    log("=" * 70)
    log("7. CUSTOMER SATISFACTION")
    log("=" * 70)
    log("Average satisfaction by transport mode:")
    log(df.groupby("transport_mode")["customer_satisfaction"].mean().round(2).to_string())
    log("\nAverage satisfaction: delayed vs on-time shipments:")
    log(df.groupby("is_delayed")["customer_satisfaction"].mean().round(2).to_string())
    log("\nDamage rate by mode (%):")
    log((df.groupby("transport_mode")["damaged_in_transit"].mean() * 100).round(2).to_string())

    return "\n".join(lines)


def main() -> None:
    df = load_dataset()
    report = run_eda(df)
    print(report)
    config.EDA_SUMMARY_PATH.write_text(report)
    print(f"\n\nSaved -> {config.EDA_SUMMARY_PATH}")


if __name__ == "__main__":
    main()
