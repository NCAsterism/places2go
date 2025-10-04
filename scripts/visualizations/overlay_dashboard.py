"""
overlay_dashboard.py
--------------------

This script creates a comprehensive multi-dataset overlay dashboard that integrates
all individual visualizations (weather, flights, costs, destinations) into a single
interactive interface with tabbed navigation and cross-dataset comparison.

The dashboard includes:
- Tab 1: Overview Dashboard with summary statistics
- Tab 2: Destinations Map with interactive features
- Tab 3: Weather Forecast with 7-day trends
- Tab 4: Flight Prices with time-series analysis
- Tab 5: Cost of Living comparisons
- Tab 6: Destination Comparison with radar charts

Output: `.build/visualizations/overlay_dashboard.html`
"""

import logging
import sys
from pathlib import Path
from typing import Dict, List

import pandas as pd
import plotly.graph_objects as go

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.core.data_loader import DataLoader  # noqa: E402

# Import chart functions from individual visualization modules
from scripts.visualizations.weather_forecast import (  # noqa: E402
    create_temperature_trends_chart,
    create_rainfall_chart,
    create_uv_index_heatmap,
    create_comfort_index_chart,
)
from scripts.visualizations.flight_prices import (  # noqa: E402
    create_price_trends_chart,
    create_price_distribution_boxplot,
    create_weekly_heatmap,
)
from scripts.visualizations.cost_comparison import (  # noqa: E402
    create_total_cost_chart,
    create_cost_breakdown_chart,
)
from scripts.visualizations.destinations_map import (  # noqa: E402
    create_interactive_map,
)

# Configure logging
log_dir = Path(__file__).resolve().parents[2] / ".build" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_dir / "overlay_dashboard.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)

# Shared color palette for destinations
DESTINATION_COLORS = {
    "Alicante": "#1f77b4",
    "Malaga": "#ff7f0e",
    "Majorca": "#2ca02c",
    "Faro": "#d62728",
    "Corfu": "#9467bd",
    "Rhodes": "#8c564b",
}


def create_overview_summary(
    destinations_df: pd.DataFrame,
    costs_df: pd.DataFrame,
    flights_df: pd.DataFrame,
    weather_df: pd.DataFrame,
) -> str:
    """
    Create overview summary HTML with key statistics.

    Args:
        destinations_df: Destinations DataFrame
        costs_df: Cost of living DataFrame
        flights_df: Flight prices DataFrame
        weather_df: Weather data DataFrame

    Returns:
        HTML string with summary statistics
    """
    logger.info("Creating overview summary")

    # Calculate statistics
    total_destinations = len(destinations_df)
    avg_flight_price = flights_df["price"].mean() if not flights_df.empty else 0
    avg_monthly_cost = (
        costs_df["monthly_living_cost"].mean() if not costs_df.empty else 0
    )

    # Best weather destination (highest avg temp)
    if not weather_df.empty:
        weather_with_names = weather_df.merge(
            destinations_df[["destination_id", "name"]], on="destination_id"
        )
        avg_temps = weather_with_names.groupby("name")["temp_avg_c"].mean()
        best_weather = avg_temps.idxmax()
        best_weather_temp = avg_temps.max()
    else:
        best_weather = "N/A"
        best_weather_temp = 0

    # Cheapest and most expensive destinations
    if not costs_df.empty:
        costs_with_names = costs_df.merge(
            destinations_df[["destination_id", "name"]], on="destination_id"
        )
        cheapest_dest = costs_with_names.loc[
            costs_with_names["monthly_living_cost"].idxmin()
        ]
        most_expensive_dest = costs_with_names.loc[
            costs_with_names["monthly_living_cost"].idxmax()
        ]
    else:
        cheapest_dest = {"name": "N/A", "monthly_living_cost": 0}
        most_expensive_dest = {"name": "N/A", "monthly_living_cost": 0}

    # Best flight deal
    if not flights_df.empty:
        flights_with_names = flights_df.merge(
            destinations_df[["destination_id", "name"]], on="destination_id"
        )
        best_flight = flights_with_names.loc[flights_with_names["price"].idxmin()]
    else:
        best_flight = {"name": "N/A", "price": 0, "departure_date": "N/A"}

    html = f"""
    <div class="overview-container">
        <h2>📊 Dashboard Overview</h2>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">🗺️</div>
                <div class="stat-label">Total Destinations</div>
                <div class="stat-value">{total_destinations}</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">✈️</div>
                <div class="stat-label">Avg Flight Price</div>
                <div class="stat-value">£{avg_flight_price:.0f}</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">💰</div>
                <div class="stat-label">Avg Monthly Cost</div>
                <div class="stat-value">£{avg_monthly_cost:.0f}</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🌡️</div>
                <div class="stat-label">Best Weather</div>
                <div class="stat-value">{best_weather}</div>
                <div class="stat-detail">{best_weather_temp:.1f}°C avg</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🏆</div>
                <div class="stat-label">Cheapest Destination</div>
                <div class="stat-value">{cheapest_dest['name']}</div>
                <div class="stat-detail">£{cheapest_dest['monthly_living_cost']:.0f}/month</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">💎</div>
                <div class="stat-label">Most Expensive</div>
                <div class="stat-value">{most_expensive_dest['name']}</div>
                <div class="stat-detail">£{most_expensive_dest['monthly_living_cost']:.0f}/month</div>
            </div>
        </div>

        <div class="insights-panel">
            <h3>💡 Key Insights</h3>
            <ul>
                <li><strong>Best Flight Deal:</strong> {best_flight['name']} on {best_flight['departure_date']} for £{best_flight['price']:.0f}</li>
                <li><strong>Weather Winner:</strong> {best_weather} has the warmest average temperature at {best_weather_temp:.1f}°C</li>
                <li><strong>Budget Champion:</strong> {cheapest_dest['name']} offers the lowest monthly living costs at £{cheapest_dest['monthly_living_cost']:.0f}</li>
                <li><strong>Value Analysis:</strong> Compare destinations across all metrics in the Comparison tab</li>
            </ul>
        </div>
    </div>
    """

    return html


