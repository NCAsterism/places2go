# Development Guide

Comprehensive guide for contributing to Places2Go development.

---

## Table of Contents

1. [Development Setup](#development-setup)
2. [Project Structure](#project-structure)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Testing](#testing)
6. [Git Workflow](#git-workflow)
7. [CI/CD](#cicd)

---

## Development Setup

### Prerequisites

- Python 3.9-3.12
- Git
- GitHub account (for contributing)
- VS Code (recommended) or your preferred IDE

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/NCAsterism/places2go.git
cd places2go

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\Activate.ps1

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development tools (Phase 2+)
pip install pre-commit mypy
pre-commit install
```

### IDE Configuration

**VS Code Recommended Settings:**

Create `.vscode/settings.json`:
```json
{
  "python.formatting.provider": "black",
  "python.linting.flake8Enabled": true,
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "editor.formatOnSave": true,
  "editor.rulers": [88],
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    ".pytest_cache": true,
    ".coverage": true,
    "htmlcov": true
  }
}
```

---

## Project Structure

```
places2go/
├── .github/
│   ├── workflows/
│   │   └── ci.yml              # CI/CD pipeline
│   └── ISSUE_TEMPLATE/         # Issue templates
│       ├── bug_report.md
│       ├── feature_request.md
│       └── test_request.md
├── data/
│   └── dummy_data.csv          # Sample dataset
├── docs/
│   ├── branching_strategy.md  # GitFlow documentation
│   └── task_breakdown.md      # Project tasks
├── scripts/
│   ├── dashboard.py           # Main dashboard script
│   ├── create_issues.py       # GitHub issue automation
│   └── push_to_github.ps1     # Deployment script
├── src/                       # Source code (Phase 3+)
│   └── data/                  # Data modules
├── tests/
│   └── test_data.py           # Test suite
├── output/                    # Generated files
├── .gitignore                 # Git exclusions
├── .env.example               # Environment template
├── LICENSE                    # MIT License
├── pyproject.toml             # Project configuration
├── requirements.txt           # Python dependencies
├── README.md                  # Project overview
├── ROADMAP.md                 # Development timeline
├── CONTRIBUTING.md            # Contribution guide
└── BUILD_SUMMARY.md           # Build documentation
```

### Module Organization (Future)

```
src/
├── __init__.py
├── data/
│   ├── __init__.py
│   ├── loader.py              # Data loading
│   ├── models.py              # Pydantic models
│   └── validator.py           # Data validation
├── dashboard/
│   ├── __init__.py
│   ├── charts.py              # Chart generation
│   └── streamlit_app.py       # Streamlit interface
├── api/
│   ├── __init__.py
│   ├── flights.py             # Flight API clients
│   └── weather.py             # Weather API clients
└── utils/
    ├── __init__.py
    ├── logger.py              # Logging utilities
    └── exceptions.py          # Custom exceptions
```

---

## Development Workflow

### 1. Pick an Issue

Browse [open issues](https://github.com/NCAsterism/places2go/issues) and find one that interests you.

**Good first issues:**
- Issues labeled `good first issue`
- Issues labeled `phase-2` (current milestone)
- Test-related issues

### 2. Create a Feature Branch

```bash
# Ensure you're on develop
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/issue-number-brief-description

# Example
git checkout -b feature/1-comprehensive-test-suite
```

### 3. Make Changes

- Write code following our [Code Style](Code-Style)
- Add tests for new functionality
- Update documentation as needed

### 4. Test Your Changes

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=scripts --cov=tests --cov-report=html

# Format code
black scripts/ tests/ src/

# Check linting
flake8 scripts/ tests/ src/

# Type checking (Phase 2+)
mypy scripts/ src/
```

### 5. Commit Your Changes

Use [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Format: <type>(<scope>): <description>

# Examples
git commit -m "feat(dashboard): add temperature filter"
git commit -m "fix(data): handle missing CSV columns"
git commit -m "test(dashboard): add chart generation tests"
git commit -m "docs(readme): update installation steps"
```

**Commit Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring
- `style:` Formatting
- `chore:` Maintenance

### 6. Push and Create PR

```bash
# Push your branch
git push origin feature/issue-number-brief-description

# Create pull request via GitHub
# Target: develop branch
```

---

## Coding Standards

### Python Style

- **Formatter:** Black (line length: 88)
- **Linter:** Flake8
- **Import Order:** Standard lib → Third party → Local
- **Type Hints:** Required (Phase 2+)

**Example:**
```python
from pathlib import Path
from typing import List, Dict

import pandas as pd
import plotly.express as px

from src.data.models import Destination


def load_data(file_path: Path) -> pd.DataFrame:
    """
    Load destination data from CSV file.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        DataFrame containing destination data
        
    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If CSV format is invalid
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")
    
    return pd.read_csv(file_path)
```

### Documentation

- **Docstrings:** Google style for all functions/classes
- **Comments:** Explain why, not what
- **README:** Keep up-to-date with features

### Testing

- **Coverage:** Aim for 90%+
- **Test Names:** `test_<function>_<scenario>`
- **Fixtures:** Use pytest fixtures for setup
- **Mocking:** Mock external dependencies

**Example:**
```python
import pytest
from pathlib import Path
import pandas as pd

from scripts.dashboard import load_data


def test_load_data_success():
    """Test successful data loading from valid CSV."""
    data_path = Path("data/dummy_data.csv")
    df = load_data(data_path)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "Destination" in df.columns


def test_load_data_file_not_found():
    """Test error handling for missing file."""
    with pytest.raises(FileNotFoundError):
        load_data(Path("nonexistent.csv"))
```

---

## Testing

### Running Tests

```bash
# All tests
pytest

# Specific file
pytest tests/test_data.py

# Specific test
pytest tests/test_data.py::test_load_data_types

# With coverage
pytest --cov=scripts --cov-report=html

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

### Writing Tests

**Test Structure:**
```python
# tests/test_module.py

import pytest
from module import function_to_test


class TestFunctionName:
    """Tests for function_to_test."""
    
    def test_happy_path(self):
        """Test normal execution."""
        result = function_to_test(valid_input)
        assert result == expected_output
    
    def test_edge_case(self):
        """Test boundary conditions."""
        result = function_to_test(edge_case_input)
        assert result is not None
    
    def test_error_handling(self):
        """Test exception handling."""
        with pytest.raises(ValueError):
            function_to_test(invalid_input)
```

### Coverage Goals

- **Overall:** 90%+ coverage
- **Critical paths:** 100% coverage
- **Error handling:** All branches tested

---

## Git Workflow

### GitFlow Strategy

We use GitFlow branching model:

**Main Branches:**
- `main` - Production-ready code
- `develop` - Integration branch

**Supporting Branches:**
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Urgent production fixes
- `release/*` - Release preparation

### Branch Naming

```bash
feature/issue-number-brief-description
bugfix/issue-number-bug-description
hotfix/critical-issue-description
release/version-number
```

### Workflow Example

```bash
# Start new feature
git checkout develop
git pull origin develop
git checkout -b feature/42-add-weather-filter

# Make changes and commit
git add .
git commit -m "feat(dashboard): add weather filter component"

# Keep up-to-date with develop
git fetch origin
git rebase origin/develop

# Push and create PR
git push origin feature/42-add-weather-filter
```

---

## CI/CD

### GitHub Actions Pipeline

Our CI pipeline runs on every push and PR:

**Jobs:**
1. **Test** - Run pytest on Python 3.9-3.12
2. **Lint** - Check code with flake8
3. **Format** - Verify Black formatting
4. **Coverage** - Generate coverage report

**Configuration:** `.github/workflows/ci.yml`

### Pre-commit Hooks (Phase 2+)

Automatic checks before commit:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.4.1
    hooks:
      - id: mypy
```

Install hooks:
```bash
pip install pre-commit
pre-commit install
```

---

## Next Steps

- 📋 [Contributing Guidelines](Contributing) - Detailed contribution process
- 🧪 [Testing Guide](Testing) - Comprehensive testing documentation
- 🏗️ [Architecture](Architecture) - System design and structure
- 📊 [Roadmap](Roadmap) - Development timeline

---

**Questions?** Check the [FAQ](FAQ) or open a [discussion](https://github.com/NCAsterism/places2go/discussions).
