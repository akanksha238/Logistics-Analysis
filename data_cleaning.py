"""
data_cleaning.py

Loads raw order/shipment data and produces a cleaned dataset ready for
exploratory analysis and modeling.

Expected raw schema (data/raw/orders.csv):
    order_id, order_date, delivery_date, warehouse_id,
    delivery_lat, delivery_lon, product_id, quantity, promised_window_hrs
"""

from pathlib import Path
import pandas as pd

RAW_PATH = Path("data/raw/orders.csv")
PROCESSED_PATH = Path("data/processed/orders_clean.csv")

REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "delivery_date",
    "warehouse_id",
    "delivery_lat",
    "delivery_lon",
]


def load_raw(path: Path = RAW_PATH) -> pd.DataFrame:
    """Load the raw orders CSV."""
    if not path.exists():
        raise FileNotFoundError(
            f"Raw data not found at {path}. Place a CSV with columns "
            f"{REQUIRED_COLUMNS} in data/raw/."
        )
    return pd.read_csv(path)


def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Clean a raw orders dataframe.

    Steps:
      1. Drop duplicate orders.
      2. Drop rows missing critical fields.
      3. Parse dates and derive delivery_days.
      4. Flag on-time deliveries against promised_window_hrs (if present).
      5. Validate lat/lon are within plausible bounds.
    """
    df = df.copy()

    # 1. Remove duplicate orders
    df = df.drop_duplicates(subset="order_id")

    # 2. Drop rows missing critical fields
    missing_required = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_required:
        raise ValueError(f"Missing required columns: {missing_required}")
    df = df.dropna(subset=REQUIRED_COLUMNS)

    # 3. Standardize datetimes and derive delivery duration
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["delivery_date"] = pd.to_datetime(df["delivery_date"], errors="coerce")
    df = df.dropna(subset=["order_date", "delivery_date"])
    df["delivery_days"] = (df["delivery_date"] - df["order_date"]).dt.days
    df["delivery_hours"] = (
        df["delivery_date"] - df["order_date"]
    ).dt.total_seconds() / 3600

    # 4. On-time delivery flag (KPI: On-Time Delivery Rate)
    if "promised_window_hrs" in df.columns:
        df["on_time"] = df["delivery_hours"] <= df["promised_window_hrs"]

    # 5. Validate geographic coordinates
    df = df[df["delivery_lat"].between(-90, 90)]
    df = df[df["delivery_lon"].between(-180, 180)]

    return df.reset_index(drop=True)


def save_processed(df: pd.DataFrame, path: Path = PROCESSED_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved {len(df):,} cleaned rows to {path}")


def main() -> None:
    raw = load_raw()
    cleaned = clean_orders(raw)
    save_processed(cleaned)

    if "on_time" in cleaned.columns:
        otdr = cleaned["on_time"].mean() * 100
        print(f"On-Time Delivery Rate: {otdr:.1f}%")


if __name__ == "__main__":
    main()
