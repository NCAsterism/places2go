# Visualizations

This directory contains scripts that generate standalone interactive HTML visualizations using Plotly.

## Available Visualizations

### 1. Weather Forecast Dashboard
**Script:** `weather_forecast.py`  
**Output:** `.build/visualizations/weather_forecast.html`

Interactive 7-day weather forecast dashboard displaying:
- Temperature trends (high/low/avg) for each destination
- Daily weather cards with icons and conditions
- Rainfall bar chart by destination
- UV index heatmap
- Weather conditions distribution pie chart
- Comfort index chart (temp/humidity/wind)

**Usage:**
```bash
python scripts/visualizations/weather_forecast.py
```

**Data Source:** `DataLoader.load_weather(data_source='demo1', forecast_only=True)`

### 2. Cost of Living Comparison
**Script:** `cost_comparison.py`  
**Output:** `.build/visualizations/cost_comparison.html`

Interactive cost of living comparison dashboard displaying:
- Total monthly living cost horizontal bar chart (sorted by cost)
- Stacked bar chart showing cost breakdown by category (rent, food, transport, utilities, internet)
- Grouped bar chart for dining & leisure cost comparison
- Box plot showing cost distribution and outliers across categories
- Summary statistics (average, min/max costs, cost range)

**Usage:**
```bash
python scripts/visualizations/cost_comparison.py
```

**Data Source:** `DataLoader.load_costs(data_source='demo1')`

### 3. Flight Prices Time-Series
**Script:** `flight_prices.py`  
**Output:** `.build/visualizations/flight_prices.html`

Interactive flight prices dashboard displaying:
- Price trends over departure dates
- Weekly calendar heatmap
- Price distribution box plots
- Airline comparison
- Duration vs cost analysis

**Usage:**
```bash
python scripts/visualizations/flight_prices.py
```

**Data Source:** `DataLoader.load_flights(data_source='demo1')`

### 4. Destinations Map
**Script:** `destinations_map.py`  
**Output:** `.build/visualizations/destinations_map.html`

Interactive map dashboard displaying:
- Geographic visualization of all destinations
- Color-coded by region
- Summary statistics
- Destination detail cards

**Usage:**
```bash
python scripts/visualizations/destinations_map.py
```

**Data Source:** `DataLoader.load_destinations()`

### 5. Multi-Dataset Overlay Dashboard
**Script:** `overlay_dashboard.py`  
**Output:** `.build/visualizations/overlay_dashboard.html`

Comprehensive dashboard integrating all visualizations with tabbed navigation:
- **Tab 1:** Overview with summary statistics and insights
- **Tab 2:** Destinations map
- **Tab 3:** Weather forecasts
- **Tab 4:** Flight prices
- **Tab 5:** Cost of living
- **Tab 6:** Destination comparison with radar chart

**Usage:**
```bash
python scripts/visualizations/overlay_dashboard.py
```

**Data Sources:** All datasets via DataLoader (destinations, costs, flights, weather)

## Development

### Adding New Visualizations

When creating a new visualization:

1. Create a new Python script in `scripts/visualizations/`
2. Import and use `DataLoader` from `scripts.core.data_loader`
3. Use Plotly for interactive charts
4. Generate standalone HTML with embedded Plotly.js
5. Save output to `.build/visualizations/`
6. Match the styling of existing dashboards
7. Add tests in `tests/test_<visualization_name>.py`
8. Update this README

### Styling Guidelines

All visualizations should follow consistent styling:

```python
# CSS styling
- Font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, etc.
- Background: #f5f5f5
- Container: white background, rounded corners, box shadow
- Primary color: #1f77b4 (blue)
- Stats cards: #f9f9f9 background with blue left border
- Info boxes: #e7f3ff background with blue left border

# Plotly template
- Template: "plotly_white"
- Include Plotly.js: 'require' (inline) for first chart, False for others
- Responsive: True
- Hover templates: Show exact values with proper formatting
```

### Destination Colors

Use consistent colors across all visualizations:

```python
DESTINATION_COLORS = {
    "Alicante": "#1f77b4",
    "Malaga": "#ff7f0e",
    "Majorca": "#2ca02c",
    "Faro": "#d62728",
    "Corfu": "#9467bd",
    "Rhodes": "#8c564b",
}
```

### Testing

Each visualization should have comprehensive tests:

- Unit tests for individual chart functions
- Integration test that runs main() and checks HTML output
- Validation of chart types, titles, and data
- Check for presence of all expected elements

Run tests:
```bash
pytest tests/test_<visualization_name>.py -v
```

## Output Files

All generated HTML files are saved to `.build/visualizations/` which is git-ignored. These are standalone files that can be:
- Opened directly in a web browser
- Deployed to a web server
- Embedded in other web pages

The HTML files are self-contained with embedded Plotly.js (~3.5MB) and require no external dependencies.
