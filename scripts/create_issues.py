#!/usr/bin/env python
"""
Script to create GitHub issues from the GITHUB_ISSUES.md file.

This script can be run to automatically create all Phase 2 issues
on GitHub. Requires the GitHub CLI (gh) to be installed and authenticated.

Usage:
    python scripts/create_issues.py

Prerequisites:
    - Install GitHub CLI: https://cli.github.com/
    - Authenticate: gh auth login
    - Set repository: gh repo set-default
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, Any

# Issue definitions
ISSUES = [
    {
        "number": 1,
        "title": "Add Tests for Chart Generation Functions",
        "labels": ["testing", "phase-2", "high-priority"],
        "milestone": "v0.2.0",
        "body": """Add comprehensive test coverage for the chart generation functions in `scripts/dashboard.py`. Currently, only data loading is tested (44% coverage). This task will increase coverage to 60%+.

## Tasks
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

## Acceptance Criteria
- [ ] All new tests passing
- [ ] Code coverage increases to 60%+
- [ ] Tests use pytest fixtures for temp directories
- [ ] Tests clean up generated files
- [ ] Error cases are documented

## Technical Notes
```python
# Example test structure
import pytest
from pathlib import Path
from scripts.dashboard import create_flight_cost_chart

def test_create_flight_cost_chart_creates_file(tmp_path, sample_df):
    \"\"\"Test that chart function creates HTML file.\"\"\"
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    
    create_flight_cost_chart(sample_df, output_dir)
    
    assert (output_dir / "flight_costs.html").exists()
```

## Dependencies
- Requires `pytest-mock` for mocking file operations
- Requires sample DataFrame fixture

## Related
- Contributes to Phase 2: Enhanced Testing & Code Quality
- See ROADMAP.md for full context
""",
    },
    {
        "number": 2,
        "title": "Add Integration Test for Full Dashboard Workflow",
        "labels": ["testing", "phase-2", "integration", "high-priority"],
        "milestone": "v0.2.0",
        "body": """Create an end-to-end integration test that validates the complete dashboard workflow from data loading to chart generation.

## Tasks
- [ ] Create `tests/test_integration.py`
- [ ] Implement `test_full_dashboard_workflow()`:
  - Load CSV data
  - Generate both charts
  - Verify both HTML files exist
  - Verify files are non-empty
  - Verify files contain Plotly chart markers
- [ ] Test with actual dummy_data.csv
- [ ] Test cleanup of generated files

## Acceptance Criteria
- [ ] Integration test passes consistently
- [ ] Test uses temp directory for outputs
- [ ] Test verifies data flow through entire pipeline
- [ ] Test runs in under 5 seconds
- [ ] Test can be run independently

## Technical Notes
```python
def test_full_dashboard_workflow(tmp_path):
    \"\"\"Test complete workflow from data load to chart generation.\"\"\"
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

## Related
- Contributes to Phase 2: Enhanced Testing & Code Quality
- Depends on: Issue #1
""",
    },
    {
        "number": 3,
        "title": "Add Type Hints to All Functions in dashboard.py",
        "labels": ["code-quality", "phase-2", "medium-priority"],
        "milestone": "v0.2.0",
        "body": """Add Python type hints to all functions in `scripts/dashboard.py` to improve code clarity and enable static type checking with mypy.

## Tasks
- [ ] Add type hints to `load_data()` function
- [ ] Add type hints to `create_flight_cost_chart()` function
- [ ] Add type hints to `create_time_vs_cost_chart()` function
- [ ] Add type hints to `main()` function
- [ ] Add necessary imports from `typing` module
- [ ] Update function docstrings to match type hints

## Acceptance Criteria
- [ ] All functions have complete type annotations
- [ ] Import statements include necessary typing modules
- [ ] Type hints match docstring descriptions
- [ ] Code passes mypy static type checking (when configured)
- [ ] No breaking changes to existing functionality

## Example Implementation
```python
from pathlib import Path
from typing import Optional
import pandas as pd
import plotly.express as px

def load_data(csv_path: Path) -> pd.DataFrame:
    \"\"\"Read the destination dataset from a CSV file.
    
    Args:
        csv_path: Path to the CSV file containing destination data.
    
    Returns:
        A pandas DataFrame with the dataset.
    \"\"\"
    # ... implementation
```

## Reference
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [Python Type Checking Guide](https://realpython.com/python-type-checking/)

## Related
- Contributes to Phase 2: Enhanced Testing & Code Quality
- Required before: Issue #4
""",
    },
    {
        "number": 4,
        "title": "Configure mypy for Static Type Checking",
        "labels": ["code-quality", "phase-2", "tooling", "medium-priority"],
        "milestone": "v0.2.0",
        "body": """Set up mypy for static type checking and configure it in the project toolchain.

## Tasks
- [ ] Add `mypy` to requirements.txt
- [ ] Create `mypy.ini` or add `[tool.mypy]` section in `pyproject.toml`
- [ ] Configure mypy settings:
  - Enable strict mode for project files
  - Ignore missing imports for third-party libraries
  - Set Python version to 3.9+
- [ ] Add mypy check to CI/CD pipeline (`.github/workflows/ci.yml`)
- [ ] Run mypy and fix any type errors found
- [ ] Document mypy usage in CONTRIBUTING.md

## Acceptance Criteria
- [ ] mypy configuration file exists
- [ ] mypy passes without errors on all project files
- [ ] CI/CD pipeline runs mypy checks
- [ ] Documentation updated with mypy instructions

## Configuration Example
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

## CI/CD Addition
```yaml
- name: Type check with mypy
  run: |
    mypy scripts/
