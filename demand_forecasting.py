"""
demand_forecasting.py

Forecasts daily order volume per warehouse using a Random Forest regressor,
to inform inventory replenishment and staffing decisions (KPI: Inventory
Turnover Ratio).

Expects a processed dataset with one row per order (data/processed/orders_clean.csv)
containing at least: order_date, warehouse_id.
"""

from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

try:
    from sklearn.metrics import root_mean_squared_error
except ImportError:  # scikit-learn < 1.4
    from sklearn.metrics import mean_squared_error

    def root_mean_squared_error(y_true, y_pred):
        return mean_squared_error(y_true, y_pred) ** 0.5

PROCESSED_PATH = Path("data/processed/orders_clean.csv")


def build_daily_demand(orders: pd.DataFrame) -> pd.DataFrame:
    """Aggregate order-level data into daily order counts per warehouse."""
    orders = orders.copy()
    orders["order_date"] = pd.to_datetime(orders["order_date"])
    orders["date"] = orders["order_date"].dt.date

    daily = (
        orders.groupby(["date", "warehouse_id"])
        .size()
        .reset_index(name="order_count")
    )
    daily["date"] = pd.to_datetime(daily["date"])
    daily["dow"] = daily["date"].dt.dayofweek
    daily["month"] = daily["date"].dt.month

    # 7-day lag feature per warehouse
    daily = daily.sort_values(["warehouse_id", "date"])
    daily["lag_1w"] = daily.groupby("warehouse_id")["order_count"].shift(7)
    daily = daily.dropna(subset=["lag_1w"])

    # Encode warehouse_id as a numeric code for the model
    daily["warehouse_code"] = daily["warehouse_id"].astype("category").cat.codes

    return daily.reset_index(drop=True)


def train_model(daily: pd.DataFrame):
    """Train a Random Forest regressor to predict daily order_count."""
    features = ["dow", "month", "warehouse_code", "lag_1w"]
    X = daily[features]
    y = daily["order_count"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    rmse = root_mean_squared_error(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    print(f"Demand forecast — RMSE: {rmse:.2f}, MAE: {mae:.2f}")

    return model


def main() -> None:
    orders = pd.read_csv(PROCESSED_PATH)
    daily = build_daily_demand(orders)
    train_model(daily)


if __name__ == "__main__":
    main()