def create_comparison_radar_chart(
    destinations_df: pd.DataFrame,
    costs_df: pd.DataFrame,
    flights_df: pd.DataFrame,
    weather_df: pd.DataFrame,
) -> go.Figure:
    """
    Create radar/spider chart comparing destinations across multiple dimensions.

    Args:
        destinations_df: Destinations DataFrame
        costs_df: Cost of living DataFrame
        flights_df: Flight prices DataFrame
        weather_df: Weather data DataFrame

    Returns:
        Plotly figure object with radar chart
    """
    logger.info("Creating comparison radar chart")

    # Prepare data for radar chart
    comparison_data = []

    for _, dest in destinations_df.iterrows():
        dest_id = dest["destination_id"]
        dest_name = dest["name"]

        # Get metrics
        dest_costs = costs_df[costs_df["destination_id"] == dest_id]
        dest_flights = flights_df[flights_df["destination_id"] == dest_id]
        dest_weather = weather_df[weather_df["destination_id"] == dest_id]

        # Calculate normalized scores (0-100 scale)
        # For cost and flight price: lower is better (invert)
        monthly_cost = (
            dest_costs["monthly_living_cost"].mean()
            if not dest_costs.empty
            else 1000
        )
        flight_price = (
            dest_flights["price"].mean() if not dest_flights.empty else 200
        )
        avg_temp = (
            dest_weather["temp_avg_c"].mean() if not dest_weather.empty else 20
        )
        sunshine = 100 - (
            dest_weather["rainfall_mm"].mean() if not dest_weather.empty else 10
        )
        uv_index = dest_weather["uv_index"].mean() if not dest_weather.empty else 5

        # Normalize scores (higher is better for all)
        cost_score = max(0, 100 - (monthly_cost / 15))  # £1500 = 0 score
        flight_score = max(0, 100 - (flight_price / 3))  # £300 = 0 score
        temp_score = min(100, (avg_temp / 30) * 100)  # 30°C = 100 score
        sunshine_score = min(100, sunshine)
        uv_score = min(100, (uv_index / 10) * 100)  # UV 10 = 100 score

        comparison_data.append(
            {
                "name": dest_name,
                "cost_score": cost_score,
                "flight_score": flight_score,
                "temp_score": temp_score,
                "sunshine_score": sunshine_score,
                "uv_score": uv_score,
            }
        )

    # Create radar chart
    fig = go.Figure()

    categories = [
        "Affordability",
        "Flight Price",
        "Temperature",
        "Sunshine",
        "UV Index",
    ]

    for data in comparison_data:
        values = [
            data["cost_score"],
            data["flight_score"],
            data["temp_score"],
            data["sunshine_score"],
            data["uv_score"],
        ]
        # Close the radar by appending first value
        values.append(values[0])

        fig.add_trace(
            go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill="toself",
                name=data["name"],
                line=dict(
                    color=DESTINATION_COLORS.get(data["name"], "#1f77b4"), width=2
                ),
                opacity=0.6,
            )
        )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=[0, 25, 50, 75, 100],
                ticktext=["0", "25", "50", "75", "100"],
            )
        ),
        showlegend=True,
        title="Multi-Dimensional Destination Comparison",
        height=600,
        template="plotly_white",
    )

    return fig


