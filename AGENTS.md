# places2go Agent Guide

Welcome! This repository powers the **Places2Go** data exploration dashboards. Use this guide to align with the existing tooling,
documentation, and quality bar before you start coding.

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
- Update README sections or files in `docs/` when behaviour or workflows change. Architectural adjustments belong in `docs/architecture/`,
process updates in `docs/processes/`, and contributor workflows in `docs/development/`.
- Dashboard-facing changes should also refresh any generated artefacts or usage docs referenced from `.build/visualizations/README.md`.
- PR summaries must include:
  1. User- or developer-facing impacts in bullet form.
  2. A test checklist with the exact commands run and their outcomes.
- Review `docs/PR_BEST_PRACTICES.md` before opening a pull request to ensure your communication style matches the project norm.

Thanks for contributing, and enjoy exploring the data!
