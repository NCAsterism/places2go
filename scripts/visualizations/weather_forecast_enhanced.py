"""
weather_forecast_enhanced.py
----------------------------

Enhanced weather forecast visualization with user preferences support.

This is a demonstration of Phase 4C user features integrated into the
weather forecast visualization. It includes:
- User preferences panel (currency, temperature unit, theme)
- Favorites management
- URL sharing
- Temperature unit conversion
- Dark/light theme support

Output: `.build/visualizations/weather_forecast_enhanced.html`
"""

import logging
import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.core.data_loader import DataLoader  # noqa: E402
from scripts.core.preferences_panel import inject_preferences_into_html  # noqa: E402

# Configure logging
log_dir = Path(__file__).resolve().parents[2] / ".build" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_dir / "weather_forecast_enhanced.log"),
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
    "Rainy": "🌧️",
    "Stormy": "⛈️",
    "Snowy": "❄️",
    "Foggy": "🌫️",
    "Windy": "💨",
}


def get_weather_icon(condition: str) -> str:
    """Return emoji for weather condition."""
    return WEATHER_ICONS.get(condition, "🌤️")


def create_temperature_chart(df: pd.DataFrame) -> go.Figure:
    """Create temperature trends chart with both C and F scales."""
    fig = go.Figure()

    # Group by destination
    for dest_name in df["name"].unique():
        dest_data = df[df["name"] == dest_name].sort_values("date")

        # Add temperature traces
        fig.add_trace(
            go.Scatter(
                x=dest_data["date"],
                y=dest_data["temp_high_c"],
                name=f"{dest_name} (High)",
                mode="lines+markers",
                line=dict(dash="solid"),
                customdata=dest_data[["destination_id"]],
            )
        )

    fig.update_layout(
        title="7-Day Temperature Forecast",
        xaxis_title="Date",
        yaxis_title="Temperature",
        hovermode="x unified",
        height=400,
        showlegend=True,
    )

    return fig


def create_simple_html(df: pd.DataFrame, output_path: Path) -> None:
    """Create simplified HTML with preferences support."""

    # Create temperature chart
    temp_fig = create_temperature_chart(df)
    temp_html = temp_fig.to_html(include_plotlyjs="cdn", div_id="temp-chart")

    # Calculate stats
    avg_temp = df["temp_avg_c"].mean()
    total_rainfall = df["rainfall_mm"].sum()
    avg_humidity = df["humidity_percent"].mean()

    # Get unique destinations for favorites
    destinations = df[["destination_id", "name"]].drop_duplicates()
    destination_cards = ""
    for _, row in destinations.iterrows():
        destination_cards += f"""
        <div class="destination-card" data-destination-id="{row['destination_id']}">
            <span class="favorite-star" 
                  onclick="toggleFavorite('{row['destination_id']}', '{row['name']}')"
                  title="Add to favorites">
                ★
            </span>
            <h3>{row['name']}</h3>
        </div>
        """

    # Create basic HTML without preferences first
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Forecast - Places2Go</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
            transition: background 0.3s, color 0.3s;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            margin-bottom: 10px;
        }}
        .subtitle {{
            color: #666;
            margin-bottom: 30px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
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
        .destinations-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 30px 0;
        }}
        .destination-card {{
            background: #f9f9f9;
            padding: 20px;
            border-radius: 8px;
            position: relative;
            transition: transform 0.2s;
        }}
        .destination-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .destination-card h3 {{
            margin: 0;
            font-size: 18px;
            color: #333;
        }}
        .destination-card .favorite-star {{
            position: absolute;
            top: 10px;
            right: 10px;
        }}
        .info-box {{
            background: #e7f3ff;
            border-left: 4px solid #1f77b4;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .feature-badge {{
            display: inline-block;
            background: #28a745;
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
            margin-left: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌤️ Weather Forecast Dashboard <span class="feature-badge">Enhanced with Preferences</span></h1>
        <p class="subtitle">Interactive 7-day forecast with user preferences support</p>

        <div class="info-box">
            <strong>✨ New Features:</strong> 
            Click the ⚙️ button (bottom right) to customize preferences • 
            Click ⭐ on destinations to add favorites • 
            Use 📤 to share your view • 
            Try dark theme!
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-label">Average Temperature</div>
                <div class="stat-value" id="stat-avg-temp">{avg_temp:.1f}°C</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Total Rainfall</div>
                <div class="stat-value">{total_rainfall:.1f} mm</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Avg Humidity</div>
                <div class="stat-value">{avg_humidity:.0f}%</div>
            </div>
        </div>

        <h2>Destinations</h2>
        <div class="destinations-grid">
            {destination_cards}
        </div>

        <h2>Temperature Forecast</h2>
        <div id="temp-chart">
            {temp_html}
        </div>

        <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px;">
            <p><strong>About this enhanced dashboard:</strong> This is a demonstration of Phase 4C user features
            integrated with the weather forecast. All preferences are stored in your browser's localStorage.</p>
            <p><strong>Features:</strong> Temperature unit conversion, theme switching, favorites management, 
            URL sharing with state preservation.</p>
        </div>
    </div>

    <script>
        // Custom visualization state management
        function getCurrentState() {{
            return {{
                preferences: PreferencesManager.load(),
                destinations: FavoritesManager.getIds(),
                filters: {{}}
            }};
        }}

        function applyPreferencesToData(prefs) {{
            // Update temperature display
            const avgTempElement = document.getElementById('stat-avg-temp');
            if (avgTempElement) {{
                const currentTemp = {avg_temp:.1f}; // Celsius value
                const convertedTemp = prefs.temp_unit === 'C' 
                    ? currentTemp 
                    : PreferencesManager.convertTemperature(currentTemp, 'F');
                avgTempElement.textContent = PreferencesManager.formatTemperature(
                    convertedTemp, 
                    prefs.temp_unit
                );
            }}

            // Update chart axis labels
            const tempChart = document.getElementById('temp-chart');
            if (tempChart && Plotly) {{
                Plotly.relayout('temp-chart', {{
                    'yaxis.title': prefs.temp_unit === 'C' 
                        ? 'Temperature (°C)' 
                        : 'Temperature (°F)'
                }});
            }}
        }}

        function applyStateToVisualization(state) {{
            // Apply filters or other state from URL
            console.log('Applying state from URL:', state);
        }}

        // Initialize favorite stars on page load
        document.addEventListener('DOMContentLoaded', function() {{
            const favorites = FavoritesManager.getIds();
            favorites.forEach(destId => {{
                const star = document.querySelector(`[data-destination-id="${{destId}}"] .favorite-star`);
                if (star) {{
                    star.classList.add('favorited');
                }}
            }});
        }});
    </script>
</body>
</html>
    """

    # Inject preferences panel
    html_content = inject_preferences_into_html(html_content)

    # Write to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_content, encoding="utf-8")
    logger.info(f"Enhanced weather forecast dashboard saved to {output_path}")


def main() -> None:
    """Main entry point."""
    logger.info("Starting enhanced weather forecast generation")

    # Load data
    loader = DataLoader()
    destinations = loader.load_destinations()
    weather = loader.load_weather(data_source="demo1", forecast_only=True)

    # Merge with destination names
    df = weather.merge(destinations[["destination_id", "name"]], on="destination_id")

    # Generate output
    project_root = Path(__file__).resolve().parents[2]
    output_path = project_root / ".build" / "visualizations" / "weather_forecast_enhanced.html"

    create_simple_html(df, output_path)
    logger.info("Enhanced weather forecast generation completed")


if __name__ == "__main__":
    main()
