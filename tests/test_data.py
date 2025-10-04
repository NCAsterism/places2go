"""Tests for the dashboard data loading functions.

These tests run against the dummy dataset included in the repository.  They
verify that the DataFrame is loaded with the correct columns and that all
numeric columns have numeric dtypes.
"""

import pandas as pd
from pathlib import Path

from scripts.dashboard import load_data


def test_load_data_types(tmp_path):
    """Ensure numeric columns are loaded with numeric dtypes."""
    project_root = Path(__file__).resolve().parents[1]
    csv_path = project_root / "data" / "dummy_data.csv"
    df = load_data(csv_path)
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
    # Check that each numeric column has a numeric dtype
    for col in numeric_cols:
        assert pd.api.types.is_numeric_dtype(df[col]), f"Column {col} should be numeric"


def test_load_data_columns():
    """Ensure all expected columns are present in the loaded DataFrame."""
    project_root = Path(__file__).resolve().parents[1]
    csv_path = project_root / "data" / "dummy_data.csv"
    df = load_data(csv_path)
    expected_columns = {
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
    assert set(df.columns) == expected_columns
