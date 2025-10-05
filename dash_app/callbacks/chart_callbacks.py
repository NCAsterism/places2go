"""
Chart callbacks for handling chart interactions and updates.

These callbacks update individual charts based on filter selections
and handle chart interactions like click events.
"""

import sys
from pathlib import Path

import pandas as pd
from dash import Input, Output, State

# Add project root to path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from dash_app.components.charts import (
    create_destinations_map_component,
    create_temperature_chart_component,
    create_rainfall_chart_component,
    create_cost_comparison_component,
    create_cost_breakdown_component,
    create_flight_prices_component,
    create_flight_duration_scatter_component,
)


def register_chart_callbacks(app, loader):
    """
    Register all chart-related callbacks.
    
    Args:
        app: Dash application instance
        loader: DataLoader instance with cached data
    """
    
    # Load all data once
    destinations_df = loader.load_destinations()
    weather_df = loader.load_weather(data_source="demo1")
    costs_df = loader.load_costs(data_source="demo1")
    flights_df = loader.load_flights(data_source="demo1")
    
    @app.callback(
        Output("destinations-map", "figure"),
        Input("filtered-data-store", "data")
    )
    def update_destinations_map(filter_data):
        """Update destinations map based on filters."""
        if not filter_data or not filter_data.get("destinations"):
            return create_destinations_map_component(destinations_df).figure
        
        # Filter destinations
        filtered_df = destinations_df[
            destinations_df["name"].isin(filter_data["destinations"])
        ]
        
        return create_destinations_map_component(destinations_df, filtered_df).figure
    
    @app.callback(
        Output("temperature-chart", "figure"),
        Input("filtered-data-store", "data")
    )
    def update_temperature_chart(filter_data):
        """Update temperature chart based on filters."""
        if not filter_data:
            return create_temperature_chart_component(weather_df, destinations_df).figure
        
        selected_dest = filter_data.get("destinations", [])
        if not selected_dest:
            selected_dest = destinations_df["name"].tolist()
        
        # Filter by date range if provided
        df = weather_df.copy()
        if filter_data.get("start_date") and filter_data.get("end_date"):
            df = df[
                (df["forecast_date"] >= filter_data["start_date"]) &
                (df["forecast_date"] <= filter_data["end_date"])
            ]
        
        # Filter by temperature
        if filter_data.get("min_temp") is not None:
            df = df[df["temp_high"] >= filter_data["min_temp"]]
        if filter_data.get("max_temp") is not None:
            df = df[df["temp_low"] <= filter_data["max_temp"]]
        
        return create_temperature_chart_component(df, destinations_df, selected_dest).figure
    
    @app.callback(
        Output("rainfall-chart", "figure"),
        Input("filtered-data-store", "data")
    )
    def update_rainfall_chart(filter_data):
        """Update rainfall chart based on filters."""
        if not filter_data:
            return create_rainfall_chart_component(weather_df, destinations_df).figure
        
        selected_dest = filter_data.get("destinations", [])
        if not selected_dest:
            selected_dest = destinations_df["name"].tolist()
        
        # Filter by date range if provided
        df = weather_df.copy()
        if filter_data.get("start_date") and filter_data.get("end_date"):
            df = df[
                (df["forecast_date"] >= filter_data["start_date"]) &
                (df["forecast_date"] <= filter_data["end_date"])
            ]
        
        return create_rainfall_chart_component(df, destinations_df, selected_dest).figure
    
    @app.callback(
        Output("cost-comparison-chart", "figure"),
        Input("filtered-data-store", "data")
    )
    def update_cost_comparison_chart(filter_data):
        """Update cost comparison chart based on filters."""
        if not filter_data:
            return create_cost_comparison_component(costs_df, destinations_df).figure
        
        selected_dest = filter_data.get("destinations", [])
        if not selected_dest:
            selected_dest = destinations_df["name"].tolist()
        
        # Filter by budget
        df = costs_df.copy()
        if filter_data.get("min_budget") is not None and filter_data.get("max_budget") is not None:
            df = df[
                (df["monthly_living_cost"] >= filter_data["min_budget"]) &
                (df["monthly_living_cost"] <= filter_data["max_budget"])
            ]
        
        return create_cost_comparison_component(df, destinations_df, selected_dest).figure
    
    @app.callback(
        Output("cost-breakdown-chart", "figure"),
        Input("filtered-data-store", "data")
    )
    def update_cost_breakdown_chart(filter_data):
        """Update cost breakdown chart based on filters."""
        if not filter_data:
            return create_cost_breakdown_component(costs_df, destinations_df).figure
        
        selected_dest = filter_data.get("destinations", [])
        if not selected_dest:
            selected_dest = destinations_df["name"].tolist()
        
        # Filter by budget
        df = costs_df.copy()
        if filter_data.get("min_budget") is not None and filter_data.get("max_budget") is not None:
            df = df[
                (df["monthly_living_cost"] >= filter_data["min_budget"]) &
                (df["monthly_living_cost"] <= filter_data["max_budget"])
            ]
        
        return create_cost_breakdown_component(df, destinations_df, selected_dest).figure
    
    @app.callback(
        Output("flight-prices-chart", "figure"),
        Input("filtered-data-store", "data")
    )
    def update_flight_prices_chart(filter_data):
        """Update flight prices chart based on filters."""
        if not filter_data:
            return create_flight_prices_component(flights_df, destinations_df).figure
        
        selected_dest = filter_data.get("destinations", [])
        if not selected_dest:
            selected_dest = destinations_df["name"].tolist()
        
        # Filter by date range
        df = flights_df.copy()
        if filter_data.get("start_date") and filter_data.get("end_date"):
            df = df[
                (df["departure_date"] >= filter_data["start_date"]) &
                (df["departure_date"] <= filter_data["end_date"])
            ]
        
        # Filter by duration
        if filter_data.get("max_duration") is not None:
            df = df[df["duration_hours"] <= filter_data["max_duration"]]
        
        # Filter by direct flights only
        if filter_data.get("direct_only"):
            df = df[df["direct_flight"] == True]
        
        return create_flight_prices_component(df, destinations_df, selected_dest).figure
    
    @app.callback(
        Output("flight-duration-scatter", "figure"),
        Input("filtered-data-store", "data")
    )
    def update_flight_duration_scatter(filter_data):
        """Update flight duration scatter chart based on filters."""
        if not filter_data:
            return create_flight_duration_scatter_component(flights_df, destinations_df).figure
        
        selected_dest = filter_data.get("destinations", [])
        if not selected_dest:
            selected_dest = destinations_df["name"].tolist()
        
        # Filter by date range
        df = flights_df.copy()
        if filter_data.get("start_date") and filter_data.get("end_date"):
            df = df[
                (df["departure_date"] >= filter_data["start_date"]) &
                (df["departure_date"] <= filter_data["end_date"])
            ]
        
        # Filter by duration
        if filter_data.get("max_duration") is not None:
            df = df[df["duration_hours"] <= filter_data["max_duration"]]
        
        # Filter by direct flights only
        if filter_data.get("direct_only"):
            df = df[df["direct_flight"] == True]
        
        return create_flight_duration_scatter_component(df, destinations_df, selected_dest).figure
