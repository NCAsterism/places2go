"""
dashboard.py
---------------

This script demonstrates how to load a dataset of travel destinations and produce
interactive charts using Plotly.  It reads data from ``data/dummy_data.csv`` and
generates two HTML files in the ``output/`` directory:

* ``flight_costs.html`` — a bar chart showing the cost of flights by destination
  with bars grouped by departure airport (Exeter or Bristol).
* ``flight_time_vs_cost.html`` — a scatter plot comparing flight time and cost,
  where the size of each point indicates the monthly living cost at the
  destination.

To run the script:

.. code:: bash

    python scripts/dashboard.py

Dependencies: ``pandas`` and ``plotly``.  Install them via pip if needed.
"""

import os
from pathlib import Path

import pandas as pd
import plotly.express as px


def load_data(csv_path: Path) -> pd.DataFrame:
    """Read the destination dataset from a CSV file.

    Args:
        csv_path: Path to the CSV file containing destination data.

    Returns:
        A pandas DataFrame with the dataset.
    """
    df = pd.read_csv(csv_path)
    # Ensure correct dtypes for numeric columns
    numeric_cols = [
        "Flight Cost (GBP)",
        "Flight Time (hrs)",
        "Avg Temp (°C)",
        "UV Index",
        "Monthly Living Cost (GBP)",
        "Meal Cost (GBP)",
        "Beer Cost (GBP)",
        "Weed Cost (GBP per gram)",
    ]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    return df


def create_flight_cost_chart(df: pd.DataFrame, output_dir: Path) -> None:
    """Generate a bar chart of flight costs by destination and save as HTML.

    Args:
        df: The DataFrame containing destination data.
        output_dir: Directory where the HTML file will be saved.
    """
    fig = px.bar(
        df,
        x="Destination",
        y="Flight Cost (GBP)",
        color="Airport",
        barmode="group",
        title="Flight Cost by Destination and Airport",
    )
    output_path = output_dir / "flight_costs.html"
    fig.write_html(output_path)
    print(f"Flight cost chart saved to {output_path}")


def create_time_vs_cost_chart(df: pd.DataFrame, output_dir: Path) -> None:
    """Generate a scatter plot of flight time vs cost with living cost as size.

    Args:
        df: The DataFrame containing destination data.
        output_dir: Directory where the HTML file will be saved.
    """
    fig = px.scatter(
        df,
        x="Flight Time (hrs)",
        y="Flight Cost (GBP)",
        size="Monthly Living Cost (GBP)",
        color="Destination",
        hover_name="Destination",
        title="Flight Time vs Cost (Bubble size = Monthly Living Cost)",
    )
    output_path = output_dir / "flight_time_vs_cost.html"
    fig.write_html(output_path)
    print(f"Flight time vs cost chart saved to {output_path}")


def main():
    project_root = Path(__file__).resolve().parents[1]
    data_path = project_root / "data" / "dummy_data.csv"
    output_dir = project_root / "output"
    output_dir.mkdir(exist_ok=True)

    df = load_data(data_path)
    create_flight_cost_chart(df, output_dir)
    create_time_vs_cost_chart(df, output_dir)


if __name__ == "__main__":
    main()
