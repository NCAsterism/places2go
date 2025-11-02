# Destination Dashboard PoC

This repository contains a proof‑of‑concept (PoC) for an interactive dashboard that helps compare and evaluate travel destinations reachable from the UK airports in Exeter and Bristol. The goal is to display a range of metrics—such as weather conditions, flight costs and times, UV index, living expenses, and typical costs for food, drinks and recreational cannabis—in a single, easy‑to‑navigate interface.

While the PoC uses dummy data for demonstration purposes, the project is structured to make it easy to replace the static data with live data sources (APIs) later.  We also outline a suggested branching strategy and testing process for scaling this into a robust, open‑source project.

## Quick start

1. **Install dependencies.**  Navigate to the project root and install the minimal packages required for the PoC:

   ```bash
   pip install pandas plotly
   ```

2. **Run the dashboard script.**  The script loads the dummy dataset from `data/dummy_data.csv` and produces interactive HTML charts in the `output/` directory.  Execute it with:

   ```bash
   python scripts/dashboard.py
   ```

3. **Open the results.**  After running the script, open the files in `output/` in a web browser to explore the bar and scatter plots.

## Interactive Visualizations

The project includes comprehensive interactive HTML visualization pages for exploring destination data:

- **Weather Forecast Dashboard** - 7-day forecasts with temperature trends, rainfall, UV index, and comfort metrics
- **Destinations Map** (planned) - Interactive world map with destination markers and details
- **Cost Comparison** (planned) - Living costs comparison with category breakdowns
- **Flight Prices** (planned) - Time-series analysis of flight pricing trends

### Generate Visualizations

```bash
# Generate weather forecast dashboard
python scripts/visualizations/weather_forecast.py

# Generate enhanced version with user preferences (Phase 4C)
python scripts/visualizations/weather_forecast_enhanced.py

# Output: .build/visualizations/weather_forecast.html
```

### View Visualizations

Simply open the generated HTML files in any web browser. No server required!

**📚 Full Documentation:** [.build/visualizations/README.md](.build/visualizations/README.md)

For detailed usage, customization guides, and technical details, see the comprehensive visualization documentation.

## 🎨 Phase 4C: User Preferences & Personalization (NEW!)

The enhanced visualizations now include user customization features:

- **⚙️ Preferences Panel**: Currency (GBP/USD/EUR), Temperature (°C/°F), Theme (Light/Dark), Date Format
- **⭐ Favorites**: Save and manage favorite destinations with one-click access
- **📤 URL Sharing**: Share your exact view including preferences and filters
- **💾 localStorage**: All preferences persist across browser sessions
- **🎯 Performance**: Loads instantly (< 10ms), no database required

**Try it:** Open `.build/visualizations/weather_forecast_enhanced.html` and click the floating buttons (bottom-right)!

**📖 Documentation:** See [docs/project/PHASE4C_README.md](docs/project/PHASE4C_README.md) for implementation guide.

## Repository structure

```
places2go/
├── .build/              # Build artifacts (gitignored)
│   ├── output/          # Generated HTML charts
│   ├── logs/            # Application logs
│   ├── coverage/        # Test coverage reports
│   └── visualizations/  # Interactive visualization pages
│       ├── README.md    # Visualization documentation
│       └── *.html       # Generated visualization dashboards
├── data/                # Data files
│   └── dummy_data.csv   # Sample dataset (to be split into multiple CSVs)
├── docs/                # Documentation (organized by category)
│   ├── architecture/    # System design and data models
│   ├── development/     # Development guides
│   ├── processes/       # Workflows and best practices
│   └── project/         # Project planning and roadmaps
├── scripts/             # Python application code
│   ├── core/            # Core modules (planned)
│   ├── visualizations/  # Interactive visualization generators
│   ├── dashboard.py     # Main dashboard script
│   └── exceptions.py    # Custom exception classes
├── tests/               # Test suite
│   ├── test_charts.py   # Chart generation tests
│   ├── test_data.py     # Data loading tests
│   └── test_integration.py  # Integration tests
├── wiki/                # GitHub Wiki content
├── .github/             # GitHub configuration (workflows, issue templates)
├── .pre-commit-config.yaml  # Pre-commit hooks configuration
├── pyproject.toml       # Project configuration
├── requirements.txt     # Python dependencies
├── CONTRIBUTING.md      # Contribution guidelines
└── README.md            # This file
```

For detailed documentation, see [docs/README.md](docs/README.md).

## Design goals