```

## Related
- Contributes to Phase 2: Enhanced Testing & Code Quality
- Depends on: Issue #3
""",
    },
    {
        "number": 5,
        "title": "Add Logging Framework Throughout Dashboard",
        "labels": ["code-quality", "phase-2", "high-priority"],
        "milestone": "v0.2.0",
        "body": """Replace print statements with proper logging using Python's logging module. This will improve debugging and production monitoring.

## Tasks
- [ ] Set up logging configuration in `scripts/dashboard.py`
- [ ] Replace all `print()` statements with appropriate log levels:
  - Info: Normal operation messages
  - Debug: Detailed diagnostic information
  - Warning: Unexpected situations that don't prevent execution
  - Error: Error conditions
- [ ] Add logging to file in addition to console
- [ ] Create `logs/` directory in `.gitignore`
- [ ] Add logging configuration examples to documentation

## Acceptance Criteria
- [ ] No print statements remain (except in `if __name__ == '__main__'` if needed)
- [ ] All log messages use appropriate levels
- [ ] Log format includes timestamp, level, and message
- [ ] Logs are written to both console and file
- [ ] Log files are excluded from git
- [ ] Documentation includes logging examples

## Implementation Example
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

## Related
- Contributes to Phase 2: Enhanced Testing & Code Quality
""",
    },
    {
        "number": 6,
        "title": "Add Custom Exceptions for Domain Errors",
        "labels": ["code-quality", "phase-2", "error-handling", "medium-priority"],
        "milestone": "v0.2.0",
        "body": """Create custom exception classes for domain-specific errors to improve error handling and debugging.

## Tasks
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

## Acceptance Criteria
- [ ] Custom exception module created
- [ ] All exceptions inherit from appropriate base classes
- [ ] Exceptions include helpful error messages
- [ ] Functions raise appropriate exceptions
- [ ] Tests verify exception behavior
- [ ] Exceptions documented

## Related
- Contributes to Phase 2: Enhanced Testing & Code Quality
- Used by: Issue #7
""",
    },
    {
        "number": 7,
        "title": "Add Data Validation with Error Handling",
        "labels": ["code-quality", "phase-2", "high-priority", "error-handling"],
        "milestone": "v0.2.0",
        "body": """Add comprehensive data validation to ensure CSV data meets requirements before processing.

## Tasks
- [ ] Create `validate_dataframe()` function
- [ ] Check for required columns
- [ ] Validate data types
- [ ] Check for null values in critical columns
- [ ] Validate value ranges (e.g., costs > 0)
- [ ] Add validation to `load_data()` function
- [ ] Write tests for validation logic
- [ ] Add validation for empty DataFrames

## Acceptance Criteria
- [ ] Validation function implemented and tested
- [ ] All data quality issues detected
- [ ] Helpful error messages for each validation failure
- [ ] Validation runs automatically on data load
- [ ] Tests cover all validation scenarios
- [ ] Documentation includes validation rules

## Related
- Contributes to Phase 2: Enhanced Testing & Code Quality
- Depends on: Issue #6
""",
    },
    {
        "number": 8,
        "title": "Add Pre-commit Hooks for Code Quality",
        "labels": ["tooling", "phase-2", "developer-experience", "medium-priority"],
        "milestone": "v0.2.0",
        "body": """Set up pre-commit hooks to automatically format and lint code before commits.

## Tasks
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

## Acceptance Criteria
- [ ] Pre-commit configuration file exists
- [ ] All hooks configured and tested
- [ ] Documentation includes setup instructions
- [ ] Hooks run automatically on commit
- [ ] CI verifies hooks were executed

## Setup Instructions
```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## Related
- Contributes to Phase 2: Enhanced Testing & Code Quality
""",
    },
]


def check_gh_cli() -> bool:
    """Check if GitHub CLI is installed and authenticated."""
    try:
        result = subprocess.run(
            ["gh", "auth", "status"], capture_output=True, text=True, check=True
        )
        print("✓ GitHub CLI is authenticated")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ GitHub CLI is not installed or not authenticated")
        print("\nPlease install and authenticate:")
        print("  1. Install: https://cli.github.com/")
        print("  2. Authenticate: gh auth login")
        return False


def create_issue(issue: Dict[str, Any]) -> bool:
    """Create a single GitHub issue."""
    print(f"\nCreating Issue #{issue['number']}: {issue['title']}...")

    # Build the command
    cmd = [
        "gh",
        "issue",
        "create",
        "--title",
        issue["title"],
        "--body",
        issue["body"],
        "--label",
        ",".join(issue["labels"]),
    ]

    if "milestone" in issue:
        cmd.extend(["--milestone", issue["milestone"]])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✓ Created: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed: {e.stderr}")
        return False


def main() -> None:
    """Main function to create all issues."""
    print("=" * 60)
    print("GitHub Issues Creator for Places2Go")
    print("=" * 60)

    # Check prerequisites
    if not check_gh_cli():
        sys.exit(1)

    print(f"\nReady to create {len(ISSUES)} issues for Phase 2")
    response = input("\nProceed? (y/n): ")

    if response.lower() != "y":
        print("Cancelled.")
        sys.exit(0)

    # Create issues
    success_count = 0
    for issue in ISSUES:
        if create_issue(issue):
            success_count += 1

    # Summary
    print("\n" + "=" * 60)
    print(f"Summary: {success_count}/{len(ISSUES)} issues created successfully")
    print("=" * 60)

    if success_count == len(ISSUES):
        print("\n✓ All issues created! View them with: gh issue list")
    else:
        print("\n⚠ Some issues failed. Check errors above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
