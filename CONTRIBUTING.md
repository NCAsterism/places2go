# Contributing to Places2Go

Thank you for your interest in contributing to the Places2Go destination dashboard! This guide will help you get started.

## Code of Conduct

This project follows a simple code of conduct:
- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the community
- Show empathy towards other contributors

## Getting Started

### Prerequisites
- Python 3.9 or higher
- Git
- A GitHub account

### Development Setup

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/places2go.git
   cd places2go
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up pre-commit hooks** (recommended)
   ```bash
   pre-commit install
   ```

   This will automatically run code formatting and linting before each commit. You can also run hooks manually:
   ```bash
   # Run on all files
   pre-commit run --all-files

   # Run on staged files only
   pre-commit run
   ```

5. **Run tests to verify setup**
   ```bash
   pytest
   ```

## Development Workflow

We follow a GitFlow branching strategy:

### Branch Types
- `main` - Production-ready code only
- `develop` - Integration branch for features
- `feature/*` - New features (branch from `develop`)
- `bugfix/*` - Bug fixes (branch from `develop`)
- `hotfix/*` - Critical production fixes (branch from `main`)
- `release/*` - Release preparation (branch from `develop`)

### Working on a Feature

1. **Create a feature branch**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, readable code
   - Follow the code style guide (below)
   - Add tests for new functionality
   - Update documentation as needed

3. **Run quality checks**
   ```bash
   # Format code
   black scripts tests

   # Check for issues
   flake8 scripts tests

   # Type check with mypy
   mypy scripts/

   # Run tests
   pytest

   # Check coverage
   pytest --cov=scripts --cov-report=term
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then open a PR on GitHub targeting the `develop` branch.

   **Important:** Review our [PR Best Practices](docs/PR_BEST_PRACTICES.md) guide before creating PRs to avoid merge conflicts and ensure smooth collaboration.

## Code Style Guide

### Python Style
- Follow PEP 8 style guidelines
- Use Black for code formatting (line length: 88)
- Use meaningful variable and function names
- Add type hints to function signatures
- Write docstrings for all functions and classes
- Code passes mypy static type checking (when configured)

### Documentation Style
- Write copy and comments in British English (e.g., “favour”, “optimise”). Configure your editor to use an `en-GB` dictionary—our `.editorconfig` file exposes `spelling_language = en-GB` for tools that support it.

### Type Hints
All functions should include type annotations for parameters and return values:

```python
from pathlib import Path
from typing import Optional
import pandas as pd

def load_data(csv_path: Path) -> pd.DataFrame:
    """Read the destination dataset from a CSV file.

    Args:
        csv_path: Path to the CSV file containing destination data.

    Returns:
        A pandas DataFrame with the dataset.
    """
    # ... implementation
```

Run mypy to check for type errors:
```bash
mypy scripts/
```

### Example Function
```python
def calculate_flight_cost(
    origin: str, destination: str, date: datetime
) -> float:
    """Calculate the estimated flight cost for a route.

    Args:
        origin: Origin airport code (e.g., "EXT" for Exeter)
        destination: Destination airport code
        date: Departure date

    Returns:
        Estimated cost in GBP

    Raises:
        ValueError: If airport codes are invalid
    """
    # Implementation here
    pass
```

### Commit Message Format
We use conventional commits:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Examples:
```
feat: add weather API integration
fix: correct path bug in test_data.py
docs: update README with new installation steps
test: add tests for flight cost calculation
```

## Testing Guidelines

### Writing Tests
- Place tests in the `tests/` directory
- Name test files as `test_*.py`
- Name test functions as `test_*`
- Use descriptive test names that explain what is being tested
- Aim for 80%+ code coverage

### Test Structure
```python
def test_function_name_scenario():
    """Test function_name when scenario occurs."""
    # Arrange - Set up test data
    input_data = ...

    # Act - Execute the function
    result = function_name(input_data)

    # Assert - Verify the result
    assert result == expected_value
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=scripts

# Run specific test file
pytest tests/test_data.py

