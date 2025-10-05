"""
Chart components for the dashboard.

Wraps existing Plotly chart functions from Phase 3 visualizations
and adapts them for use in Dash with interactive updates.
"""

import sys
from pathlib import Path

import pandas as pd
from dash import dcc

# Add project root to path for imports
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

# Import chart creation functions from Phase 3 visualizations
from scripts.visualizations.destinations_map import create_interactive_map
from scripts.visualizations.weather_forecast import (
    create_temperature_trends_chart,
    create_rainfall_chart,
    create_uv_index_heatmap,
    create_comfort_index_chart,
)
from scripts.visualizations.cost_comparison import (
    create_total_cost_chart,
    create_cost_breakdown_chart,
    create_category_comparison_chart,
)
from scripts.visualizations.flight_prices import (
    create_price_trends_chart,
    create_price_distribution_boxplot,
    create_airline_comparison_chart,
    create_duration_vs_cost_scatter,
)


def create_destinations_map_component(destinations_df, filtered_df=None):
    """
    Create destinations map component for Dash.
    
    Args:
        destinations_df: Full destinations DataFrame
        filtered_df: Filtered destinations DataFrame (optional)
        
    Returns:
        Dash Graph component with destinations map
    """
    df = filtered_df if filtered_df is not None else destinations_df
    if df.empty:
        return dcc.Graph(
            id="destinations-map",
            figure={"data": [], "layout": {"title": "No destinations match filters"}}
        )
    
    fig = create_interactive_map(df)
    return dcc.Graph(id="destinations-map", figure=fig)


def create_temperature_chart_component(weather_df, destinations_df, filtered_dest=None):
    """
    Create temperature trends chart component for Dash.
    
    Args:
        weather_df: Weather data DataFrame
        destinations_df: Destinations DataFrame
        filtered_dest: List of filtered destination names (optional)
        
    Returns:
        Dash Graph component with temperature chart
    """
    df = weather_df.copy()
    if filtered_dest:
        # Filter by destination
        dest_ids = destinations_df[destinations_df["name"].isin(filtered_dest)]["destination_id"].tolist()
        df = df[df["destination_id"].isin(dest_ids)]
    
    if df.empty:
        return dcc.Graph(
            id="temperature-chart",
            figure={"data": [], "layout": {"title": "No data match filters"}}
        )
    
    fig = create_temperature_trends_chart(df, destinations_df)
    return dcc.Graph(id="temperature-chart", figure=fig)


def create_rainfall_chart_component(weather_df, destinations_df, filtered_dest=None):
    """
    Create rainfall chart component for Dash.
    
    Args:
        weather_df: Weather data DataFrame
        destinations_df: Destinations DataFrame
        filtered_dest: List of filtered destination names (optional)
        
    Returns:
        Dash Graph component with rainfall chart
    """
    df = weather_df.copy()
    if filtered_dest:
        dest_ids = destinations_df[destinations_df["name"].isin(filtered_dest)]["destination_id"].tolist()
        df = df[df["destination_id"].isin(dest_ids)]
    
    if df.empty:
        return dcc.Graph(
            id="rainfall-chart",
            figure={"data": [], "layout": {"title": "No data match filters"}}
        )
    
    fig = create_rainfall_chart(df, destinations_df)
    return dcc.Graph(id="rainfall-chart", figure=fig)


def create_cost_comparison_component(costs_df, destinations_df, filtered_dest=None):
    """
    Create cost comparison chart component for Dash.
    
    Args:
        costs_df: Cost of living DataFrame
        destinations_df: Destinations DataFrame
        filtered_dest: List of filtered destination names (optional)
        
    Returns:
        Dash Graph component with cost comparison chart
    """
    df = costs_df.copy()
    if filtered_dest:
        dest_ids = destinations_df[destinations_df["name"].isin(filtered_dest)]["destination_id"].tolist()
        df = df[df["destination_id"].isin(dest_ids)]
    
    if df.empty:
        return dcc.Graph(
            id="cost-comparison-chart",
            figure={"data": [], "layout": {"title": "No data match filters"}}
        )
    
    fig = create_total_cost_chart(df, destinations_df)
    return dcc.Graph(id="cost-comparison-chart", figure=fig)


def create_cost_breakdown_component(costs_df, destinations_df, filtered_dest=None):
    """
    Create cost breakdown chart component for Dash.
    
    Args:
        costs_df: Cost of living DataFrame
        destinations_df: Destinations DataFrame
        filtered_dest: List of filtered destination names (optional)
        
    Returns:
        Dash Graph component with cost breakdown chart
    """
    df = costs_df.copy()
    if filtered_dest:
        dest_ids = destinations_df[destinations_df["name"].isin(filtered_dest)]["destination_id"].tolist()
        df = df[df["destination_id"].isin(dest_ids)]
    
    if df.empty:
        return dcc.Graph(
            id="cost-breakdown-chart",
            figure={"data": [], "layout": {"title": "No data match filters"}}
        )
    
    fig = create_cost_breakdown_chart(df, destinations_df)
    return dcc.Graph(id="cost-breakdown-chart", figure=fig)


def create_flight_prices_component(flights_df, destinations_df, filtered_dest=None):
    """
    Create flight prices chart component for Dash.
    
    Args:
        flights_df: Flight prices DataFrame
        destinations_df: Destinations DataFrame
        filtered_dest: List of filtered destination names (optional)
        
    Returns:
        Dash Graph component with flight prices chart
    """
    df = flights_df.copy()
    if filtered_dest:
        dest_ids = destinations_df[destinations_df["name"].isin(filtered_dest)]["destination_id"].tolist()
        df = df[df["destination_id"].isin(dest_ids)]
    
    if df.empty:
        return dcc.Graph(
            id="flight-prices-chart",
            figure={"data": [], "layout": {"title": "No data match filters"}}
        )
    
    fig = create_price_trends_chart(df, destinations_df)
    return dcc.Graph(id="flight-prices-chart", figure=fig)


def create_flight_duration_scatter_component(flights_df, destinations_df, filtered_dest=None):
    """
    Create flight duration vs cost scatter chart component for Dash.
    
    Args:
        flights_df: Flight prices DataFrame
        destinations_df: Destinations DataFrame
        filtered_dest: List of filtered destination names (optional)
        
    Returns:
        Dash Graph component with duration scatter chart
    """
    df = flights_df.copy()
    if filtered_dest:
        dest_ids = destinations_df[destinations_df["name"].isin(filtered_dest)]["destination_id"].tolist()
        df = df[df["destination_id"].isin(dest_ids)]
    
    if df.empty:
        return dcc.Graph(
            id="flight-duration-scatter",
            figure={"data": [], "layout": {"title": "No data match filters"}}
        )
    
    fig = create_duration_vs_cost_scatter(df, destinations_df)
    return dcc.Graph(id="flight-duration-scatter", figure=fig)
