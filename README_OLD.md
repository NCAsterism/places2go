# Places2Go - Travel Destination Dashboard 🌍✈️

An interactive Python dashboard for comparing and evaluating travel destinations reachable from UK airports (Exeter and Bristol). Compare flight costs, travel times, weather conditions, and more—all in one easy-to-navigate interface.

**Current Version:** v0.1.0 (Phase 1 Complete ✅)  
**Next Milestone:** v0.2.0 - Enhanced Testing & Code Quality  
**Repository:** https://github.com/NCAsterism/places2go  
**Wiki:** https://github.com/NCAsterism/places2go/wiki

---

## 📚 Documentation

**Complete documentation is available in our [GitHub Wiki](https://github.com/NCAsterism/places2go/wiki):**

- 📖 [**Wiki Home**](https://github.com/NCAsterism/places2go/wiki) - Start here!
- 🚀 [**Quick Start**](https://github.com/NCAsterism/places2go/wiki/Quick-Start) - Get running in 5 minutes
- 💾 [**Installation Guide**](https://github.com/NCAsterism/places2go/wiki/Installation) - Detailed setup instructions
- 🛠️ [**Development Guide**](https://github.com/NCAsterism/places2go/wiki/Development-Guide) - For contributors
- 🤝 [**Contributing**](https://github.com/NCAsterism/places2go/wiki/Contributing) - How to contribute
- 🏗️ [**Architecture**](https://github.com/NCAsterism/places2go/wiki/Architecture) - Technical design
- 📊 [**Roadmap**](https://github.com/NCAsterism/places2go/wiki/Roadmap) - Development timeline
- ❓ [**FAQ**](https://github.com/NCAsterism/places2go/wiki/FAQ) - Common questions

---

## 🚀 Features

- ✈️ **Flight Cost Comparison** - Compare prices across destinations
- ⏱️ **Flight Time Analysis** - Time vs. cost scatter plots
- 🌡️ **Weather Data** - Temperature and climate information
- 📊 **Interactive Charts** - Plotly visualizations
- 🔄 **Easy Data Updates** - CSV-based data management

### Coming Soon
- 🧪 Enhanced testing & code quality (Phase 2)
- 🔍 Data validation with Pydantic (Phase 3)
- 🖥️ Interactive Streamlit UI (Phase 4)
- 🌐 Real-time API integration (Phase 5)
- 🗄️ Database & production deployment (Phase 6)

---

## ⚡ Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/NCAsterism/places2go.git
cd places2go

# Create and activate virtual environment
python -m venv venv

# Windows PowerShell
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Dashboard

```bash
python scripts/dashboard.py
```

This generates interactive HTML charts in `output/`:
- `flight_costs.html` - Flight cost comparison
- `flight_time_vs_cost.html` - Time vs. cost analysis

Open these files in your browser to explore the visualizations!

📖 **For detailed instructions, see the [Quick Start Guide](https://github.com/NCAsterism/places2go/wiki/Quick-Start)**

---

## Repository structure

```
destination_dashboard/
├── data/                # Static or cached data.  Contains the dummy dataset for the PoC.
├── docs/                # Documentation and design notes (branching strategy, task breakdown, etc.).
├── scripts/             # Python scripts used for data processing and visualization.
├── output/              # Generated outputs (HTML charts for the PoC).
├── tests/               # Unit tests and integration tests.
└── README.md            # Project overview and setup instructions.
```

## Design goals

* **Interactive dashboard.**  The PoC demonstrates how to visualize multiple metrics with interactive Plotly charts.  The final version might be built with frameworks such as Dash or Streamlit to allow users to filter by date, airport, or destination and to refresh data on demand.
* **Modular data streams.**  Each metric (flight cost/time, weather, UV, living cost, food, drinks, weed) will have its own data‑retrieval module.  These modules will expose functions that return tidy dataframes, making it straightforward to swap in real data sources later.
* **Testability.**  The project is configured to use `pytest` for unit tests.  Dummy data and mocks will be used to test the behavior of the data‑retrieval modules without making external API calls.
* **Extensible architecture.**  The repository is structured so that adding new data sources or visualizations only requires adding new modules and corresponding tests.

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