# Project Structure Reorganization Plan

**Date:** October 4, 2025
**Status:** Proposed
**Purpose:** Improve organization and reduce merge conflicts

---

## Current Problems

1. **Root directory cluttered** - Too many markdown files at root
2. **Documentation scattered** - Some in root, some in docs/, some in wiki/
3. **Scripts not modular** - dashboard.py handles everything
4. **Data structure unclear** - Single CSV for all data types
5. **Output mixed with source** - output/, logs/, htmlcov/ at root

---

## Proposed Structure

```
places2go/
├── .github/                      # GitHub-specific files (unchanged)
│   ├── ISSUE_TEMPLATE/
│   ├── workflows/
│   └── README.md
│
├── data/                         # Data directory (reorganized)
│   ├── destinations/             # Static destination data
│   │   ├── destinations.csv      # Core destination info
│   │   └── cost_of_living.csv    # Monthly costs per destination
│   ├── flights/                  # Flight data (time-series)
│   │   └── flight_prices.csv     # Date, origin, dest, price, duration
│   ├── weather/                  # Weather data (time-series)
│   │   └── weather_data.csv      # Date, destination, temp, conditions
│   └── README.md                 # Data schema documentation
│
├── docs/                         # All project documentation
│   ├── architecture/
│   │   ├── data_model.md         # Database/CSV schema
│   │   ├── system_design.md      # Overall architecture
│   │   └── tech_stack.md         # Technology decisions
│   ├── development/
│   │   ├── setup.md              # Dev environment setup
│   │   ├── testing.md            # Testing guidelines
│   │   └── debugging.md          # Common issues & solutions
│   ├── processes/
│   │   ├── PR_BEST_PRACTICES.md  # (moved from root)
│   │   ├── branching.md          # Git workflow
│   │   └── code_review.md        # Review checklist
│   ├── project/
│   │   ├── ROADMAP.md            # (moved from root)
│   │   ├── PHASE1_COMPLETE.md    # (moved from root)
│   │   ├── PHASE2_COMPLETE.md    # (moved from root)
│   │   └── PHASE3_PLAN.md        # (moved from root)
│   └── README.md                 # Documentation index
│
├── scripts/                      # Reorganized scripts
│   ├── core/                     # Core application modules
│   │   ├── __init__.py
│   │   ├── data_loader.py        # Load and merge CSV files
│   │   ├── data_validator.py     # Validate data integrity
│   │   ├── chart_builder.py      # Chart creation logic
│   │   ├── exceptions.py         # (existing)
│   │   └── config.py             # Configuration management
│   ├── cli/                      # Command-line interface
│   │   ├── __init__.py
│   │   └── dashboard_cli.py      # CLI for static dashboard
│   ├── utils/                    # Utility functions
│   │   ├── __init__.py
│   │   ├── file_utils.py         # File operations
│   │   └── date_utils.py         # Date/time helpers
│   ├── dashboard.py              # Main entry point (simplified)
│   └── __init__.py
│
├── tests/                        # Test directory (organized)
│   ├── unit/                     # Unit tests
│   │   ├── test_data_loader.py
│   │   ├── test_chart_builder.py
│   │   └── test_validators.py
│   ├── integration/              # Integration tests
│   │   ├── test_full_workflow.py
│   │   └── test_data_pipeline.py
│   ├── fixtures/                 # Test data and fixtures
│   │   ├── sample_destinations.csv
│   │   └── sample_flights.csv
│   ├── test_charts.py            # (existing - keep for now)
│   ├── test_data.py              # (existing - keep for now)
│   └── conftest.py               # Pytest configuration
│
├── wiki/                         # GitHub Wiki content (unchanged)
│
├── .build/                       # Build artifacts (new, gitignored)
│   ├── coverage/                 # Coverage reports
│   ├── logs/                     # Application logs
│   └── output/                   # Generated charts
│
├── .venv/                        # Virtual environment (gitignored)
│
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt          # New: dev-only dependencies
├── setup.py                      # Package installation
│
├── README.md                     # Main readme (stays at root)
├── CONTRIBUTING.md               # Contributor guide (stays at root)
├── LICENSE                       # License (stays at root)
└── CHANGELOG.md                  # New: Version history

```

