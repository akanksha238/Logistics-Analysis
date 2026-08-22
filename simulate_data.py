"""
Step 1: Data Simulation

Generates a hypothetical logistics dataset representing shipments handled
over a 6-month period across multiple regions, transportation modes and
carriers. Relationships are built in deliberately (e.g. distance drives
cost and delivery time; mode affects cost-per-km; weekend dispatch raises
delay risk) so downstream EDA and visualizations surface genuine,
interpretable patterns.

Usage:
    python -m src.simulate_data
"""

import numpy as np
import pandas as pd

from src import config


def simulate_dataset(seed: int = config.RANDOM_SEED, n: int = config.N_RECORDS) -> pd.DataFrame:
    """Build and return the simulated logistics DataFrame."""
    rng = np.random.default_rng(seed)
    np.random.seed(seed)  # some helpers below use the legacy global RNG

    df = pd.DataFrame({
        "shipment_id": [f"SHP{1000 + i}" for i in range(n)],
        "region": np.random.choice(config.REGIONS, n, p=config.REGION_WEIGHTS),
        "transport_mode": np.random.choice(config.TRANSPORT_MODES, n, p=config.MODE_WEIGHTS),
        "carrier": np.random.choice(config.CARRIERS, n, p=config.CARRIER_WEIGHTS),
        "product_category": np.random.choice(
            config.PRODUCT_CATEGORIES, n, p=config.CATEGORY_WEIGHTS
        ),
    })

    start = pd.Timestamp(config.SIMULATION_START_DATE)
    df["dispatch_date"] = start + pd.to_timedelta(
        np.random.randint(0, config.SIMULATION_DAYS, n), unit="D"
    )
    df["day_of_week"] = df["dispatch_date"].dt.day_name()
    df["is_weekend"] = df["dispatch_date"].dt.dayofweek >= 5

    df["distance_km"] = df["transport_mode"].apply(
        lambda m: max(20, np.random.normal(config.MODE_DISTANCE_BASE[m], config.MODE_DISTANCE_SD[m]))
    ).round(1)

    df["shipment_weight_kg"] = df["product_category"].apply(
        lambda c: max(10, np.random.gamma(shape=3.0, scale=config.CATEGORY_WEIGHT_BASE[c] / 3.0))
    ).round(1)

    df["transportation_cost_usd"] = df.apply(_compute_cost, axis=1).round(2)
    df["delivery_time_days"] = df.apply(_compute_delivery_time, axis=1).round(2)

    df["promised_delivery_days"] = df["transport_mode"].map(config.MODE_PROMISE_DAYS)
    df["delay_days"] = (df["delivery_time_days"] - df["promised_delivery_days"]).round(2)
    df["is_delayed"] = df["delay_days"] > 0

    df["customer_satisfaction"] = df.apply(_compute_satisfaction, axis=1)
    df["fuel_surcharge_pct"] = np.round(np.random.normal(8.5, 2.0, n).clip(2, 18), 1)
    df["damaged_in_transit"] = df["transport_mode"].apply(
        lambda m: np.random.rand() < config.MODE_DAMAGE_PROB[m]
    )

    cols = [
        "shipment_id", "dispatch_date", "day_of_week", "is_weekend", "region",
        "transport_mode", "carrier", "product_category", "distance_km",
        "shipment_weight_kg", "transportation_cost_usd", "promised_delivery_days",
        "delivery_time_days", "delay_days", "is_delayed", "fuel_surcharge_pct",
        "damaged_in_transit", "customer_satisfaction",
    ]
    return df[cols]


def _compute_cost(row) -> float:
    tons = row["shipment_weight_kg"] / 1000.0
    rate = config.MODE_COST_PER_KM_PER_TON[row["transport_mode"]]
    cost = config.MODE_BASE_HANDLING_FEE[row["transport_mode"]] + rate * row["distance_km"] * max(tons, 0.05)
    weekend_surcharge = 1.08 if row["is_weekend"] else 1.0
    noise = np.random.normal(1.0, 0.08)
    return max(15, cost * weekend_surcharge * noise)


def _compute_delivery_time(row) -> float:
    mode = row["transport_mode"]
    travel_days = row["distance_km"] / config.MODE_SPEED_KMPD[mode]
    base = config.MODE_BASE_DAYS[mode]
    weekend_delay = np.random.uniform(0.3, 1.2) if row["is_weekend"] else 0
    noise = np.random.normal(0, 0.4)
    return max(0.5, base + travel_days + weekend_delay + noise)


def _compute_satisfaction(row) -> float:
    penalty = max(0, row["delay_days"]) * 0.6
    score = np.random.normal(4.4, 0.4) - penalty
    return float(np.clip(round(score * 2) / 2, 1, 5))


def main() -> None:
    df = simulate_dataset()
    config.DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(config.DATASET_PATH, index=False)
    print(f"Simulated {len(df)} shipment records -> {config.DATASET_PATH}")
    print(df.head())


if __name__ == "__main__":
    main()
