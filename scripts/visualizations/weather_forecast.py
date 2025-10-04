"""
weather_forecast.py
-------------------

This script creates an interactive weather forecast visualization dashboard
displaying 7-day forecasts for all destinations with multiple chart types.

The dashboard includes:
- Temperature trends (high/low/avg) for each destination
- Daily weather cards with icons and conditions
- Rainfall bar chart by destination
- UV index heatmap
- Weather conditions distribution pie chart
- Comfort index chart (temp/humidity/wind)

Output: `.build/visualizations/weather_forecast.html`
"""

import logging
import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.core.data_loader import DataLoader  # noqa: E402

# Configure logging
log_dir = Path(__file__).resolve().parents[2] / ".build" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_dir / "weather_forecast.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)

# Weather condition to emoji mapping
WEATHER_ICONS = {
    "Sunny": "☀️",
    "Clear": "🌤️",
    "Partly Cloudy": "⛅",
    "Cloudy": "☁️",
    "Light Rain": "🌦️",
    "Rain": "🌧️",
    "Heavy Rain": "⛈️",
    "Thunderstorm": "⛈️",
    "Snow": "🌨️",
    "Fog": "🌫️",
    "Windy": "💨",
}

# Color palette for destinations (consistent with map visualization)
DESTINATION_COLORS = {
    "Alicante": "#1f77b4",
    "Malaga": "#ff7f0e",
    "Majorca": "#2ca02c",
    "Faro": "#d62728",
    "Corfu": "#9467bd",
    "Rhodes": "#8c564b",
}


def hex_to_rgba(hex_color: str, alpha: float = 0.1) -> str:
    """Convert hex color to rgba string."""
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


def get_weather_icon(condition: str) -> str:
    """Get emoji icon for weather condition."""
    return WEATHER_ICONS.get(condition, "🌡️")


def create_temperature_trends_chart(
    df: pd.DataFrame, destinations_df: pd.DataFrame
) -> go.Figure:
    """
    Create multi-line temperature trends chart showing high/low/avg for each destination.

    Args:
        df: Weather data DataFrame
        destinations_df: Destinations DataFrame with names

    Returns:
        Plotly figure object
    """
    logger.info("Creating temperature trends chart")

    # Merge with destination names
    df_merged = df.merge(
        destinations_df[["destination_id", "name"]], on="destination_id"
    )

    fig = go.Figure()

    # Add traces for each destination
    for dest_name in df_merged["name"].unique():
        dest_data = df_merged[df_merged["name"] == dest_name].sort_values("date")
        color = DESTINATION_COLORS.get(dest_name, "#666666")

        # High temperature line
        fig.add_trace(
            go.Scatter(
                x=dest_data["date"],
                y=dest_data["temp_high_c"],
                name=f"{dest_name} (High)",
                line=dict(color=color, width=2, dash="solid"),
                mode="lines+markers",
                hovertemplate=f"<b>{dest_name}</b><br>"
                + "Date: %{x|%b %d}<br>"
                + "High: %{y}°C<extra></extra>",
            )
        )

        # Low temperature line
        fig.add_trace(
            go.Scatter(
                x=dest_data["date"],
                y=dest_data["temp_low_c"],
                name=f"{dest_name} (Low)",
                line=dict(color=color, width=1, dash="dash"),
                mode="lines+markers",
                fill="tonexty",
                fillcolor=hex_to_rgba(color, 0.1),
                hovertemplate=f"<b>{dest_name}</b><br>"
                + "Date: %{x|%b %d}<br>"
                + "Low: %{y}°C<extra></extra>",
            )
        )

        # Average temperature line
        fig.add_trace(
            go.Scatter(
                x=dest_data["date"],
                y=dest_data["temp_avg_c"],
                name=f"{dest_name} (Avg)",
                line=dict(color=color, width=2, dash="dot"),
                mode="lines+markers",
                hovertemplate=f"<b>{dest_name}</b><br>"
                + "Date: %{x|%b %d}<br>"
                + "Avg: %{y}°C<extra></extra>",
            )
        )

    fig.update_layout(
        title="Temperature Trends (7-Day Forecast)",
        xaxis_title="Date",
        yaxis_title="Temperature (°C)",
        hovermode="x unified",
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            font=dict(size=10),
        ),
        height=500,
    )

    return fig


