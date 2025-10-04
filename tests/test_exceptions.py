"""Tests for custom exceptions in the dashboard.

These tests verify that custom exceptions are raised appropriately in various
error scenarios, including file not found, empty dataframes, missing columns,
and chart generation failures.
"""

import pandas as pd
import pytest
from pathlib import Path

from scripts.dashboard import (
    load_data,
    create_flight_cost_chart,
    create_time_vs_cost_chart,
)
from scripts.exceptions import (
    DataLoadError,
    DataValidationError,
    MissingColumnError,
    ChartGenerationError,
)


class TestDataLoadError:
    """Test DataLoadError exception scenarios."""

    def test_file_not_found(self, tmp_path):
        """Test that DataLoadError is raised when CSV file doesn't exist."""
        non_existent_path = tmp_path / "non_existent.csv"

        with pytest.raises(DataLoadError) as exc_info:
            load_data(non_existent_path)

        assert "CSV file not found" in str(exc_info.value)
        assert str(non_existent_path) in str(exc_info.value)

    def test_corrupted_csv(self, tmp_path):
        """Test that DataLoadError is raised when CSV parsing fails."""
        corrupted_csv = tmp_path / "corrupted.csv"
        # Create a CSV with mismatched quotes that pandas can't parse
        corrupted_csv.write_text('col1,col2\n"unclosed quote,value\nnormal,row')

        with pytest.raises(DataLoadError) as exc_info:
            load_data(corrupted_csv)

        assert "Failed to read CSV file" in str(exc_info.value)


class TestDataValidationError:
    """Test DataValidationError exception scenarios."""

    def test_empty_dataframe(self, tmp_path):
        """Test that DataValidationError is raised for empty CSV."""
        empty_csv = tmp_path / "empty.csv"
        # Create CSV with headers but no data rows
        empty_csv.write_text("Destination,Airport\n")

        with pytest.raises(DataValidationError) as exc_info:
            load_data(empty_csv)

        assert "empty" in str(exc_info.value).lower()

    def test_empty_dataframe_in_chart_creation(self):
        """Test DataValidationError when creating chart from empty df."""
        empty_df = pd.DataFrame()
        output_dir = Path(".")

        with pytest.raises(DataValidationError) as exc_info:
            create_flight_cost_chart(empty_df, output_dir)

        assert "empty" in str(exc_info.value).lower()


class TestMissingColumnError:
    """Test MissingColumnError exception scenarios."""

    def test_missing_single_column(self, tmp_path):
        """Test MissingColumnError when one required column is missing."""
        csv_path = tmp_path / "missing_column.csv"
        # Create CSV without "Flight Cost (GBP)" column
        csv_data = (
            "Destination,Airport,Flight Time (hrs),Avg Temp (°C),UV Index,"
            "Monthly Living Cost (GBP),Meal Cost (GBP),Beer Cost (GBP),"
            "Weed Cost (GBP per gram)\n"
            "Barcelona,Exeter,2.5,18.0,7,2500,15.0,5.0,10.0"
        )
        csv_path.write_text(csv_data)

        with pytest.raises(MissingColumnError) as exc_info:
            load_data(csv_path)

        assert "Flight Cost (GBP)" in str(exc_info.value)
        assert "missing" in str(exc_info.value).lower()

    def test_missing_multiple_columns(self, tmp_path):
        """Test MissingColumnError when multiple required columns missing."""
        csv_path = tmp_path / "missing_columns.csv"
        # Create CSV with only two columns
        csv_data = """Destination,Airport
Barcelona,Exeter"""
        csv_path.write_text(csv_data)

        with pytest.raises(MissingColumnError) as exc_info:
            load_data(csv_path)

        # Should mention multiple columns are missing
        assert "missing" in str(exc_info.value).lower()
        # Should show available columns
        assert "Available columns" in str(exc_info.value)

    def test_missing_column_in_chart_creation(self):
        """Test MissingColumnError creating chart with missing columns."""
        # Create dataframe without required columns for chart
        df = pd.DataFrame(
            {
                "Destination": ["Barcelona"],
                "Airport": ["Exeter"],
            }
        )
        output_dir = Path(".")

        with pytest.raises(MissingColumnError) as exc_info:
            create_flight_cost_chart(df, output_dir)

        assert "Flight Cost (GBP)" in str(exc_info.value)


class TestChartGenerationError:
    """Test ChartGenerationError exception scenarios."""

    def test_chart_save_to_invalid_directory(self, tmp_path):
        """Test ChartGenerationError when output dir not writable."""
        project_root = Path(__file__).resolve().parents[1]
        csv_path = project_root / "data" / "dummy_data.csv"
        df = load_data(csv_path)

        # Try to save to a file (not a directory)
        invalid_output = tmp_path / "file.txt"
        invalid_output.write_text("test")

        with pytest.raises(ChartGenerationError) as exc_info:
            create_flight_cost_chart(df, invalid_output)

        assert "flight_costs" in str(exc_info.value)


class TestExceptionHierarchy:
    """Test exception inheritance and attributes."""

    def test_all_exceptions_inherit_from_base(self):
        """Test that all custom exceptions inherit from DashboardError."""
        from scripts.exceptions import DashboardError

        assert issubclass(DataLoadError, DashboardError)
        assert issubclass(DataValidationError, DashboardError)
        assert issubclass(MissingColumnError, DataValidationError)
        assert issubclass(ChartGenerationError, DashboardError)

    def test_data_load_error_with_path(self):
        """Test that DataLoadError stores the path attribute."""
        error = DataLoadError("Test error", path="/test/path.csv")
        assert error.path == "/test/path.csv"
        assert "/test/path.csv" in str(error)

    def test_missing_column_error_attributes(self):
        """Test that MissingColumnError stores column information."""
        missing_cols = ["Column1", "Column2"]
        available_cols = ["ColumnA", "ColumnB"]

        error = MissingColumnError(missing_cols, available_cols)
        assert error.missing_columns == missing_cols
        assert error.available_columns == available_cols
        assert "Column1" in str(error)
        assert "Column2" in str(error)

    def test_chart_generation_error_with_chart_type(self):
        """Test that ChartGenerationError stores the chart_type attribute."""
        error = ChartGenerationError("Test error", chart_type="test_chart")
        assert error.chart_type == "test_chart"
        assert "test_chart" in str(error)


class TestSuccessfulOperation:
    """Test that no exceptions are raised in successful scenarios."""

    def test_successful_data_load(self):
        """Test that loading valid data doesn't raise exceptions."""
        project_root = Path(__file__).resolve().parents[1]
        csv_path = project_root / "data" / "dummy_data.csv"

        # Should not raise any exception
        df = load_data(csv_path)
        assert not df.empty
        assert len(df) > 0

    def test_successful_chart_generation(self, tmp_path):
        """Test that generating charts with valid data doesn't raise exceptions."""
        project_root = Path(__file__).resolve().parents[1]
        csv_path = project_root / "data" / "dummy_data.csv"
        df = load_data(csv_path)

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Should not raise any exception
        create_flight_cost_chart(df, output_dir)
        create_time_vs_cost_chart(df, output_dir)

        # Verify charts were created
        assert (output_dir / "flight_costs.html").exists()
        assert (output_dir / "flight_time_vs_cost.html").exists()