def create_comparison_table(
    destinations_df: pd.DataFrame,
    costs_df: pd.DataFrame,
    flights_df: pd.DataFrame,
    weather_df: pd.DataFrame,
) -> str:
    """
    Create HTML table comparing all destinations side by side.

    Args:
        destinations_df: Destinations DataFrame
        costs_df: Cost of living DataFrame
        flights_df: Flight prices DataFrame
        weather_df: Weather data DataFrame

    Returns:
        HTML string with comparison table
    """
    logger.info("Creating comparison table")

    # Build comparison data
    table_rows = []

    for _, dest in destinations_df.iterrows():
        dest_id = dest["destination_id"]
        dest_name = dest["name"]

        # Get metrics
        dest_costs = costs_df[costs_df["destination_id"] == dest_id]
        dest_flights = flights_df[flights_df["destination_id"] == dest_id]
        dest_weather = weather_df[weather_df["destination_id"] == dest_id]

        monthly_cost = (
            f"£{dest_costs['monthly_living_cost'].mean():.0f}"
            if not dest_costs.empty
            else "N/A"
        )
        flight_price = (
            f"£{dest_flights['price'].mean():.0f}"
            if not dest_flights.empty
            else "N/A"
        )
        avg_temp = (
            f"{dest_weather['temp_avg_c'].mean():.1f}°C"
            if not dest_weather.empty
            else "N/A"
        )
        rainfall = (
            f"{dest_weather['rainfall_mm'].mean():.1f}mm"
            if not dest_weather.empty
            else "N/A"
        )
        uv_index = (
            f"{dest_weather['uv_index'].mean():.1f}"
            if not dest_weather.empty
            else "N/A"
        )

        color = DESTINATION_COLORS.get(dest_name, "#666666")

        table_rows.append(
            f"""
            <tr>
                <td><span class="dest-badge" style="background-color: {color};">{dest_name}</span></td>
                <td>{dest['country']}</td>
                <td>{monthly_cost}</td>
                <td>{flight_price}</td>
                <td>{avg_temp}</td>
                <td>{rainfall}</td>
                <td>{uv_index}</td>
            </tr>
            """
        )

    html = f"""
    <div class="comparison-table-container">
        <h3>📋 Destination Comparison Table</h3>
        <table class="comparison-table">
            <thead>
                <tr>
                    <th>Destination</th>
                    <th>Country</th>
                    <th>Monthly Cost</th>
                    <th>Avg Flight</th>
                    <th>Avg Temp</th>
                    <th>Avg Rainfall</th>
                    <th>Avg UV</th>
                </tr>
            </thead>
            <tbody>
                {''.join(table_rows)}
            </tbody>
        </table>
    </div>
    """

    return html