def create_rainfall_chart(df: pd.DataFrame, destinations_df: pd.DataFrame) -> go.Figure:
    """
    Create bar chart showing daily rainfall by destination.

    Args:
        df: Weather data DataFrame
        destinations_df: Destinations DataFrame with names

    Returns:
        Plotly figure object
    """
    logger.info("Creating rainfall chart")

    # Merge with destination names
    df_merged = df.merge(
        destinations_df[["destination_id", "name"]], on="destination_id"
    )

    fig = go.Figure()

    # Add bar traces for each destination
    for dest_name in df_merged["name"].unique():
        dest_data = df_merged[df_merged["name"] == dest_name].sort_values("date")
        color = DESTINATION_COLORS.get(dest_name, "#666666")

        fig.add_trace(
            go.Bar(
                x=dest_data["date"],
                y=dest_data["rainfall_mm"],
                name=dest_name,
                marker_color=color,
                hovertemplate=f"<b>{dest_name}</b><br>"
                + "Date: %{x|%b %d}<br>"
                + "Rainfall: %{y} mm<extra></extra>",
            )
        )

    fig.update_layout(
        title="Daily Rainfall by Destination",
        xaxis_title="Date",
        yaxis_title="Rainfall (mm)",
        barmode="group",
        hovermode="x unified",
        height=400,
    )

    return fig


def create_uv_index_heatmap(
    df: pd.DataFrame, destinations_df: pd.DataFrame
) -> go.Figure:
    """
    Create UV index heatmap showing UV levels across dates and destinations.

    Args:
        df: Weather data DataFrame
        destinations_df: Destinations DataFrame with names

    Returns:
        Plotly figure object
    """
    logger.info("Creating UV index heatmap")

    # Merge with destination names
    df_merged = df.merge(
        destinations_df[["destination_id", "name"]], on="destination_id"
    )

    # Pivot data for heatmap
    heatmap_data = df_merged.pivot(index="name", columns="date", values="uv_index")

    # Format dates for display
    date_labels = [date.strftime("%b %d") for date in heatmap_data.columns]

    fig = go.Figure(
        data=go.Heatmap(
            z=heatmap_data.values,
            x=date_labels,
            y=heatmap_data.index,
            colorscale="YlOrRd",
            colorbar=dict(title="UV Index"),
            hovertemplate="<b>%{y}</b><br>"
            + "Date: %{x}<br>"
            + "UV Index: %{z}<extra></extra>",
        )
    )

    fig.update_layout(
        title="UV Index Heatmap",
        xaxis_title="Date",
        yaxis_title="Destination",
        height=300,
    )

    return fig


def create_conditions_pie_chart(
    df: pd.DataFrame, destinations_df: pd.DataFrame
) -> go.Figure:
    """
    Create pie chart showing distribution of weather conditions.

    Args:
        df: Weather data DataFrame
        destinations_df: Destinations DataFrame with names

    Returns:
        Plotly figure object
    """
    logger.info("Creating conditions distribution pie chart")

    # Count conditions
    conditions_count = df["conditions"].value_counts()

    # Add emojis to labels
    labels = [f"{get_weather_icon(cond)} {cond}" for cond in conditions_count.index]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=conditions_count.values,
                hovertemplate="<b>%{label}</b><br>"
                + "Count: %{value}<br>"
                + "Percentage: %{percent}<extra></extra>",
            )
        ]
    )

    fig.update_layout(title="Weather Conditions Distribution", height=400)

    return fig


