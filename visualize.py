"""
Step 3: Visualizations

Generates 8 charts covering distributions, relationships, and trends in
the logistics dataset, saved as PNG files under outputs/charts/.

Usage:
    python -m src.visualize
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src import config
from src.eda import load_dataset, NUMERIC_COLS

sns.set_theme(style="whitegrid", font_scale=1.0)


def _save(fig, name: str) -> None:
    fig.tight_layout()
    path = config.CHARTS_DIR / f"{name}.png"
    fig.savefig(path, dpi=config.CHART_DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"saved {path}")


def plot_delivery_time_distribution(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    sns.histplot(df["delivery_time_days"], bins=30, kde=True, color=config.CHART_PALETTE[0], ax=ax)
    ax.set_title("Distribution of Delivery Time")
    ax.set_xlabel("Delivery Time (days)")
    ax.set_ylabel("Number of Shipments")
    _save(fig, "01_delivery_time_distribution")


def plot_cost_by_mode_boxplot(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    order = df.groupby("transport_mode")["transportation_cost_usd"].median().sort_values().index
    sns.boxplot(data=df, x="transport_mode", y="transportation_cost_usd", order=order,
                hue="transport_mode", palette=config.CHART_PALETTE, legend=False, ax=ax)
    ax.set_title("Transportation Cost Spread by Mode")
    ax.set_xlabel("Transport Mode")
    ax.set_ylabel("Transportation Cost (USD)")
    _save(fig, "02_cost_by_mode_boxplot")


def plot_distance_vs_deliverytime(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    sns.scatterplot(data=df, x="distance_km", y="delivery_time_days", hue="transport_mode",
                     palette=config.CHART_PALETTE, alpha=0.6, s=35, ax=ax)
    ax.set_title("Distance vs. Delivery Time by Transport Mode")
    ax.set_xlabel("Distance (km)")
    ax.set_ylabel("Delivery Time (days)")
    ax.legend(title="Mode", loc="upper left")
    _save(fig, "03_distance_vs_deliverytime_scatter")


def plot_correlation_heatmap(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 6))
    corr = df[NUMERIC_COLS].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0, vmin=-1, vmax=1,
                square=True, linewidths=0.5, ax=ax, cbar_kws={"shrink": 0.8})
    ax.set_title("Correlation Matrix of Key Logistics Metrics")
    plt.setp(ax.get_xticklabels(), rotation=40, ha="right")
    _save(fig, "04_correlation_heatmap")


def plot_delay_rate_by_mode(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    delay_rate = (df.groupby("transport_mode")["is_delayed"].mean() * 100).sort_values(ascending=False)
    bars = ax.bar(delay_rate.index, delay_rate.values, color=config.CHART_PALETTE)
    ax.set_title("Shipment Delay Rate by Transport Mode")
    ax.set_xlabel("Transport Mode")
    ax.set_ylabel("Delayed Shipments (%)")
    for b in bars:
        ax.annotate(f"{b.get_height():.1f}%", (b.get_x() + b.get_width() / 2, b.get_height()),
                    ha="center", va="bottom", fontsize=10)
    _save(fig, "05_delay_rate_by_mode")


def plot_monthly_trend(df: pd.DataFrame) -> None:
    df = df.copy()
    df["month"] = df["dispatch_date"].dt.to_period("M").astype(str)
    monthly = df.groupby("month").agg(
        shipments=("shipment_id", "count"),
        avg_cost=("transportation_cost_usd", "mean"),
    ).reset_index()

    fig, ax1 = plt.subplots(figsize=(8, 4.8))
    ax2 = ax1.twinx()
    ax1.plot(monthly["month"], monthly["shipments"], marker="o",
              color=config.CHART_PALETTE[0], label="Shipment Volume")
    ax2.plot(monthly["month"], monthly["avg_cost"], marker="s",
              color=config.CHART_PALETTE[3], label="Avg. Cost (USD)")
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Shipment Volume", color=config.CHART_PALETTE[0])
    ax2.set_ylabel("Average Transportation Cost (USD)", color=config.CHART_PALETTE[3])
    ax1.tick_params(axis="y", labelcolor=config.CHART_PALETTE[0])
    ax2.tick_params(axis="y", labelcolor=config.CHART_PALETTE[3])
    ax1.set_title("Monthly Shipment Volume and Average Cost Trend")
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
    _save(fig, "06_monthly_trend")


def plot_category_by_region(df: pd.DataFrame) -> None:
    pivot = df.pivot_table(index="region", columns="product_category",
                            values="shipment_id", aggfunc="count", fill_value=0)
    fig, ax = plt.subplots(figsize=(8, 5))
    pivot.plot(kind="bar", stacked=True, color=config.CHART_PALETTE, ax=ax)
    ax.set_title("Shipment Volume by Product Category and Region")
    ax.set_xlabel("Region")
    ax.set_ylabel("Number of Shipments")
    ax.legend(title="Product Category", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.setp(ax.get_xticklabels(), rotation=0)
    _save(fig, "07_category_by_region_stacked")


def plot_satisfaction_delay_violin(df: pd.DataFrame) -> None:
    df = df.copy()
    df["Delivery Status"] = df["is_delayed"].map({True: "Delayed", False: "On-Time"})
    fig, ax = plt.subplots(figsize=(6.5, 4.8))
    sns.violinplot(data=df, x="Delivery Status", y="customer_satisfaction",
                    hue="Delivery Status",
                    palette=[config.CHART_PALETTE[1], config.CHART_PALETTE[3]],
                    legend=False, ax=ax, inner="quartile")
    ax.set_title("Customer Satisfaction: On-Time vs. Delayed Shipments")
    ax.set_xlabel("")
    ax.set_ylabel("Customer Satisfaction (1-5)")
    _save(fig, "08_satisfaction_delay_violin")


CHART_FUNCS = [
    plot_delivery_time_distribution,
    plot_cost_by_mode_boxplot,
    plot_distance_vs_deliverytime,
    plot_correlation_heatmap,
    plot_delay_rate_by_mode,
    plot_monthly_trend,
    plot_category_by_region,
    plot_satisfaction_delay_violin,
]


def main() -> None:
    df = load_dataset()
    for fn in CHART_FUNCS:
        fn(df)
    print("\nAll charts generated.")


if __name__ == "__main__":
    main()
