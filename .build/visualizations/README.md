# Places2Go - Interactive Visualization Pages

Welcome to the Places2Go visualization documentation! This guide covers the interactive HTML visualization pages that help explore and analyze destination data for travel planning.

## Table of Contents

- [Overview](#overview)
- [Visualization Pages](#visualization-pages)
  - [Destinations Map](#destinations-map)
  - [Cost of Living Comparison](#cost-of-living-comparison)
  - [Flight Prices Time-Series](#flight-prices-time-series)
  - [Weather Forecast Dashboard](#weather-forecast-dashboard)
  - [Multi-Dataset Overlay](#multi-dataset-overlay-future)
- [Getting Started](#getting-started)
- [Customization Guide](#customization-guide)
- [Technical Details](#technical-details)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)

## Overview

### Purpose

The visualization pages provide interactive, standalone HTML dashboards for exploring destination data. Each page focuses on a specific dataset (destinations, costs, flights, weather) with rich visualizations that help identify patterns, compare options, and make informed travel decisions.

### How They Complement the Dashboard

While the main dashboard (`scripts/dashboard.py`) provides a quick overview, these visualization pages offer:

- **Deep data exploration** - Interactive charts with hover details, zooming, and filtering
- **Standalone files** - No server required, just open in a browser
- **Comprehensive views** - Multiple chart types for different perspectives
- **Data quality insights** - Identify outliers, gaps, and patterns
- **Export-ready** - Share visualizations easily via HTML files

### Data Sources and DataLoader Usage

All visualizations use the `DataLoader` class from `scripts/core/data_loader.py` to load data from CSV files:

```python
from scripts.core.data_loader import DataLoader

loader = DataLoader()

# Individual datasets
destinations = loader.load_destinations()
costs = loader.load_costs(data_source='demo1')
flights = loader.load_flights(data_source='demo1')
weather = loader.load_weather(data_source='demo1', forecast_only=True)

# Merged view (all datasets combined)
all_data = loader.load_all(data_source='demo1')

# Aggregated statistics
stats = loader.get_aggregates(data_source='demo1')
```

**Data Sources:**
- `demo1` - Primary demo dataset with 6 destinations, 7-day forecasts
- `demo2` - Alternative demo dataset (if available)
- `live` - Live data from APIs (future feature)

## Visualization Pages

### Destinations Map

**Status:** Planned (Issue #17)
**File:** `.build/visualizations/destinations_map.html`
**Purpose:** Interactive map showing all travel destinations with geographic context

#### Features
- Interactive world map with destination markers
- Hover to see destination details (name, country, coordinates, airport codes)
- Color-coded by region or country
- Click markers for detailed information panel
- Filter by country or region
- Summary statistics (total destinations, regions covered)

#### How to Generate

```bash
cd /home/runner/work/places2go/places2go
python scripts/visualizations/destinations_map.py
```

#### Interactive Features
- **Pan and Zoom:** Navigate the map freely
- **Hover Details:** See destination information without clicking
- **Click for More:** Detailed panel with all destination data
- **Filters:** Show/hide destinations by country or region
- **Legend:** Color key for region/country groupings

#### Use Cases
- Get geographic overview of available destinations
- Understand regional distribution
- Plan multi-destination trips by proximity
- Identify destinations in preferred regions

---

### Cost of Living Comparison

**Status:** Planned (Issue #18)
**File:** `.build/visualizations/cost_comparison.html`
**Purpose:** Compare living costs across destinations with detailed breakdowns

#### Features
- Bar chart comparing total monthly costs
- Stacked bar chart showing cost category breakdown
- Box plot for cost distribution analysis
- Grouped bar chart for category-by-category comparison
- Sort by total cost, specific category, or alphabetically
- Filter destinations to compare subset
- Export data table

#### How to Generate

```bash
cd /home/runner/work/places2go/places2go
python scripts/visualizations/cost_comparison.py
```

#### Interactive Features
- **Sorting Controls:** Reorder by total cost or any category
- **Hover Details:** See exact cost values and percentages
- **Toggle Categories:** Show/hide specific cost categories
- **Zoom:** Focus on specific cost ranges
- **Legend Interaction:** Click to show/hide categories

#### Cost Categories
- Accommodation (monthly rent)
- Food (groceries and restaurants)
- Transportation (public transit and taxis)
- Utilities (electricity, water, internet)
- Entertainment (activities and leisure)
- Other expenses

#### Use Cases
- Find the most affordable destinations
- Understand cost structure (accommodation vs. food vs. transport)
- Budget planning for extended stays
- Compare destinations with similar cost profiles

---

### Flight Prices Time-Series

**Status:** Planned (Issue #19)
**File:** `.build/visualizations/flight_prices.html`
**Purpose:** Analyze flight pricing trends over the 7-day forecast period

#### Features
- Multi-line time-series chart showing price trends
- Box plot for price distribution by destination
- Scatter plot: flight duration vs. cost
- Airline comparison bar chart
- Calendar heatmap showing best days to fly
- Price statistics (min, max, average, median)

#### How to Generate

```bash
cd /home/runner/work/places2go/places2go
python scripts/visualizations/flight_prices.py
```

#### Interactive Features
- **Time Navigation:** Select date ranges
- **Destination Filtering:** Show/hide specific destinations
- **Airline Filtering:** Compare specific airlines
- **Hover Details:** See exact prices, airlines, flight times
- **Cross-Chart Selection:** Select on one chart to highlight in others

#### Flight Details Shown
- Price (GBP)
- Departure airport (EXT/BRS)
- Destination airport
- Airline
- Flight duration (hours)
- Date and time
- Data source flag

#### Use Cases
- Find cheapest days to fly
- Compare prices across dates
- Identify price patterns (weekday vs. weekend)
- Analyze duration vs. cost trade-offs
- Compare airlines for specific routes

---

### Weather Forecast Dashboard

**Status:** ✅ Complete (Issue #20)
**File:** `.build/visualizations/weather_forecast.html`
**Purpose:** Display 7-day weather forecasts for all destinations with comparisons

#### Features
- Temperature trends (high/low/average) multi-line chart
- Daily weather cards with icons and key metrics
- Rainfall bar chart by destination
- UV index calendar heatmap
- Weather conditions distribution pie chart
- Comfort index (temperature + humidity + wind)

#### How to Generate

```bash
cd /home/runner/work/places2go/places2go
python scripts/visualizations/weather_forecast.py
```

The dashboard will be generated at `.build/visualizations/weather_forecast.html`.

#### Interactive Features
- **Date Navigation:** Focus on specific days
- **Destination Filtering:** Compare selected destinations
- **Hover Details:** See all weather metrics (temp, humidity, wind, UV, rainfall, conditions)
- **Color Coding:** Consistent colors per destination across all charts
- **Legend Toggle:** Click legend items to show/hide destinations

#### Weather Metrics Displayed
- Temperature (°C): high, low, average
- Conditions: sunny, partly cloudy, cloudy, rainy
- Rainfall (mm): daily precipitation
- Wind speed (km/h): average wind conditions
- Humidity (%): relative humidity
- UV index: sun exposure intensity (0-11+ scale)
- Comfort index: combined metric (0-100)

#### Use Cases
- Compare weather across destinations for a specific date
- Find destinations with best weather conditions
- Avoid high UV or rainfall days
- Plan activities based on weather patterns
- Identify comfortable travel periods

#### Weather Card Details

Each daily forecast card shows:
- Date
- Destination name
- Weather icon (☀️ sunny, ⛅ partly cloudy, ☁️ cloudy, 🌧️ rainy)
- High/Low temperatures
- Conditions description
- Key metrics (rainfall, wind, humidity, UV)

---

### Multi-Dataset Overlay (Future)

**Status:** Planned (Issue #21) - Phase 3C
**File:** `.build/visualizations/dashboard_overlay.html`
**Purpose:** Comprehensive dashboard overlaying all datasets for insights

#### Planned Features
- **Master Map:** Destinations with flight routes and weather overlays
- **Timeline View:** Aligned flight prices and weather by date
- **Value Finder:** Scatter plot identifying best value destinations
- **Destination Comparison:** Radar charts comparing multiple metrics
- **Insights Panel:** AI-generated recommendations
- **Cross-Filtering:** Selections on one chart filter all others

#### Dependencies
Requires completion of individual visualization pages (#17-20)

#### Future Capabilities
- Find "sweet spot" destinations (low cost + good weather + cheap flights)
- Correlate weather with flight pricing patterns
- Multi-criteria destination ranking
- Export insights as PDF report
- Save custom views and comparisons

## Getting Started

### Prerequisites

**Required Software:**
- Python 3.9 or higher
- pip (Python package manager)

**Required Python Packages:**
```bash
pip install pandas plotly
```

**Data Requirements:**
- CSV files in `data/` directory (included in repository)
- DataLoader class (`scripts/core/data_loader.py`)

### How to Generate All Visualizations

Generate all available visualizations at once:

```bash
cd /home/runner/work/places2go/places2go

# Generate weather forecast (currently available)
python scripts/visualizations/weather_forecast.py

# Future: Generate destinations map (when implemented)
# python scripts/visualizations/destinations_map.py

# Future: Generate cost comparison (when implemented)
# python scripts/visualizations/cost_comparison.py

# Future: Generate flight prices (when implemented)
# python scripts/visualizations/flight_prices.py
```

### Where Files Are Saved

All visualization HTML files are saved to:
```
.build/visualizations/
├── README.md                  # This file
├── weather_forecast.html      # Weather dashboard (available)
├── destinations_map.html      # Destinations map (planned)
├── cost_comparison.html       # Cost comparison (planned)
├── flight_prices.html         # Flight prices (planned)
├── dashboard_overlay.html     # Multi-dataset overlay (future)
└── examples/
    └── *.png                  # Screenshots (for documentation)
```

**Note:** The `.build/` directory is excluded from git via `.gitignore`.

### How to View

Simply open any HTML file in your web browser:

**Option 1: File Explorer**
1. Navigate to `.build/visualizations/` in your file explorer
2. Double-click any `.html` file
3. It will open in your default browser

**Option 2: Command Line**

**macOS:**
```bash
open .build/visualizations/weather_forecast.html
```

**Linux:**
```bash
xdg-open .build/visualizations/weather_forecast.html
```

**Windows:**
```bash
start .build/visualizations/weather_forecast.html
```

**Option 3: Drag and Drop**
- Drag the HTML file onto a browser window

**No Server Required:** These are standalone HTML files with embedded JavaScript. No web server or internet connection needed after generation!

## Customization Guide

### Modifying Colors and Themes

All visualizations use Plotly, which provides flexible theming. To customize colors:

#### 1. Edit Individual Visualization Script

Open the visualization Python script (e.g., `scripts/visualizations/weather_forecast.py`) and modify color settings:

```python
# Find the color definitions (usually at top or in chart creation)
COLORS = {
    'Bangkok': '#FF6B6B',
    'Tokyo': '#4ECDC4',
    'Barcelona': '#45B7D1',
    'Prague': '#FFA07A',
    'Lisbon': '#98D8C8',
    'Marrakech': '#F7DC6F'
}

# Or modify Plotly template
fig.update_layout(
    template='plotly_white',  # Options: plotly, plotly_white, plotly_dark, ggplot2, seaborn, simple_white
    colorway=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']
)
```

#### 2. Available Plotly Templates
- `plotly` - Default Plotly theme
- `plotly_white` - Clean white background
- `plotly_dark` - Dark mode theme
- `ggplot2` - R's ggplot2 style
- `seaborn` - Seaborn statistical graphics style
- `simple_white` - Minimal white theme
- `presentation` - Large fonts for presentations

#### 3. Regenerate Visualization

After editing, regenerate the HTML:
```bash
python scripts/visualizations/weather_forecast.py
```

### Adding New Charts

To add a new chart to an existing visualization:

#### 1. Create Chart Function

Add a new function to the visualization script:

```python
def create_new_chart(df: pd.DataFrame, destinations_df: pd.DataFrame) -> go.Figure:
    """
    Create a new custom chart.

    Args:
        df: Main data DataFrame
        destinations_df: Destinations reference data

    Returns:
        Plotly figure object
    """
    fig = go.Figure()

    # Add your chart logic here
    fig.add_trace(go.Bar(
        x=df['date'],
        y=df['some_metric'],
        name='Your Chart'
    ))

    fig.update_layout(
        title='Your New Chart Title',
        xaxis_title='Date',
        yaxis_title='Metric',
        template='plotly_white'
    )

    return fig
```

#### 2. Add to Dashboard

In the main dashboard creation function:

```python
def create_weather_dashboard(output_path: Path, df: pd.DataFrame, destinations_df: pd.DataFrame) -> None:
    # ... existing charts ...

    # Add your new chart
    new_chart = create_new_chart(df, destinations_df)
    new_chart_html = new_chart.to_html(include_plotlyjs=False, div_id="new_chart")

    # Add to HTML template
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <body>
        <!-- ... existing content ... -->

        <div class="chart-full">
            {new_chart_html}
        </div>

    </body>
    </html>
    """
```

### Filtering Data

To modify which data is displayed:

#### Filter by Date Range

```python
# In the visualization script
import pandas as pd

# Filter to specific date range
start_date = pd.Timestamp('2025-10-05')
end_date = pd.Timestamp('2025-10-10')
df_filtered = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
```

#### Filter by Destination

```python
# Show only specific destinations
selected_destinations = ['Bangkok', 'Tokyo', 'Barcelona']
df_filtered = df[df['destination_name'].isin(selected_destinations)]
```

#### Filter by Conditions

```python
# Show only sunny days
df_sunny = df[df['conditions'].str.contains('sunny', case=False)]

# Show days with low rainfall
df_dry = df[df['rainfall_mm'] < 5.0]

# Show comfortable temperatures
df_comfortable = df[(df['avg_temp_c'] >= 18) & (df['avg_temp_c'] <= 25)]
```

### Changing Date Ranges

To modify the forecast period shown:

```python
# Load weather data with custom date range
weather_df = loader.load_weather(data_source='demo1', forecast_only=True)

# Filter to your desired range
weather_df = weather_df[
    (weather_df['date'] >= '2025-10-05') &
    (weather_df['date'] <= '2025-10-11')
]
```

### Styling Tips

#### Custom CSS for HTML Output

Modify the CSS in the HTML template section of visualization scripts:

```python
html_content = f"""
<style>
    body {{
        font-family: 'Arial', sans-serif;  /* Change font */
        background-color: #f5f5f5;         /* Background color */
        color: #333;                        /* Text color */
    }}

    .stat-card {{
        border-radius: 8px;                 /* Rounded corners */
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);  /* Shadow effect */
        padding: 20px;
    }}

    h1 {{
        color: #2c3e50;                     /* Custom heading color */
        font-size: 32px;
    }}
</style>
"""
```

#### Chart Size and Layout

Adjust chart dimensions:

```python
fig.update_layout(
    height=600,        # Chart height in pixels
    width=1200,        # Chart width (or use autosize=True)
    margin=dict(l=50, r=50, t=80, b=50),  # Margins (left, right, top, bottom)
    autosize=True      # Auto-resize to container
)
```

#### Font Customization

```python
fig.update_layout(
    font=dict(
        family='Arial, sans-serif',
        size=14,
        color='#333333'
    ),
    title_font=dict(
        size=24,
        family='Georgia, serif'
    )
)
```

## Technical Details

### Plotly Configuration

All visualizations use **Plotly 2.26.0** or compatible version, loaded via CDN:

```html
<script src="https://cdn.plot.ly/plotly-2.26.0.min.js"></script>
```

#### Key Plotly Features Used

- **Interactive Charts:** Hover, zoom, pan, legend toggle
- **Multiple Chart Types:** Line, bar, scatter, pie, heatmap, box plots
- **Responsive Design:** Auto-resize to container
- **No External Dependencies:** Standalone HTML files
- **Export Options:** Built-in PNG export (via camera icon)

#### Plotly Configuration Options

Default configuration used:

```python
config = {
    'displayModeBar': True,         # Show toolbar
    'displaylogo': False,           # Hide Plotly logo
    'modeBarButtonsToRemove': ['lasso2d', 'select2d'],  # Remove specific tools
    'toImageButtonOptions': {
        'format': 'png',             # Export format
        'filename': 'visualization',
        'height': 1080,
        'width': 1920,
        'scale': 2                   # Higher quality
    }
}

fig.show(config=config)
```

### Data Transformation Pipeline

#### 1. Data Loading

```python
# DataLoader reads CSV files
loader = DataLoader()
weather_df = loader.load_weather(data_source='demo1', forecast_only=True)
destinations_df = loader.load_destinations()
```

#### 2. Data Validation

DataLoader automatically:
- Validates column names and data types
- Converts date strings to `datetime` objects
- Handles missing values appropriately
- Filters by data source and forecast flags

#### 3. Data Merging

```python
# Join weather data with destination details
merged_df = weather_df.merge(
    destinations_df,
    on='destination_id',
    how='left'
)
```

#### 4. Aggregation

```python
# Calculate statistics by destination
stats_df = df.groupby('destination_name').agg({
    'avg_temp_c': 'mean',
    'rainfall_mm': 'sum',
    'uv_index': 'max'
}).reset_index()
```

#### 5. Chart Creation

```python
# Transform data into Plotly figure
fig = px.line(
    df,
    x='date',
    y='avg_temp_c',
    color='destination_name',
    title='Temperature Trends'
)
```

#### 6. HTML Generation

```python
# Convert to standalone HTML
html = fig.to_html(
    include_plotlyjs='cdn',  # Use CDN for Plotly
    full_html=True,          # Complete HTML document
    config=config
)
```

### Performance Considerations

#### Data Volume
- Current dataset: ~42 weather records, 6 destinations
- Plotly handles up to 10,000+ points efficiently
- For larger datasets, consider:
  - Data aggregation
  - Sampling techniques
  - Lazy loading with Dash

#### File Sizes
- Weather forecast HTML: ~90KB
- Includes all chart data inline
- For very large datasets, consider:
  - External JSON data files
  - Server-side rendering with Dash
  - Data pagination

#### Rendering Performance
- Modern browsers handle Plotly efficiently
- Avoid too many traces (>50) on single chart
- Use `scattergl` instead of `scatter` for 1000+ points
- Enable WebGL rendering for better performance:

```python
fig = go.Figure(data=go.Scattergl(  # Note: Scattergl instead of Scatter
    x=df['x'],
    y=df['y'],
    mode='markers'
))
```

### Browser Compatibility

#### Supported Browsers
✅ Chrome/Chromium 90+
✅ Firefox 88+
✅ Safari 14+
✅ Edge 90+
✅ Opera 76+

#### Mobile Support
✅ iOS Safari 14+
✅ Chrome Mobile
✅ Firefox Mobile

#### Features Requiring Modern Browsers
- WebGL rendering (for high-performance charts)
- ES6 JavaScript features
- CSS Grid and Flexbox layouts
- HTML5 Canvas

#### Fallbacks
- Plotly automatically falls back to Canvas if WebGL unavailable
- Responsive layouts adapt to mobile screens
- Touch interactions supported on mobile devices

#### Testing Recommendations
Test visualizations in:
1. Desktop browsers (Chrome, Firefox, Safari)
2. Mobile browsers (iOS Safari, Chrome Mobile)
3. Different screen sizes (responsive design)
4. Offline mode (verify standalone functionality)

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: "No module named 'pandas'"

**Symptom:** Error when running visualization scripts
**Cause:** Missing Python dependencies

**Solution:**
```bash
pip install pandas plotly
```

#### Issue 2: "FileNotFoundError: data/destinations/destinations.csv"

**Symptom:** Script can't find CSV files
**Cause:** Running script from wrong directory or missing data files

**Solution:**
```bash
# Ensure you're in project root
cd /home/runner/work/places2go/places2go

# Verify data files exist
ls data/destinations/
ls data/weather/

# Run script
python scripts/visualizations/weather_forecast.py
```

#### Issue 3: HTML File Opens but Charts Don't Display

**Symptom:** Blank page or missing charts
**Cause:** JavaScript errors or CDN loading issues

**Solutions:**
1. Check browser console for errors (F12 → Console tab)
2. Verify internet connection (Plotly CDN requires internet on first load)
3. Try a different browser
4. Check if popup/script blockers are interfering

#### Issue 4: Outdated Data Displayed

**Symptom:** Old data shown in visualization
**Cause:** HTML file not regenerated after data update

**Solution:**
```bash
# Regenerate visualization
python scripts/visualizations/weather_forecast.py

# Refresh browser (hard refresh: Ctrl+Shift+R or Cmd+Shift+R)
```

#### Issue 5: Charts Not Responsive on Mobile

**Symptom:** Charts too small or not fitting mobile screen
**Cause:** Missing responsive configuration

**Solution:**
Add to chart layout in visualization script:
```python
fig.update_layout(
    autosize=True,
    margin=dict(l=10, r=10, t=40, b=10)
)
```

Ensure HTML has viewport meta tag:
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

#### Issue 6: "PermissionError: [Errno 13] Permission denied"

**Symptom:** Can't write HTML file
**Cause:** Insufficient write permissions or file locked

**Solutions:**
1. Close HTML file if open in browser
2. Check folder permissions: `ls -la .build/visualizations/`
3. Try deleting old file: `rm .build/visualizations/weather_forecast.html`
4. Regenerate visualization

#### Issue 7: Colors Not Matching Across Charts

**Symptom:** Same destination has different colors in different charts
**Cause:** Inconsistent color mapping

**Solution:**
Define color dictionary at script level:
```python
DESTINATION_COLORS = {
    'Bangkok': '#FF6B6B',
    'Tokyo': '#4ECDC4',
    'Barcelona': '#45B7D1',
    'Prague': '#FFA07A',
    'Lisbon': '#98D8C8',
    'Marrakech': '#F7DC6F'
}

# Use in all charts
fig.update_traces(marker_color=[DESTINATION_COLORS[d] for d in destinations])
```

### Data Validation

Before generating visualizations, validate your data:

#### Check Data Loading

```python
from scripts.core.data_loader import DataLoader

loader = DataLoader()

# Load and inspect data
df = loader.load_weather(data_source='demo1', forecast_only=True)
print(f"Records loaded: {len(df)}")
print(f"Columns: {df.columns.tolist()}")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
print(f"\nFirst few records:")
print(df.head())
```

#### Validate Data Quality

```python
# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())

# Check data types
print("\nData types:")
print(df.dtypes)

# Check value ranges
print("\nTemperature range:", df['avg_temp_c'].min(), "to", df['avg_temp_c'].max())
print("UV index range:", df['uv_index'].min(), "to", df['uv_index'].max())
```

#### Verify Destination Matching

```python
# Ensure all destinations have data
destinations = loader.load_destinations()
weather_destinations = df['destination_id'].unique()

print(f"\nTotal destinations: {len(destinations)}")
print(f"Destinations with weather data: {len(weather_destinations)}")

# Find any missing
all_dest_ids = set(destinations['destination_id'])
weather_dest_ids = set(weather_destinations)
missing = all_dest_ids - weather_dest_ids
if missing:
    print(f"Warning: Missing weather data for: {missing}")
```

### Regenerating Visualizations

#### Full Regeneration

```bash
# Delete old files
rm -rf .build/visualizations/*.html

# Regenerate all (as they become available)
python scripts/visualizations/weather_forecast.py
# python scripts/visualizations/destinations_map.py
# python scripts/visualizations/cost_comparison.py
# python scripts/visualizations/flight_prices.py
```

#### Force Fresh Data

```python
# In your script, clear DataLoader cache if needed
loader = DataLoader()
# DataLoader automatically loads fresh data on each call

# If implementing caching, you might add:
# loader.clear_cache()
```

### Debugging Tips

#### Enable Debug Logging

Add to top of visualization script:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

#### Inspect Intermediate Data

Add debug prints at key steps:

```python
# After loading data
logger.debug(f"Loaded data shape: {df.shape}")
logger.debug(f"Columns: {df.columns.tolist()}")

# After transformations
logger.debug(f"After filtering: {filtered_df.shape}")
logger.debug(f"Unique destinations: {df['destination_name'].unique()}")

# Before chart creation
logger.debug(f"Creating chart with {len(df)} records")
```

#### Test Chart Creation Separately

Create minimal test script:

```python
import plotly.graph_objects as go

# Minimal test
fig = go.Figure(data=go.Bar(x=['A', 'B', 'C'], y=[1, 2, 3]))
fig.show()  # Opens in browser
```

#### Check HTML Output

View generated HTML source:
1. Open HTML file in browser
2. Right-click → "View Page Source"
3. Check for JavaScript errors
4. Verify Plotly script loaded
5. Look for data in script tags

## Future Enhancements

### Planned Features

#### Phase 3C - Advanced Analytics
- **Multi-dataset overlay dashboard** - Comprehensive view combining all datasets
- **Value finder algorithm** - AI-powered recommendations for best destinations
- **Correlation analysis** - Automatic pattern detection across datasets
- **Custom filtering** - Save and share filter configurations
- **Report generation** - Export insights as PDF reports

#### API Integration
- **Live weather data** - Real-time weather updates from APIs
- **Flight price APIs** - Current flight pricing from travel sites
- **Cost of living APIs** - Updated cost data from Numbeo, Expatistan
- **Auto-refresh** - Periodic data updates without regeneration

#### Real-Time Updates
- **WebSocket support** - Live data streaming
- **Auto-regeneration** - Scheduled updates (daily/weekly)
- **Change notifications** - Alert on significant price/weather changes
- **Version history** - Track data changes over time

#### Interactive Overlays
- **Drag-and-drop** - Rearrange dashboard components
- **Custom dashboards** - Build your own visualization combinations
- **Saved views** - Bookmark favorite configurations
- **Collaboration** - Share annotated visualizations
- **Embedded maps** - Full Leaflet/Mapbox integration

#### Enhanced Chart Types
- **3D visualizations** - Plotly 3D scatter and surface plots
- **Animated charts** - Time-series animations
- **Network graphs** - Destination connections and routes
- **Sankey diagrams** - Flow analysis (costs, travel paths)
- **Tree maps** - Hierarchical data visualization

#### Mobile App
- **Progressive Web App (PWA)** - Install as mobile app
- **Offline mode** - View cached visualizations offline
- **Mobile-optimized** - Touch gestures and mobile-first design
- **Push notifications** - Price alerts and weather warnings

#### Data Export
- **CSV export** - Download filtered data
- **JSON API** - Programmatic access to data
- **PDF reports** - Formatted travel planning documents
- **Image export** - High-resolution chart images
- **Shareable links** - Direct links to specific views

### Contributing

Want to contribute to visualization development? See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

**Focus areas:**
- Adding new chart types
- Improving performance
- Mobile responsiveness
- Accessibility features
- Documentation improvements

### Roadmap

**Q4 2024:**
- ✅ Weather forecast dashboard (Complete)
- 🚧 Destinations map visualization
- 🚧 Cost comparison charts
- 🚧 Flight prices time-series

**Q1 2025:**
- Multi-dataset overlay dashboard
- API integration planning
- Performance optimization
- Mobile PWA prototype

**Q2 2025:**
- Real-time data updates
- AI-powered recommendations
- Custom dashboard builder
- Collaborative features

---

## Need Help?

- **Issues:** [GitHub Issues](https://github.com/NCAsterism/places2go/issues)
- **Discussions:** [GitHub Discussions](https://github.com/NCAsterism/places2go/discussions)
- **Documentation:** [Main README](../../README.md)
- **Contributing:** [CONTRIBUTING.md](../../CONTRIBUTING.md)

**Last Updated:** October 2024
**Version:** 1.0
**Maintainer:** NCAsterism