---

## Changes Breakdown

### 1. Documentation Reorganization

**Move from root to docs/:**
- `ROADMAP.md` → `docs/project/ROADMAP.md`
- `PHASE1_COMPLETE.md` → `docs/project/PHASE1_COMPLETE.md`
- `PHASE2_COMPLETE.md` → `docs/project/PHASE2_COMPLETE.md`
- `PHASE3_PLAN.md` → `docs/project/PHASE3_PLAN.md`
- `BUILD_SUMMARY.md` → `docs/project/BUILD_SUMMARY.md` (or delete if outdated)
- `READY_TO_PUSH.md` → `docs/project/READY_TO_PUSH.md` (or delete if outdated)
- `WIKI_COMPLETE.md` → `docs/project/WIKI_COMPLETE.md` (or delete if outdated)
- `WIKI_SUMMARY.md` → `docs/project/WIKI_SUMMARY.md` (or delete if outdated)

**Keep at root:**
- `README.md` - Primary entry point
- `CONTRIBUTING.md` - Visible to contributors
- `LICENSE` - Required at root

**New documentation:**
- `docs/README.md` - Documentation index
- `docs/architecture/data_model.md` - Data schema
- `CHANGELOG.md` - Version history

### 2. Data Structure Reorganization

**Current:**
```
data/
  dummy_data.csv  (everything mixed together)
```

**Proposed:**
```
data/
  destinations/
    destinations.csv         # Core info: name, country, coordinates
    cost_of_living.csv       # Monthly costs: rent, food, transport
  flights/
    flight_prices.csv        # Time-series flight data
  weather/
    weather_data.csv         # Weather observations
  README.md                  # Schema documentation
```

**Benefits:**
- Separate static from time-series data
- Easier to update individual data types
- Clearer data ownership
- Better for version control (fewer conflicts)

### 3. Scripts Modularization

**Current:**
```python
# scripts/dashboard.py - 200+ lines doing everything
def main():
    # Load data
    # Validate data
    # Create charts
    # Save outputs
    # Handle errors
```

**Proposed:**
```python
# scripts/dashboard.py - Orchestration only
from core.data_loader import DataLoader
from core.chart_builder import ChartBuilder

def main():
    loader = DataLoader()
    data = loader.load_all()
    builder = ChartBuilder()
    builder.create_all_charts(data)

# scripts/core/data_loader.py - Data operations
class DataLoader:
    def load_destinations(self): ...
    def load_flights(self): ...
    def merge_data(self): ...

# scripts/core/chart_builder.py - Chart creation
class ChartBuilder:
    def create_cost_chart(self, data): ...
    def create_time_chart(self, data): ...
```

**Benefits:**
- Smaller, focused files
- Easier to test individual components
- Fewer merge conflicts
- Better code reuse
- Clearer separation of concerns

### 4. Output Directory Consolidation

**Move to .build/ (gitignored):**
- `output/` → `.build/output/`
- `logs/` → `.build/logs/`
- `htmlcov/` → `.build/coverage/`

**Update .gitignore:**
```gitignore
.build/
!.build/.gitkeep
```

### 5. Test Organization

**Separate unit and integration tests:**
```
tests/
  unit/              # Fast, isolated tests
  integration/       # Full workflow tests
  fixtures/          # Test data
  conftest.py        # Shared fixtures
```

---

## Migration Plan

### Phase 1: Documentation (Day 1)
```bash
# Create new structure
mkdir -p docs/{architecture,development,processes,project}

# Move files
mv ROADMAP.md docs/project/
mv PHASE*.md docs/project/
mv docs/PR_BEST_PRACTICES.md docs/processes/
mv docs/branching_strategy.md docs/processes/branching.md
mv docs/task_breakdown.md docs/project/

# Create index
# Create docs/README.md
```

