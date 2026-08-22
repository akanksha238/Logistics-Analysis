#!/usr/bin/env python3
"""
Run the full Logistics Analyzer pipeline end-to-end:

    1. Simulate the shipment dataset  -> data/logistics_dataset.csv
    2. Run exploratory data analysis  -> outputs/eda_summary.txt
    3. Generate all visualizations    -> outputs/charts/*.png

Usage:
    python run_pipeline.py
"""

from src import simulate_data, eda, visualize


def main() -> None:
    print("Step 1/3: Simulating dataset...")
    simulate_data.main()

    print("\nStep 2/3: Running exploratory data analysis...")
    eda.main()

    print("\nStep 3/3: Generating visualizations...")
    visualize.main()

    print("\nPipeline complete. See the outputs/ directory for results.")


if __name__ == "__main__":
    main()
