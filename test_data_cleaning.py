import pandas as pd
import pytest

from src.data_cleaning import clean_orders


def make_raw_df():
    return pd.DataFrame(
        {
            "order_id": [1, 2, 2, 3, 4],
            "order_date": ["2026-01-01", "2026-01-02", "2026-01-02", "2026-01-03", None],
            "delivery_date": ["2026-01-03", "2026-01-04", "2026-01-04", "2026-01-05", "2026-01-06"],
            "warehouse_id": ["W1", "W1", "W1", "W2", "W2"],
            "delivery_lat": [17.38, 17.40, 17.40, 91.0, 17.45],  # row 4 has invalid lat
            "delivery_lon": [78.48, 78.50, 78.50, 78.55, 78.60],
            "promised_window_hrs": [48, 48, 48, 48, 48],
        }
    )


def test_drops_duplicate_orders():
    df = clean_orders(make_raw_df())
    assert df["order_id"].is_unique


def test_drops_missing_critical_fields():
    df = clean_orders(make_raw_df())
    # row with order_id=4 has null order_date -> dropped
    assert 4 not in df["order_id"].values


def test_invalid_latitude_removed():
    df = clean_orders(make_raw_df())
    assert df["delivery_lat"].between(-90, 90).all()


def test_delivery_days_computed():
    df = clean_orders(make_raw_df())
    assert "delivery_days" in df.columns
    assert (df["delivery_days"] >= 0).all()


def test_on_time_flag_present():
    df = clean_orders(make_raw_df())
    assert "on_time" in df.columns
    assert df["on_time"].dtype == bool


def test_missing_required_column_raises():
    df = make_raw_df().drop(columns=["warehouse_id"])
    with pytest.raises(ValueError):
        clean_orders(df)
