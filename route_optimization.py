"""
route_optimization.py

Solves a per-zone Vehicle Routing Problem (VRP) to sequence deliveries into
minimum-distance routes, using Google OR-Tools. This directly targets the
Cost per Delivery (CPD) KPI.

Note: requires the `ortools` package (see requirements.txt).
"""

from pathlib import Path
from math import radians, sin, cos, sqrt, atan2
import pandas as pd

try:
    from ortools.constraint_solver import routing_enums_pb2, pywrapcp
    ORTOOLS_AVAILABLE = True
except ImportError:  # pragma: no cover
    ORTOOLS_AVAILABLE = False

ZONED_PATH = Path("data/processed/orders_with_zones.csv")


def haversine_km(lat1, lon1, lat2, lon2) -> float:
    """Great-circle distance between two lat/lon points, in km."""
    r = 6371.0
    dlat, dlon = radians(lat2 - lat1), radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return r * 2 * atan2(sqrt(a), sqrt(1 - a))


def build_distance_matrix(points: list[tuple[float, float]]) -> list[list[int]]:
    """Build an integer (meters) distance matrix for OR-Tools."""
    n = len(points)
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i][j] = int(
                    haversine_km(points[i][0], points[i][1], points[j][0], points[j][1]) * 1000
                )
    return matrix


def optimize_route(depot: tuple[float, float], delivery_points: list[tuple[float, float]]) -> list[int]:
    """Solve a single-vehicle TSP-style route from depot through delivery_points.

    Returns the visiting order as a list of indices into
    [depot] + delivery_points.
    """
    if not ORTOOLS_AVAILABLE:
        raise ImportError("ortools is required for route_optimization. pip install ortools")

    points = [depot] + delivery_points
    distance_matrix = build_distance_matrix(points)

    manager = pywrapcp.RoutingIndexManager(len(points), 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_params.time_limit.FromSeconds(30)

    solution = routing.SolveWithParameters(search_params)
    if solution is None:
        raise RuntimeError("No route solution found")

    route = []
    index = routing.Start(0)
    while not routing.IsEnd(index):
        route.append(manager.IndexToNode(index))
        index = solution.Value(routing.NextVar(index))
    route.append(manager.IndexToNode(index))
    return route


def main() -> None:
    df = pd.read_csv(ZONED_PATH)

    for zone_id, zone_df in df.groupby("zone_id"):
        depot = (zone_df["delivery_lat"].mean(), zone_df["delivery_lon"].mean())
        points = list(zip(zone_df["delivery_lat"], zone_df["delivery_lon"]))[:25]  # cap for demo

        if len(points) < 2:
            continue

        route = optimize_route(depot, points)
        print(f"Zone {zone_id}: optimized route visits {len(route)} stops")


if __name__ == "__main__":
    main()
