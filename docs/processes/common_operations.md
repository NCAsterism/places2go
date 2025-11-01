# Common Operations Reference

**Single Source of Truth for procedural workflows and commands.**

This document contains frequently-changing technical procedures referenced by AGENTS.md and other documentation.
Keep behavioural guidelines in AGENTS.md; keep commands and workflows here.

---

## Environment Management

### Virtual Environment Activation

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
```powershell
python --version  # Should show Python 3.9+
python -c "import sys; print(sys.executable)"  # Should show path to .venv
```

### Package Installation
```powershell
pip install -e .  # Editable install for development
pip install -r requirements.txt  # Install all dependencies
```

---

## Version Control Operations

### Common Git Commands (Auto-Approved)

**Status checks:**
```powershell
git status
git log --oneline -10
git diff
git branch -a
```

**Safe read operations:**
```powershell
git show <commit>
git blame <file>
git log --follow <file>
```

**Standard workflow:**
```powershell
git add <files>
git commit -m "message"
git push origin <branch>
```

**Branch operations:**
```powershell
git checkout develop
git checkout -b feature/new-feature
git merge <branch>
```

---

## Testing & Quality Checks

### Test Execution

**Run all tests:**
```powershell
pytest
```

**Run with coverage:**
```powershell
pytest --cov=scripts --cov-report=term-missing
pytest --cov=scripts --cov-report=html:.build/coverage/htmlcov
```

**Run specific tests:**
```powershell
pytest tests/test_specific.py
pytest tests/test_specific.py::TestClass::test_method
pytest -k "test_pattern"
```

**Verbose output:**
```powershell
pytest -v --tb=short
```

### Code Formatting

**Check formatting:**
```powershell
black --check scripts tests
```

**Apply formatting:**
```powershell
black scripts tests
black .  # Format entire project
```

### Linting

**Run flake8:**
```powershell
flake8 scripts tests --max-line-length=88 --extend-ignore=E203,W503,E501
```

**Run mypy:**
```powershell
mypy scripts
```

---

## Quality Gate Workflow

### Pre-Commit Checklist

**Automated quality check:**
```powershell
./scripts/quality_check.ps1  # Windows
./scripts/quality_check.sh   # Unix
```

**Manual steps (if scripts not available):**
1. Run tests: `pytest`
2. Check formatting: `black --check scripts tests`
3. Run linting: `flake8 scripts tests`
4. Type checking: `mypy scripts`

**If checks fail:**
- Fix issues shown in output
- Re-run quality checks
- Commit once all checks pass

---

## Pre-Commit Hook Management

### Trailing Whitespace Fix Pattern

**Problem:** Pre-commit hook fails with "files were modified by this hook"

**Solution (auto-approve this):**
```powershell
# Hook already fixed files, just re-stage and commit
git add <files>
git commit -m "your message"
```

**Prevent in future:**
- Configure editor: `"files.trimTrailingWhitespace": true` (VS Code)
- Or manually trim before committing

### Other Common Hook Failures

**End-of-file fixer:**
- Hook adds newline at end of file
- Re-stage and commit (same pattern as trailing whitespace)

**YAML/JSON validation:**
- Fix syntax errors shown in output
- Commit after fixing

---

## GitHub Operations

### Issue Management

**List issues:**
```powershell
gh issue list
gh issue list --limit 100
gh issue list --label "bug"
```

**Create issue:**
```powershell
gh issue create --title "Title" --body "Description"
gh issue create --title "Title" --body-file body.md
```

### Pull Request Management

**List PRs:**
```powershell
gh pr list
gh pr view <number>
gh pr checkout <number>
```

**Create PR (use helper for long descriptions):**
```powershell
# For long descriptions, use helper to avoid PowerShell limits
python scripts/create_pr.py --title "feat: feature" --body-file pr_body.md --base develop
```

**Alternative (short descriptions):**
```powershell
gh pr create --title "feat: feature" --body "Short description" --base develop
```

---

## Data Operations

### Dashboard Regeneration

**Regenerate all visualizations:**
```powershell
python scripts/visualizations/weather_dashboard.py
python scripts/visualizations/cost_dashboard.py
python scripts/visualizations/flight_dashboard.py
```

**Check data structure:**
```powershell
python scripts/setup_data_dirs.py  # Validate structure
```

---

## Project Status Tracking

### Status Reports

**Display current status:**
```powershell
python scripts/reports/project_status_tracker.py
```

**Save snapshot:**
```powershell
python scripts/reports/project_status_tracker.py --snapshot
```

**View trends:**
```powershell
python scripts/reports/project_status_tracker.py --trends
```

---

## Troubleshooting Common Issues

### Module Import Errors

**Symptoms:** `ModuleNotFoundError` when running tests

**Solutions:**
1. Ensure editable install: `pip install -e .`
2. Check PYTHONPATH (Windows): `$env:PYTHONPATH = "D:\repo\<project-name>"`
3. Verify imports: `python -c "from scripts.core import data_loader"`

### Test Configuration Issues

**Symptoms:** Tests can't find modules or data files

**Check pytest configuration:**
```powershell
pytest --collect-only  # See what tests are discovered
pytest --setup-plan    # See fixture setup order
```

**Verify pyproject.toml has:**
```toml
[tool.pytest.ini_options]
pythonpath = "."
testpaths = ["tests"]
```

### PowerShell Command Length Limits

**Problem:** Long commands (gh pr create, git commit) fail

**Solution:** Use helper scripts or file-based input
```powershell
# Write to file
"Long message" | Out-File message.txt -Encoding utf8

# Use file as input
python scripts/create_pr.py --body-file message.txt
git commit -F message.txt
```

---

## Package Management

### Install Development Dependencies
```powershell
pip install pytest pytest-cov black flake8 mypy
```

### Update Dependencies
```powershell
pip list --outdated
pip install --upgrade <package>
pip freeze > requirements.txt  # Update requirements file
```

### Clean Virtual Environment
```powershell
deactivate  # Exit venv first
Remove-Item -Recurse -Force .venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

---

## Documentation Updates

### Auto-Approved Documentation Changes

**Safe to commit without asking:**
- README updates
- Documentation fixes (typos, clarity)
- AGENTS.md improvements from experience
- Adding examples or troubleshooting sections

**Commit pattern:**
```powershell
git add docs/ README.md AGENTS.md
git commit -m "docs: improve troubleshooting section"
```

---

## Maintenance Commands

### Repository Health Checks

**Check for uncommitted work:**
```powershell
git status --short
```

**List recent commits:**
```powershell
git log --oneline -10
```

**Check remote sync:**
```powershell
git fetch --dry-run
git status -sb  # Show branch tracking info
```

### Clean Up Operations

**Remove untracked files (dry run first):**
```powershell
git clean -n  # Preview what would be deleted
git clean -fd # Actually delete untracked files and directories
```

**Clean Python cache:**
```powershell
Get-ChildItem -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force
```

---

## Related Documentation

- [AGENTS.md](../../AGENTS.md) - Behavioural guidelines and autonomy rules
- [CONTRIBUTING.md](../../CONTRIBUTING.md) - Contribution guidelines
- [docs/processes/BRANCH_MANAGEMENT.md](BRANCH_MANAGEMENT.md) - GitFlow branching strategy
- [docs/processes/MERGE_TO_MAIN.md](MERGE_TO_MAIN.md) - Release workflow
- [docs/processes/PR_BEST_PRACTICES.md](PR_BEST_PRACTICES.md) - Pull request guidelines

---

**Last Updated:** 2025-11-01
**Maintainers:** Update this file when commands or procedures change.
