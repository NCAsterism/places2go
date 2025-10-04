# Quick Start Guide

Get up and running with Places2Go in minutes!

---

## 5-Minute Quickstart

### 1. Install Places2Go

```bash
# Clone and navigate to the repository
git clone https://github.com/NCAsterism/places2go.git
cd places2go

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Dashboard

```bash
python scripts/dashboard.py
```

### 3. View the Results

Open the generated HTML files in your browser:
- `output/flight_costs.html` - Flight cost comparison
- `output/flight_time_vs_cost.html` - Time vs. cost analysis

That's it! 🎉

---

## Understanding the Data

### Current Dataset

The dashboard currently uses dummy data for 6 destinations:

| Destination | Airport | Flight Cost | Flight Time | Temperature |
|-------------|---------|-------------|-------------|-------------|
| Alicante, Spain | Exeter | £120 | 2h 30m | 28°C |
| Malaga, Spain | Exeter | £150 | 2h 45m | 30°C |
| Majorca, Spain | Bristol | £180 | 2h 50m | 29°C |
| Faro, Portugal | Bristol | £130 | 2h 40m | 27°C |
| Corfu, Greece | Exeter | £200 | 3h 30m | 32°C |
| Rhodes, Greece | Bristol | £220 | 4h 0m | 31°C |

### Data Fields

Each destination includes:
- **Destination** - City and country
- **Origin Airport** - UK departure airport
- **Flight Cost** - Round-trip price in GBP
- **Flight Time** - Duration (one-way)
- **Temperature** - Average temperature in °C

---

## Using the Dashboard

### Flight Cost Comparison Chart

The first chart shows a bar graph comparing flight costs across all destinations.

**Insights you can see:**
- Which destinations are most affordable
- Price differences between destinations
- Origin airport variations

**Example output:**
```
Rhodes (Bristol): £220
Corfu (Exeter): £200
Majorca (Bristol): £180
Malaga (Exeter): £150
Faro (Bristol): £130
Alicante (Exeter): £120
```

### Flight Time vs. Cost Chart

The second chart is a scatter plot showing the relationship between flight duration and cost.

**Insights you can see:**
- Value for money destinations (low time, low cost)
- Premium destinations (high time, high cost)
- Optimal trade-offs

**Interpretation:**
- **Bottom-left quadrant:** Best value (quick & cheap)
- **Top-right quadrant:** Premium options (long & expensive)
- **Size of markers:** Varies by temperature (warmer = bigger)

---

## Common Tasks

### Adding New Data

To add destinations, edit `data/dummy_data.csv`:

```csv
Destination,Origin Airport,Flight Cost (GBP),Flight Time (hours),Temperature (C)
Nice, France,Exeter,170,2.2,26
```

Then run:
```bash
python scripts/dashboard.py
```

### Running Tests

Verify your changes work correctly:

```bash
pytest
```

### Formatting Code

If you modify any Python files:

```bash
black scripts/ tests/
```

### Checking Code Quality

```bash
flake8 scripts/ tests/
```

---

## What's Next?

### Explore Features (Coming Soon)

**Phase 2 (v0.2.0)** - Enhanced testing and code quality
- Type hints throughout codebase
- Comprehensive test coverage (90%+)
- Error handling and validation
- Pre-commit hooks

**Phase 3 (v0.3.0)** - Structured data models
- Pydantic models for data validation
- Custom exception handling
- Logging framework

**Phase 4 (v0.4.0)** - Interactive dashboard
- Streamlit web interface
- Filters and search
- Real-time updates

**Phase 5 (v0.5.0)** - External API integration
- Live flight price data
- Weather forecasts
- Cost of living data

**Phase 6 (v1.0.0)** - Production-ready
- Database integration
- Caching and optimization
- Comprehensive documentation

See the [Roadmap](Roadmap) for detailed timeline.

---

## Learning Resources

### Documentation
- [Dashboard Features](Dashboard-Features) - Deep dive into visualizations
- [Data Sources](Data-Sources) - Understanding the data
- [Architecture](Architecture) - How it works

### Development
- [Development Guide](Development-Guide) - Contributing to the project
- [Testing Guide](Testing) - Writing and running tests
- [Code Style](Code-Style) - Formatting standards

### Getting Help
- [FAQ](FAQ) - Common questions
- [Troubleshooting](Troubleshooting) - Solving common issues
- [GitHub Issues](https://github.com/NCAsterism/places2go/issues) - Report bugs or request features

---

## Next Steps

✅ **You've completed the Quick Start!**

**Choose your path:**

🎓 **Learn More:** Explore [Dashboard Features](Dashboard-Features)  
🛠️ **Start Developing:** Read the [Development Guide](Development-Guide)  
🚀 **Deploy:** Check out [Deployment](Local-Deployment)  
💡 **Contribute:** See [Contributing Guidelines](Contributing)

---

**Happy exploring! 🌍✈️**
