# Installation Guide

This guide will help you install and set up Places2Go on your local machine.

---

## Prerequisites

Before installing Places2Go, ensure you have the following:

### Required
- **Python 3.9 or higher** (3.9, 3.10, 3.11, or 3.12)
- **pip** (Python package manager)
- **Git** (for cloning the repository)

### Recommended
- **Virtual environment tool** (`venv`, `virtualenv`, or `conda`)
- **VS Code** or your preferred IDE

---

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/NCAsterism/places2go.git
cd places2go
```

### 2. Create a Virtual Environment

**Using venv (recommended):**
```bash
python -m venv venv
```

**Activate the virtual environment:**

**Windows:**
```powershell
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages:
- `pandas` - Data manipulation
- `plotly` - Interactive visualizations
- `python-dotenv` - Environment variable management
- `pytest` - Testing framework
- `black` - Code formatting
- `flake8` - Code linting

### 4. Verify Installation

Run the test suite to ensure everything is working:

```bash
pytest
```

Expected output:
```
============================= test session starts ==============================
collected 2 items

tests/test_data.py ..                                                    [100%]

============================== 2 passed in 0.12s ===============================
```

### 5. Run the Dashboard

```bash
python scripts/dashboard.py
```

This will generate:
- `output/flight_costs.html` - Flight cost comparison chart
- `output/flight_time_vs_cost.html` - Time vs. cost analysis chart

Open these HTML files in your browser to view the visualizations.

---

## Optional Setup

### Development Tools

For development, you may want to install additional tools:

```bash
# Install pre-commit hooks (Phase 2)
pip install pre-commit
pre-commit install

# Install mypy for type checking (Phase 2)
pip install mypy
```

### IDE Configuration

**VS Code Settings (recommended):**

Create `.vscode/settings.json`:
```json
{
  "python.formatting.provider": "black",
  "python.linting.flake8Enabled": true,
  "python.linting.enabled": true,
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "editor.formatOnSave": true
}
```

---

## Environment Variables

Create a `.env` file for configuration (optional):

```bash
cp .env.example .env
```

Edit `.env` with your settings (currently not required for basic usage).

---

## Troubleshooting

### Python Version Issues

If you get version errors:
```bash
python --version  # Check your Python version
```

Ensure you have Python 3.9+. If not, download from [python.org](https://www.python.org/downloads/).

### Dependency Conflicts

If you encounter dependency issues:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Virtual Environment Not Activating

**Windows PowerShell Execution Policy:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Import Errors

Ensure your virtual environment is activated and all dependencies are installed:
```bash
pip list  # Check installed packages
```

---

## Uninstallation

To remove Places2Go:

1. Deactivate virtual environment:
   ```bash
   deactivate
   ```

2. Delete the project directory:
   ```bash
   cd ..
   rm -rf places2go  # macOS/Linux
   rmdir /s places2go  # Windows
   ```

---

## Next Steps

- 📖 [Quick Start Guide](Quick-Start) - Learn basic usage
- 🛠️ [Development Guide](Development-Guide) - Set up for development
- ⚙️ [Configuration](Configuration) - Customize your setup

---

**Need Help?** Check the [FAQ](FAQ) or [Troubleshooting](Troubleshooting) pages.
