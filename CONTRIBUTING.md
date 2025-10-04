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

4. **Run tests to verify setup**
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

## Code Style Guide

### Python Style
- Follow PEP 8 style guidelines
- Use Black for code formatting (line length: 88)
- Use meaningful variable and function names
- Add type hints to function signatures
- Write docstrings for all functions and classes

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
