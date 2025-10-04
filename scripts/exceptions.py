"""
exceptions.py
-------------

Custom exception classes for domain-specific errors in the destination dashboard.

This module defines exception classes that provide clear error messages for various
failure scenarios that can occur when loading data, validating data, and generating
charts.

Exception Hierarchy:
    Exception
    └── DashboardError (base class for all dashboard exceptions)
        ├── DataLoadError (CSV loading failures)
        ├── DataValidationError (invalid data format)
        │   └── MissingColumnError (required columns missing)
        └── ChartGenerationError (chart creation failures)

Usage Example:
    from scripts.exceptions import DataLoadError, MissingColumnError

    if not csv_path.exists():
        raise DataLoadError(f"CSV file not found: {csv_path}")

    if "Flight Cost (GBP)" not in df.columns:
        raise MissingColumnError("Flight Cost (GBP)", list(df.columns))
"""


class DashboardError(Exception):
    """Base class for all dashboard-related exceptions.

    This serves as the parent class for all custom exceptions in the dashboard
    application, making it easy to catch all dashboard-specific errors.
    """

    pass


class DataLoadError(DashboardError):
    """Raised when CSV data cannot be loaded.

    This exception is raised when there are issues reading the CSV file, such as:
    - File not found
    - File not readable
    - Corrupted CSV format
    - Permission errors

    Args:
        message: Description of the loading error.
        path: Optional path to the CSV file that failed to load.

    Example:
        raise DataLoadError("Failed to read CSV file", path="/data/dummy_data.csv")
    """

    def __init__(self, message: str, path: str = None):
        self.path = path
        if path:
            super().__init__(f"{message}: {path}")
        else:
            super().__init__(message)


class DataValidationError(DashboardError):
    """Raised when data format is invalid or doesn't meet requirements.

    This exception is raised when loaded data doesn't meet expected requirements:
    - Invalid data types
    - Empty dataframe
    - Unexpected data structure
    - Invalid numeric values

    Args:
        message: Description of the validation error.

    Example:
        raise DataValidationError("DataFrame is empty")
    """

    pass


class MissingColumnError(DataValidationError):
    """Raised when required columns are missing from the dataset.

    This exception is raised when one or more required columns are not present
    in the loaded dataframe. It provides clear information about which columns
    are missing and which columns are available.

    Args:
        missing_columns: Single column name or list of missing column names.
        available_columns: Optional list of columns that are available.

    Example:
        raise MissingColumnError(
            "Flight Cost (GBP)",
            available_columns=["Destination", "Airport"]
        )
    """

    def __init__(self, missing_columns, available_columns=None):
        if isinstance(missing_columns, str):
            missing_columns = [missing_columns]

        self.missing_columns = missing_columns
        self.available_columns = available_columns

        if len(missing_columns) == 1:
            message = f"Required column missing: {missing_columns[0]}"
        else:
            message = f"Required columns missing: {', '.join(missing_columns)}"

        if available_columns:
            message += f"\nAvailable columns: {', '.join(available_columns)}"

        super().__init__(message)


class ChartGenerationError(DashboardError):
    """Raised when chart generation fails.

    This exception is raised when there are issues creating or saving charts:
    - Plotly figure creation errors
    - File writing failures
    - Invalid chart parameters
    - Output directory issues

    Args:
        message: Description of the chart generation error.
        chart_type: Optional name of the chart type that failed.

    Example:
        raise ChartGenerationError(
            "Failed to save chart to file",
            chart_type="flight_costs"
        )
    """

    def __init__(self, message: str, chart_type: str = None):
        self.chart_type = chart_type
        if chart_type:
            super().__init__(f"Chart generation failed ({chart_type}): {message}")
        else:
            super().__init__(f"Chart generation failed: {message}")