def create_comfort_index_chart(
    df: pd.DataFrame, destinations_df: pd.DataFrame
) -> go.Figure:
    """
    Create scatter plot showing comfort index based on temp/humidity/wind.

    Args:
        df: Weather data DataFrame
        destinations_df: Destinations DataFrame with names

    Returns:
        Plotly figure object
    """
    logger.info("Creating comfort index chart")

    # Merge with destination names
    df_merged = df.merge(
        destinations_df[["destination_id", "name"]], on="destination_id"
    )

    # Calculate simple comfort score (0-100)
    # Higher is better: moderate temp, low humidity, low wind
    df_merged["comfort_score"] = (
        100
        - abs(df_merged["temp_avg_c"] - 24) * 2  # Ideal temp ~24°C
        - (df_merged["humidity_percent"] - 50) / 2  # Ideal humidity ~50%
        - df_merged["wind_speed_kmh"]  # Lower wind is better
    )

    fig = go.Figure()

    # Add scatter trace for each destination
    for dest_name in df_merged["name"].unique():
        dest_data = df_merged[df_merged["name"] == dest_name].sort_values("date")

        fig.add_trace(
            go.Scatter(
                x=dest_data["temp_avg_c"],
                y=dest_data["humidity_percent"],
                name=dest_name,
                mode="markers",
                marker=dict(
                    size=dest_data["wind_speed_kmh"],
                    color=dest_data["comfort_score"],
                    colorscale="RdYlGn",
                    showscale=True,
                    colorbar=dict(title="Comfort<br>Score", x=1.15),
                    line=dict(width=1, color="white"),
                ),
                text=dest_data["date"].dt.strftime("%b %d"),
                hovertemplate=f"<b>{dest_name}</b><br>"
                + "Date: %{text}<br>"
                + "Temp: %{x}°C<br>"
                + "Humidity: %{y}%<br>"
                + "Wind: %{marker.size} km/h<br>"
                + "Comfort: %{marker.color:.1f}<extra></extra>",
            )
        )

    fig.update_layout(
        title="Comfort Index (Temp vs Humidity, marker size = wind speed)",
        xaxis_title="Average Temperature (°C)",
        yaxis_title="Humidity (%)",
        height=450,
    )

    return fig


def create_weather_cards_html(df: pd.DataFrame, destinations_df: pd.DataFrame) -> str:
    """
    Create HTML for daily weather cards grid.

    Args:
        df: Weather data DataFrame
        destinations_df: Destinations DataFrame with names

    Returns:
        HTML string
    """
    logger.info("Creating weather cards HTML")

    # Merge with destination names
    df_merged = df.merge(
        destinations_df[["destination_id", "name"]], on="destination_id"
    ).sort_values(["date", "name"])

    cards_html = """
    <div style="margin: 20px 0;">
        <h2>7-Day Weather Forecast</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px;">
    """

    for _, row in df_merged.iterrows():
        icon = get_weather_icon(row["conditions"])
        color = DESTINATION_COLORS.get(row["name"], "#666666")
        date_str = row["date"].strftime("%b %d")

        card = f"""
        <div style="border: 2px solid {color}; border-radius: 8px; padding: 10px; background: #f9f9f9;">
            <div style="font-weight: bold; color: {color}; font-size: 14px;">{row['name']}</div>
            <div style="font-size: 12px; color: #666;">{date_str}</div>
            <div style="font-size: 36px; text-align: center; margin: 5px 0;">{icon}</div>
            <div style="font-size: 12px; text-align: center; color: #333;">{row['conditions']}</div>
            <div style="margin-top: 8px; font-size: 13px;">
                <div>🌡️ {row['temp_high_c']:.0f}°C / {row['temp_low_c']:.0f}°C</div>
                <div>💧 {row['humidity_percent']}%</div>
                <div>🌧️ {row['rainfall_mm']} mm</div>
                <div>☀️ UV {row['uv_index']}</div>
            </div>
        </div>
        """
        cards_html += card

    cards_html += """
        </div>
    </div>
    """

    return cards_html


