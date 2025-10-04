"""Custom exceptions for the destination dashboard.

This module defines domain-specific exceptions for better error handling and
debugging throughout the application.
"""


class DataLoadError(Exception):
    """Raised when CSV file cannot be loaded or parsed."""

    pass


class DataValidationError(Exception):
    """Raised when data does not meet validation requirements."""

    pass


class MissingColumnError(DataValidationError):
    """Raised when required columns are missing from the dataset."""

    pass


class ChartGenerationError(Exception):
    """Raised when chart creation fails."""

    pass
