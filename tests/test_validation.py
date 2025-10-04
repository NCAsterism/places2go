"""Tests for data validation logic.

These tests verify that the validate_dataframe() function correctly detects
various data quality issues and raises appropriate exceptions with helpful
error messages.
"""

import pandas as pd
import pytest
from pathlib import Path

from scripts.dashboard import validate_dataframe, load_data
from scripts.exceptions import DataValidationError, MissingColumnError


def test_validate_empty_dataframe():
    """Test that validation rejects empty DataFrames."""
    df = pd.DataFrame()
    with pytest.raises(DataValidationError, match="DataFrame is empty"):
        validate_dataframe(df)


def test_validate_missing_columns():
    """Test that validation detects missing required columns."""
    df = pd.DataFrame(
        {
            "Destination": ["Paris"],
            "Airport": ["Exeter"],
            "Flight Cost (GBP)": [100],
        }
    )
    with pytest.raises(MissingColumnError, match="Missing required columns"):
        validate_dataframe(df)


def test_validate_all_required_columns():
    """Test that validation detects multiple missing columns."""
    df = pd.DataFrame(
        {
            "Destination": ["Paris"],
            "Airport": ["Exeter"],
        }
    )
    with pytest.raises(MissingColumnError) as exc_info:
        validate_dataframe(df)
    error_msg = str(exc_info.value)
    assert "Flight Cost (GBP)" in error_msg
    assert "Flight Time (hrs)" in error_msg


def test_validate_non_numeric_columns():
    """Test that validation detects non-numeric data in numeric columns."""
    df = pd.DataFrame(
        {
            "Destination": ["Paris"],
            "Airport": ["Exeter"],
            "Flight Cost (GBP)": ["expensive"],  # Should be numeric
            "Flight Time (hrs)": [2.5],
            "Avg Temp (°C)": [20],
            "UV Index": [5],
            "Monthly Living Cost (GBP)": [800],
            "Meal Cost (GBP)": [10],
            "Beer Cost (GBP)": [3],
            "Weed Cost (GBP per gram)": [10],
        }
    )
    with pytest.raises(DataValidationError, match="Columns must be numeric"):
        validate_dataframe(df)


def test_validate_null_in_critical_columns():
    """Test that validation detects null values in critical columns."""
    df = pd.DataFrame(
        {
            "Destination": [None],
            "Airport": ["Exeter"],
            "Flight Cost (GBP)": [100.0],
            "Flight Time (hrs)": [2.5],
            "Avg Temp (°C)": [20.0],
            "UV Index": [5.0],
            "Monthly Living Cost (GBP)": [800.0],
            "Meal Cost (GBP)": [10.0],
            "Beer Cost (GBP)": [3.0],
            "Weed Cost (GBP per gram)": [10.0],
        }
    )
    with pytest.raises(
        DataValidationError, match="Critical columns contain null values"
    ):
        validate_dataframe(df)


def test_validate_negative_cost():
    """Test that validation rejects negative cost values."""
    df = pd.DataFrame(
        {
            "Destination": ["Paris"],
            "Airport": ["Exeter"],
            "Flight Cost (GBP)": [-100.0],  # Negative cost
            "Flight Time (hrs)": [2.5],
            "Avg Temp (°C)": [20.0],
            "UV Index": [5.0],
            "Monthly Living Cost (GBP)": [800.0],
            "Meal Cost (GBP)": [10.0],
            "Beer Cost (GBP)": [3.0],
            "Weed Cost (GBP per gram)": [10.0],
        }
    )
    with pytest.raises(
        DataValidationError, match="Cost columns must contain values > 0"
    ):
        validate_dataframe(df)


def test_validate_zero_cost():
    """Test that validation rejects zero cost values."""
    df = pd.DataFrame(
        {
            "Destination": ["Paris"],
            "Airport": ["Exeter"],
            "Flight Cost (GBP)": [100.0],
            "Flight Time (hrs)": [2.5],
            "Avg Temp (°C)": [20.0],
            "UV Index": [5.0],
            "Monthly Living Cost (GBP)": [0.0],  # Zero cost
            "Meal Cost (GBP)": [10.0],
            "Beer Cost (GBP)": [3.0],
            "Weed Cost (GBP per gram)": [10.0],
        }
    )
    with pytest.raises(
        DataValidationError, match="Cost columns must contain values > 0"
    ):
        validate_dataframe(df)


def test_validate_negative_flight_time():
    """Test that validation rejects negative flight times."""
    df = pd.DataFrame(
        {
            "Destination": ["Paris"],
            "Airport": ["Exeter"],
            "Flight Cost (GBP)": [100.0],
            "Flight Time (hrs)": [-2.5],  # Negative time
            "Avg Temp (°C)": [20.0],
            "UV Index": [5.0],
            "Monthly Living Cost (GBP)": [800.0],
            "Meal Cost (GBP)": [10.0],
            "Beer Cost (GBP)": [3.0],
            "Weed Cost (GBP per gram)": [10.0],
        }
    )
    with pytest.raises(DataValidationError, match="Flight Time \\(hrs\\) must be > 0"):
        validate_dataframe(df)