# Run specific test
pytest tests/test_data.py::test_load_data_types
```

## Pull Request Process

1. **Before submitting:**
   - Run all tests and ensure they pass
   - Format code with Black
   - Check for linting errors with flake8
   - Run mypy type checking and fix any errors
   - Update documentation if needed
   - Rebase on latest `develop` if needed

2. **PR Description should include:**
   - Clear description of changes
   - Link to related issue (if applicable)
   - Screenshots (for UI changes)
   - Testing steps
   - Any breaking changes

3. **PR Review:**
   - At least one approval required
   - All CI checks must pass
   - No merge conflicts
   - Code coverage should not decrease

4. **After approval:**
   - Squash commits if requested
   - PR will be merged by maintainers

## Project Structure

```
places2go/
├── .github/
│   └── workflows/        # CI/CD configurations
├── data/                 # Data files
├── docs/                 # Documentation
├── scripts/              # Main Python scripts
├── tests/                # Test files
├── output/               # Generated outputs
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── pyproject.toml        # Project configuration
├── requirements.txt      # Python dependencies
└── README.md             # Project overview
```

## Adding New Features

### Data Sources
If adding a new data source:
1. Create a class implementing the data source interface
2. Add comprehensive tests with mocked API responses
3. Update `.env.example` with any new API keys
4. Document the API in the data source module
5. Add usage examples to documentation

### Dashboard Features
If adding dashboard features:
1. Design the feature first (mockups help)
2. Implement backend logic with tests
3. Create the UI component
4. Test on multiple screen sizes
5. Update user documentation

### Visualizations
If adding or modifying visualization pages:

#### Creating New Visualizations
1. **Create script in `scripts/visualizations/`**
   ```python
   # scripts/visualizations/my_visualization.py
   from scripts.core.data_loader import DataLoader
   import plotly.graph_objects as go
   from pathlib import Path
   
   def create_my_visualization(output_path: Path, df: pd.DataFrame) -> None:
       """Create custom visualization."""
       # Implementation here
   ```

2. **Use DataLoader for data access**
   ```python
   loader = DataLoader()
   data = loader.load_destinations()  # or other methods
   ```

3. **Follow Plotly best practices**
   - Use consistent color schemes across charts
   - Include hover details for interactivity
   - Add titles, axis labels, and legends
   - Make responsive (autosize=True)
   - Include loading indicators for large datasets

4. **Output to `.build/visualizations/`**
   ```python
   project_root = Path(__file__).resolve().parents[2]
   output_dir = project_root / ".build" / "visualizations"
   output_path = output_dir / "my_visualization.html"
   ```

5. **Add logging for debugging**
   ```python
   import logging
   logger = logging.getLogger(__name__)
   logger.info("Creating visualization...")
   ```

6. **Write tests in `tests/test_*.py`**
   ```python
   def test_my_visualization_creation():
       """Test visualization generates valid HTML."""
       # Test implementation
   ```

7. **Document in `.build/visualizations/README.md`**
   - Add section describing the visualization
   - Include purpose, features, and usage
   - Provide code examples
   - Add screenshots if possible

#### Visualization Guidelines
- **Consistency:** Use same color palette as other visualizations
- **Interactivity:** Enable hover, zoom, pan, legend toggle
- **Responsive:** Test on desktop and mobile
- **Performance:** Optimize for datasets with 1000+ records
- **Accessibility:** Include alt text and ARIA labels
- **Documentation:** Update both code docstrings and README
- **Browser Testing:** Test in Chrome, Firefox, Safari, Edge

#### Color Palette
Use the standard destination colors for consistency:
```python
DESTINATION_COLORS = {
    'Bangkok': '#FF6B6B',
    'Tokyo': '#4ECDC4',
    'Barcelona': '#45B7D1',
    'Prague': '#FFA07A',
    'Lisbon': '#98D8C8',
    'Marrakech': '#F7DC6F'
}
```

#### Example Visualization Script Structure
```python
#!/usr/bin/env python3
"""
Visualization description and purpose.
"""

import logging
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from scripts.core.data_loader import DataLoader

logger = logging.getLogger(__name__)

def create_chart(df: pd.DataFrame) -> go.Figure:
    """Create chart from data."""
    fig = go.Figure()
    # Chart creation logic
    return fig

def create_visualization(output_path: Path, df: pd.DataFrame) -> None:
    """Generate complete HTML file."""
    chart = create_chart(df)
    chart_html = chart.to_html(include_plotlyjs='cdn')
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>My Visualization - Places2Go</title>
    </head>
    <body>
        {chart_html}
    </body>
    </html>
    """
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_content)
    logger.info(f"Visualization saved to {output_path}")

def main() -> None:
    """Main entry point."""
    logger.info("Starting visualization generation")
    loader = DataLoader()
    df = loader.load_destinations()
    
    project_root = Path(__file__).resolve().parents[2]
    output_path = project_root / ".build" / "visualizations" / "my_viz.html"
    
    create_visualization(output_path, df)
    logger.info("Visualization generation completed")

if __name__ == "__main__":
    main()
```

#### Testing Visualizations
```python
# tests/test_my_visualization.py
import pytest
from pathlib import Path
from scripts.visualizations.my_visualization import create_visualization
from scripts.core.data_loader import DataLoader

def test_visualization_generates_html(tmp_path):
    """Test that visualization creates HTML file."""
    loader = DataLoader()
    df = loader.load_destinations()
    output_path = tmp_path / "test.html"
    
    create_visualization(output_path, df)
    
    assert output_path.exists()
    assert output_path.stat().st_size > 0
    
    content = output_path.read_text()
    assert "<!DOCTYPE html>" in content
    assert "plotly" in content.lower()
```

For more details, see [.build/visualizations/README.md](.build/visualizations/README.md).

### API Keys and Secrets
- Never commit API keys or secrets
- Use `.env` file for local development
- Document required keys in `.env.example`
- Use environment variables in production

## Getting Help

- **Questions?** Open a discussion on GitHub Discussions
- **Bug?** Open an issue with the `bug` label
- **Feature idea?** Open an issue with the `enhancement` label
- **Documentation issue?** Open an issue with the `documentation` label

## Recognition

Contributors will be acknowledged in:
- GitHub contributors page
- Release notes
- Project README (for significant contributions)

Thank you for contributing to Places2Go! 🌍✈️
