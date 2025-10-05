# Copilot Bot Workflow Best Practices

**Created:** October 5, 2025
**Purpose:** Prevent formatting issues and branch sync problems when working with GitHub Copilot bots

## The Problem

When Copilot creates PRs, they may fail CI checks due to:
1. **Formatting issues** (Black, Flake8)
2. **Trailing whitespace**
3. **Branch divergence** (main/develop out of sync)

## Solutions Implemented

### 1. EditorConfig for Automatic Formatting

**File:** `.editorconfig`

**What it does:**
- Automatically trims trailing whitespace on save
- Enforces UTF-8 encoding
- Sets consistent indentation
- Works with all major editors (VS Code, PyCharm, Sublime)

**Benefits:**
- Prevents formatting issues before they reach Copilot
- Contributors don't need to configure their editors
- Pre-commit hooks pass on first try

### 2. CI Workflow Auto-Approval for Copilot

**File:** `.github/workflows/ci.yml`

**Changes made:**
```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  pull_request_target:  # NEW: Auto-approve Copilot
    branches: [ main, develop ]
    types: [ opened, synchronize, reopened ]

permissions:  # NEW: Explicit permissions
  contents: read
  pull-requests: write
  checks: write
```

**Benefits:**
- Copilot PRs auto-run CI (no manual approval)
- Still secure for external contributors
- Faster feedback loop

### 3. Pre-commit Hooks

**File:** `.pre-commit-config.yaml`

**Hooks enabled:**
- Black (formatting)
- Flake8 (linting)
- trailing-whitespace (auto-fix)
- end-of-file-fixer
- check-yaml
- check-merge-conflict

**Benefits:**
- Catches issues locally before push
- Auto-fixes simple issues
- Prevents CI failures

## Workflow for Copilot PRs

### Before Assigning to Copilot

1. **Ensure branches are synced:**
   ```bash
   # On develop
   git pull origin main
   git push origin develop
   ```

2. **Verify EditorConfig is working:**
   - Check that `.editorconfig` exists
   - Your editor should show "EditorConfig" in status bar

3. **Create detailed issue:**
   - Clear acceptance criteria
   - Code examples
   - Reference existing patterns (e.g., DataLoader usage)

### After Copilot Creates PR

1. **Check CI status immediately:**
   ```bash
   gh pr view <number> --json statusCheckRollup
   ```

2. **If CI fails on formatting:**
   ```bash
   # Checkout the Copilot branch
   git fetch origin
   git checkout <copilot-branch-name>

   # Fix formatting
   black scripts/
   flake8 scripts/ --max-line-length=127

   # Commit and push
   git add -A
   git commit -m "style: fix formatting issues"
   git push origin <copilot-branch-name>
   ```

3. **Wait for CI to pass, then merge**

### After Merging Copilot PR

1. **Sync branches immediately:**
   ```bash
   # If PR merged to develop
   gh pr create --base main --head develop --title "Phase X Complete"

   # Or if PR merged to main
   git checkout develop
   git merge origin/main
   git push origin develop
   ```

## Common Issues & Fixes

### Issue 1: "Black would reformat X file"

**Cause:** Copilot didn't run Black before pushing

**Fix:**
```bash
# Checkout Copilot branch
git checkout <copilot-branch>

# Run Black
black scripts/

# Commit and push
git add -A
git commit -m "style: format with Black"
git push origin <copilot-branch>
```

### Issue 2: "E501 line too long"

**Cause:** Lines exceed 127 characters

**Fix:**
```python
# Before (line 150 > 127 chars)
logger.info(f"Creating chart for {destination} with parameters {params} and additional context")

# After (split across lines)
logger.info(
    f"Creating chart for {destination} with parameters "
    f"{params} and additional context"
)
```

### Issue 3: "F401 imported but unused"

**Cause:** Unused imports

**Fix:**
```python
# Before
from typing import Dict, List  # Dict and List unused

# After
# Removed unused imports
```

### Issue 4: Main and Develop Diverged

**Cause:** PRs merged to different branches without syncing

