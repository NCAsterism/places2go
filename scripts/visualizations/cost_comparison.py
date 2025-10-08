"""
cost_comparison.py
------------------

This script creates an interactive cost of living comparison visualization dashboard
displaying cost breakdowns and comparisons across all destinations.

The dashboard includes:
- Total cost comparison horizontal bar chart (sorted by cost)
- Stacked bar chart showing cost breakdown by category
- Grouped bar chart for specific category comparisons
- Box plot showing cost distribution and outliers
- Interactive tooltips with exact values and percentages
- Sort/filter controls

Output: `.build/visualizations/cost_comparison.html`
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
        logging.FileHandler(log_dir / "cost_comparison.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)

# Color palette for destinations (matching map colors)
DESTINATION_COLORS = {
    "Alicante": "#1f77b4",
    "Malaga": "#ff7f0e",
    "Majorca": "#2ca02c",
    "Faro": "#d62728",
    "Corfu": "#9467bd",
    "Rhodes": "#8c564b",
}


def create_total_cost_chart(
    df: pd.DataFrame, destinations_df: pd.DataFrame
) -> go.Figure:
    """
    Create horizontal bar chart comparing total monthly costs by destination.

    Args:
        df: Cost of living DataFrame
        destinations_df: Destinations DataFrame

    Returns:
        Plotly Figure object
    """
    logger.info("Creating total cost comparison chart")

    # Merge with destinations to get names
    merged = df.merge(destinations_df[["destination_id", "name"]], on="destination_id")

    # Sort by monthly living cost
    merged = merged.sort_values("monthly_living_cost", ascending=True)

    # Create colors list
    colors = [DESTINATION_COLORS.get(name, "#1f77b4") for name in merged["name"]]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=merged["name"],
            x=merged["monthly_living_cost"],
            orientation="h",
            marker=dict(color=colors),
            text=merged["monthly_living_cost"].apply(lambda x: f"£{x:.0f}"),
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>"
            + "Monthly Cost: £%{x:.2f}<br>"
            + "<extra></extra>",
        )
    )

    fig.update_layout(
        title="Total Monthly Living Cost by Destination",
        xaxis_title="Monthly Cost (£ GBP)",
        yaxis_title="Destination",
        height=400,
        template="plotly_white",
        showlegend=False,
        margin=dict(l=100, r=100, t=60, b=60),
    )

    return fig


def create_cost_breakdown_chart(
    df: pd.DataFrame, destinations_df: pd.DataFrame
) -> go.Figure:
    """
    Create stacked bar chart showing cost breakdown by category.

    Args:
        df: Cost of living DataFrame
        destinations_df: Destinations DataFrame

    Returns:
        Plotly Figure object
    """
    logger.info("Creating cost breakdown stacked chart")

    # Merge with destinations to get names
    merged = df.merge(destinations_df[["destination_id", "name"]], on="destination_id")

    # Sort by monthly living cost
    merged = merged.sort_values("monthly_living_cost", ascending=False)

    # Define cost categories for breakdown
    categories = {
        "Rent (Center)": "rent_1br_center",
        "Food": "monthly_food",
        "Transport": "monthly_transport",
        "Utilities": "utilities",
        "Internet": "internet",
    }

    fig = go.Figure()

    # Add traces for each category
    for label, column in categories.items():
        fig.add_trace(
            go.Bar(
                name=label,
                x=merged["name"],
                y=merged[column],
                text=merged[column].apply(lambda x: f"£{x:.0f}"),
                textposition="inside",
                hovertemplate="<b>%{x}</b><br>"
                + f"{label}: £%{{y:.2f}}<br>"
                + "<extra></extra>",
            )
        )

    fig.update_layout(
        title="Cost Breakdown by Category",
        xaxis_title="Destination",
        yaxis_title="Monthly Cost (£ GBP)",
        barmode="stack",
        height=500,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=60, r=60, t=100, b=60),
    )

    return fig


def create_category_comparison_chart(
    df: pd.DataFrame, destinations_df: pd.DataFrame
) -> go.Figure:
    """
    Create grouped bar chart for specific category comparisons.

    Args:
        df: Cost of living DataFrame
        destinations_df: Destinations DataFrame

    Returns:
        Plotly Figure object
    """
    logger.info("Creating category comparison chart")

    # Merge with destinations to get names
    merged = df.merge(destinations_df[["destination_id", "name"]], on="destination_id")

    # Sort by name for consistency
    merged = merged.sort_values("name")

    # Categories to compare
    categories = {
        "Meal (Inexpensive)": "meal_inexpensive",
        "Meal (Mid-range)": "meal_mid_range",
        "Beer (Domestic)": "beer_domestic",
    }

    fig = go.Figure()

    # Add traces for each category
    for label, column in categories.items():
        fig.add_trace(
            go.Bar(
                name=label,
                x=merged["name"],
                y=merged[column],
                text=merged[column].apply(lambda x: f"£{x:.1f}"),
                textposition="outside",
                hovertemplate="<b>%{x}</b><br>"
                + f"{label}: £%{{y:.2f}}<br>"
                + "<extra></extra>",
            )
        )

    fig.update_layout(
        title="Dining & Leisure Cost Comparison",
        xaxis_title="Destination",
        yaxis_title="Cost (£ GBP)",
        barmode="group",
        height=450,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=60, r=60, t=100, b=60),
    )

    return fig


def create_cost_distribution_chart(
    df: pd.DataFrame, destinations_df: pd.DataFrame
) -> go.Figure:
    """
    Create box plot showing cost distribution and outliers.

    Args:
        df: Cost of living DataFrame
        destinations_df: Destinations DataFrame

    Returns:
        Plotly Figure object
    """
    logger.info("Creating cost distribution box plot")

    # Merge with destinations to get names
    merged = df.merge(destinations_df[["destination_id", "name"]], on="destination_id")

    # Prepare data for box plot - stack all cost categories
    cost_categories = [
        "rent_1br_center",
        "rent_1br_outside",
        "monthly_food",
        "monthly_transport",
        "utilities",
        "internet",
    ]

    category_labels = {
        "rent_1br_center": "Rent (Center)",
        "rent_1br_outside": "Rent (Outside)",
        "monthly_food": "Food",
        "monthly_transport": "Transport",
        "utilities": "Utilities",
        "internet": "Internet",
    }

    fig = go.Figure()

    for category in cost_categories:
        fig.add_trace(
            go.Box(
                y=merged[category],
                name=category_labels[category],
                boxmean="sd",
                hovertemplate="<b>%{fullData.name}</b><br>"
                + "Median: £%{median:.2f}<br>"
                + "Q1: £%{q1:.2f}<br>"
                + "Q3: £%{q3:.2f}<br>"
                + "<extra></extra>",
            )
        )

    fig.update_layout(
        title="Cost Distribution by Category",
        yaxis_title="Monthly Cost (£ GBP)",
        height=450,
        template="plotly_white",
        showlegend=True,
        margin=dict(l=60, r=60, t=60, b=60),
    )

    return fig


def create_cost_dashboard(
    output_path: Path, df: pd.DataFrame, destinations_df: pd.DataFrame
) -> None:
    """
    Create complete cost comparison dashboard HTML file.

    Args:
        output_path: Path to save HTML file
        df: Cost of living DataFrame
        destinations_df: Destinations DataFrame
    """
    logger.info("Creating cost comparison dashboard")

    # Get data date for display
    data_date = df["data_date"].iloc[0] if not df.empty else "N/A"
    data_source = df["data_source"].iloc[0] if not df.empty else "N/A"

    # Calculate summary statistics with safety checks for empty/invalid data
    avg_cost_display = "N/A"
    min_cost_display = "N/A"
    max_cost_display = "N/A"
    range_display = "N/A"
    min_dest = "N/A"
    max_dest = "N/A"

    if not df.empty and "monthly_living_cost" in df.columns:
        numeric_costs = pd.to_numeric(
            df["monthly_living_cost"], errors="coerce", downcast="float"
        )
        valid_costs = numeric_costs.dropna()

        if not valid_costs.empty:
            avg_cost_value = float(valid_costs.mean())
            min_cost_value = float(valid_costs.min())
            max_cost_value = float(valid_costs.max())

            avg_cost_display = f"£{avg_cost_value:.0f}/mo"
            min_cost_display = f"£{min_cost_value:.0f}/mo"
            max_cost_display = f"£{max_cost_value:.0f}/mo"
            range_display = f"£{(max_cost_value - min_cost_value):.0f}"

            if (
                "destination_id" in df.columns
                and "destination_id" in destinations_df.columns
            ):
                min_index = valid_costs.idxmin()
                max_index = valid_costs.idxmax()

                if pd.notna(min_index):
                    min_dest_id = df.loc[min_index, "destination_id"]
                    min_dest_match = destinations_df.loc[
                        destinations_df["destination_id"] == min_dest_id, "name"
                    ]
                    if not min_dest_match.empty:
                        min_dest = str(min_dest_match.iloc[0])

                if pd.notna(max_index):
                    max_dest_id = df.loc[max_index, "destination_id"]
                    max_dest_match = destinations_df.loc[
                        destinations_df["destination_id"] == max_dest_id, "name"
                    ]
                    if not max_dest_match.empty:
                        max_dest = str(max_dest_match.iloc[0])

    # Create all charts
    total_chart = create_total_cost_chart(df, destinations_df)
    breakdown_chart = create_cost_breakdown_chart(df, destinations_df)
    category_chart = create_category_comparison_chart(df, destinations_df)
    distribution_chart = create_cost_distribution_chart(df, destinations_df)

    # Convert charts to HTML
    # Include plotly.js inline in the first chart
    total_html = total_chart.to_html(
        include_plotlyjs="require", div_id="total_chart", config={"responsive": True}
    )
    breakdown_html = breakdown_chart.to_html(
        include_plotlyjs=False, div_id="breakdown_chart", config={"responsive": True}
    )
    category_html = category_chart.to_html(
        include_plotlyjs=False, div_id="category_chart", config={"responsive": True}
    )
    distribution_html = distribution_chart.to_html(
        include_plotlyjs=False, div_id="distribution_chart", config={"responsive": True}
    )

    # Create complete HTML document
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cost of Living Comparison - Places2Go</title>
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
        footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>💰 Cost of Living Comparison</h1>

        <div class="info-box">
            <strong>Data Information:</strong> Cost of living data as of {data_date} |
            Source: {data_source} | Currency: £ GBP
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-label">Average Cost</div>
                <div class="stat-value">{avg_cost_display}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Most Affordable</div>
                <div class="stat-value">{min_dest}<br><span style="font-size: 18px;">{min_cost_display}</span></div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Most Expensive</div>
                <div class="stat-value">{max_dest}<br><span style="font-size: 18px;">{max_cost_display}</span></div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Cost Range</div>
                <div class="stat-value">{range_display}</div>
            </div>
        </div>

        <div class="chart-full">
            {total_html}
        </div>

        <div class="chart-full">
            {breakdown_html}
        </div>

        <div class="chart-grid">
            <div>
                {category_html}
            </div>
            <div>
                {distribution_html}
            </div>
        </div>

        <footer>
            <p><strong>About this dashboard:</strong> This interactive cost of living comparison dashboard displays
            comprehensive cost breakdowns across all destinations. Hover over charts for detailed information.
            Click legend items to toggle visibility of specific categories.</p>
            <p><strong>Cost Categories:</strong> Monthly living cost includes rent (1BR center), food, transport,
            utilities, and internet. Additional metrics show dining and leisure costs for lifestyle comparison.</p>
        </footer>
    </div>
</body>
</html>
    """

    # Write HTML file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_content, encoding="utf-8")
    logger.info(f"Dashboard saved to {output_path}")


def main() -> None:
    """Main entry point for cost comparison visualization."""
    logger.info("Starting cost comparison visualization generation")

    # Initialize data loader
    loader = DataLoader()

    # Load data
    logger.info("Loading cost of living data")
    costs_df = loader.load_costs(data_source="demo1")
    destinations_df = loader.load_destinations()

    if costs_df.empty:
        logger.error("No cost data found")
        return

    logger.info(
        f"Loaded {len(costs_df)} cost records for {len(costs_df['destination_id'].unique())} destinations"
    )

    # Create output directory and generate dashboard
    output_dir = Path(__file__).resolve().parents[2] / ".build" / "visualizations"
    output_path = output_dir / "cost_comparison.html"

    create_cost_dashboard(output_path, costs_df, destinations_df)

    logger.info("Cost comparison visualization completed successfully")
    logger.info(f"View dashboard at: {output_path}")


if __name__ == "__main__":
    main()
