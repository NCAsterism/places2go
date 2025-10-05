"""
Filter callbacks for handling filter updates.

These callbacks update the dashboard charts based on filter selections.
"""

import sys
from pathlib import Path

import pandas as pd
from dash import Input, Output, State

# Add project root to path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))


def register_filter_callbacks(app, loader):
    """
    Register all filter-related callbacks.
    
    Args:
        app: Dash application instance
        loader: DataLoader instance with cached data
    """
    
    @app.callback(
        Output("filtered-data-store", "data"),
        [
            Input("destination-filter", "value"),
            Input("date-range-filter", "start_date"),
            Input("date-range-filter", "end_date"),
            Input("budget-filter", "value"),
            Input("min-temp-filter", "value"),
            Input("max-temp-filter", "value"),
            Input("max-duration-filter", "value"),
            Input("direct-flight-filter", "value"),
        ]
    )
    def update_filtered_data(
        selected_destinations,
        start_date,
        end_date,
        budget_range,
        min_temp,
        max_temp,
        max_duration,
        direct_only
    ):
        """
        Update filtered data store based on all filter inputs.
        
        Returns:
            Dictionary with filtered data info (destinations, date range, etc.)
        """
        # Return filter state as a dictionary
        return {
            "destinations": selected_destinations or [],
            "start_date": start_date,
            "end_date": end_date,
            "min_budget": budget_range[0] if budget_range else 0,
            "max_budget": budget_range[1] if budget_range else 5000,
            "min_temp": min_temp,
            "max_temp": max_temp,
            "max_duration": max_duration,
            "direct_only": "direct" in (direct_only or [])
        }
