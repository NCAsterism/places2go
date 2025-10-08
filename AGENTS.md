# places2go Agent Guide

Welcome! This repository powers the **Places2Go** data exploration dashboards. Use this guide to align with the existing tooling,
documentation, and quality bar before you start coding.

## Before You Start: Environment Setup

**CRITICAL**: Always ensure the Python virtual environment is activated before running any commands, tests, or scripts.

### Which Virtual Environment?

This project has **two** virtual environment folders:
- **`.venv`** - **USE THIS ONE** (active, current)
- **`.venv-1`** - Legacy/backup (can be deleted)

The `.venv` folder is the correct one to use. If you see `.venv-1`, it's an older environment that can be safely removed.

### Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### Verify Environment
After activation, your prompt should show `(.venv)` and you can verify with:
```powershell
python --version  # Should show Python 3.9+
python -c "import sys; print(sys.executable)"  # Should show D:\repo\places2go\.venv\Scripts\python.exe
```

### Install/Update Package
After activation, ensure the package is installed in editable mode:
```powershell
pip install -e .
```

This is required for tests to import modules correctly.

## Tech Stack & Project Layout
- **Language**: Python 3.9+ with type hints.
- **Core libraries**: `pandas` for data wrangling, `plotly` for interactive dashboards, and `pytest` for automated tests.
- **Key modules**:
  - `scripts/core/` holds data access utilities such as the modular `DataLoader`.
  - `scripts/visualizations/` contains Plotly dashboard builders (weather, costs, flights, etc.).
  - `tests/` mirrors the runtime packages; prefer colocating tests with the feature you touch.
- Review `README.md` for quick-start commands and `docs/` for deeper architecture, process, and workflow references.

## Coding Practices
- Keep business logic in focused, testable functions. Favour pure, deterministic helpers over implicit globals.
- Use descriptive names, docstrings, and type annotations for public functions and classes.
- Follow PEP 8 conventions; the project standardises on Black (line length 88) and mypy type checking as listed in `CONTRIBUTING.md`.
- Format code with Black before committing (use `black scripts tests` for staged work, or `black .` when in doubt) so `black --check` stays clean in CI.
- Data wrangling belongs in `scripts/core`; visual formatting and layout tweaks stay under `scripts/visualizations`.
- When integrating new data sources, extend the existing `DataLoader` patterns (explicit schema validation, null handling, and
dedicated parsing helpers). Do **not** catch-and-silence import errors—fail fast when dependencies are missing.

## Testing Expectations
- Back every new logic branch with unit tests in `tests/`. Mirror edge cases already covered (e.g., forecast filtering, empty
Dashboards) and add regression scenarios when fixing bugs.
- Use pytest fixtures or inline DataFrames for deterministic coverage. Seed randomness whenever pseudo-random data is required.
- Run at minimum:
  - `pytest`
  - `black --check scripts tests`
  - `flake8 scripts tests`
  - `mypy scripts`
  These commands appear in `CONTRIBUTING.md`; execute them locally and report results in your PR notes.

## Documentation & Communication
- Use British English spelling in documentation, UI copy, and inline comments. Editors that honour `.editorconfig` will pick up the `spelling_language = en-GB` hint, and you can extend local spell-checkers with `en-GB` dictionaries when drafting content.
- Update README sections or files in `docs/` when behaviour or workflows change. Architectural adjustments belong in `docs/architecture/`,
process updates in `docs/processes/`, and contributor workflows in `docs/development/`.
- Dashboard-facing changes should also refresh any generated artefacts or usage docs referenced from `.build/visualizations/README.md`.
- PR summaries must include:
  1. User- or developer-facing impacts in bullet form.
  2. A test checklist with the exact commands run and their outcomes.
- Review `docs/PR_BEST_PRACTICES.md` before opening a pull request to ensure your communication style matches the project norm.

Thanks for contributing, and enjoy exploring the data!
