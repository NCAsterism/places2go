# MCP Tool Evaluation - November 2025

**Purpose:** Test available MCP tools for common tasks, evaluate effectiveness, build approved tool list

**Evaluation Period:** November 1-15, 2025
**Status:** In Progress

---

## Available MCP Tools (From VS Code)

### GitHub Pull Requests Category
- `github-pull-request_renderIssues` - Render issues in markdown table
- `github-pull-request_activePullRequest` - Get active PR info
- `github-pull-request_openPullRequest` - Get open PR info
- `github-pull-request_copilotCodingAgent` - Async task completion via PR
- `github-pull-request_suggest-fix` - Summarize and suggest fix for issue
- `github-pull-request_doSearch` - Search GitHub issues/PRs
- `github-pull-request_formSearchQuery` - Convert natural language to GitHub search query

### Azure Category
- `azure_resources-query_azure_resource_graph` - Query Azure Resource Graph (ARG)
- `azureResources_getAzureActivityLog` - Get Azure activity log
- Azure MCP (various Azure operations)

### Python Category
- `mcp_pylance_mcp_s_pylanceInvokeRefactoring` - Python code refactoring
- `mcp_pylance_mcp_s_pylanceDocuments` - Search Pylance documentation

### Documentation Category
- `mcp_microsoft_doc_microsoft_docs_search` - Search Microsoft/Azure docs
- `mcp_microsoft_doc_microsoft_docs_fetch` - Fetch full doc pages
- `mcp_microsoft_doc_microsoft_code_sample_search` - Search code samples

### Infrastructure Category
- `mcp_bicep_experim_get_az_resource_type_schema` - Get Azure resource schema
- `mcp_bicep_experim_get_bicep_best_practices` - Get Bicep best practices
- `mcp_bicep_experim_list_avm_metadata` - List Azure Verified Modules

---

## Common Tasks to Evaluate

### 1. Issue/Task Management
**Current Method:** Manually read/edit `data/issues.csv`, format in tables manually

**MCP Tools to Test:**
- [ ] `renderIssues` - Auto-format issues as table
- [ ] `suggest-fix` - Get AI suggestions for issue resolution
- [ ] `doSearch` - Search issues across repos

**Test Scenarios:**
- Display all high-priority tasks
- Find related issues across projects
- Get fix suggestions for specific issues

**Results:** _To be completed during testing_

---

### 2. Project Status Reporting
**Current Method:** Run `scripts/reports/project_status_tracker.py`, manual CSV reading

**MCP Tools to Test:**
- [ ] `renderIssues` - Format project status
- [ ] Custom Python scripts combined with MCP rendering

**Test Scenarios:**
- Quick status overview of all 5 projects
- Filter by status/priority
- Cross-project dependency view

**Results:** _To be completed during testing_

---

### 3. Pull Request Management
**Current Method:** Manual git commands, GitHub web UI navigation

**MCP Tools to Test:**
- [ ] `activePullRequest` - Get current PR details
- [ ] `openPullRequest` - Get visible PR info
- [ ] `copilotCodingAgent` - Create PR from issue asynchronously

**Test Scenarios:**
- Review current PR status
- Check PR reviews/comments
- Create PR from issue description

**Results:** _To be completed during testing_

---

### 4. Code Refactoring (Python)
**Current Method:** Manual edits, Black formatting, manual import cleanup

**MCP Tools to Test:**
- [ ] `pylanceInvokeRefactoring` with `source.unusedImports`
- [ ] `pylanceInvokeRefactoring` with `source.convertImportFormat`
- [ ] `pylanceInvokeRefactoring` with `source.fixAll.pylance`

**Test Scenarios:**
- Remove unused imports across module
- Convert import formats consistently
- Apply all Pylance fixes at once

**Results:** _To be completed during testing_

---

### 5. Documentation Research
**Current Method:** Web search, manual reading, copy-paste from docs

**MCP Tools to Test:**
- [ ] `microsoft_docs_search` - Quick doc lookup
- [ ] `microsoft_docs_fetch` - Get complete doc pages
- [ ] `microsoft_code_sample_search` - Find code examples

**Test Scenarios:**
- Look up Azure CLI commands
- Find Python best practices
- Get code samples for specific SDK

**Results:** _To be completed during testing_

---

### 6. Quality Gate Workflow
**Current Method:** Manual command sequences (Black, flake8, mypy, pytest)