def create_overlay_dashboard(output_path: Path) -> None:
    """
    Create comprehensive multi-dataset overlay dashboard HTML file.

    Args:
        output_path: Path to save HTML file
    """
    logger.info("Starting overlay dashboard generation")

    # Load all datasets
    loader = DataLoader()
    destinations_df = loader.load_destinations()
    costs_df = loader.load_costs(data_source="demo1")
    flights_df = loader.load_flights(data_source="demo1")
    weather_df = loader.load_weather(data_source="demo1", forecast_only=True)

    logger.info(f"Loaded {len(destinations_df)} destinations")
    logger.info(f"Loaded {len(costs_df)} cost records")
    logger.info(f"Loaded {len(flights_df)} flight records")
    logger.info(f"Loaded {len(weather_df)} weather records")

    # Create overview summary
    overview_html = create_overview_summary(
        destinations_df, costs_df, flights_df, weather_df
    )

    # Create all charts
    # Tab 2: Map
    map_chart = create_interactive_map(destinations_df)
    map_html = map_chart.to_html(include_plotlyjs=False, div_id="map_chart")

    # Tab 3: Weather
    temp_chart = create_temperature_trends_chart(weather_df, destinations_df)
    rainfall_chart = create_rainfall_chart(weather_df, destinations_df)
    uv_heatmap = create_uv_index_heatmap(weather_df, destinations_df)
    comfort_chart = create_comfort_index_chart(weather_df, destinations_df)

    temp_html = temp_chart.to_html(include_plotlyjs=False, div_id="temp_chart")
    rainfall_html = rainfall_chart.to_html(
        include_plotlyjs=False, div_id="rainfall_chart"
    )
    uv_html = uv_heatmap.to_html(include_plotlyjs=False, div_id="uv_heatmap")
    comfort_html = comfort_chart.to_html(include_plotlyjs=False, div_id="comfort_chart")

    # Tab 4: Flights
    price_trends_chart = create_price_trends_chart(flights_df, destinations_df)
    price_dist_chart = create_price_distribution_boxplot(flights_df, destinations_df)
    weekly_heatmap_chart = create_weekly_heatmap(flights_df, destinations_df)

    price_trends_html = price_trends_chart.to_html(
        include_plotlyjs=False, div_id="price_trends_chart"
    )
    price_dist_html = price_dist_chart.to_html(
        include_plotlyjs=False, div_id="price_dist_chart"
    )
    weekly_heatmap_html = weekly_heatmap_chart.to_html(
        include_plotlyjs=False, div_id="weekly_heatmap_chart"
    )

    # Tab 5: Costs
    total_cost_chart = create_total_cost_chart(costs_df, destinations_df)
    cost_breakdown_chart = create_cost_breakdown_chart(costs_df, destinations_df)

    total_cost_html = total_cost_chart.to_html(
        include_plotlyjs=False, div_id="total_cost_chart"
    )
    cost_breakdown_html = cost_breakdown_chart.to_html(
        include_plotlyjs=False, div_id="cost_breakdown_chart"
    )

    # Tab 6: Comparison
    radar_chart = create_comparison_radar_chart(
        destinations_df, costs_df, flights_df, weather_df
    )
    radar_html = radar_chart.to_html(include_plotlyjs=False, div_id="radar_chart")
    comparison_table_html = create_comparison_table(
        destinations_df, costs_df, flights_df, weather_df
    )

    # Create complete HTML document
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multi-Dataset Overlay Dashboard - Places2Go</title>
    <script src="https://cdn.plot.ly/plotly-2.26.0.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: #f5f5f5;
        }}

        .header {{
            background: linear-gradient(135deg, #1f77b4 0%, #2ca02c 100%);
            color: white;
            padding: 30px 20px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .header h1 {{
            font-size: 32px;
            margin-bottom: 10px;
        }}

        .header p {{
            font-size: 16px;
            opacity: 0.9;
        }}

        .tab-navigation {{
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            padding: 0;
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            position: sticky;
            top: 0;
            z-index: 1000;
        }}

        .tab-button {{
            padding: 15px 25px;
            background: white;
            border: none;
            border-bottom: 3px solid transparent;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            color: #666;
            transition: all 0.3s ease;
        }}

        .tab-button:hover {{
            background: #f5f5f5;
            color: #333;
        }}

        .tab-button.active {{
            color: #1f77b4;
            border-bottom-color: #1f77b4;
            background: #f5f5f5;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px 20px;
        }}

        .tab-content {{
            display: none;
            animation: fadeIn 0.3s ease-in;
        }}

        .tab-content.active {{
            display: block;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .content-panel {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}

        h2 {{
            color: #333;
            margin-bottom: 20px;
            border-bottom: 2px solid #1f77b4;
            padding-bottom: 10px;
        }}

        h3 {{
            color: #555;
            margin: 25px 0 15px 0;
        }}

        /* Overview styles */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 25px 0;
        }}

        .stat-card {{
            background: linear-gradient(135deg, #f9f9f9 0%, #ffffff 100%);
            border-left: 4px solid #1f77b4;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: transform 0.2s ease;
        }}

        .stat-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}

        .stat-icon {{
            font-size: 32px;
            margin-bottom: 10px;
        }}

        .stat-label {{
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
            margin-bottom: 5px;
        }}

        .stat-value {{
            font-size: 28px;
            font-weight: bold;
            color: #1f77b4;
            margin-bottom: 5px;
        }}

        .stat-detail {{
            font-size: 13px;
            color: #888;
        }}

        .insights-panel {{
            background: #e7f3ff;
            border-left: 4px solid #1f77b4;
            border-radius: 5px;
            padding: 20px;
            margin-top: 25px;
        }}

        .insights-panel h3 {{
            margin-top: 0;
        }}

        .insights-panel ul {{
            list-style: none;
            padding: 0;
        }}

        .insights-panel li {{
            padding: 10px 0;
            border-bottom: 1px solid #d0e7f9;
        }}

        .insights-panel li:last-child {{
            border-bottom: none;
        }}

        /* Chart containers */
        .chart-full {{
            margin: 25px 0;
        }}

        .chart-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 25px;
            margin: 25px 0;
        }}

        /* Comparison table styles */
        .comparison-table-container {{
            margin: 25px 0;
            overflow-x: auto;
        }}

        .comparison-table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
        }}

        .comparison-table th {{
            background: #1f77b4;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 500;
        }}

        .comparison-table td {{
            padding: 12px;
            border-bottom: 1px solid #e0e0e0;
        }}

        .comparison-table tr:hover {{
            background: #f5f5f5;
        }}

        .dest-badge {{
            display: inline-block;
            color: white;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 13px;
            font-weight: 500;
        }}

        /* Info boxes */
        .info-box {{
            background: #e7f3ff;
            border-left: 4px solid #1f77b4;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }}

        /* Responsive design */
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 24px;
            }}

            .tab-button {{
                padding: 12px 15px;
                font-size: 12px;
            }}

            .stats-grid {{
                grid-template-columns: 1fr;
            }}

            .chart-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌍 Places2Go - Multi-Dataset Overlay Dashboard</h1>
        <p>Comprehensive destination analysis combining weather, flights, costs, and locations</p>
    </div>

    <div class="tab-navigation">
        <button class="tab-button active" onclick="openTab(event, 'overview')">
            📊 Overview
        </button>
        <button class="tab-button" onclick="openTab(event, 'map')">
            🗺️ Destinations Map
        </button>
        <button class="tab-button" onclick="openTab(event, 'weather')">
            🌤️ Weather Forecast
        </button>
        <button class="tab-button" onclick="openTab(event, 'flights')">
            ✈️ Flight Prices
        </button>
        <button class="tab-button" onclick="openTab(event, 'costs')">
            💰 Cost of Living
        </button>
        <button class="tab-button" onclick="openTab(event, 'comparison')">
            📊 Comparison
        </button>
    </div>

    <div class="container">
        <!-- Tab 1: Overview -->
        <div id="overview" class="tab-content active">
            <div class="content-panel">
                {overview_html}
            </div>
        </div>

        <!-- Tab 2: Destinations Map -->
        <div id="map" class="tab-content">
            <div class="content-panel">
                <h2>🗺️ Destinations Map</h2>
                <p>Interactive map showing all destinations with geographic context.</p>
                <div class="chart-full">
                    {map_html}
                </div>
                <div class="info-box">
                    <strong>💡 Tip:</strong> Click on markers to view destination details. Use zoom and pan controls to explore the map.
                </div>
            </div>
        </div>

        <!-- Tab 3: Weather Forecast -->
        <div id="weather" class="tab-content">
            <div class="content-panel">
                <h2>🌤️ Weather Forecast Dashboard</h2>
                <p>7-day weather forecasts for all destinations including temperature, rainfall, and UV index.</p>
                
                <h3>Temperature Trends</h3>
                <div class="chart-full">
                    {temp_html}
                </div>

                <div class="chart-grid">
                    <div>
                        <h3>Rainfall by Destination</h3>
                        {rainfall_html}
                    </div>
                    <div>
                        <h3>Comfort Index</h3>
                        {comfort_html}
                    </div>
                </div>

                <h3>UV Index Heatmap</h3>
                <div class="chart-full">
                    {uv_html}
                </div>

                <div class="info-box">
                    <strong>💡 Insights:</strong> Compare weather patterns across destinations. Hover over charts for detailed daily forecasts.
                </div>
            </div>
        </div>

        <!-- Tab 4: Flight Prices -->
        <div id="flights" class="tab-content">
            <div class="content-panel">
                <h2>✈️ Flight Prices Dashboard</h2>
                <p>Flight price trends, distributions, and patterns across departure dates.</p>
                
                <h3>Price Trends Over Time</h3>
                <div class="chart-full">
                    {price_trends_html}
                </div>

                <h3>Weekly Price Heatmap</h3>
                <div class="chart-full">
                    {weekly_heatmap_html}
                </div>

                <h3>Price Distribution by Destination</h3>
                <div class="chart-full">
                    {price_dist_html}
                </div>

                <div class="info-box">
                    <strong>💡 Insights:</strong> Identify best days to fly and compare prices across destinations. Look for patterns in the heatmap.
                </div>
            </div>
        </div>

        <!-- Tab 5: Cost of Living -->
        <div id="costs" class="tab-content">
            <div class="content-panel">
                <h2>💰 Cost of Living Dashboard</h2>
                <p>Monthly living costs and cost breakdowns for each destination.</p>
                
                <h3>Total Monthly Cost Comparison</h3>
                <div class="chart-full">
                    {total_cost_html}
                </div>

                <h3>Cost Breakdown by Category</h3>
                <div class="chart-full">
                    {cost_breakdown_html}
                </div>

                <div class="info-box">
                    <strong>💡 Insights:</strong> Compare affordability across destinations. Consider both fixed and variable costs.
                </div>
            </div>
        </div>

        <!-- Tab 6: Comparison View -->
        <div id="comparison" class="tab-content">
            <div class="content-panel">
                <h2>📊 Destination Comparison</h2>
                <p>Side-by-side comparison of all destinations across multiple dimensions.</p>
                
                <h3>Multi-Dimensional Comparison</h3>
                <div class="chart-full">
                    {radar_html}
                </div>

                {comparison_table_html}

                <div class="info-box">
                    <strong>💡 How to use:</strong> The radar chart shows normalized scores (0-100) across five key dimensions. 
                    Higher values are better for all metrics. Use the table for detailed numerical comparisons.
                </div>
            </div>
        </div>
    </div>

    <script>
        function openTab(evt, tabName) {{
            // Hide all tab contents
            var tabContents = document.getElementsByClassName("tab-content");
            for (var i = 0; i < tabContents.length; i++) {{
                tabContents[i].classList.remove("active");
            }}

            // Remove active class from all buttons
            var tabButtons = document.getElementsByClassName("tab-button");
            for (var i = 0; i < tabButtons.length; i++) {{
                tabButtons[i].classList.remove("active");
            }}

            // Show selected tab and mark button as active
            document.getElementById(tabName).classList.add("active");
            evt.currentTarget.classList.add("active");

            // Trigger Plotly relayout for responsive charts
            setTimeout(function() {{
                window.dispatchEvent(new Event('resize'));
            }}, 100);
        }}

        // Handle initial page load
        window.addEventListener('load', function() {{
            window.dispatchEvent(new Event('resize'));
        }});
    </script>
</body>
</html>
"""

    # Save HTML file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_content, encoding="utf-8")
    logger.info(f"Overlay dashboard saved to {output_path}")


def main() -> None:
    """Main function to generate overlay dashboard."""
    logger.info("=" * 60)
    logger.info("Starting Multi-Dataset Overlay Dashboard Generation")
    logger.info("=" * 60)

    try:
        project_root = Path(__file__).resolve().parents[2]
        output_path = project_root / ".build" / "visualizations" / "overlay_dashboard.html"

        create_overlay_dashboard(output_path)

        logger.info("=" * 60)
        logger.info("Overlay Dashboard Generation Completed Successfully")
        logger.info(f"Output: {output_path}")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Failed to generate overlay dashboard: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
