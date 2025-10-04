# GitHub Issues for Places2Go - Detailed Task List

This document contains detailed GitHub issues that can be created and assigned to GitHub agents or contributors. Each issue is self-contained with clear acceptance criteria.

---

## Phase 2: Enhanced Testing & Code Quality (v0.2.0)

### Issue #1: Add Tests for Chart Generation Functions
**Labels:** `testing`, `phase-2`, `high-priority`  
**Assignee:** GitHub Agent  
**Estimated Effort:** 4 hours

**Description:**
Add comprehensive test coverage for the chart generation functions in `scripts/dashboard.py`. Currently, only data loading is tested (44% coverage). This task will increase coverage to 60%+.

**Tasks:**
- [ ] Create `tests/test_charts.py` file
- [ ] Add test for `create_flight_cost_chart()`:
  - Test HTML file is created in correct location
  - Test file contains expected Plotly chart structure
  - Test chart has correct data points
  - Test error handling for empty DataFrame
  - Test error handling for missing output directory
- [ ] Add test for `create_time_vs_cost_chart()`:
  - Test HTML file is created
  - Test bubble size mapping is correct
  - Test color mapping per destination
  - Test hover text contains expected fields
  - Test error handling for missing columns

**Acceptance Criteria:**
- [ ] All new tests passing
- [ ] Code coverage increases to 60%+
- [ ] Tests use pytest fixtures for temp directories
- [ ] Tests clean up generated files
- [ ] Error cases are documented

**Technical Notes:**
```python
# Example test structure
import pytest
from pathlib import Path
from scripts.dashboard import create_flight_cost_chart

def test_create_flight_cost_chart_creates_file(tmp_path, sample_df):
    """Test that chart function creates HTML file."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    
    create_flight_cost_chart(sample_df, output_dir)
    
    assert (output_dir / "flight_costs.html").exists()
```

**Dependencies:**
- Requires `pytest-mock` for mocking file operations
- Requires sample DataFrame fixture

---

### Issue #2: Add Integration Test for Full Dashboard Workflow
**Labels:** `testing`, `phase-2`, `integration`, `high-priority`  
**Assignee:** GitHub Agent  
**Estimated Effort:** 2 hours

**Description:**
Create an end-to-end integration test that validates the complete dashboard workflow from data loading to chart generation.

**Tasks:**
- [ ] Create `tests/test_integration.py`
- [ ] Implement `test_full_dashboard_workflow()`:
  - Load CSV data
  - Generate both charts
  - Verify both HTML files exist
  - Verify files are non-empty
  - Verify files contain Plotly chart markers
- [ ] Test with actual dummy_data.csv
- [ ] Test cleanup of generated files

**Acceptance Criteria:**
- [ ] Integration test passes consistently
- [ ] Test uses temp directory for outputs
- [ ] Test verifies data flow through entire pipeline
- [ ] Test runs in under 5 seconds
- [ ] Test can be run independently

**Technical Notes:**
```python
def test_full_dashboard_workflow(tmp_path):
    """Test complete workflow from data load to chart generation."""
    # Setup
    project_root = Path(__file__).resolve().parents[1]
    data_path = project_root / "data" / "dummy_data.csv"
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    
    # Execute full workflow
    df = load_data(data_path)
    create_flight_cost_chart(df, output_dir)
    create_time_vs_cost_chart(df, output_dir)
    
    # Verify
    assert (output_dir / "flight_costs.html").exists()
    assert (output_dir / "flight_time_vs_cost.html").exists()
    assert (output_dir / "flight_costs.html").stat().st_size > 1000
```

---

### Issue #3: Add Type Hints to All Functions in dashboard.py
**Labels:** `code-quality`, `phase-2`, `medium-priority`  
**Assignee:** GitHub Agent  
**Estimated Effort:** 2 hours

**Description:**
Add Python type hints to all functions in `scripts/dashboard.py` to improve code clarity and enable static type checking with mypy.

**Tasks:**
- [ ] Add type hints to `load_data()` function
- [ ] Add type hints to `create_flight_cost_chart()` function
- [ ] Add type hints to `create_time_vs_cost_chart()` function
- [ ] Add type hints to `main()` function
- [ ] Add necessary imports from `typing` module
- [ ] Update function docstrings to match type hints