def create_weather_dashboard(
    output_path: Path, df: pd.DataFrame, destinations_df: pd.DataFrame
) -> None:
    """
    Create complete weather forecast dashboard HTML file.

    Args:
        output_path: Path to save HTML file
        df: Weather data DataFrame
        destinations_df: Destinations DataFrame
    """
    logger.info("Creating weather forecast dashboard")

    # Create all charts
    temp_chart = create_temperature_trends_chart(df, destinations_df)
    rainfall_chart = create_rainfall_chart(df, destinations_df)
    uv_heatmap = create_uv_index_heatmap(df, destinations_df)
    conditions_pie = create_conditions_pie_chart(df, destinations_df)
    comfort_chart = create_comfort_index_chart(df, destinations_df)
    weather_cards = create_weather_cards_html(df, destinations_df)

    # Convert charts to HTML
    temp_html = temp_chart.to_html(include_plotlyjs=False, div_id="temp_chart")
    rainfall_html = rainfall_chart.to_html(
        include_plotlyjs=False, div_id="rainfall_chart"
    )
    uv_html = uv_heatmap.to_html(include_plotlyjs=False, div_id="uv_heatmap")
    conditions_html = conditions_pie.to_html(
        include_plotlyjs=False, div_id="conditions_pie"
    )
    comfort_html = comfort_chart.to_html(include_plotlyjs=False, div_id="comfort_chart")

    # Create complete HTML document
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Forecast Dashboard - Places2Go</title>
    <script src="https://cdn.plot.ly/plotly-2.26.0.min.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #1f77b4;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #555;
            margin-top: 30px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: #f9f9f9;
            border-left: 4px solid #1f77b4;
            padding: 15px;
            border-radius: 5px;
        }}
        .stat-label {{
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
        }}
        .stat-value {{
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-top: 5px;
        }}
        .chart-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 20px 0;
        }}
        .chart-full {{
            grid-column: 1 / -1;
        }}
        .info-box {{
            background: #e7f3ff;
            border-left: 4px solid #1f77b4;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        @media (max-width: 768px) {{
            .chart-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌤️ Weather Forecast Dashboard</h1>

        <div class="info-box">
            <strong>📊 Data Overview:</strong> 7-day weather forecast for 6 destinations (Oct 5-11, 2025) •
            {len(df)} total forecast records • All data from demo1 source
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-label">Average Temperature</div>
                <div class="stat-value">{df['temp_avg_c'].mean():.1f}°C</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Rainfall</div>
                <div class="stat-value">{df['rainfall_mm'].sum():.1f} mm</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Avg Humidity</div>
                <div class="stat-value">{df['humidity_percent'].mean():.0f}%</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Avg UV Index</div>
                <div class="stat-value">{df['uv_index'].mean():.1f}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Avg Sunshine</div>
                <div class="stat-value">{df['sunshine_hours'].mean():.1f} hrs</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Avg Wind Speed</div>
                <div class="stat-value">{df['wind_speed_kmh'].mean():.1f} km/h</div>
            </div>
        </div>

        <div class="chart-full">
            {temp_html}
        </div>

        {weather_cards}

        <div class="chart-grid">
            <div>
                {rainfall_html}
            </div>
            <div>
                {conditions_html}
            </div>
        </div>

        <div class="chart-full">
            {uv_html}
        </div>

        <div class="chart-full">
            {comfort_html}
        </div>

        <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px;">
            <p><strong>About this dashboard:</strong> This interactive weather forecast dashboard displays 7-day forecasts
            for all destinations with multiple visualization types. Use hover interactions to explore detailed metrics.
            All forecast data is from the demo1 data source.</p>
            <p><strong>Legend:</strong> Each destination is color-coded consistently across all charts.
            Click legend items to show/hide specific destinations.</p>
        </div>
    </div>
</body>
</html>
    """

    # Write to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_content)
    logger.info(f"Weather forecast dashboard saved to {output_path}")


def main() -> None:
    """Main function to generate weather forecast dashboard."""
    logger.info("Starting weather forecast dashboard generation")

    # Initialize data loader
    loader = DataLoader()

    # Load data
    logger.info("Loading weather data")
    weather_df = loader.load_weather(data_source="demo1", forecast_only=True)
    destinations_df = loader.load_destinations()

    logger.info(
        f"Loaded {len(weather_df)} weather records for {len(destinations_df)} destinations"
    )

    # Create output directory
    project_root = Path(__file__).resolve().parents[2]
    output_dir = project_root / ".build" / "visualizations"
    output_path = output_dir / "weather_forecast.html"

    # Create dashboard
    create_weather_dashboard(output_path, weather_df, destinations_df)

    logger.info("Weather forecast dashboard generation completed successfully")


if __name__ == "__main__":
    main()