**Fix:**
```bash
# On develop
git merge origin/main -m "Merge main into develop"

# Resolve conflicts (usually keep develop version)
git checkout --theirs <conflicted-file>
git add -A
git commit

# Push and create PR
git push origin develop
gh pr create --base main --head develop
```

## Prevention Checklist

### Before Starting Work

- [ ] Main and develop are synced
- [ ] EditorConfig is installed in your editor
- [ ] Pre-commit hooks are installed (`pre-commit install`)
- [ ] Issue has clear acceptance criteria

### When Copilot Creates PR

- [ ] Check CI status immediately
- [ ] If formatting fails, fix on Copilot branch
- [ ] Wait for all checks to pass
- [ ] Review code before merging

### After Merging

- [ ] Sync main and develop branches
- [ ] Create PR if branches diverged
- [ ] Update milestones and close issues
- [ ] Document lessons learned

## Editor Configuration

### VS Code

**Install Extensions:**
1. EditorConfig for VS Code
2. Python (Microsoft)
3. Black Formatter

**Settings (settings.json):**
```json
{
  "editor.formatOnSave": true,
  "python.formatting.provider": "black",
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
}
```

### PyCharm

1. **Enable EditorConfig:**
   - Settings → Editor → Code Style → Enable EditorConfig support

2. **Configure Black:**
   - Settings → Tools → External Tools → Add Black
   - Program: `black`
   - Arguments: `$FilePath$`

3. **Format on Save:**
   - Settings → Tools → Actions on Save → Enable "Reformat code"

## Monitoring Tools

### Check CI Status
```bash
# View PR status
gh pr view <number>

# Watch CI run
gh run watch <run-id>

# List failed runs
gh run list --workflow=CI --status=failure
```

### Check Branch Sync
```bash
# Compare branches
git log --oneline main..develop  # In develop but not main
git log --oneline develop..main  # In main but not develop

# Check if branches diverged
git fetch origin
git log --graph --oneline --all -20
```

### Check Formatting Locally
```bash
# Check without fixing
black --check scripts/ tests/
flake8 scripts/ tests/ --max-line-length=127

# Fix automatically
black scripts/ tests/
```

## Success Metrics

### Good Indicators
- ✅ Copilot PRs pass CI on first or second try
- ✅ Main and develop stay in sync
- ✅ Pre-commit hooks catch issues locally
- ✅ No manual formatting needed

### Bad Indicators
- ❌ Repeated CI failures for formatting
- ❌ Main and develop constantly diverged
- ❌ Manual fixes needed after every Copilot PR
- ❌ Merge conflicts on every sync

## Emergency Procedures

### If Branches Are Badly Diverged

```bash
# Nuclear option: Reset develop to match main + add new commits
git checkout develop
git fetch origin

# Save develop's unique work
git diff origin/main..origin/develop > develop-changes.patch

# Reset develop to main
git reset --hard origin/main

# Apply develop's changes
git apply develop-changes.patch

# Force push (⚠️ DANGEROUS - coordinate with team)
git push --force origin develop
```

### If Pre-commit Hooks Are Broken

```bash
# Skip pre-commit (emergency only)
git commit --no-verify -m "emergency commit"

# Fix pre-commit hooks
pre-commit uninstall
pre-commit install
pre-commit run --all-files
```

## Future Improvements

### Potential Enhancements

1. **GitHub Action for Auto-formatting:**
   - Bot automatically commits formatting fixes
   - Runs on Copilot PRs only

2. **Branch Protection Rules:**
   - Require CI to pass before merge
   - Require develop to be up-to-date with main

3. **Automated Sync:**
   - GitHub Action to auto-sync develop with main
   - Runs daily or after each merge to main

4. **Copilot Configuration:**
   - Add `.copilot-instructions.md` with formatting requirements
   - Configure Copilot to run Black before creating PR

## References

- EditorConfig: https://editorconfig.org/
- Black: https://black.readthedocs.io/
- Pre-commit: https://pre-commit.com/
- GitHub Actions: https://docs.github.com/en/actions

---

**Last Updated:** October 5, 2025
**Status:** ✅ Implemented and tested
**Next Review:** After Phase 4A completion
