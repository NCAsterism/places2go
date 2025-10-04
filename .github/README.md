# GitHub Issues Setup - Ready for Automation

## Overview
This directory contains everything needed to create and manage GitHub issues for the Places2Go project. Issues are organized by phase and can be created manually or automatically using the provided scripts.

## Files

### Issue Templates
Located in `.github/ISSUE_TEMPLATE/`:
- `feature_request.md` - Template for new feature requests
- `bug_report.md` - Template for bug reports
- `test_task.md` - Template for testing tasks

### Issue Definitions
- `GITHUB_ISSUES.md` - Detailed issue descriptions for Phases 2-3
- `create_issues.py` - Python script to auto-create Phase 2 issues

## Phase 2 Issues (v0.2.0) - 8 Issues Ready

### Testing Issues (High Priority)
1. **Add Tests for Chart Generation Functions** - 4 hours
   - Increase coverage from 44% to 60%+
   - Test both chart generation functions
   - Add error handling tests

2. **Add Integration Test for Full Dashboard Workflow** - 2 hours
   - End-to-end workflow testing
   - Verify complete data pipeline

### Code Quality Issues (Medium-High Priority)
3. **Add Type Hints to All Functions** - 2 hours
   - Complete type annotations
   - Prepare for mypy

4. **Configure mypy for Static Type Checking** - 1 hour
   - Setup mypy configuration
   - Add to CI/CD pipeline

5. **Add Logging Framework** - 3 hours
   - Replace print statements
   - Setup file and console logging

6. **Add Custom Exceptions** - 2 hours
   - Domain-specific exceptions
   - Better error handling

7. **Add Data Validation** - 3 hours
   - Validate CSV data quality
   - Comprehensive error checking

8. **Add Pre-commit Hooks** - 2 hours
   - Auto-format and lint
   - Improve developer experience

**Total Estimated Time:** ~19 hours

## Creating Issues

### Option 1: Automatic Creation (Recommended)

Using the Python script (requires GitHub CLI):

```bash
# Prerequisites
# 1. Install GitHub CLI: https://cli.github.com/
# 2. Authenticate: gh auth login
# 3. Set repo: gh repo set-default

# Run the script
python scripts/create_issues.py
```

The script will:
- Verify GitHub CLI is installed and authenticated
- Create all 8 Phase 2 issues
- Apply appropriate labels and milestones
- Provide summary of created issues

### Option 2: Using GitHub CLI Manually

```bash
# Example: Create Issue #1
gh issue create \
  --title "Add Tests for Chart Generation Functions" \
  --body-file .github/issue_bodies/issue_01.md \
  --label "testing,phase-2,high-priority" \
  --milestone "v0.2.0"
```

### Option 3: Manual Creation on GitHub

1. Go to repository → Issues → New Issue
2. Copy content from `GITHUB_ISSUES.md`
3. Apply appropriate labels
4. Assign to milestone "v0.2.0"

## Labels to Create

Before creating issues, ensure these labels exist in your repository:

### Priority Labels
- `high-priority` (red)
- `medium-priority` (orange)
- `low-priority` (yellow)

### Type Labels
- `testing` (green)
- `code-quality` (blue)
- `error-handling` (purple)
- `tooling` (gray)
- `integration` (light blue)

### Phase Labels
- `phase-2` (pink)
- `phase-3` (light pink)
- `phase-4` (lighter pink)

### Other Labels
- `enhancement` (default green)
- `bug` (default red)
- `documentation` (default blue)
- `good-first-issue` (default green)
- `developer-experience` (teal)
- `architecture` (dark blue)

## Milestones to Create

Create these milestones in your GitHub repository:

1. **v0.2.0 - Enhanced Testing & Code Quality**
   - Due date: October 18, 2025
   - Description: "Improve test coverage to 80%+ and enhance code quality with type hints, logging, and error handling"