**Acceptance Criteria:**
- [ ] All functions have complete type annotations
- [ ] Import statements include necessary typing modules
- [ ] Type hints match docstring descriptions
- [ ] Code passes mypy static type checking (when configured)
- [ ] No breaking changes to existing functionality

**Example Implementation:**
```python
from pathlib import Path
from typing import Optional
import pandas as pd
import plotly.express as px

def load_data(csv_path: Path) -> pd.DataFrame:
    """Read the destination dataset from a CSV file.
    
    Args:
        csv_path: Path to the CSV file containing destination data.
    
    Returns:
        A pandas DataFrame with the dataset.
    """
    # ... implementation
```

**Reference:**
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [Python Type Checking Guide](https://realpython.com/python-type-checking/)

---

### Issue #4: Configure mypy for Static Type Checking
**Labels:** `code-quality`, `phase-2`, `tooling`, `medium-priority`  
**Assignee:** GitHub Agent  
**Estimated Effort:** 1 hour

**Description:**
Set up mypy for static type checking and configure it in the project toolchain.

**Tasks:**
- [ ] Add `mypy` to requirements.txt
- [ ] Create `mypy.ini` or add `[tool.mypy]` section in `pyproject.toml`
- [ ] Configure mypy settings:
  - Enable strict mode for project files
  - Ignore missing imports for third-party libraries
  - Set Python version to 3.9+
- [ ] Add mypy check to CI/CD pipeline (`.github/workflows/ci.yml`)
- [ ] Run mypy and fix any type errors found
- [ ] Document mypy usage in CONTRIBUTING.md

**Acceptance Criteria:**
- [ ] mypy configuration file exists
- [ ] mypy passes without errors on all project files
- [ ] CI/CD pipeline runs mypy checks
- [ ] Documentation updated with mypy instructions

**Configuration Example:**
```toml
# In pyproject.toml
[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
ignore_missing_imports = true
exclude = [
    "tests/",
    ".venv/",
]
```

**CI/CD Addition:**
```yaml
- name: Type check with mypy
  run: |
    mypy scripts/
```

---

### Issue #5: Add Logging Framework Throughout Dashboard
**Labels:** `code-quality`, `phase-2`, `high-priority`  
**Assignee:** GitHub Agent  
**Estimated Effort:** 3 hours

**Description:**
Replace print statements with proper logging using Python's logging module. This will improve debugging and production monitoring.

**Tasks:**
- [ ] Set up logging configuration in `scripts/dashboard.py`
- [ ] Replace all `print()` statements with appropriate log levels:
  - Info: Normal operation messages
  - Debug: Detailed diagnostic information
  - Warning: Unexpected situations that don't prevent execution
  - Error: Error conditions
- [ ] Add logging to file in addition to console
- [ ] Create `logs/` directory in `.gitignore`
- [ ] Add logging configuration examples to documentation

**Acceptance Criteria:**
- [ ] No print statements remain (except in `if __name__ == '__main__'` if needed)
- [ ] All log messages use appropriate levels
- [ ] Log format includes timestamp, level, and message
- [ ] Logs are written to both console and file
- [ ] Log files are excluded from git
- [ ] Documentation includes logging examples

**Implementation Example:**
```python
import logging
from pathlib import Path

# Configure logging
log_dir = Path(__file__).resolve().parents[1] / 'logs'
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'dashboard.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Usage
logger.info(f"Loading data from {csv_path}")
logger.debug(f"DataFrame shape: {df.shape}")
logger.error(f"Failed to create chart: {error}")
```

---

### Issue #6: Add Custom Exceptions for Domain Errors
**Labels:** `code-quality`, `phase-2`, `error-handling`, `medium-priority`  
**Assignee:** GitHub Agent  
**Estimated Effort:** 2 hours

**Description:**
Create custom exception classes for domain-specific errors to improve error handling and debugging.

**Tasks:**
- [ ] Create `scripts/exceptions.py` module
- [ ] Define custom exception classes:
  - `DataLoadError` - For CSV loading failures
  - `DataValidationError` - For invalid data format
  - `ChartGenerationError` - For chart creation failures
  - `MissingColumnError` - For required columns missing
- [ ] Update `dashboard.py` to use custom exceptions
- [ ] Add error handling in all functions
- [ ] Write tests for exception scenarios
- [ ] Document exceptions in module docstrings

**Acceptance Criteria:**
- [ ] Custom exception module created
- [ ] All exceptions inherit from appropriate base classes
- [ ] Exceptions include helpful error messages
- [ ] Functions raise appropriate exceptions
- [ ] Tests verify exception behavior
- [ ] Exceptions documented

**Implementation Example:**
```python
# scripts/exceptions.py
"""Custom exceptions for the Places2Go dashboard."""

class DashboardError(Exception):
    """Base exception for dashboard errors."""
    pass

class DataLoadError(DashboardError):
    """Raised when data cannot be loaded from source."""
    pass

class DataValidationError(DashboardError):
    """Raised when data fails validation checks."""
    
    def __init__(self, missing_columns: list[str]):
        self.missing_columns = missing_columns
        super().__init__(
            f"Required columns missing: {', '.join(missing_columns)}"
        )

class ChartGenerationError(DashboardError):
    """Raised when chart generation fails."""
    pass
```

---

### Issue #7: Add Data Validation with Error Handling
**Labels:** `code-quality`, `phase-2`, `high-priority`, `error-handling`  
**Assignee:** GitHub Agent  
**Estimated Effort:** 3 hours

**Description:**
Add comprehensive data validation to ensure CSV data meets requirements before processing.

**Tasks:**
- [ ] Create `validate_dataframe()` function
- [ ] Check for required columns
- [ ] Validate data types
- [ ] Check for null values in critical columns
- [ ] Validate value ranges (e.g., costs > 0)
- [ ] Add validation to `load_data()` function
- [ ] Write tests for validation logic
- [ ] Add validation for empty DataFrames

**Acceptance Criteria:**
- [ ] Validation function implemented and tested
- [ ] All data quality issues detected
- [ ] Helpful error messages for each validation failure
- [ ] Validation runs automatically on data load
- [ ] Tests cover all validation scenarios
- [ ] Documentation includes validation rules

**Implementation Example:**
```python
from scripts.exceptions import DataValidationError, MissingColumnError

def validate_dataframe(df: pd.DataFrame) -> None:
    """Validate DataFrame meets requirements.
    
    Args:
        df: DataFrame to validate
        
    Raises:
        DataValidationError: If validation fails
        MissingColumnError: If required columns missing
    """
    required_columns = [
        'Destination', 'Airport', 'Flight Cost (GBP)',
        'Flight Time (hrs)', 'Avg Temp (°C)'
    ]
    
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise MissingColumnError(missing)
    
    if df.empty:
        raise DataValidationError("DataFrame is empty")
    
    # Validate positive costs
    cost_col = 'Flight Cost (GBP)'
    if (df[cost_col] <= 0).any():
        raise DataValidationError(f"{cost_col} contains non-positive values")
```

---

### Issue #8: Add Pre-commit Hooks for Code Quality
**Labels:** `tooling`, `phase-2`, `developer-experience`, `medium-priority`  
**Assignee:** GitHub Agent  
**Estimated Effort:** 2 hours

**Description:**
Set up pre-commit hooks to automatically format and lint code before commits.

**Tasks:**
- [ ] Add `pre-commit` to requirements.txt
- [ ] Create `.pre-commit-config.yaml` configuration
- [ ] Add hooks for:
  - Black (code formatting)
  - Flake8 (linting)
  - Trailing whitespace removal
  - YAML validation
  - Large file prevention
- [ ] Add pre-commit setup instructions to CONTRIBUTING.md
- [ ] Test pre-commit hooks locally
- [ ] Add CI check that pre-commit hooks were run

**Acceptance Criteria:**
- [ ] Pre-commit configuration file exists
- [ ] All hooks configured and tested
- [ ] Documentation includes setup instructions
- [ ] Hooks run automatically on commit
- [ ] CI verifies hooks were executed

**Configuration Example:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11
        
  - repo: https://github.com/PyCQA/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=88', '--extend-ignore=E203']
        
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```

**Setup Instructions:**
```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

---

## Phase 3: Data Module Architecture (v0.3.0)

### Issue #9: Create Data Module Directory Structure
**Labels:** `architecture`, `phase-3`, `high-priority`  
**Assignee:** GitHub Agent  
**Estimated Effort:** 1 hour

**Description:**
Set up the foundational directory structure for the data module architecture.

**Tasks:**
- [ ] Create `src/` directory
- [ ] Create `src/data/` directory
- [ ] Create `src/data/__init__.py`
- [ ] Create `src/data/sources/` directory
- [ ] Create `src/data/models/` directory
- [ ] Create `src/models/` directory for Pydantic models
- [ ] Add `src/` to Python path in relevant files
- [ ] Update `.gitignore` if needed
- [ ] Create README.md in `src/data/` explaining architecture

**Acceptance Criteria:**
- [ ] All directories created with proper `__init__.py` files
- [ ] Directory structure documented
- [ ] Python can import from new modules
- [ ] No breaking changes to existing code

**Directory Structure:**
```
src/
├── __init__.py
├── data/
│   ├── __init__.py
│   ├── base.py          # Abstract base classes
│   ├── sources/
│   │   ├── __init__.py
│   │   ├── csv_source.py
│   │   ├── api_source.py
│   │   └── weather_api.py
│   └── models/
│       ├── __init__.py
│       └── destination.py
└── README.md
```

---

### Issue #10: Implement Abstract DataSource Base Class
**Labels:** `architecture`, `phase-3`, `high-priority`  
**Assignee:** GitHub Agent  
**Estimated Effort:** 3 hours

**Description:**
Create an abstract base class that defines the interface all data sources must implement.

**Tasks:**
- [ ] Create `src/data/base.py`
- [ ] Define `DataSource` abstract base class
- [ ] Define required methods:
  - `fetch()` - Retrieve data
  - `validate()` - Validate data quality
  - `cache()` - Cache data locally
  - `get_cached()` - Retrieve from cache
- [ ] Add type hints and comprehensive docstrings
- [ ] Create example implementation in docstring
- [ ] Write unit tests for abstract class structure

**Acceptance Criteria:**
- [ ] Abstract base class defined with ABC module
- [ ] All required methods declared as abstract
- [ ] Type hints complete
- [ ] Documentation includes usage examples
- [ ] Tests verify abstract methods enforced

**Implementation:**
```python
from abc import ABC, abstractmethod
from typing import Optional, Any
from datetime import datetime, timedelta
import pandas as pd

class DataSource(ABC):
    """Abstract base class for all data sources.
    
    All data sources must implement fetch(), validate(), and caching methods.
    This ensures consistent interface across different data providers.
    """
    
    def __init__(self, cache_ttl: timedelta = timedelta(hours=24)):
        """Initialize data source.
        
        Args:
            cache_ttl: Time-to-live for cached data
        """
        self.cache_ttl = cache_ttl
        self._cache: Optional[pd.DataFrame] = None
        self._cache_time: Optional[datetime] = None
    
    @abstractmethod
    def fetch(self, **kwargs) -> pd.DataFrame:
        """Fetch data from source.
        
        Returns:
            DataFrame with fetched data
            
        Raises:
            DataLoadError: If fetch fails
        """
        pass
    
    @abstractmethod
    def validate(self, df: pd.DataFrame) -> bool:
        """Validate data quality.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            True if valid, False otherwise
            
        Raises:
            DataValidationError: If critical validation fails
        """
        pass
    
    def get_data(self, use_cache: bool = True, **kwargs) -> pd.DataFrame:
        """Get data, using cache if available and valid.
        
        Args:
            use_cache: Whether to use cached data if available
            **kwargs: Arguments passed to fetch()
            
        Returns:
            DataFrame with data
        """
        if use_cache and self._is_cache_valid():
            return self._cache.copy()
        
        df = self.fetch(**kwargs)
        self.validate(df)
        self._update_cache(df)
        return df
    
    def _is_cache_valid(self) -> bool:
        """Check if cache is still valid."""
        if self._cache is None or self._cache_time is None:
            return False
        return datetime.now() - self._cache_time < self.cache_ttl
    
    def _update_cache(self, df: pd.DataFrame) -> None:
        """Update cache with new data."""
        self._cache = df.copy()
        self._cache_time = datetime.now()
```

---

### Issue #11: Implement Pydantic Models for Data Validation
**Labels:** `architecture`, `phase-3`, `data-modeling`, `high-priority`  
**Assignee:** GitHub Agent  
**Estimated Effort:** 4 hours

**Description:**
Create Pydantic models to represent domain entities with automatic validation.

**Tasks:**
- [ ] Add `pydantic` to requirements.txt (if not already present)
- [ ] Create `src/models/__init__.py`
- [ ] Create `src/models/destination.py` with models:
  - `Destination` - Basic destination info
  - `FlightInfo` - Flight details (cost, time, airport)
  - `WeatherInfo` - Weather and UV data
  - `CostInfo` - Living costs breakdown
- [ ] Add field validators for each model
- [ ] Add example data in docstrings
- [ ] Write tests for model validation
- [ ] Create factory functions for creating models from DataFrame rows

**Acceptance Criteria:**
- [ ] All models defined with proper field types
- [ ] Validation rules enforced automatically
- [ ] Models can be serialized to/from JSON
- [ ] Tests cover validation scenarios
- [ ] Documentation includes examples

**Implementation Example:**
```python
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class FlightInfo(BaseModel):
    """Flight information for a destination."""
    
    origin_airport: str = Field(..., description="Origin airport code (e.g., 'EXT')")
    destination: str = Field(..., description="Destination city name")
    cost_gbp: float = Field(..., gt=0, description="Flight cost in GBP")
    duration_hours: float = Field(..., gt=0, description="Flight duration in hours")
    checked_at: datetime = Field(default_factory=datetime.now)
    
    @validator('origin_airport')
    def validate_airport_code(cls, v):
        """Ensure airport code is uppercase and 3 characters."""
        if len(v) != 3:
            raise ValueError('Airport code must be 3 characters')
        return v.upper()
    
    @validator('cost_gbp')
    def validate_reasonable_cost(cls, v):
        """Ensure cost is within reasonable range."""
        if v > 10000:
            raise ValueError('Flight cost seems unreasonably high')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "origin_airport": "EXT",
                "destination": "Alicante",
                "cost_gbp": 120.50,
                "duration_hours": 2.5,
            }
        }

class WeatherInfo(BaseModel):
    """Weather information for a destination."""
    
    destination: str
    temperature_celsius: float = Field(..., ge=-50, le=60)
    uv_index: int = Field(..., ge=0, le=11)
    conditions: Optional[str] = None
    measured_at: datetime = Field(default_factory=datetime.now)

class CostInfo(BaseModel):
    """Cost of living information."""
    
    destination: str
    monthly_living_gbp: float = Field(..., gt=0)
    meal_cost_gbp: float = Field(..., gt=0)
    beer_cost_gbp: float = Field(..., gt=0)
    transport_monthly_gbp: Optional[float] = Field(None, gt=0)
    
class Destination(BaseModel):
    """Complete destination information."""
    
    name: str
    flight: FlightInfo
    weather: WeatherInfo
    costs: CostInfo
    
    def total_monthly_cost(self) -> float:
        """Calculate estimated total monthly cost including flight amortization."""
        # Amortize flight cost over 3 months
        flight_monthly = self.flight.cost_gbp / 3
        return self.costs.monthly_living_gbp + flight_monthly
```

---

### Issue #12: Refactor CSV Loading into CSVDataSource Class
**Labels:** `refactoring`, `phase-3`, `high-priority`  
**Assignee:** GitHub Agent  
**Estimated Effort:** 3 hours

**Description:**
Migrate the existing CSV loading logic from `dashboard.py` into a proper `CSVDataSource` class that implements the `DataSource` interface.

**Tasks:**
- [ ] Create `src/data/sources/csv_source.py`
- [ ] Implement `CSVDataSource` class extending `DataSource`
- [ ] Move `load_data()` logic into `fetch()` method
- [ ] Add data validation in `validate()` method
- [ ] Add caching logic
- [ ] Update `dashboard.py` to use new CSVDataSource
- [ ] Ensure backward compatibility
- [ ] Write comprehensive tests
- [ ] Update documentation

**Acceptance Criteria:**
- [ ] CSVDataSource fully implements DataSource interface
- [ ] All existing CSV loading functionality preserved
- [ ] dashboard.py uses new CSVDataSource
- [ ] All tests passing
- [ ] Code coverage maintained or improved
- [ ] No breaking changes for existing users

**Implementation:**
```python
# src/data/sources/csv_source.py
from pathlib import Path
import pandas as pd
from src.data.base import DataSource
from scripts.exceptions import DataLoadError, DataValidationError

class CSVDataSource(DataSource):
    """Data source for CSV files."""
    
    def __init__(self, csv_path: Path, **kwargs):
        """Initialize CSV data source.
        
        Args:
            csv_path: Path to CSV file
        """
        super().__init__(**kwargs)
        self.csv_path = Path(csv_path)
        
        if not self.csv_path.exists():
            raise DataLoadError(f"CSV file not found: {csv_path}")
    
    def fetch(self, **kwargs) -> pd.DataFrame:
        """Load data from CSV file.
        
        Returns:
            DataFrame with CSV data
            
        Raises:
            DataLoadError: If CSV cannot be loaded
        """
        try:
            df = pd.read_csv(self.csv_path)
            
            # Convert numeric columns
            numeric_cols = [
                'Flight Cost (GBP)', 'Flight Time (hrs)',
                'Avg Temp (°C)', 'UV Index',
                'Monthly Living Cost (GBP)', 'Meal Cost (GBP)',
                'Beer Cost (GBP)', 'Weed Cost (GBP per gram)',
            ]
            df[numeric_cols] = df[numeric_cols].apply(
                pd.to_numeric, errors='coerce'
            )
            
            return df
            
        except Exception as e:
            raise DataLoadError(f"Failed to load CSV: {e}")
    
    def validate(self, df: pd.DataFrame) -> bool:
        """Validate CSV data quality.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            True if valid
            
        Raises:
            DataValidationError: If validation fails
        """
        required_columns = {
            'Destination', 'Airport', 'Flight Cost (GBP)',
            'Flight Time (hrs)', 'Avg Temp (°C)', 'UV Index'
        }
        
        missing = required_columns - set(df.columns)
        if missing:
            raise DataValidationError(
                f"Missing required columns: {missing}"
            )
        
        if df.empty:
            raise DataValidationError("DataFrame is empty")
        
        # Check for null values in critical columns
        critical_nulls = df[list(required_columns)].isnull().sum()
        if critical_nulls.any():
            raise DataValidationError(
                f"Null values in critical columns: {critical_nulls[critical_nulls > 0]}"
            )
        
        return True

# Usage in dashboard.py
from src.data.sources.csv_source import CSVDataSource

def main():
    project_root = Path(__file__).resolve().parents[1]
    data_path = project_root / 'data' / 'dummy_data.csv'
    
    # Use new data source
    csv_source = CSVDataSource(data_path)
    df = csv_source.get_data()
    
    # Rest of dashboard logic...
```

---

## Quick Reference for Creating Issues

To create these issues on GitHub, you can either:

1. **Manual Creation:** Copy each issue section and paste into GitHub's "New Issue" form
2. **GitHub CLI:** Use the `gh issue create` command
3. **API/Script:** Use GitHub's REST API to batch create issues

### Example GitHub CLI Command:
```bash
gh issue create \
  --title "Add Tests for Chart Generation Functions" \
  --body "$(cat issue_01.md)" \
  --label "testing,phase-2,high-priority" \
  --assignee "@me"
```

---

**Note:** Issues #13-30 covering Phases 4, 5, and 6 can be created following the same detailed format. Would you like me to continue with those phases?