* **Interactive dashboard.**  The PoC demonstrates how to visualize multiple metrics with interactive Plotly charts.  The final version might be built with frameworks such as Dash or Streamlit to allow users to filter by date, airport, or destination and to refresh data on demand.
* **Modular data streams.**  Each metric (flight cost/time, weather, UV, living cost, food, drinks, weed) will have its own data‑retrieval module.  These modules will expose functions that return tidy dataframes, making it straightforward to swap in real data sources later.
* **Testability.**  The project is configured to use `pytest` for unit tests.  Dummy data and mocks will be used to test the behavior of the data‑retrieval modules without making external API calls.
* **Extensible architecture.**  The repository is structured so that adding new data sources or visualizations only requires adding new modules and corresponding tests.

## Logging

The dashboard uses Python's built-in `logging` module to provide better debugging and monitoring capabilities. Logs are written to both the console and a log file.

### Log Configuration

Logs are automatically configured when running the dashboard script:
- **Log Level:** INFO (change to DEBUG for more detailed output)
- **Log Format:** `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- **Log File:** `.build/logs/dashboard.log` (created automatically)
- **Console Output:** All log messages are also printed to the console

### Log Levels

- **INFO:** Normal operation messages (e.g., "Loading data", "Creating chart")
- **DEBUG:** Detailed diagnostic information (e.g., DataFrame shapes, column details)
- **WARNING:** Unexpected situations that don't prevent execution
- **ERROR:** Error conditions that need attention

### Example Usage

```python
import logging
from pathlib import Path

# Configure logging
log_dir = Path(__file__).resolve().parents[1] / 'logs'
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / 'dashboard.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Use logging instead of print
logger.info("Loading data from CSV")
logger.debug(f"DataFrame shape: {df.shape}")
logger.error(f"Failed to create chart: {error}")
```

### Viewing Logs

- **Console:** Logs appear in the terminal when running the script
- **File:** Check `logs/dashboard.log` for persistent log history
- **Note:** Log files are excluded from git via `.gitignore`

## Branching strategy

We recommend a simplified version of GitFlow to organize collaborative work.  This structure aligns with the workflows used in many of your existing projects and makes it easy to manage concurrent feature development.

- **`main`** — Always contains production‑ready code.  Releases are tagged on this branch.
- **`develop`** — Integration branch where features are merged before being released.  CI tests run on this branch to ensure stability before releases.
- **`feature/<name>`** — Each new feature (e.g. “flight‑data”, “weather‑data”, “dashboard‑layout”) gets its own branch off of `develop`.  After completion and review, the branch is merged back into `develop` via a pull request.
- **`release/<version>`** — When the `develop` branch is stable and ready for a release, a release branch is created to prepare versioning, documentation and final testing.  Once approved, it is merged into `main` and tagged.
- **`hotfix/<issue>`** — Used for critical fixes in production.  These are branched off of `main` and merged back into both `main` and `develop`.

## Testing process

1. **Unit tests** — Each data‑retrieval module should have corresponding unit tests in the `tests/` directory.  Use fixtures or mocking libraries to simulate API responses.  Tests should cover edge cases such as missing data or network errors.
2. **Integration tests** — When multiple modules are combined (e.g. merging flight and weather dataframes), integration tests should verify that the combined dataset has the expected columns and types.
3. **Continuous Integration** — Configure GitHub Actions to run `pytest` and linting (e.g. with `flake8` or `black`) on each pull request.  This ensures that new code is tested automatically and follows style guidelines.
4. **Documentation tests** — Use tools like `pytest‑doctest` or `mkdocs` to ensure that examples in your documentation remain valid as the code evolves.

## Next steps

The following tasks can be created as issues and assigned to GitHub agents or contributors:

| Workstream | Task | Description |
|-----------|------|-------------|
| **Layout & UI** | `feature/dashboard-ui` | Design and implement the dashboard layout using a framework such as Dash or Streamlit.  This includes navigation, filtering widgets, and responsive design. |
| **Flight data** | `feature/flight-data` | Implement data retrieval for flight prices and times from Exeter and Bristol to various destinations.  Initially mock this data; later integrate with real APIs. |
| **Weather & UV** | `feature/weather-data` | Retrieve current and forecast weather and UV index for each destination.  Use a weather API and handle API keys securely. |
| **Living costs** | `feature/cost-of-living` | Gather data on housing, food, transport and recreational expenses (including weed) for each destination.  Consider using open datasets or scraping sources with permission. |
| **Testing & CI** | `feature/test-infra` | Set up unit and integration tests with `pytest` and configure GitHub Actions for continuous integration. |
| **Docs** | `feature/documentation` | Build out the `docs/` folder with setup instructions, contribution guidelines and API usage documentation. |

Feel free to adapt these tasks to suit your team's workflow and experience.  Once the PoC is validated, you can convert this repository into a public GitHub repo under your `ncasterism` account and start opening issues and pull requests to track progress.
