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

import logging
from pathlib import Path

import pandas as pd
import plotly.express as px

try:
    # Try relative import first (when run as module)
    from .exceptions import (
        DataLoadError,
        DataValidationError,
        MissingColumnError,
        ChartGenerationError,
    )
except ImportError:
    # Fall back to direct import (when run as script)
    from exceptions import (
        DataLoadError,
        DataValidationError,
        MissingColumnError,
        ChartGenerationError,
    )

# Configure logging
log_dir = Path(__file__).resolve().parents[1] / "logs"
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_dir / "dashboard.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def load_data(csv_path: Path) -> pd.DataFrame:
    """Read the destination dataset from a CSV file.

    Args:
        csv_path: Path to the CSV file containing destination data.

    Returns:
        A pandas DataFrame with the dataset.

    Raises:
        DataLoadError: If the CSV file cannot be read.
        DataValidationError: If the loaded dataframe is empty.
        MissingColumnError: If required columns are missing.
    """
    logger.info(f"Loading data from {csv_path}")
    
    # Check if file exists
    if not csv_path.exists():
        logger.error(f"CSV file not found: {csv_path}")
        raise DataLoadError("CSV file not found", path=str(csv_path))

    # Try to read the CSV file
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        logger.error(f"Failed to read CSV file: {e}")
        raise DataLoadError(f"Failed to read CSV file: {e}", path=str(csv_path))

    # Validate the dataframe is not empty
    if df.empty:
        logger.error("Loaded dataframe is empty")
        raise DataValidationError("Loaded dataframe is empty")

    # Define required columns
    required_cols = [
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
    ]

    # Check for missing columns
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        logger.error(f"Missing required columns: {missing_cols}")
        raise MissingColumnError(missing_cols, list(df.columns))

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
    logger.debug(f"DataFrame loaded with shape: {df.shape}")
    return df


def create_flight_cost_chart(df: pd.DataFrame, output_dir: Path) -> None:
    """Generate a bar chart of flight costs by destination and save as HTML.

    Args:
        df: The DataFrame containing destination data.
        output_dir: Directory where the HTML file will be saved.

    Raises:
        DataValidationError: If the dataframe is empty.
        MissingColumnError: If required columns are missing.
        ChartGenerationError: If chart creation or saving fails.
    """
    logger.info("Creating flight cost chart")
    
    # Validate dataframe is not empty
    if df.empty:
        logger.error("Cannot create chart from empty dataframe")
        raise DataValidationError("Cannot create chart from empty dataframe")

    # Check required columns
    required_cols = ["Destination", "Flight Cost (GBP)", "Airport"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        logger.error(f"Missing required columns for chart: {missing_cols}")
        raise MissingColumnError(missing_cols, list(df.columns))

    # Try to create the chart
    try:
        fig = px.bar(
            df,
            x="Destination",
            y="Flight Cost (GBP)",
            color="Airport",
            barmode="group",
            title="Flight Cost by Destination and Airport",
        )
    except Exception as e:
        logger.error(f"Failed to create bar chart: {e}")
        raise ChartGenerationError(
            f"Failed to create bar chart: {e}", chart_type="flight_costs"
        )

    # Try to save the chart
    try:
        output_path = output_dir / "flight_costs.html"
        fig.write_html(output_path)
        logger.info(f"Flight cost chart saved to {output_path}")
    except Exception as e:
        logger.error(f"Failed to save chart to {output_path}: {e}")
        raise ChartGenerationError(
            f"Failed to save chart to file: {e}", chart_type="flight_costs"
        )


def create_time_vs_cost_chart(df: pd.DataFrame, output_dir: Path) -> None:
    """Generate a scatter plot of flight time vs cost with living cost as size.

    Args:
        df: The DataFrame containing destination data.
        output_dir: Directory where the HTML file will be saved.

    Raises:
        DataValidationError: If the dataframe is empty.
        MissingColumnError: If required columns are missing.
        ChartGenerationError: If chart creation or saving fails.
    """
    logger.info("Creating flight time vs cost chart")
    
    # Validate dataframe is not empty
    if df.empty:
        logger.error("Cannot create chart from empty dataframe")
        raise DataValidationError("Cannot create chart from empty dataframe")

    # Check required columns
    required_cols = [
        "Flight Time (hrs)",
        "Flight Cost (GBP)",
        "Monthly Living Cost (GBP)",
        "Destination",
    ]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        logger.error(f"Missing required columns for chart: {missing_cols}")
        raise MissingColumnError(missing_cols, list(df.columns))

    # Try to create the chart
    try:
        fig = px.scatter(
            df,
            x="Flight Time (hrs)",
            y="Flight Cost (GBP)",
            size="Monthly Living Cost (GBP)",
            color="Destination",
            hover_name="Destination",
            title="Flight Time vs Cost (Bubble size = Monthly Living Cost)",
        )
    except Exception as e:
        logger.error(f"Failed to create scatter plot: {e}")
        raise ChartGenerationError(
            f"Failed to create scatter plot: {e}", chart_type="flight_time_vs_cost"
        )

    # Try to save the chart
    try:
        output_path = output_dir / "flight_time_vs_cost.html"
        fig.write_html(output_path)
        logger.info(f"Flight time vs cost chart saved to {output_path}")
    except Exception as e:
        logger.error(f"Failed to save chart to {output_path}: {e}")
        raise ChartGenerationError(
            f"Failed to save chart to file: {e}", chart_type="flight_time_vs_cost"
        )


def main() -> None:
    """Main function to run the dashboard generation process.

    This function orchestrates the data loading and chart generation workflow,
    with appropriate error handling for various failure scenarios.
    """
    logger.info("Starting dashboard generation")
    try:
        project_root = Path(__file__).resolve().parents[1]
        data_path = project_root / "data" / "dummy_data.csv"
        output_dir = project_root / "output"
        output_dir.mkdir(exist_ok=True)

        df = load_data(data_path)
        create_flight_cost_chart(df, output_dir)
        create_time_vs_cost_chart(df, output_dir)
        logger.info("Dashboard generation completed successfully")
    except DataLoadError as e:
        logger.error(f"Error loading data: {e}")
        raise
    except DataValidationError as e:
        logger.error(f"Error validating data: {e}")
        raise
    except ChartGenerationError as e:
        logger.error(f"Error generating chart: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise


if __name__ == "__main__":
    main()
