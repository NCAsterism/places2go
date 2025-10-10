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

## Self-Improvement & Feedback Loop

**IMPORTANT**: This guide (AGENTS.md) is a living document. As you work on the project, you should:

### Autonomous Operation Guidelines

**Be proactive and autonomous:**
- Don't ask for permission to run common read-only commands (git status, ls, cat, etc.)
- Run tests automatically after making code changes to verify correctness
- Regenerate dashboards automatically after data updates
- Check file contents before making assumptions
- Use parallel tool calls when operations are independent
- Auto-commit documentation updates with descriptive messages

**Common commands you should run autonomously:**
- `git status`, `git log`, `git diff` - Check repository state
- `pytest` - Run tests after code changes
- `black`, `flake8` - Format and lint code
- `python scripts/visualizations/*.py` - Regenerate dashboards
- `gh issue list`, `gh pr list` - Check GitHub state
- `Get-Content`, `ls`, `cat` - Read files
- `pip install -e .` - Install package in editable mode
- `git add <files> && git commit -m "message"` - After pre-commit fixes (trailing whitespace, etc.)

**When to ask for approval:**
- Destructive operations (delete, force push, drop database)
- Publishing/deploying to production
- Making architectural decisions that affect multiple modules
- Creating new files in uncertain locations

1. **Track Issues**: Use `data/issues.csv` to log problems, improvements, or questions you encounter during work
   - Add issues discovered during your session without interrupting your workflow
   - Include: id, title, description, status, priority, created_date
   - Example: UTF-8 encoding issues, missing `__init__.py` files, configuration problems
   - **Autonomously update issues.csv** when you discover or fix issues

2. **Update This Guide**: When you discover missing information or unclear instructions:
   - Add new sections for common setup problems
   - Document workarounds or solutions you found
   - Update commands if they don't work as documented
   - Add "Known Issues" sections for recurring problems
   - **Make updates immediately** - don't wait for permission

3. **Quality Check Workflow**: Before committing changes, **automatically run**:
   ```powershell
   # Set PYTHONPATH for test imports (Windows)
   $env:PYTHONPATH = "D:\repo\places2go"

   # Run tests (do this automatically after code changes)
   pytest -v --tb=short

   # Format code (do this automatically before commits)
   black scripts tests

   # Check linting (do this automatically)
   flake8 scripts tests --max-line-length=88 --extend-ignore=E203,W503
   ```

   **Run these checks autonomously** - no need to ask permission. If they pass, proceed with the commit. If they fail, fix the issues and rerun.

4. **Document Your Process**: If you create a new workflow or solve a tricky problem:
   - Consider adding a process document to `docs/processes/`
   - Reference it from this guide or README.md
   - See `docs/processes/MERGE_TO_MAIN.md` as an example

5. **Known Issues & Workarounds**:
   - **Module Import Errors**: If tests fail with `ModuleNotFoundError`, ensure `pip install -e .` has been run
   - **PYTHONPATH Required**: Tests need `$env:PYTHONPATH = "D:\repo\places2go"` set on Windows
   - **UTF-8 Encoding**: 10 tests fail on Windows when reading HTML files (tracked in issues.csv #1)
   - **Missing `__init__.py`**: All package directories need `__init__.py` files for imports to work

**Remember**: If you spend more than 5 minutes solving a problem, document it here so the next agent (or human) doesn't have to solve it again!

### Learning & Adaptation Patterns

**Continuous Improvement Cycle:**
1. **Observe** - Notice patterns in failures, workarounds, or repeated questions
2. **Document** - Add to AGENTS.md, issues.csv, or create new process docs
3. **Automate** - Create scripts or update settings to prevent repeated manual work
4. **Share** - Commit documentation updates so all agents benefit

**Self-Learning Triggers:**
- Encounter the same problem twice? Document the solution.
- Run the same command sequence 3+ times? Create a script or add to auto-approve.
- Answer the same question twice? Add to FAQ or AGENTS.md.
- Fix the same type of bug repeatedly? Add to test suite or linting rules.

**Autonomy Checklist:**
- ✅ Read files without asking
- ✅ Run tests after code changes
- ✅ Format code before commits
- ✅ Check git status frequently
- ✅ List GitHub issues/PRs to understand state
- ✅ Update issues.csv when discovering issues
- ✅ Regenerate dashboards after data changes
- ✅ Create process documentation for new workflows
- ❌ Don't delete files without confirmation
- ❌ Don't force push or rewrite history without approval
- ❌ Don't deploy to production without explicit request

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

## Key Reference Documents

When working on this project, consult these documents for specific workflows:

- **`README.md`** - Quick start, installation, and high-level overview
- **`CONTRIBUTING.md`** - Detailed contribution guidelines, code style, testing patterns
- **`data/issues.csv`** - Current open issues and known problems (add to this!)
- **`docs/processes/MERGE_TO_MAIN.md`** - Complete workflow for merging develop to main
- **`docs/processes/PR_BEST_PRACTICES.md`** - Pull request guidelines
- **`docs/processes/branching.md`** - GitFlow branching strategy
- **`docs/development/COPILOT_WORKFLOW.md`** - Best practices for working with GitHub Copilot
- **`docs/architecture/DATA_STRUCTURE.md`** - Data schema and CSV structure
- **`.build/visualizations/README.md`** - Visualization documentation and examples

## Quick Troubleshooting

### Tests Won't Import Modules
```powershell
pip install -e .  # Install package in editable mode
$env:PYTHONPATH = "D:\repo\places2go"  # Set Python path
```

### Pre-commit Hooks Failing - Trailing Whitespace

**Problem:** `trailing-whitespace hook failed - files were modified by this hook`

**What happened:** The pre-commit hook automatically removed trailing whitespace from your files. This is NORMAL and expected behavior.

**Solution - Run this automatically:**
```powershell
# The hook already fixed the files, just re-stage and commit
git add <files>
git commit -m "your message"
```

**Why this happens:**
- Markdown and text files often have trailing spaces
- The pre-commit hook removes them automatically
- You just need to re-stage the cleaned files

**Prevent it in the future:**
1. Configure your editor to trim trailing whitespace on save
2. VS Code: Add to settings.json:
   ```json
   "files.trimTrailingWhitespace": true
   ```

**Autonomy Note:** When you see this error, automatically re-stage and re-commit without asking permission. It's a routine cleanup operation.

### Black Formatting Failures
```powershell
black scripts tests  # Auto-format code
git add <files>      # Re-stage after formatting
```

### Multiple Virtual Environments
- Use **`.venv`** (active)
- Ignore **`.venv-1`** (legacy, can delete)

### Package Configuration Issues
- Check `pyproject.toml` has all subpackages listed
- Verify all directories have `__init__.py` files

Thanks for contributing, and enjoy exploring the data!
