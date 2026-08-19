"""
zone_clustering.py

Segments delivery addresses into geographically coherent zones using K-Means,
providing the basis for route planning and warehouse-to-zone assignment.
"""

from pathlib import Path
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

PROCESSED_PATH = Path("data/processed/orders_clean.csv")
OUTPUT_PATH = Path("data/processed/orders_with_zones.csv")


def assign_zones(df: pd.DataFrame, n_clusters: int = 8, random_state: int = 42) -> pd.DataFrame:
    """Cluster delivery coordinates into n_clusters zones."""
    df = df.copy()
    coords = df[["delivery_lat", "delivery_lon"]]

    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    df["zone_id"] = kmeans.fit_predict(coords)

    score = silhouette_score(coords, df["zone_id"])
    print(f"Zone clustering (k={n_clusters}) — silhouette score: {score:.3f}")

    return df, kmeans


def main() -> None:
    df = pd.read_csv(PROCESSED_PATH)
    zoned, _ = assign_zones(df)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    zoned.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved zoned deliveries to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