2. **v0.3.0 - Data Module Architecture**
   - Due date: November 8, 2025
   - Description: "Create modular data retrieval system with abstract base classes and Pydantic models"

3. **v0.4.0 - Interactive Dashboard**
   - Due date: December 1, 2025
   - Description: "Upgrade from static HTML to interactive Streamlit dashboard"

4. **v0.5.0 - Cost of Living**
   - Due date: January 5, 2026
   - Description: "Add comprehensive cost of living data and extended metrics"

5. **v1.0.0 - Production Release**
   - Due date: February 1, 2026
   - Description: "Deploy application and prepare for public use"

## Assigning Issues

### To GitHub Agents
When creating issues, you can assign them to GitHub Copilot agents:

```bash
gh issue create \
  --title "Issue Title" \
  --body "Issue body" \
  --assignee "@me"  # Or specific username
```

### Assignment Strategy
- **High Priority + Testing:** Assign first (Issues #1, #2, #5, #7)
- **Medium Priority:** Assign after high priority complete
- **Dependencies:** Respect dependency order:
  - Issue #3 before #4 (type hints before mypy)
  - Issue #6 before #7 (exceptions before validation)

## Issue Workflow

### 1. Issue Created
- Issue appears in project board "To Do" column
- Labels and milestone assigned
- Agent or contributor assigned

### 2. Work Begins
- Move to "In Progress" column
- Create feature branch: `feature/issue-{number}-description`
- Commit regularly with references: `git commit -m "feat: ... (#1)"`

### 3. Pull Request
- Create PR with reference: "Fixes #1"
- Request review
- CI/CD checks must pass

### 4. Review & Merge
- At least 1 approval required
- All checks passing
- Merge to `develop` branch
- Issue automatically closed

### 5. Testing
- Feature tested on `develop`
- Included in next release

## Project Board Setup

Create a GitHub Project board with these columns:

1. **Backlog** - Future issues not yet prioritized
2. **To Do** - Ready to work on
3. **In Progress** - Currently being worked on
4. **In Review** - PR open, awaiting review
5. **Done** - Completed and merged

## Automated Issue Management

Consider setting up these GitHub Actions:

1. **Label Based on Title**
   ```yaml
   - If title contains "[TEST]" → add "testing" label
   - If title contains "[BUG]" → add "bug" label
   - If title contains "[FEATURE]" → add "enhancement" label
   ```

2. **Stale Issue Management**
   - Mark issues inactive for 30 days as "stale"
   - Close issues inactive for 60 days

3. **Auto-assign to Project**
   - New issues automatically added to project board

## Next Steps

1. **Push to GitHub** (if not already done):
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/places2go.git
   git push -u origin main
   git push -u origin develop
   ```

2. **Create Labels**:
   ```bash
   gh label create "high-priority" --color "d73a4a"
   gh label create "phase-2" --color "fbca04"
   # ... (see labels section above)
   ```

3. **Create Milestones**:
   ```bash
   gh api repos/:owner/:repo/milestones -f title="v0.2.0" -f due_on="2025-10-18T00:00:00Z"
   ```

4. **Run Issue Creation Script**:
   ```bash
   python scripts/create_issues.py
   ```

5. **Set Up Project Board**:
   - Go to repository → Projects → New Project
   - Choose "Board" template
   - Add automation rules

## FAQ

**Q: Can I modify issues after creation?**
A: Yes, use `gh issue edit <number>` or edit directly on GitHub.

**Q: How do I assign issues to myself?**
A: `gh issue develop <number> --checkout` or click "Assign yourself" on GitHub.

**Q: Can I create custom issue templates?**
A: Yes, add more .md files to `.github/ISSUE_TEMPLATE/`.

**Q: How do I track progress?**
A: Use GitHub Projects board or run `gh issue list --milestone "v0.2.0"`.

---

**Ready to create issues?** Run `python scripts/create_issues.py` to get started!
