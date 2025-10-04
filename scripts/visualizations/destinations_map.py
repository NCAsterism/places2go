"""
destinations_map.py
-------------------

This script creates an interactive map visualization displaying all destinations
with detailed information overlays, color-coding by region, and summary statistics.

The map includes:
- All 6 destinations plotted with correct coordinates
- Hover details (name, country, airports, coordinates)
- Click for full details panel
- Color-coding by region
- Summary statistics panel
- Filtering by country/region

Output: `.build/visualizations/destinations_map.html`
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
        logging.FileHandler(log_dir / "destinations_map.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)

# Color palette for regions
REGION_COLORS = {
    "Costa Blanca": "#1f77b4",  # Blue
    "Costa del Sol": "#ff7f0e",  # Orange
    "Balearic Islands": "#2ca02c",  # Green
    "Algarve": "#d62728",  # Red
    "Ionian Islands": "#9467bd",  # Purple
    "Dodecanese": "#8c564b",  # Brown
}


def create_interactive_map(df: pd.DataFrame) -> go.Figure:
    """
    Create interactive map with all destinations plotted.

    Args:
        df: Destinations DataFrame with coordinates and details

    Returns:
        Plotly figure object with scatter_geo map
    """
    logger.info("Creating interactive destinations map")

    # Create hover text with detailed information
    hover_text = []
    for _, row in df.iterrows():
        text = (
            f"<b>{row['name']}</b><br>"
            f"Country: {row['country']}<br>"
            f"Region: {row['region']}<br>"
            f"Airport: {row['airport_name']} ({row['airport_code']})<br>"
            f"Coordinates: {row['latitude']:.4f}°N, "
            f"{abs(row['longitude']):.4f}°{'E' if row['longitude'] >= 0 else 'W'}<br>"
            f"Timezone: {row['timezone']}<br>"
            f"Origin: {row['origin_airport']}"
        )
        hover_text.append(text)

    # Create the figure
    fig = go.Figure()

    # Group by region for color-coding
    for region in df["region"].unique():
        region_df = df[df["region"] == region]
        color = REGION_COLORS.get(region, "#333333")

        fig.add_trace(
            go.Scattergeo(
                lon=region_df["longitude"],
                lat=region_df["latitude"],
                text=region_df["name"],
                customdata=region_df[
                    [
                        "country",
                        "region",
                        "airport_name",
                        "airport_code",
                        "timezone",
                        "origin_airport",
                    ]
                ].values,
                hovertemplate="<b>%{text}</b><br>"
                + "Country: %{customdata[0]}<br>"
                + "Region: %{customdata[1]}<br>"
                + "Airport: %{customdata[2]} (%{customdata[3]})<br>"
                + "Coordinates: %{lat:.4f}°N, %{lon:.4f}°E<br>"
                + "Timezone: %{customdata[4]}<br>"
                + "Origin: %{customdata[5]}"
                + "<extra></extra>",
                mode="markers",
                marker=dict(
                    size=15,
                    color=color,
                    line=dict(width=2, color="white"),
                    symbol="circle",
                ),
                name=region,
                showlegend=True,
            )
        )

    # Update layout for better map appearance
    fig.update_layout(
        title={
            "text": "🗺️ Destinations Map - Places2Go",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 24, "color": "#333"},
        },
        geo=dict(
            scope="europe",
            projection_type="natural earth",
            showland=True,
            landcolor="rgb(243, 243, 243)",
            coastlinecolor="rgb(204, 204, 204)",
            countrycolor="rgb(204, 204, 204)",
            showlakes=True,
            lakecolor="rgb(220, 240, 255)",
            showcountries=True,
            resolution=50,
            lonaxis=dict(range=[-10, 30]),
            lataxis=dict(range=[34, 42]),
        ),
        height=700,
        margin=dict(l=0, r=0, t=60, b=0),
        legend=dict(
            title=dict(text="Region", font=dict(size=14, color="#333")),
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="#ccc",
            borderwidth=1,
        ),
        hovermode="closest",
    )

    return fig


def create_summary_stats_html(df: pd.DataFrame) -> str:
    """
    Create HTML for summary statistics panel.

    Args:
        df: Destinations DataFrame

    Returns:
        HTML string with summary statistics
    """
    logger.info("Creating summary statistics panel")

    # Count by country
    country_counts = df["country"].value_counts()

    # Count by region
    region_counts = df["region"].value_counts()

    # Build country stats HTML
    country_html = ""
    for country, count in country_counts.items():
        country_html += f"""
        <div class="stat-item">
            <span class="stat-country">{country}</span>
            <span class="stat-count">{count}</span>
        </div>
        """

    # Build region stats HTML
    region_html = ""
    for region, count in region_counts.items():
        color = REGION_COLORS.get(region, "#333333")
        region_html += f"""
        <div class="stat-item">
            <span class="stat-region">
                <span class="region-color" style="background-color: {color};"></span>
                {region}
            </span>
            <span class="stat-count">{count}</span>
        </div>
        """

    stats_html = f"""
    <div class="summary-stats">
        <div class="stat-section">
            <h3>📍 By Country</h3>
            {country_html}
        </div>
        <div class="stat-section">
            <h3>🌍 By Region</h3>
            {region_html}
        </div>
    </div>
    """

    return stats_html


def create_destination_details_html(df: pd.DataFrame) -> str:
    """
    Create HTML for detailed destination information cards.

    Args:
        df: Destinations DataFrame

    Returns:
        HTML string with destination cards
    """
    logger.info("Creating destination details cards")

    cards_html = '<div class="destination-cards">'

    for _, row in df.iterrows():
        color = REGION_COLORS.get(row["region"], "#333333")
        cards_html += f"""
        <div class="destination-card" style="border-left-color: {color};">
            <h4>{row['name']}</h4>
            <div class="card-details">
                <p><strong>🌍 Country:</strong> {row['country']} ({row['country_code']})</p>
                <p><strong>📍 Region:</strong> {row['region']}</p>
                <p><strong>✈️ Airport:</strong> {row['airport_name']} ({row['airport_code']})</p>
                <p><strong>📌 Coordinates:</strong> {row['latitude']:.4f}°N, {row['longitude']:.4f}°E</p>
                <p><strong>🕐 Timezone:</strong> {row['timezone']}</p>
                <p><strong>🛫 From:</strong> {row['origin_airport']}</p>
            </div>
        </div>
        """

    cards_html += "</div>"
    return cards_html


def create_destinations_map_html(output_path: Path, df: pd.DataFrame) -> None:
    """
    Create complete destinations map HTML file.

    Args:
        output_path: Path to save HTML file
        df: Destinations DataFrame
    """
    logger.info("Creating destinations map HTML")

    # Create the map
    map_fig = create_interactive_map(df)

    # Convert to HTML
    map_html = map_fig.to_html(include_plotlyjs=False, div_id="destinations_map")

    # Create summary stats
    stats_html = create_summary_stats_html(df)

    # Create destination cards
    cards_html = create_destination_details_html(df)

    # Create complete HTML document
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Destinations Map - Places2Go</title>
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
            margin-bottom: 20px;
        }}
        h2 {{
            color: #555;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        h3 {{
            color: #666;
            font-size: 16px;
            margin-bottom: 10px;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 5px;
        }}
        .info-box {{
            background: #e7f3ff;
            border-left: 4px solid #1f77b4;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .stats-overview {{
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
        .summary-stats {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin: 30px 0;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 5px;
        }}
        .stat-section {{
            padding: 15px;
        }}
        .stat-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            margin: 5px 0;
            background: white;
            border-radius: 3px;
            border-left: 3px solid #ddd;
        }}
        .stat-country, .stat-region {{
            font-weight: 500;
            color: #333;
        }}
        .stat-region {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .region-color {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            border: 2px solid white;
            box-shadow: 0 0 3px rgba(0,0,0,0.3);
        }}
        .stat-count {{
            font-weight: bold;
            color: #1f77b4;
            font-size: 18px;
        }}
        .destination-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .destination-card {{
            background: white;
            border: 1px solid #e0e0e0;
            border-left: 4px solid #1f77b4;
            border-radius: 5px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            transition: box-shadow 0.3s ease;
        }}
        .destination-card:hover {{
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}
        .destination-card h4 {{
            margin: 0 0 15px 0;
            color: #333;
            font-size: 20px;
            border-bottom: 2px solid #f0f0f0;
            padding-bottom: 10px;
        }}
        .card-details p {{
            margin: 8px 0;
            color: #555;
            font-size: 14px;
            line-height: 1.6;
        }}
        .card-details strong {{
            color: #333;
        }}
        @media (max-width: 768px) {{
            .summary-stats {{
                grid-template-columns: 1fr;
            }}
            .destination-cards {{
                grid-template-columns: 1fr;
            }}
            .stats-overview {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🗺️ Destinations Map</h1>

        <div class="info-box">
            <strong>📊 Data Overview:</strong> Interactive map showing all {len(df)} destinations with detailed information •
            Hover over markers for quick details • Click legend items to filter by region •
            Zoom and pan to explore the map
        </div>

        <div class="stats-overview">
            <div class="stat-card">
                <div class="stat-label">Total Destinations</div>
                <div class="stat-value">{len(df)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Countries</div>
                <div class="stat-value">{df['country'].nunique()}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Regions</div>
                <div class="stat-value">{df['region'].nunique()}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Airports</div>
                <div class="stat-value">{df['airport_code'].nunique()}</div>
            </div>
        </div>

        <div class="chart-full">
            {map_html}
        </div>

        <h2>📈 Summary Statistics</h2>
        {stats_html}

        <h2>📋 Destination Details</h2>
        {cards_html}

        <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px;">
            <p><strong>About this map:</strong> This interactive map displays all
            travel destinations with their locations, airport information, and
            regional groupings. Each destination is color-coded by region for
            easy identification.</p>
            <p><strong>How to use:</strong> Hover over markers for quick
            information. Click legend items to show/hide specific regions.
            Use zoom and pan controls to explore the map. Each destination card
            below provides complete details.</p>
            <p><strong>Data Source:</strong> Destinations data from
            data/destinations/destinations.csv</p>
        </div>
    </div>
</body>
</html>
    """

    # Write to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_content, encoding="utf-8")
    logger.info(f"Destinations map saved to {output_path}")


def main() -> None:
    """Main function to generate destinations map."""
    logger.info("Starting destinations map generation")

    # Initialize data loader
    loader = DataLoader()

    # Load destinations data
    logger.info("Loading destinations data")
    destinations_df = loader.load_destinations()

    logger.info(f"Loaded {len(destinations_df)} destinations")

    # Create output directory
    project_root = Path(__file__).resolve().parents[2]
    output_dir = project_root / ".build" / "visualizations"
    output_path = output_dir / "destinations_map.html"

    # Create map
    create_destinations_map_html(output_path, destinations_df)

    logger.info("Destinations map generation completed successfully")


if __name__ == "__main__":
    main()
