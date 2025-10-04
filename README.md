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

## 📁 Project Structure

```
places2go/
├── .github/
│   ├── workflows/        # CI/CD pipelines
│   └── ISSUE_TEMPLATE/   # Issue templates
├── data/
│   └── dummy_data.csv    # Sample destination data
├── docs/                 # Additional documentation
├── scripts/
│   ├── dashboard.py      # Main dashboard script
│   ├── create_issues.py  # GitHub automation
│   └── push_to_github.ps1
├── tests/
│   └── test_data.py      # Test suite
├── wiki/                 # Wiki content (local)
├── output/               # Generated visualizations
├── pyproject.toml        # Project configuration
├── requirements.txt      # Python dependencies
├── ROADMAP.md           # Development roadmap
├── CONTRIBUTING.md      # Contribution guidelines
└── README.md            # This file
```

---

## 🛠️ Technology Stack

- **Language:** Python 3.9-3.12
- **Data Processing:** Pandas
- **Visualization:** Plotly
- **Testing:** pytest, pytest-cov
- **Code Quality:** Black, Flake8
- **Type Checking:** mypy (Phase 2+)
- **CI/CD:** GitHub Actions

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=scripts --cov=tests --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

**Current Coverage:** 44% (Phase 1 baseline)  
**Target:** 90%+ (Phase 2)

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Find an Issue** - Browse [open issues](https://github.com/NCAsterism/places2go/issues)
2. **Fork & Clone** - Fork the repo and clone your fork
3. **Create Branch** - `git checkout -b feature/your-feature`
4. **Make Changes** - Follow our code style guide
5. **Test** - Run tests and ensure they pass
6. **Submit PR** - Target the `develop` branch

📖 **Full details:** [Contributing Guide](https://github.com/NCAsterism/places2go/wiki/Contributing)

### Current Priorities (Phase 2)

We're actively working on these issues:
- [#1 Comprehensive Test Suite](https://github.com/NCAsterism/places2go/issues/1)
- [#2 Add Type Hints](https://github.com/NCAsterism/places2go/issues/2)
- [#3 Mypy Integration](https://github.com/NCAsterism/places2go/issues/3)
- [#4 Logging Framework](https://github.com/NCAsterism/places2go/issues/4)
- [#5 Custom Exceptions](https://github.com/NCAsterism/places2go/issues/5)
- [#6 Pydantic Models](https://github.com/NCAsterism/places2go/issues/6)
- [#7 Pre-commit Hooks](https://github.com/NCAsterism/places2go/issues/7)
- [#8 Error Handling](https://github.com/NCAsterism/places2go/issues/8)

---

## 📊 Development Roadmap

| Phase | Version | Focus | Target | Status |
|-------|---------|-------|--------|--------|
| **1** | v0.1.0 | Basic Dashboard | Oct 4 | ✅ Complete |
| **2** | v0.2.0 | Testing & Quality | Oct 18 | 🚧 In Progress |
| **3** | v0.3.0 | Data Models | Nov 8 | 📋 Planned |
| **4** | v0.4.0 | Interactive UI | Dec 6 | 📋 Planned |
| **5** | v0.5.0 | API Integration | Jan 10 | 📋 Planned |
| **6** | v1.0.0 | Production Ready | Feb 14 | 📋 Planned |

📖 **Full roadmap:** [Roadmap](https://github.com/NCAsterism/places2go/wiki/Roadmap)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [Plotly](https://plotly.com/)
- Data processing with [Pandas](https://pandas.pydata.org/)
- Testing with [pytest](https://pytest.org/)

---

## 📞 Support

- 📖 [**Documentation**](https://github.com/NCAsterism/places2go/wiki)
- 🐛 [**Report a Bug**](https://github.com/NCAsterism/places2go/issues/new?template=bug_report.md)
- 💡 [**Request a Feature**](https://github.com/NCAsterism/places2go/issues/new?template=feature_request.md)
- 💬 [**Discussions**](https://github.com/NCAsterism/places2go/discussions)
- ❓ [**FAQ**](https://github.com/NCAsterism/places2go/wiki/FAQ)

---

**Made with ❤️ for travelers and developers**
