# Frequently Asked Questions (FAQ)

Common questions and answers about Places2Go.

---

## General Questions

### What is Places2Go?

Places2Go is an interactive dashboard for comparing travel destinations from UK airports. It helps travelers make informed decisions by comparing flight costs, travel times, weather, and cost of living across multiple destinations.

### Who is Places2Go for?

- **Travelers** looking to compare destination options
- **Travel planners** researching trip possibilities
- **Data enthusiasts** interested in travel analytics
- **Developers** learning Python data visualization

### Is Places2Go free?

Yes! Places2Go is open source under the MIT License. It's completely free to use, modify, and distribute.

### What airports are supported?

Currently: Exeter (EXT) and Bristol (BRS)

Future phases will expand to include more UK airports.

---

## Installation & Setup

### What are the system requirements?

- **Operating System:** Windows, macOS, or Linux
- **Python:** 3.9, 3.10, 3.11, or 3.12
- **Memory:** 512MB RAM minimum
- **Storage:** ~100MB for dependencies

### Do I need to know Python to use Places2Go?

For basic usage: No. Just install and run the dashboard script.

For development: Yes, Python knowledge is required.

### How do I install Places2Go?

See the [Installation Guide](Installation) for detailed steps.

Quick version:
```bash
git clone https://github.com/NCAsterism/places2go.git
cd places2go
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
```

### Why use a virtual environment?

Virtual environments isolate project dependencies, preventing conflicts with other Python projects on your system. It's a Python best practice.

### Can I use conda instead of venv?

Yes! Conda works perfectly:
```bash
conda create -n places2go python=3.11
conda activate places2go
pip install -r requirements.txt
```

---

## Usage Questions

### How do I run the dashboard?

```bash
python scripts/dashboard.py
```

This generates HTML charts in the `output/` directory.

### Where is the data stored?

Currently in `data/dummy_data.csv`.

Future phases will support:
- External APIs (Phase 5)
- Database storage (Phase 6)

### Can I add my own destinations?

Yes! Edit `data/dummy_data.csv`:

```csv
Destination,Origin Airport,Flight Cost (GBP),Flight Time (hours),Temperature (C)
Nice, France,Exeter,170,2.2,26
```

Then run: `python scripts/dashboard.py`

### Why are there only 6 destinations?

Phase 1 is a proof-of-concept with dummy data. Future phases will:
- Phase 5: Integrate real flight APIs
- Phase 6: Support hundreds of destinations

### Can I export the charts?

Yes! The generated HTML files in `output/` can be:
- Opened in any browser
- Shared via email/cloud storage
- Embedded in websites (with proper credits)

### How often is data updated?

**Phase 1 (current):** Manual CSV updates only

**Phase 5 (future):** Automatic API updates with configurable refresh intervals

---

## Development Questions

### How can I contribute?

See our [Contributing Guide](Contributing) for detailed instructions.

Quick steps:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### What's the development roadmap?

See the [Roadmap](Roadmap) for the complete timeline.

**Current Phase:** Phase 2 - Testing & Code Quality (v0.2.0)

### Are there good first issues?

Yes! Look for issues labeled:
- `good first issue`
- `phase-2` (current milestone)
- `testing` (great for beginners)

Browse: https://github.com/NCAsterism/places2go/issues

### How do I run tests?

```bash
pytest                    # Run all tests
pytest --cov              # With coverage
pytest -v                 # Verbose output
pytest tests/test_data.py # Specific file
```

### What's the code style?

- **Formatter:** Black (88 char lines)
- **Linter:** Flake8
- **Type Hints:** Required (Phase 2+)
- **Docstrings:** Google style

Format code:
```bash
black scripts/ tests/
flake8 scripts/ tests/
```

### How do I set up my IDE?

