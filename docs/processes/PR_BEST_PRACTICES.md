# Pull Request Best Practices

**Last Updated:** October 4, 2025
**Based on:** Phase 2 lessons learned

---

## Overview

This document outlines best practices for creating and managing Pull Requests to avoid merge conflicts and maintain code quality.

## Lessons Learned from Phase 2

### Problems Encountered
1. **Overlapping PRs** - Multiple PRs modified the same files (dashboard.py)
2. **Merge Conflicts** - PRs #10, #12, #13, #15, #16 all had conflicts
3. **Bad Merges** - PR #15 was merged with unresolved conflict markers (`<<<<<<< HEAD`)
4. **Bot PR Quality** - GitHub Copilot bot PRs sometimes had CI failures or conflicts
5. **Large PRs** - Some PRs tried to do too much, making conflicts harder to resolve

### Key Learnings
- ✅ **Small, focused PRs** are easier to review and merge
- ✅ **Manual review** of bot PRs is essential
- ✅ **Test locally** before merging, even if CI passes
- ✅ **Check for conflict markers** in merged code
- ✅ **Sequential merging** is safer than parallel for overlapping changes
- ✅ **Sometimes starting fresh** is better than fixing conflicts

---

## PR Creation Guidelines

### 1. Before Creating a PR

**Check existing PRs:**
```bash
# List all open PRs
gh pr list

# Check if your target files are in other PRs
gh pr view <PR_NUMBER> --json files
```

**Update your branch:**
```bash
# Switch to your feature branch
git checkout feature/your-feature

# Fetch latest changes
git fetch origin

# Rebase on latest develop
git rebase origin/develop
```

**Run all checks locally:**
```bash
# Format code
black .

# Type checking
mypy scripts tests

# Run tests
pytest -v

# Run pre-commit hooks
pre-commit run --all-files
```

### 2. PR Size Guidelines

**Ideal PR sizes:**
- **Small:** 1-50 lines changed (1 day review)
- **Medium:** 51-200 lines changed (2-3 day review)
- **Large:** 201-500 lines changed (week-long review)
- **Too Large:** 500+ lines (consider splitting)

**One PR should address:**
- ✅ One feature or bug fix
- ✅ One logical unit of work
- ✅ Changes that naturally go together

**Split large changes into:**
1. Infrastructure/setup PR
2. Core functionality PR
3. Tests PR
4. Documentation PR

### 3. Files to Avoid Simultaneous Changes

**High-conflict files** (coordinate carefully):
- `scripts/dashboard.py` - Core application logic
- `requirements.txt` - Dependencies
- `pyproject.toml` - Project configuration
- `CONTRIBUTING.md` - Process documentation
- `.github/workflows/ci.yml` - CI configuration

**Strategy for high-conflict files:**
1. Check if others are modifying them
2. Coordinate merge order
3. Merge sequentially, not in parallel
4. Update your branch after each merge

### 4. PR Description Template

```markdown
## Description
Brief description of what this PR does (1-2 sentences)

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #<issue_number>

## Changes Made
- Bullet point list of specific changes
- Be specific about files modified
- Explain why changes were needed

## Testing
- [ ] All existing tests pass
- [ ] New tests added (if applicable)
- [ ] Manual testing performed
- [ ] Pre-commit hooks pass

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated (if needed)
- [ ] No console.log or debug statements
- [ ] Branch is up-to-date with develop

## Screenshots (if UI changes)
[Add screenshots here]

## Additional Notes
Any other context, concerns, or discussion points
```

---

## PR Review Process

### For PR Authors

**Before requesting review:**
```bash
# 1. Self-review your changes
git diff develop...HEAD

# 2. Check for common issues
grep -r "<<<<<<" .  # Check for conflict markers
grep -r "TODO" .    # Check for unfinished work
grep -r "console.log\|print(" .  # Check for debug statements

# 3. Run full test suite
pytest -v --cov

# 4. Check CI status
gh pr checks
```

