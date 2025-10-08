# Merging develop to main

This document outlines the process for merging `develop` branch into `main` after completing a development phase or milestone.

## Pre-Merge Checklist

Before merging to `main`, ensure all quality checks pass on the `develop` branch.

### 1. Environment Setup

Ensure you're in the correct virtual environment:

```powershell
# Activate environment
.\.venv\Scripts\Activate.ps1

# Verify environment
python --version  # Should be Python 3.9+
python -c "import sys; print(sys.executable)"  # Should point to .venv

# Ensure package is installed
pip install -e .
```

### 2. Run Test Suite

```powershell
# Set PYTHONPATH for test imports
$env:PYTHONPATH = "D:\repo\places2go"

# Run all tests with coverage
pytest -v --tb=short --cov=scripts --cov-report=term

# Expected: Most tests passing
# Known issues: UTF-8 encoding failures on Windows (tracked in data/issues.csv)
```

**Acceptance Criteria:**
- ✅ Core functionality tests passing (>90%)
- ✅ Known failures are documented in issues.csv
- ✅ No new regressions introduced

### 3. Code Formatting Check

```powershell
# Run Black formatter
black scripts tests

# Verify formatting
black --check scripts tests
```

**Acceptance Criteria:**
- ✅ All files pass Black formatting
- ✅ No "would reformat" messages

### 4. Linting Check

```powershell
# Run flake8
flake8 scripts tests --max-line-length=88 --extend-ignore=E203,W503
```

**Acceptance Criteria:**
- ✅ No critical errors (F-level)
- ✅ Line length issues in HTML strings are acceptable
- ✅ Unused imports documented or removed

### 5. Type Checking (Optional but Recommended)

```powershell
# Run mypy
mypy scripts/
```

**Acceptance Criteria:**
- ✅ No type errors in core modules
- ✅ Visualization modules may have Plotly-related type issues (acceptable)

### 6. Documentation Check

Ensure all documentation is up to date:

- ✅ README.md reflects current state
- ✅ CONTRIBUTING.md has latest guidelines
- ✅ AGENTS.md has environment instructions
- ✅ Changelog or milestone documents updated
- ✅ Any new features documented in relevant places

## Merge Process

### Option 1: Direct Merge (Recommended for Minor Updates)

```powershell
# Ensure you're on develop
git checkout develop
git pull origin develop

# Checkout main and merge
git checkout main
git pull origin main
git merge develop --no-ff -m "Merge develop into main: [brief description]"

# Push to remote
git push origin main

# Return to develop
git checkout develop
```

### Option 2: Pull Request (Recommended for Major Releases)

```powershell
# Create a release branch from develop
git checkout develop
git pull origin develop
git checkout -b release/v0.X.0

# Push release branch
git push origin release/v0.X.0

# Create PR via GitHub CLI
gh pr create --base main --head release/v0.X.0 \
  --title "Release v0.X.0: [description]" \
  --body "See CHANGELOG.md for details"
```

Then:
1. Review PR on GitHub
2. Wait for CI checks to pass
3. Merge PR via GitHub interface
4. Delete release branch
5. Tag the release:
   ```powershell
   git checkout main
   git pull origin main
   git tag -a v0.X.0 -m "Version 0.X.0: [description]"
   git push origin v0.X.0
   ```

## Post-Merge Tasks

### 1. Sync develop with main

After merging to main, sync develop to keep branches aligned:

```powershell
git checkout develop
git pull origin main
git push origin develop
```

### 2. Update Issues/Milestones

- Close completed issues
- Update milestone progress
- Update issues.csv if using it

### 3. Deploy (if applicable)

Follow deployment procedures in `docs/deployment/` (if exists) or project README.

## Common Issues & Solutions

### Issue: Merge Conflicts

**Solution:**
```powershell
# If conflicts occur during merge
git status  # See conflicting files
# Resolve conflicts manually in editor
git add <resolved-files>
git commit
```

### Issue: Tests Fail After Merge

**Solution:**
- Revert the merge: `git reset --hard origin/main`
- Fix issues on develop
- Retry merge process

### Issue: CI Fails on Main

**Solution:**
- If caught immediately, can force push a fix
- Otherwise, create hotfix branch from main
- Fix and merge hotfix back to both main and develop

## Quality Gates Summary

| Check | Command | Expected Result |
|-------|---------|-----------------|
| Tests | `pytest -v` | >90% passing, documented failures |
| Formatting | `black --check scripts tests` | All files formatted |
| Linting | `flake8 scripts tests` | No critical errors |
| Type Check | `mypy scripts/` | No type errors in core |
| Documentation | Manual review | All docs current |

## Automation Opportunities

Consider creating:
1. **Pre-merge script** (`scripts/pre_merge_check.ps1`) - Runs all quality checks
2. **GitHub Action** - Automated checks on PR to main
3. **Release automation** - Script to create release branches and tags

## Related Documents

- [Branching Strategy](branching.md)
- [PR Best Practices](PR_BEST_PRACTICES.md)
- [Contributing Guidelines](../../CONTRIBUTING.md)
- [Agent Guide](../../AGENTS.md)

---

**Last Updated:** October 8, 2025
**Maintained By:** Project maintainers