See [Development Guide - IDE Configuration](Development-Guide#ide-configuration) for VS Code settings.

---

## Technical Questions

### What technology stack is used?

**Core:**
- Python 3.9-3.12
- Pandas (data processing)
- Plotly (visualizations)

**Testing:**
- pytest
- pytest-cov

**Code Quality:**
- Black (formatting)
- Flake8 (linting)
- mypy (type checking, Phase 2+)

### Why Python?

Python is ideal for:
- Data analysis (Pandas)
- Visualization (Plotly)
- Rapid development
- Large ecosystem
- Active community

### Why Plotly instead of Matplotlib?

Plotly provides:
- Interactive charts (zoom, hover, pan)
- Professional aesthetics out-of-box
- Web-ready HTML output
- Better user experience

### Will there be a web interface?

Yes! Phase 4 introduces Streamlit for an interactive web dashboard with filters, search, and real-time updates.

### How is data validated?

**Phase 1:** Basic Pandas validation

**Phase 3:** Pydantic models with:
- Type checking
- Range validation
- Custom validators
- Automatic error messages

### What about performance?

**Current:** Sub-second for 6 destinations

**Future optimizations:**
- Redis caching (Phase 6)
- Database indexing (Phase 6)
- Async API calls (Phase 5)

### Is there API documentation?

Coming in Phase 3+. See [API Reference](API-Reference) (future).

---

## Data Questions

### Where does the data come from?

**Phase 1:** Manually curated dummy data

**Phase 5:** Real-time APIs:
- Skyscanner/Kiwi.com (flights)
- OpenWeatherMap (weather)
- Numbeo (cost of living)

### How accurate is the data?

**Phase 1:** Representative dummy data for demonstration

**Phase 5+:** Real-time API data updated regularly

### Can I use my own data sources?

Yes! Places2Go is designed to be extensible. You can:
- Replace CSV with your own data
- Add custom data loaders
- Integrate different APIs

### What data fields are available?

**Current:**
- Destination (city, country)
- Origin Airport
- Flight Cost (GBP)
- Flight Time (hours)
- Temperature (°C)

**Future (Phase 5):**
- UV index
- Humidity
- Cost of living breakdown
- Flight dates/times
- Multiple airlines

---

## Troubleshooting

### Installation fails with dependency errors

```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Tests fail after installation

Ensure virtual environment is activated:
```bash
# Check Python version
python --version

# Verify packages
pip list | grep -E "pandas|plotly|pytest"
```

### ModuleNotFoundError when running scripts

Activate virtual environment:
```bash
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\Activate.ps1  # Windows
```

### Charts not displaying correctly

- Open HTML files in modern browser (Chrome, Firefox, Edge)
- Ensure JavaScript is enabled
- Try different browser if issues persist

### Permission errors on Windows

Run PowerShell as Administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Git push rejected

```bash
git pull origin develop --rebase
git push origin feature-branch
```

For more troubleshooting, see [Troubleshooting](Troubleshooting).

---

## Project Questions

### Who maintains Places2Go?

Currently maintained by [@NCAsterism](https://github.com/NCAsterism) with community contributions.

### What's the release schedule?

See [Roadmap](Roadmap) for the timeline:
- v0.2.0 - October 18, 2025
- v0.3.0 - November 8, 2025
- v0.4.0 - December 6, 2025
- v0.5.0 - January 10, 2026
- v1.0.0 - February 14, 2026

### How do I report security issues?

Email security concerns to: [project maintainer]

Do not create public issues for security vulnerabilities.

### Can I use Places2Go commercially?

Yes! The MIT License allows commercial use with attribution.

### How do I cite Places2Go?

```
Places2Go - Travel Destination Dashboard
GitHub: https://github.com/NCAsterism/places2go
License: MIT
```

---

## Community Questions

### Where can I get help?

- 📖 **Wiki:** Browse documentation
- 💬 **Discussions:** [GitHub Discussions](https://github.com/NCAsterism/places2go/discussions)
- 🐛 **Issues:** [Bug reports](https://github.com/NCAsterism/places2go/issues)
- 📧 **Email:** [Contact maintainer]

### How do I stay updated?

- ⭐ Star the repository on GitHub
- 👁️ Watch the repository for notifications
- 📰 Check [Release Notes](Release-Notes)

### Can I suggest features?

Absolutely! Use the [feature request template](https://github.com/NCAsterism/places2go/issues/new?template=feature_request.md).

### Is there a code of conduct?

Yes, see [Contributing - Code of Conduct](Contributing#code-of-conduct).

---

## Still Have Questions?

- 📖 Check the [Wiki Home](Home)
- 💬 Ask in [Discussions](https://github.com/NCAsterism/places2go/discussions)
- 🐛 Open an [Issue](https://github.com/NCAsterism/places2go/issues)

---

**Last Updated:** October 4, 2025
