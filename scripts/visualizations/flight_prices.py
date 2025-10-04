"""
flight_prices.py
----------------

This script creates an interactive flight prices time-series visualization dashboard
displaying price trends over time with filtering and analysis features.

The dashboard includes:
- Price trends multi-line chart showing prices over departure dates
- Price distribution box plot by destination
- Airline comparison grouped bar chart
- Duration vs cost scatter plot
- Weekly calendar heatmap of prices

Output: `.build/visualizations/flight_prices.html`
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
        logging.FileHandler(log_dir / "flight_prices.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)

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


def create_price_trends_chart(
    df: pd.DataFrame, destinations_df: pd.DataFrame
) -> go.Figure:
    """
    Create multi-line chart showing flight prices over departure dates.

    Args:
        df: Flight data DataFrame
        destinations_df: Destinations DataFrame with names

    Returns:
        Plotly figure object
    """
    logger.info("Creating price trends chart")

    # Merge with destination names
    df_merged = df.merge(
        destinations_df[["destination_id", "name"]], on="destination_id"
    )

    fig = go.Figure()

    # Add traces for each destination
    for dest_name in df_merged["name"].unique():
        dest_data = df_merged[df_merged["name"] == dest_name].sort_values(
            "departure_date"
        )
        color = DESTINATION_COLORS.get(dest_name, "#666666")

        # Separate direct and indirect flights
        direct_data = dest_data[dest_data["direct_flight"]]
        indirect_data = dest_data[~dest_data["direct_flight"]]

        if not direct_data.empty:
            fig.add_trace(
                go.Scatter(
                    x=direct_data["departure_date"],
                    y=direct_data["price"],
                    name=f"{dest_name} (Direct)",
                    line=dict(color=color, width=2),
                    mode="lines+markers",
                    marker=dict(size=8),
                    customdata=direct_data[["airline", "flight_duration_hours"]],
                    hovertemplate="<b>%{fullData.name}</b><br>"
                    + "Departure: %{x|%b %d}<br>"
                    + "Price: £%{y:.0f}<br>"
                    + "Airline: %{customdata[0]}<br>"
                    + "Duration: %{customdata[1]:.1f}h<extra></extra>",
                )
            )

        if not indirect_data.empty:
            fig.add_trace(
                go.Scatter(
                    x=indirect_data["departure_date"],
                    y=indirect_data["price"],
                    name=f"{dest_name} (Indirect)",
                    line=dict(color=color, width=2, dash="dash"),
                    mode="lines+markers",
                    marker=dict(size=6, symbol="diamond"),
                    customdata=indirect_data[["airline", "flight_duration_hours"]],
                    hovertemplate="<b>%{fullData.name}</b><br>"
                    + "Departure: %{x|%b %d}<br>"
                    + "Price: £%{y:.0f}<br>"
                    + "Airline: %{customdata[0]}<br>"
                    + "Duration: %{customdata[1]:.1f}h<extra></extra>",
                )
            )

    fig.update_layout(
        title="Flight Price Trends Over Time",
        xaxis_title="Departure Date",
        yaxis_title="Price (GBP)",
        hovermode="closest",
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            font=dict(size=10),
        ),
        height=500,
        xaxis=dict(
            rangeslider=dict(visible=True),
            type="date",
        ),
    )

    return fig


def create_price_distribution_boxplot(
    df: pd.DataFrame, destinations_df: pd.DataFrame
) -> go.Figure:
    """
    Create box plot showing price distribution by destination.

    Args:
        df: Flight data DataFrame
        destinations_df: Destinations DataFrame with names

    Returns:
        Plotly figure object
    """
    logger.info("Creating price distribution box plot")

    # Merge with destination names
    df_merged = df.merge(
        destinations_df[["destination_id", "name"]], on="destination_id"
    )

    fig = go.Figure()

    for dest_name in sorted(df_merged["name"].unique()):
        dest_data = df_merged[df_merged["name"] == dest_name]
        color = DESTINATION_COLORS.get(dest_name, "#666666")

        fig.add_trace(
            go.Box(
                y=dest_data["price"],
                name=dest_name,
                marker_color=color,
                boxmean="sd",
                hovertemplate="<b>%{fullData.name}</b><br>"
                + "Price: £%{y:.0f}<extra></extra>",
            )
        )

    fig.update_layout(
        title="Price Distribution by Destination",
        yaxis_title="Price (GBP)",
        xaxis_title="Destination",
        showlegend=False,
        height=400,
    )

    return fig


def create_airline_comparison_chart(
    df: pd.DataFrame, destinations_df: pd.DataFrame
) -> go.Figure:
    """
    Create grouped bar chart comparing average prices by airline.

    Args:
        df: Flight data DataFrame
        destinations_df: Destinations DataFrame with names

    Returns:
        Plotly figure object
    """
    logger.info("Creating airline comparison chart")

    # Merge with destination names
    df_merged = df.merge(
        destinations_df[["destination_id", "name"]], on="destination_id"
    )

    # Calculate average price by airline and destination
    airline_avg = df_merged.groupby(["airline", "name"])["price"].mean().reset_index()

    fig = go.Figure()

    for airline in sorted(airline_avg["airline"].unique()):
        airline_data = airline_avg[airline_avg["airline"] == airline]
        fig.add_trace(
            go.Bar(
                x=airline_data["name"],
                y=airline_data["price"],
                name=airline,
                hovertemplate="<b>%{fullData.name}</b><br>"
                + "%{x}<br>"
                + "Avg Price: £%{y:.0f}<extra></extra>",
            )
        )

    fig.update_layout(
        title="Average Price by Airline and Destination",
        xaxis_title="Destination",
        yaxis_title="Average Price (GBP)",
        barmode="group",
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
    )

    return fig


def create_duration_vs_cost_scatter(
    df: pd.DataFrame, destinations_df: pd.DataFrame
) -> go.Figure:
    """
    Create scatter plot showing correlation between duration and cost.

    Args:
        df: Flight data DataFrame
        destinations_df: Destinations DataFrame with names

    Returns:
        Plotly figure object
    """
    logger.info("Creating duration vs cost scatter plot")

    # Merge with destination names
    df_merged = df.merge(
        destinations_df[["destination_id", "name"]], on="destination_id"
    )

    fig = go.Figure()

    for dest_name in df_merged["name"].unique():
        dest_data = df_merged[df_merged["name"] == dest_name]
        color = DESTINATION_COLORS.get(dest_name, "#666666")

        fig.add_trace(
            go.Scatter(
                x=dest_data["flight_duration_hours"],
                y=dest_data["price"],
                name=dest_name,
                mode="markers",
                marker=dict(
                    size=10,
                    color=color,
                    symbol=[
                        "circle" if d else "diamond" for d in dest_data["direct_flight"]
                    ],
                ),
                customdata=dest_data[["airline", "direct_flight"]],
                hovertemplate="<b>%{name}</b><br>"
                + "Duration: %{x:.1f}h<br>"
                + "Price: £%{y:.0f}<br>"
                + "Airline: %{customdata[0]}<br>"
                + "Direct: %{customdata[1]}<extra></extra>",
            )
        )

    fig.update_layout(
        title="Flight Duration vs Cost",
        xaxis_title="Duration (hours)",
        yaxis_title="Price (GBP)",
        height=400,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            font=dict(size=10),
        ),
    )

    return fig


def create_weekly_heatmap(df: pd.DataFrame, destinations_df: pd.DataFrame) -> go.Figure:
    """
    Create calendar heatmap showing prices by day of week and destination.

    Args:
        df: Flight data DataFrame
        destinations_df: Destinations DataFrame with names

    Returns:
        Plotly figure object
    """
    logger.info("Creating weekly calendar heatmap")

    # Merge with destination names
    df_merged = df.merge(
        destinations_df[["destination_id", "name"]], on="destination_id"
    )

    # Calculate average price by destination and departure date
    heatmap_data = (
        df_merged.groupby(["name", "departure_date"])["price"].mean().reset_index()
    )

    # Pivot for heatmap
    pivot_data = heatmap_data.pivot(
        index="name", columns="departure_date", values="price"
    )

    # Format column headers as dates
    pivot_data.columns = [col.strftime("%b %d") for col in pivot_data.columns]

    fig = go.Figure(
        data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale="RdYlGn_r",
            hovertemplate="<b>%{y}</b><br>"
            + "%{x}<br>"
            + "Avg Price: £%{z:.0f}<extra></extra>",
        )
    )

    fig.update_layout(
        title="Average Price Calendar Heatmap",
        xaxis_title="Departure Date",
        yaxis_title="Destination",
        height=350,
    )

    return fig


def create_flight_dashboard(
    output_path: Path, df: pd.DataFrame, destinations_df: pd.DataFrame
) -> None:
    """
    Create complete flight prices dashboard HTML file.

    Args:
        output_path: Path to save HTML file
        df: Flight data DataFrame
        destinations_df: Destinations DataFrame
    """
    logger.info("Creating flight prices dashboard")

    # Create all charts
    price_trends = create_price_trends_chart(df, destinations_df)
    price_distribution = create_price_distribution_boxplot(df, destinations_df)
    airline_comparison = create_airline_comparison_chart(df, destinations_df)
    duration_scatter = create_duration_vs_cost_scatter(df, destinations_df)
    weekly_heatmap = create_weekly_heatmap(df, destinations_df)

    # Convert charts to HTML
    trends_html = price_trends.to_html(include_plotlyjs=False, div_id="price_trends")
    distribution_html = price_distribution.to_html(
        include_plotlyjs=False, div_id="price_distribution"
    )
    airline_html = airline_comparison.to_html(
        include_plotlyjs=False, div_id="airline_comparison"
    )
    duration_html = duration_scatter.to_html(
        include_plotlyjs=False, div_id="duration_scatter"
    )
    heatmap_html = weekly_heatmap.to_html(
        include_plotlyjs=False, div_id="weekly_heatmap"
    )

    # Calculate statistics
    min_price = df["price"].min()
    max_price = df["price"].max()
    avg_price = df["price"].mean()
    direct_flights = df["direct_flight"].sum()
    total_flights = len(df)
    airlines = df["airline"].nunique()

    # Get date range
    search_date = df["search_date"].iloc[0].strftime("%B %d, %Y")
    min_departure = df["departure_date"].min().strftime("%b %d")
    max_departure = df["departure_date"].max().strftime("%b %d")

    # Create complete HTML document
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flight Prices Dashboard - Places2Go</title>
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
        }}
        .info-box {{
            background: #e7f3ff;
            border-left: 4px solid #1f77b4;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
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
            margin-bottom: 5px;
        }}
        .stat-value {{
            font-size: 24px;
            font-weight: bold;
            color: #333;
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
        @media (max-width: 768px) {{
            .chart-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>✈️ Flight Prices Dashboard</h1>

        <div class="info-box">
            <strong>📊 Data Overview:</strong>
            Flight prices searched on {search_date} for departures
            {min_departure}-{max_departure}, 2025 •
            {total_flights} total flight records • All data from demo1 source
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-label">Minimum Price</div>
                <div class="stat-value">£{min_price:.0f}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Average Price</div>
                <div class="stat-value">£{avg_price:.0f}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Maximum Price</div>
                <div class="stat-value">£{max_price:.0f}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Direct Flights</div>
                <div class="stat-value">{direct_flights}/{total_flights}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Airlines</div>
                <div class="stat-value">{airlines}</div>
            </div>
        </div>

        <div class="chart-full">
            <h2>Price Trends Over Time</h2>
            {trends_html}
        </div>

        <div class="chart-full">
            <h2>Weekly Price Heatmap</h2>
            {heatmap_html}
        </div>

        <div class="chart-grid">
            <div>
                <h2>Price Distribution</h2>
                {distribution_html}
            </div>
            <div>
                <h2>Airline Comparison</h2>
                {airline_html}
            </div>
        </div>

        <div class="chart-full">
            <h2>Duration vs Cost Analysis</h2>
            {duration_html}
        </div>

        <div class="info-box" style="margin-top: 30px;">
            <strong>💡 Insights:</strong>
            • Direct flights shown as solid lines, indirect as dashed lines<br>
            • Click legend items to show/hide destinations<br>
            • Use the range slider below the main chart to zoom into
            specific date ranges<br>
            • Hover over any point for detailed flight information
        </div>
    </div>
</body>
</html>
"""

    # Save HTML file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_content)
    logger.info(f"Dashboard saved to {output_path}")


def main() -> None:
    """Main function to generate flight prices dashboard."""
    logger.info("Starting flight prices dashboard generation")

    # Load data
    loader = DataLoader()
    flights_df = loader.load_flights(data_source="demo1")
    destinations_df = loader.load_destinations()

    logger.info(
        f"Loaded {len(flights_df)} flight records for "
        f"{len(destinations_df)} destinations"
    )

    # Create output directory
    project_root = Path(__file__).resolve().parents[2]
    output_dir = project_root / ".build" / "visualizations"
    output_path = output_dir / "flight_prices.html"

    # Create dashboard
    create_flight_dashboard(output_path, flights_df, destinations_df)

    logger.info("Flight prices dashboard generation completed successfully")


if __name__ == "__main__":
    main()