**MCP Tools to Test:**
- [ ] `pylanceInvokeRefactoring` with `source.fixAll.pylance` - Auto-fix before tests
- [ ] Combined with terminal commands for full workflow

**Test Scenarios:**
- One-command quality check
- Auto-fix common issues before commit
- Validation without manual intervention

**Results:** _To be completed during testing_

---

### 7. Cross-Project Synchronization
**Current Method:** Manual file copying, git operations across repos

**MCP Tools to Test:**
- [ ] `doSearch` - Find similar issues/docs across repos
- [ ] Terminal commands combined with issue tracking

**Test Scenarios:**
- Apply same fix to all 5 projects
- Find inconsistencies in documentation
- Sync common files (AGENTS.md, etc.)

**Results:** _To be completed during testing_

---

## Testing Protocol

### For Each Tool:
1. **Document current approach** - Time taken, pain points
2. **Test MCP tool** - Execute on real task, note issues
3. **Compare results** - Quality, speed, reliability
4. **Rate experience** - 👍 Approve / 👎 Reject / 🤔 Conditional
5. **Document findings** - What works, what doesn't, when to use

### Rating Criteria:
- **Time savings** - Faster than manual method?
- **Quality** - Output accuracy and usefulness
- **Reliability** - Works consistently?
- **Learning curve** - Easy to remember and use?
- **Edge cases** - Handles unusual situations?

---

## Approved Tool List

_To be populated based on testing results_

### Tier 1: Use Always
_Tools that should replace manual workflows_

### Tier 2: Use When Appropriate
_Tools useful for specific scenarios_

### Tier 3: Experimental/Conditional
_Tools that need more refinement or have limitations_

### Not Recommended
_Tools that don't add value over current methods_

---

## Next Testing Session

**Focus Areas:**
1. Start with `renderIssues` - Most immediately useful for task overview
2. Test `suggest-fix` - Could accelerate issue resolution
3. Try `pylanceInvokeRefactoring` - Potential for quality gate automation

**Success Metrics:**
- Saves >30 seconds per task
- Output quality matches or exceeds manual approach
- Can be documented in simple instructions

---

## Notes & Observations

### Test 1: GitHub Issue Search & Rendering (Nov 1, 2025)

**Tools Tested:**
- `github-pull-request_formSearchQuery` ✅
- `github-pull-request_doSearch` ✅
- `github-pull-request_renderIssues` ⚠️

**What Worked:**
- `formSearchQuery` successfully converted "open issues with high priority" → proper GitHub search syntax
- `doSearch` retrieved 21 open issues from places2go repository with full metadata
- Search returns rich data: labels (with colors!), assignees, dates, URLs, comment counts

**What Didn't Work:**
- `renderIssues` has strict schema requirements - missing `reactionCount` field caused error
- Tool is finicky about exact JSON structure

**Key Finding #1: GitHub Issues vs Local CSV**
- GitHub MCP tools work ONLY with **GitHub Issues**, not local `issues.csv` files
- JobsJobsJobs has 0 GitHub Issues (uses CSV tracking)
- places2go has 21 GitHub Issues (data collection tasks)
- **Implication:** MCP GitHub tools useful for places2go, NOT for JobsJobsJobs task tracking

**Key Finding #2: Schema Strictness**
- MCP tools require exact schema matches
- Missing optional fields cause errors
- Less forgiving than manual approaches

**Time Comparison:**
- Manual: Open GitHub, navigate to Issues tab, scroll through ~15 seconds
- MCP: Search query + result retrieval ~5 seconds (once working correctly)
- **Savings: ~10 seconds per lookup** (after learning curve)

**When to Use:**
- ✅ Quick overview of issues across projects
- ✅ Filtered searches (by label, assignee, date)
- ✅ Programmatic issue tracking
- ❌ NOT for local CSV-based task management
- ❌ Complex table rendering (schema issues)

**Rating: 👍 Approve (with caveats)**
- Use `doSearch` for quick issue lookups
- Skip `renderIssues` due to schema brittleness (just format results manually)
- High value for projects using GitHub Issues (places2go)
- Zero value for CSV-based tracking (JobsJobsJobs)

**Recommendation:**
- Document in common_operations.md: "Use GitHub search MCP for places2go issue tracking"
- Consider migrating JobsJobsJobs tasks to GitHub Issues if MCP integration desired
- For now: Keep dual tracking (CSV for cross-project, GitHub Issues for per-project)