### Phase 2: Data Structure (Day 2-3)
```bash
# Create new data structure
mkdir -p data/{destinations,flights,weather}

# Split dummy_data.csv into separate files
# (Python script to do this)

# Create data/README.md with schema
```

### Phase 3: Scripts Modularization (Day 4-5)
```bash
# Create new structure
mkdir -p scripts/{core,cli,utils}

# Extract components from dashboard.py
# Create separate modules

# Update imports
# Test thoroughly
```

### Phase 4: Output Reorganization (Day 1)
```bash
# Create build directory
mkdir -p .build/{output,logs,coverage}

# Update .gitignore
# Update scripts to use new paths
# Update CI to use new paths
```

### Phase 5: Test Organization (Day 2)
```bash
# Create test structure
mkdir -p tests/{unit,integration,fixtures}

# Move/organize existing tests
# Update imports
```

---

## Implementation Strategy

### Option A: Big Bang (Not Recommended)
- Move everything at once
- High risk of breaking things
- Single large PR

### Option B: Incremental (Recommended)
- One phase at a time
- Each phase is a separate PR
- Easier to review and test
- Can pause between phases

### Option C: Hybrid (Balanced)
- Phases 1 & 4 together (low risk)
- Phase 2 separate (data structure)
- Phase 3 separate (scripts)
- Phase 5 separate (tests)

---

## Backward Compatibility

### Maintain during transition:

1. **Old paths work temporarily:**
```python
# In data_loader.py
def load_data():
    # Try new path first
    if os.path.exists('data/destinations/destinations.csv'):
        return load_new_structure()
    # Fall back to old path
    elif os.path.exists('data/dummy_data.csv'):
        logger.warning("Using deprecated data structure")
        return load_old_structure()
```

2. **Symlinks for imports:**
```bash
# During transition
ln -s scripts/core/data_loader.py scripts/data_loader.py
```

3. **Deprecation warnings:**
```python
import warnings

def old_function():
    warnings.warn(
        "old_function is deprecated, use new_function",
        DeprecationWarning
    )
```

---

## Testing Strategy

### For each phase:

1. **Before changes:**
```bash
pytest -v --cov
python scripts/dashboard.py  # Verify it works
```

2. **After changes:**
```bash
pytest -v --cov  # All tests pass
python scripts/dashboard.py  # Still works
# Manual verification of outputs
```

3. **Compare outputs:**
```bash
# Generate before
python scripts/dashboard.py
mv output output_before

# Make changes

# Generate after
python scripts/dashboard.py
mv output output_after

# Compare
diff -r output_before output_after
```

---

## Documentation Updates

### Update after reorganization:

- [ ] README.md - Update file paths
- [ ] CONTRIBUTING.md - Update setup instructions
- [ ] Wiki pages - Update code examples
- [ ] CI configuration - Update paths
- [ ] pyproject.toml - Update package structure

---

## Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Break existing code | High | Medium | Thorough testing, gradual rollout |
| CI failures | Medium | High | Update CI configs early |
| Documentation outdated | Medium | High | Update docs same PR as code |
| Import errors | High | Medium | Use relative imports, test thoroughly |
| Data migration issues | High | Low | Keep old data as backup |

---

## Success Criteria

- [ ] All documentation in docs/ directory
- [ ] Clear separation of data types
- [ ] Scripts < 100 lines each
- [ ] All tests passing
- [ ] CI green
- [ ] No functionality lost
- [ ] Improved merge conflict resistance
- [ ] Easier to navigate for new contributors

---

## Next Steps

1. Review this plan with team
2. Get feedback on structure
3. Choose implementation strategy (B recommended)
4. Create issues for each phase
5. Start with Phase 1 (documentation)

---

**Questions?** Discuss in issue or create a discussion thread.
