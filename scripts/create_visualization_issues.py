#!/usr/bin/env python3
"""
Create GitHub issues for data visualization pages.

Generates issues for building interactive HTML visualization pages for each CSV dataset.
These pages will help explore and refine data, with the goal of overlaying multiple datasets.
"""

import json
from pathlib import Path

# Issue templates for each dataset
ISSUES = [
    {
        "title": "Create interactive destinations map visualization",
        "labels": ["enhancement", "visualization", "phase-3b"],
        "body": """## Overview
Create an interactive HTML page to visualize destination locations on a map with detailed information overlays.

## Objectives
- Display all destinations on an interactive map (using Leaflet or Plotly)
- Show destination details on hover/click (name, country, airport codes, coordinates)
- Color-code by region or country
- Add filtering by country or region
- Include summary statistics panel

## Data Source
- File: `data/destinations/destinations.csv`
- DataLoader: `loader.load_destinations()`
- Fields: destination_id, name, country, country_code, region, latitude,
  longitude, timezone, airport_code, airport_name, origin_airport

## Technical Requirements
- Use Plotly for interactive map (mapbox or scatter_geo)
- Generate standalone HTML file in `.build/visualizations/`
- Match styling with existing dashboard charts
- Include data source attribution
- Add zoom/pan controls
- Responsive design

## Acceptance Criteria
- [ ] HTML file generated with interactive map
- [ ] All 6 destinations plotted with correct coordinates
- [ ] Hover shows destination details (name, country, airports)
- [ ] Click shows full details panel
- [ ] Color-coding by region
- [ ] Summary stats panel (total destinations by country/region)
- [ ] File saved to `.build/visualizations/destinations_map.html`
- [ ] Documentation in visualization README

## Future Enhancement
This will be overlaid with flight routes and weather patterns in Phase 3C.

## Estimated Effort
2-3 hours
""",
    },
    {
        "title": "Create cost of living comparison visualization",
        "labels": ["enhancement", "visualization", "phase-3b"],
        "body": """## Overview
Create an interactive HTML page to compare cost of living across destinations with detailed breakdowns.

## Objectives
- Bar chart comparing total monthly costs by destination
- Stacked bar chart showing cost breakdown (rent, food, transport, etc.)
- Interactive tooltips with exact values
- Sorting options (by total cost, by specific category)
- Filter by cost range
- Data source indicator

## Data Source
- File: `data/destinations/cost_of_living.csv`
- DataLoader: `loader.load_costs(data_source='demo1')`
- Fields: destination_id, data_date, currency, monthly_living_cost,
  rent_1br_center, rent_1br_outside, monthly_food, monthly_transport,
  utilities, internet, meal_inexpensive, meal_mid_range, beer_domestic,
  weed_cost_per_gram, data_source

## Technical Requirements
- Use Plotly for interactive bar charts
- Generate standalone HTML file in `.build/visualizations/`
- Match styling with existing dashboard
- Show currency (£ GBP)
- Include data freshness indicator (data_date)
- Responsive design

## Visualizations
1. **Total Cost Comparison**: Horizontal bar chart, sorted by cost
2. **Cost Breakdown**: Stacked bar chart showing all categories
3. **Category Comparison**: Grouped bar chart for specific categories
4. **Cost Distribution**: Box plot showing range and outliers

## Acceptance Criteria
- [ ] HTML file with multiple interactive charts
- [ ] All 6 destinations shown with correct costs
- [ ] Hover shows exact values and percentages
- [ ] Click toggles visibility of cost categories
- [ ] Sort/filter controls working
- [ ] Color-coded by destination matching map colors
- [ ] Data date and source displayed
- [ ] File saved to `.build/visualizations/cost_comparison.html`
- [ ] Documentation in visualization README

## Future Enhancement
Overlay with destination map to show cost vs location patterns.

## Estimated Effort
3-4 hours
""",
    },
    {
        "title": "Create flight prices time-series visualization",
        "labels": ["enhancement", "visualization", "phase-3b"],
        "body": """## Overview
Create an interactive HTML page showing flight price trends over time with filtering and analysis features.

## Objectives
- Line chart showing price trends for each destination over 7 days
- Interactive date range selector
- Filter by destination, airline, or price range
- Show min/max/average prices
- Highlight direct vs indirect flights
- Display search date context

## Data Source
- File: `data/flights/flight_prices.csv`
- DataLoader: `loader.load_flights(data_source='demo1')`
- Fields: flight_id, destination_id, origin_airport, search_date,
  departure_date, return_date, price, currency, flight_duration_hours,
  distance_km, airline, direct_flight, data_source

## Technical Requirements
- Use Plotly for time-series line charts
- Generate standalone HTML file in `.build/visualizations/`
- Match styling with existing dashboard
- Time-series X-axis with proper date formatting
- Multi-line chart (one line per destination)
- Interactive legend (click to hide/show destinations)
- Responsive design

## Visualizations
1. **Price Trends**: Multi-line chart showing prices over departure dates
2. **Price Distribution**: Box plot by destination
3. **Airline Comparison**: Grouped bar chart of average prices by airline
4. **Duration vs Cost**: Scatter plot showing correlation
5. **Weekly View**: Calendar heatmap of prices

## Acceptance Criteria
- [ ] HTML file with multiple interactive charts
- [ ] All 42 flight records plotted correctly
- [ ] Date range selector working (Oct 11-17)
- [ ] Filter by destination checkboxes
- [ ] Filter by airline dropdown
- [ ] Hover shows full flight details (price, airline, duration, direct)
- [ ] Legend toggles line visibility
- [ ] Color-coded by destination (matching map)
- [ ] Search date displayed prominently
- [ ] File saved to `.build/visualizations/flight_prices.html`
- [ ] Documentation in visualization README

## Future Enhancement
- Overlay with weather data to show price/weather correlation
- Add route lines on destination map
- Predict future prices based on trends

## Estimated Effort
4-5 hours
""",
    },
    {
        "title": "Create weather forecast visualization dashboard",
        "labels": ["enhancement", "visualization", "phase-3b"],
        "body": """## Overview
Create an interactive HTML page displaying weather forecasts with multiple chart types and comparison features.

## Objectives
- Temperature trends line chart for all destinations
- Daily weather cards with icons
- Comparison view (side-by-side destinations)
- Weather statistics (avg temp, rainfall, sunshine)
- UV index heatmap
- Interactive date selector

## Data Source
- File: `data/weather/weather_data.csv`
- DataLoader: `loader.load_weather(data_source='demo1', forecast_only=True)`
- Fields: weather_id, destination_id, date, temp_high_c, temp_low_c,
  temp_avg_c, rainfall_mm, humidity_percent, sunshine_hours,
  wind_speed_kmh, conditions, uv_index, forecast_flag, data_source

## Technical Requirements
- Use Plotly for interactive charts
- Generate standalone HTML file in `.build/visualizations/`
- Match styling with existing dashboard
- Weather condition icons/emojis
- Temperature range shading (high/low)
- Responsive design

## Visualizations
1. **Temperature Trends**: Multi-line chart (high/low/avg) for each destination
2. **Weather Cards**: Grid of daily forecasts with icons
3. **Rainfall Chart**: Bar chart showing daily rainfall by destination
4. **UV Index Heatmap**: Calendar heatmap showing UV levels
5. **Conditions Summary**: Pie chart of weather conditions distribution
6. **Comfort Index**: Combined temp/humidity/wind chart

## Acceptance Criteria
- [ ] HTML file with multiple interactive charts
- [ ] All 42 weather records displayed correctly
- [ ] Temperature line charts with range shading
- [ ] Daily cards with weather icons and conditions
- [ ] Date range selector (Oct 5-11)
- [ ] Filter by destination checkboxes
- [ ] Hover shows full details (all weather metrics)
- [ ] Color-coded by destination (matching map)
- [ ] Forecast flag indicator
- [ ] File saved to `.build/visualizations/weather_forecast.html`
- [ ] Documentation in visualization README

## Future Enhancement
- Overlay on destination map as colored markers
- Correlate with flight prices (weather impact on pricing)
- Add historical comparison

## Estimated Effort
4-5 hours
""",
    },
    {
        "title": "Create multi-dataset overlay visualization dashboard",
        "labels": ["enhancement", "visualization", "phase-3c", "future"],
        "body": """## Overview
Create a comprehensive HTML dashboard that overlays all datasets to reveal correlations and insights.

## Objectives
- Interactive map with destinations, flight routes, and weather overlays
- Unified timeline showing flights and weather together
- Cost vs weather/location analysis
- Best value finder (low cost + good weather + cheap flights)
- Destination comparison tool
- Export insights as report

## Data Sources
- All 4 CSV files via DataLoader
- Merged view: `loader.load_all(data_source='demo1')`
- Aggregates: `loader.get_aggregates(data_source='demo1')`

## Technical Requirements
- Use Plotly Dash or single-page HTML with multiple subplots
- Generate standalone HTML file in `.build/visualizations/`
- Consistent color scheme across all visualizations
- Cross-filtering (select on one chart filters others)
- Responsive layout with tabs or sections
- Performance optimized for 42+ records

## Visualizations
1. **Master Map**:
   - Destinations plotted with size = cost, color = avg temp
   - Flight routes as curved lines (thickness = price)
   - Weather overlay with icons
   - Click destination to filter all charts

2. **Timeline View**:
   - X-axis: dates (Oct 5-17)
   - Top: Flight prices line chart
   - Bottom: Weather conditions bars
   - Aligned by date for correlation

3. **Value Finder**:
   - Scatter plot: X=cost, Y=avg_temp, size=flight_price
   - Quadrants: "Best Value" (low cost, good weather, cheap flights)
   - Interactive selection

4. **Destination Comparison**:
   - Radar chart comparing 2-3 destinations
   - Metrics: cost, weather, flight price, sunshine, etc.
   - Normalized 0-100 scale

5. **Insights Panel**:
   - Best value destination
   - Cheapest flights by day
   - Best weather days
   - Cost savings summary

## Acceptance Criteria
- [ ] HTML file with integrated multi-dataset view
- [ ] Map shows all destinations with overlays
- [ ] Timeline aligns flights and weather
- [ ] Value finder quadrant chart working
- [ ] Destination comparison radar chart
- [ ] Cross-filtering between charts
- [ ] Insights panel with calculated recommendations
- [ ] All data sources displayed
- [ ] Color consistency across charts
- [ ] File saved to `.build/visualizations/dashboard_overlay.html`
- [ ] Documentation in visualization README
- [ ] Performance: loads < 2 seconds

## Dependencies
- Requires issues #1-4 completed first
- Build on existing visualization patterns

## Future Enhancement
- Add real-time API data integration
- Machine learning predictions
- User preferences input
- Save/share custom views

## Estimated Effort
8-10 hours (after individual visualizations complete)
""",
    },
    {
        "title": "Add visualization documentation and README",
        "labels": ["documentation", "visualization", "phase-3b"],
        "body": """## Overview
Create comprehensive documentation for the visualization pages including setup, usage, and customization guides.

## Objectives
- Create `.build/visualizations/README.md`
- Document each visualization page
- Add customization guide
- Include embedding instructions
- Provide troubleshooting tips

## Documentation Structure

### 1. Overview
- Purpose of visualization pages
- How they complement the dashboard
- Data sources and DataLoader usage

### 2. Visualization Pages
For each page (destinations map, costs, flights, weather, overlay):
- Purpose and use cases
- Key features
- How to generate
- Interactive features guide
- Screenshots/examples

### 3. Getting Started
- Prerequisites (Python, DataLoader)
- How to generate all visualizations
- Where files are saved
- How to view (open HTML in browser)

### 4. Customization Guide
- Modifying colors/themes
- Adding new charts
- Filtering data
- Changing date ranges
- Styling tips

### 5. Technical Details
- Plotly configuration
- Data transformation pipeline
- Performance considerations
- Browser compatibility

### 6. Troubleshooting
- Common issues and solutions
- Data validation
- Regenerating visualizations
- Debugging tips

### 7. Future Enhancements
- Planned features
- API integration
- Real-time updates
- Interactive overlays

## Files to Create
- `.build/visualizations/README.md` - Main documentation
- `.build/visualizations/examples/` - Screenshot folder
- Add section to main project README.md
- Update CONTRIBUTING.md with visualization guidelines

## Acceptance Criteria
- [ ] README.md created with all sections
- [ ] Each visualization documented with:
  - Purpose and features
  - Generation command
  - Usage instructions
  - Customization options
- [ ] Code examples for generating each visualization
- [ ] Screenshots or example outputs
- [ ] Troubleshooting section
- [ ] Links from main README.md
- [ ] Guidelines in CONTRIBUTING.md
- [ ] Clear, beginner-friendly writing
- [ ] Proper markdown formatting

## Estimated Effort
2-3 hours
""",
    },
]