**Responding to review comments:**
- Address all comments (or explain why not)
- Push fixes in separate commits (don't force-push)
- Mark conversations as resolved after fixing
- Thank reviewers for their time

### For PR Reviewers

**Review checklist:**
- [ ] PR description is clear and complete
- [ ] Changes match the issue description
- [ ] Code follows project conventions
- [ ] Tests are adequate and pass
- [ ] No obvious security issues
- [ ] Documentation is updated
- [ ] No merge conflicts
- [ ] CI checks pass

**When to request changes:**
- Logic errors or bugs
- Security vulnerabilities
- Missing tests for new functionality
- Unclear or undocumented code
- Style violations

**When to approve:**
- All checks pass
- Code is clear and maintainable
- Tests are comprehensive
- Minor issues can be addressed in follow-up

---

## Merge Strategy

### Sequential Merging for Overlapping PRs

When multiple PRs touch the same files:

1. **Prioritize by dependency:**
   - Infrastructure changes first
   - Core functionality second
   - Tests and documentation last

2. **Merge one at a time:**
   ```bash
   # Merge PR #1
   gh pr merge <PR_NUMBER> --squash

   # Wait for CI to complete
   # Update PR #2
   git checkout feature/pr-2
   git fetch origin
   git rebase origin/develop
   git push --force-with-lease

   # Merge PR #2
   gh pr merge <PR_NUMBER> --squash
   ```

3. **Validate after each merge:**
   ```bash
   git checkout develop
   git pull
   pytest -v
   ```

### Handling Merge Conflicts

**Option 1: Rebase (preferred for feature branches)**
```bash
git checkout feature/your-branch
git fetch origin
git rebase origin/develop

# If conflicts occur:
# 1. Fix conflicts in each file
# 2. git add <resolved-files>
# 3. git rebase --continue
# 4. Repeat until done

git push --force-with-lease
```

**Option 2: Manual Resolution (for complex conflicts)**
```bash
# Create a fresh branch
git checkout develop
git pull
git checkout -b feature/your-feature-v2

# Manually reapply your changes
# Copy logic from old branch, don't just copy-paste code
# Test thoroughly

# Create new PR
gh pr create --base develop --head feature/your-feature-v2
```

**When to start fresh:**
- Conflicts affect >30% of your changes
- Multiple files have complex conflicts
- Original branch has multiple failed merge attempts
- Easier to reimplement than resolve

### Verifying Merges

**Critical: Check merged code doesn't have conflict markers!**

```bash
# After merging, check for conflict markers
git checkout develop
git pull
grep -r "<<<<<<\|>>>>>>\|======" scripts/ tests/

# Run full test suite
pytest -v

# Check application runs
python scripts/dashboard.py
```

**Phase 2 Example:** PR #15 was merged but contained:
```python
<<<<<<< HEAD
# logging code
=======
# exception code
>>>>>>> feature/exceptions
```

This broke the application! Always verify clean merges.

---

## Bot PR Management

### GitHub Copilot Bot PRs

**Pros:**
- Fast implementation
- Follows patterns well
- Good for routine changes

**Cons:**
- May not understand full context
- Can create merge conflicts
- Might miss edge cases

**Review checklist for bot PRs:**
1. **Check CI status** - Don't merge if CI fails
2. **Review all changes** - Even if bot-generated
3. **Test locally** - Don't trust CI alone
4. **Check conflicts** - Update branch if needed
5. **Verify logic** - Ensure changes make sense
6. **Run full test suite** - Not just changed tests

**When to close bot PRs:**
- CI failures that are complex to fix
- Merge conflicts in multiple files
- Changes don't align with project goals
- Easier to implement manually

**Phase 2 Example:**
- Merged: PRs #9, #11, #12, #14 (clean, good CI)
- Closed: PRs #10, #13, #16 (conflicts, easier to redo)

---

## Conflict Prevention Strategies

### 1. Coordinate with Team

**Before starting work:**
```bash
# Check what others are working on
gh pr list
gh issue list --assignee @me

# Announce your intentions
# Comment on issue: "Starting work on this"
```

**During development:**
- Update your branch daily
- Check for new PRs affecting your files
- Communicate about overlapping work

### 2. Modular Code Structure

**Good practices:**
- Keep functions small and focused
- One function per feature
- Minimize file-level changes
- Use separate files for separate concerns

**Example:**
```
# Instead of this (everything in dashboard.py):
dashboard.py  (500 lines)

# Do this:
scripts/
  dashboard.py       (100 lines - orchestration)
  data_loader.py     (50 lines - data operations)
  chart_builder.py   (100 lines - chart creation)
  exceptions.py      (50 lines - custom errors)
  utils.py           (50 lines - helpers)
```

### 3. Feature Flags

For large features, use feature flags:

```python
# In config or environment
ENABLE_NEW_CHART_TYPE = os.getenv("ENABLE_NEW_CHART", "false") == "true"

# In code
if ENABLE_NEW_CHART_TYPE:
    create_advanced_chart(data)
else:
    create_basic_chart(data)
```

Benefits:
- Merge incomplete features safely
- Test in production without exposing
- Roll back without code changes

---

## Emergency Procedures

### Reverting a Bad Merge

```bash
# Find the bad commit
git log --oneline -10

# Revert it (creates new commit)
git revert <commit-hash> --no-edit

# Or revert and keep working tree
git revert <commit-hash> --no-commit
# Fix issues manually
git commit

# Push immediately
git push
```

**Phase 2 Example:**
```bash
# PR #15 merged with conflict markers in commit d1fff18
git revert d1fff18 --no-edit
# Removed 9 corrupted files
# Then manually recreated clean versions
```

### Hotfix Process

For critical production bugs:

```bash
# Branch from main, not develop
git checkout main
git pull
git checkout -b hotfix/critical-bug

# Make minimal fix
# Test thoroughly

# PR to main (skip develop)
gh pr create --base main --title "Hotfix: ..."

# After merge, backport to develop
git checkout develop
git cherry-pick <hotfix-commit>
git push
```

---

## Automation & Tools

### Pre-commit Hook Configuration

Ensure `.pre-commit-config.yaml` includes:
```yaml
- repo: local
  hooks:
    - id: check-merge-conflict
      name: Check for merge conflicts
      entry: Check for merge conflicts
      language: system
      always_run: true
```

### GitHub Actions CI

Ensure CI runs:
- Code formatting checks (Black)
- Type checking (mypy)
- All tests (pytest)
- Coverage reports
- Merge conflict detection

### Useful Git Aliases

Add to `~/.gitconfig`:
```ini
[alias]
    # Show files changed in PR
    pr-files = diff --name-only develop...HEAD

    # Check for conflict markers
    check-conflicts = !git grep -n "<<<<<<\\|>>>>>>\\|======"

    # Update feature branch
    sync = !git fetch origin && git rebase origin/develop

    # Clean merged branches
    cleanup = !git branch --merged | grep -v '\\*\\|main\\|develop' | xargs -n 1 git branch -d
```

---

## Summary: Phase 2 → Phase 3 Improvements

| Issue | Phase 2 Problem | Phase 3 Solution |
|-------|-----------------|------------------|
| Merge conflicts | 5 PRs had conflicts | Coordinate overlapping work, merge sequentially |
| Bad merges | PR #15 had conflict markers | Always verify merged code, no `<<<<<<<` markers |
| Bot PR quality | Mixed results | Thorough review, close if conflicts complex |
| Large file changes | dashboard.py modified by all PRs | Split into smaller modules |
| Parallel merging | Caused cascading conflicts | Sequential merging for overlapping files |
| No process docs | Learned by trial and error | This document! |

---

## Quick Reference

**Before PR:**
```bash
gh pr list                          # Check existing PRs
git rebase origin/develop           # Update branch
pre-commit run --all-files          # Run hooks
pytest -v --cov                     # Run tests
```

**Creating PR:**
```bash
gh pr create --fill                 # Use template
gh pr create --draft                # Draft for WIP
```

**After Review:**
```bash
git commit --amend                  # Fix last commit
git push --force-with-lease         # Safe force push
```

**Merging:**
```bash
gh pr merge --squash                # Squash and merge
git grep "<<<<<<" .                 # Check for conflicts
pytest -v                           # Verify tests
```

---

**Remember:** Small PRs, good communication, and thorough testing prevent 90% of merge issues!

**Questions?** Ask in GitHub Discussions or create an issue with the `question` label.
