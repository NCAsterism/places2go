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

from pathlib import Path

import pandas as pd
import plotly.express as px

try:
    from scripts.exceptions import DataValidationError, MissingColumnError
except ModuleNotFoundError:
    from exceptions import DataValidationError, MissingColumnError


def validate_dataframe(df: pd.DataFrame) -> None:
    """Validate that a DataFrame meets all data quality requirements.

    This function performs comprehensive validation checks on the loaded data:
    - Verifies all required columns are present
    - Checks data types are correct for numeric columns
    - Validates no null values exist in critical columns
    - Ensures numeric values are in valid ranges (e.g., costs > 0)
    - Confirms DataFrame is not empty

    Args:
        df: The DataFrame to validate.

    Raises:
        DataValidationError: If the DataFrame is empty.
        MissingColumnError: If required columns are missing.
        DataValidationError: If data types are incorrect.
        DataValidationError: If null values exist in critical columns.
        DataValidationError: If values are outside valid ranges.
    """
    # Check for empty DataFrame
    if df.empty:
        raise DataValidationError("DataFrame is empty. No data to process.")

    # Define required columns
    required_columns = {
        "Destination",
        "Airport",
        "Flight Cost (GBP)",
        "Flight Time (hrs)",
        "Avg Temp (°C)",
        "UV Index",
        "Monthly Living Cost (GBP)",
        "Meal Cost (GBP)",
        "Beer Cost (GBP)",
        "Weed Cost (GBP per gram)",
    }

    # Check for required columns
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise MissingColumnError(
            f"Missing required columns: {', '.join(sorted(missing_columns))}"
        )

    # Define numeric columns that must be numeric types
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

    # Validate data types
    non_numeric_cols = []
    for col in numeric_cols:
        # A column is considered valid if:
        # 1. It has a numeric dtype, OR
        # 2. All its values are NaN/None (which is acceptable for non-critical columns)
        if not pd.api.types.is_numeric_dtype(df[col]):
            # Check if all values are null (which pandas might store as object dtype)
            if not df[col].isna().all():
                non_numeric_cols.append(col)

    if non_numeric_cols:
        raise DataValidationError(
            f"Columns must be numeric: {', '.join(non_numeric_cols)}"
        )

    # Check for null values in critical columns
    critical_columns = [
        "Destination",
        "Airport",
        "Flight Cost (GBP)",
        "Flight Time (hrs)",
    ]
    null_columns = []
    for col in critical_columns:
        if df[col].isnull().any():
            null_count = df[col].isnull().sum()
            null_columns.append(f"{col} ({null_count} nulls)")

    if null_columns:
        raise DataValidationError(
            f"Critical columns contain null values: {', '.join(null_columns)}"
        )

    # Validate value ranges for cost columns (must be > 0)
    cost_columns = [
        "Flight Cost (GBP)",
        "Monthly Living Cost (GBP)",
        "Meal Cost (GBP)",
        "Beer Cost (GBP)",
        "Weed Cost (GBP per gram)",
    ]
    invalid_range_cols = []
    for col in cost_columns:
        # Check for values <= 0 (ignoring NaN values)
        if (df[col].notna() & (df[col] <= 0)).any():
            invalid_count = (df[col].notna() & (df[col] <= 0)).sum()
            invalid_range_cols.append(f"{col} ({invalid_count} invalid values)")

    if invalid_range_cols:
        raise DataValidationError(
            f"Cost columns must contain values > 0: {', '.join(invalid_range_cols)}"
        )

    # Validate flight time is positive
    if (df["Flight Time (hrs)"].notna() & (df["Flight Time (hrs)"] <= 0)).any():
        invalid_count = (
            df["Flight Time (hrs)"].notna() & (df["Flight Time (hrs)"] <= 0)
        ).sum()
        raise DataValidationError(
            f"Flight Time (hrs) must be > 0 ({invalid_count} invalid values)"
        )


def load_data(csv_path: Path) -> pd.DataFrame:
    """Read the destination dataset from a CSV file.

    Args:
        csv_path: Path to the CSV file containing destination data.

    Returns:
        A pandas DataFrame with the dataset.

    Raises:
        DataValidationError: If the data fails validation checks.
        MissingColumnError: If required columns are missing.
    """
    df = pd.read_csv(csv_path)

    # Define numeric columns
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

    # Only coerce columns that exist in the DataFrame
    existing_numeric_cols = [col for col in numeric_cols if col in df.columns]
    if existing_numeric_cols:
        df[existing_numeric_cols] = df[existing_numeric_cols].apply(
            pd.to_numeric, errors="coerce"
        )

    # Validate the DataFrame before returning
    validate_dataframe(df)

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