def main() -> None:
    """Generate GitHub issue creation script."""
    print("=" * 70)
    print("Visualization Issues Generator")
    print("=" * 70)
    print()

    # Save issues to JSON file for review
    output_file = Path(".build") / "visualization_issues.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w") as f:
        json.dump(ISSUES, f, indent=2)

    print(f"✓ Generated {len(ISSUES)} issue templates")
    print(f"✓ Saved to: {output_file}")
    print()

    # Print summary
    print("Issue Summary:")
    print("-" * 70)
    for i, issue in enumerate(ISSUES, 1):
        print(f"{i}. {issue['title']}")
        print(f"   Labels: {', '.join(issue['labels'])}")
        body = issue["body"]
        assert isinstance(body, str)  # Type narrowing for mypy
        effort = [line for line in body.split("\n") if "Estimated Effort" in line]
        if effort:
            print(f"   {effort[0].strip()}")
        print()

    # Print GitHub CLI commands
    print("=" * 70)
    print("GitHub CLI Commands (run these to create issues):")
    print("=" * 70)
    print()

    for i, issue in enumerate(ISSUES, 1):
        # Escape quotes and newlines for shell
        title = issue["title"]
        labels = ",".join(issue["labels"])
        body_file = f".build/issue_{i}_body.md"

        # Save body to temp file for easier CLI usage
        body = issue["body"]
        assert isinstance(body, str)  # Type narrowing for mypy
        with open(body_file, "w") as f:
            f.write(body)

        print(f"# Issue {i}: {title}")
        print(
            f'gh issue create --title "{title}" --label "{labels}" --body-file "{body_file}"'
        )
        print()

    # Print alternative Python script
    print("=" * 70)
    print("Alternative: Python Script Using PyGithub")
    print("=" * 70)
    print()
    print("Save this as 'create_issues_via_api.py' and run:")
    print()
    print(
        """
import json
from github import Github
from pathlib import Path

# Set your GitHub token
GITHUB_TOKEN = "your_token_here"
REPO = "NCAsterism/places2go"

g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO)

# Load issues
with open(".build/visualization_issues.json") as f:
    issues = json.load(f)

# Create issues
for issue_data in issues:
    issue = repo.create_issue(
        title=issue_data["title"],
        body=issue_data["body"],
        labels=issue_data["labels"]
    )
    print(f"✓ Created issue #{issue.number}: {issue.title}")
    """
    )

    print()
    print("=" * 70)
    print("Next Steps:")
    print("=" * 70)
    print("1. Review issues in .build/visualization_issues.json")
    print("2. Use GitHub CLI commands above to create issues")
    print("3. Or use Python script with PyGithub")
    print("4. Assign issues to bots or team members")
    print("5. Track progress in GitHub Projects")
    print()


if __name__ == "__main__":
    main()