def test_validate_valid_dataframe():
    """Test that validation passes for a valid DataFrame."""
    df = pd.DataFrame(
        {
            "Destination": ["Paris", "Rome"],
            "Airport": ["Exeter", "Bristol"],
            "Flight Cost (GBP)": [100.0, 150.0],
            "Flight Time (hrs)": [2.5, 3.0],
            "Avg Temp (°C)": [20.0, 25.0],
            "UV Index": [5.0, 7.0],
            "Monthly Living Cost (GBP)": [800.0, 900.0],
            "Meal Cost (GBP)": [10.0, 12.0],
            "Beer Cost (GBP)": [3.0, 3.5],
            "Weed Cost (GBP per gram)": [10.0, 11.0],
        }
    )
    # Should not raise any exception
    validate_dataframe(df)


def test_validate_allows_null_in_non_critical_columns():
    """Test that validation allows null values in non-critical columns."""
    df = pd.DataFrame(
        {
            "Destination": ["Paris"],
            "Airport": ["Exeter"],
            "Flight Cost (GBP)": [100.0],
            "Flight Time (hrs)": [2.5],
            "Avg Temp (°C)": [None],  # Null in non-critical column
            "UV Index": [None],  # Null in non-critical column
            "Monthly Living Cost (GBP)": [800.0],
            "Meal Cost (GBP)": [10.0],
            "Beer Cost (GBP)": [3.0],
            "Weed Cost (GBP per gram)": [10.0],
        }
    )
    # Should not raise any exception
    validate_dataframe(df)


def test_load_data_with_invalid_csv(tmp_path):
    """Test that load_data raises validation error for invalid CSV."""
    # Create a CSV with missing columns
    csv_path = tmp_path / "invalid.csv"
    csv_content = "Destination,Airport\nParis,Exeter\n"
    csv_path.write_text(csv_content)

    with pytest.raises(MissingColumnError):
        load_data(csv_path)


def test_load_data_with_invalid_values(tmp_path):
    """Test that load_data raises validation error for invalid values."""
    # Create a CSV with negative costs
    csv_path = tmp_path / "invalid.csv"
    csv_content = (
        "Destination,Airport,Flight Cost (GBP),Flight Time (hrs),"
        "Avg Temp (°C),UV Index,Monthly Living Cost (GBP),"
        "Meal Cost (GBP),Beer Cost (GBP),Weed Cost (GBP per gram)\n"
        "Paris,Exeter,-100,2.5,20,5,800,10,3,10\n"
    )
    csv_path.write_text(csv_content)

    with pytest.raises(
        DataValidationError, match="Cost columns must contain values > 0"
    ):
        load_data(csv_path)


def test_load_data_valid_csv():
    """Test that load_data successfully loads valid CSV."""
    project_root = Path(__file__).resolve().parents[1]
    csv_path = project_root / "data" / "dummy_data.csv"
    df = load_data(csv_path)

    # Should return a valid DataFrame
    assert not df.empty
    assert len(df) > 0
    assert "Destination" in df.columns


def test_validate_multiple_null_values():
    """Test that validation reports multiple null values correctly."""
    df = pd.DataFrame(
        {
            "Destination": [None, "Paris", None],
            "Airport": ["Exeter", None, "Bristol"],
            "Flight Cost (GBP)": [100.0, 150.0, 200.0],
            "Flight Time (hrs)": [2.5, 3.0, 3.5],
            "Avg Temp (°C)": [20.0, 25.0, 22.0],
            "UV Index": [5.0, 7.0, 6.0],
            "Monthly Living Cost (GBP)": [800.0, 900.0, 850.0],
            "Meal Cost (GBP)": [10.0, 12.0, 11.0],
            "Beer Cost (GBP)": [3.0, 3.5, 3.2],
            "Weed Cost (GBP per gram)": [10.0, 11.0, 10.5],
        }
    )
    with pytest.raises(DataValidationError) as exc_info:
        validate_dataframe(df)
    error_msg = str(exc_info.value)
    assert "Destination" in error_msg
    assert "2 nulls" in error_msg


def test_validate_multiple_invalid_ranges():
    """Test that validation reports multiple invalid range values correctly."""
    df = pd.DataFrame(
        {
            "Destination": ["Paris", "Rome"],
            "Airport": ["Exeter", "Bristol"],
            "Flight Cost (GBP)": [-100.0, 150.0],  # One invalid
            "Flight Time (hrs)": [2.5, 3.0],
            "Avg Temp (°C)": [20.0, 25.0],
            "UV Index": [5.0, 7.0],
            "Monthly Living Cost (GBP)": [0.0, -50.0],  # Two invalid
            "Meal Cost (GBP)": [10.0, 12.0],
            "Beer Cost (GBP)": [3.0, 3.5],
            "Weed Cost (GBP per gram)": [10.0, 11.0],
        }
    )
    with pytest.raises(DataValidationError) as exc_info:
        validate_dataframe(df)
    error_msg = str(exc_info.value)
    assert "Cost columns must contain values > 0" in error_msg
