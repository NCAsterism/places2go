# Data Validation Rules

This document describes the data validation rules applied to CSV data when loading into the dashboard.

## Overview

The `validate_dataframe()` function in `scripts/dashboard.py` performs comprehensive validation checks on all loaded data to ensure data quality and prevent processing errors.

## Validation Checks

### 1. Empty DataFrame Check
- **Rule**: DataFrame must not be empty
- **Error**: `DataValidationError: DataFrame is empty. No data to process.`
- **Purpose**: Ensures there is actual data to process

### 2. Required Columns
All of the following columns must be present in the dataset:

- `Destination`
- `Airport`
- `Flight Cost (GBP)`
- `Flight Time (hrs)`
- `Avg Temp (°C)`
- `UV Index`
- `Monthly Living Cost (GBP)`
- `Meal Cost (GBP)`
- `Beer Cost (GBP)`
- `Weed Cost (GBP per gram)`

**Error**: `MissingColumnError: Missing required columns: <column names>`

### 3. Data Types
All numeric columns must contain numeric data types (int or float):

- `Flight Cost (GBP)`
- `Flight Time (hrs)`
- `Avg Temp (°C)`
- `UV Index`
- `Monthly Living Cost (GBP)`
- `Meal Cost (GBP)`
- `Beer Cost (GBP)`
- `Weed Cost (GBP per gram)`

**Error**: `DataValidationError: Columns must be numeric: <column names>`

**Note**: Columns containing only null/NaN values are considered valid, as they will be properly handled as numeric types during processing.

### 4. Null Values in Critical Columns
The following critical columns must not contain null values:

- `Destination`
- `Airport`
- `Flight Cost (GBP)`
- `Flight Time (hrs)`

**Error**: `DataValidationError: Critical columns contain null values: <column name> (<count> nulls)`

**Note**: Non-critical columns (e.g., `Avg Temp (°C)`, `UV Index`) may contain null values, which will be handled appropriately during visualization.

### 5. Value Range Validation

#### Cost Columns (must be > 0)
All cost-related columns must contain positive values:

- `Flight Cost (GBP)`
- `Monthly Living Cost (GBP)`
- `Meal Cost (GBP)`
- `Beer Cost (GBP)`
- `Weed Cost (GBP per gram)`

**Error**: `DataValidationError: Cost columns must contain values > 0: <column name> (<count> invalid values)`

#### Flight Time (must be > 0)
Flight time must be a positive value.

**Error**: `DataValidationError: Flight Time (hrs) must be > 0 (<count> invalid values)`

## Automatic Validation

Validation is automatically performed when loading data using the `load_data()` function:

```python
from scripts.dashboard import load_data
from pathlib import Path

# Validation runs automatically
df = load_data(Path("data/dummy_data.csv"))
```

If validation fails, an exception is raised with a descriptive error message indicating which rule was violated.

## Exception Types

The validation system uses custom exceptions defined in `scripts/exceptions.py`:

- `DataValidationError`: Base exception for all validation errors
- `MissingColumnError`: Specifically for missing required columns (inherits from `DataValidationError`)

## Example Error Messages

### Missing Columns
```
MissingColumnError: Missing required columns: Flight Cost (GBP), Flight Time (hrs)
```

### Null Values in Critical Columns
```
DataValidationError: Critical columns contain null values: Destination (2 nulls), Airport (1 nulls)
```

### Invalid Value Ranges
```
DataValidationError: Cost columns must contain values > 0: Flight Cost (GBP) (1 invalid values)
```

## Testing

All validation rules are thoroughly tested in `tests/test_validation.py`, which includes:

- Tests for each validation rule
- Tests for multiple validation failures
- Tests for edge cases (e.g., all null columns)
- Integration tests with `load_data()`

Run the tests with:
```bash
pytest tests/test_validation.py -v
```
