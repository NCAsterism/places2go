"""
Places2Go Interactive Dashboard - Phase 4A

Main Dash application file that brings together all components
and callbacks for the interactive dashboard.

Usage:
    python app.py

The app will be available at http://127.0.0.1:8050
"""

import sys
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

# Add project root to path for imports
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from scripts.core.data_loader import DataLoader
from dash_app.components.filters import create_filters_panel
from dash_app.components.layout import (
    create_header,
    create_tabs,
    create_footer,
    create_sidebar,
    create_main_content,
    create_stat_card,
)
from dash_app.callbacks.filter_callbacks import register_filter_callbacks
from dash_app.callbacks.chart_callbacks import register_chart_callbacks

# Initialize Dash app with Bootstrap theme
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    ],
    suppress_callback_exceptions=True,
)

# Set app title
app.title = "Places2Go - Interactive Dashboard"

# Initialize data loader
loader = DataLoader()
destinations_df = loader.load_destinations()
weather_df = loader.load_weather(data_source="demo1")
costs_df = loader.load_costs(data_source="demo1")
flights_df = loader.load_flights(data_source="demo1")

# Get filter ranges
destination_names = destinations_df["name"].tolist()
min_date = flights_df["departure_date"].min()
max_date = flights_df["departure_date"].max()

# Create app layout
app.layout = html.Div([
    create_header(),
    
    dbc.Container([
        dbc.Row([
            # Sidebar with filters
            dbc.Col(
                create_sidebar(
                    create_filters_panel(destination_names, min_date, max_date)
                ),
                width=3,
                className="p-0"
            ),
            
            # Main content area
            dbc.Col([
                create_main_content([
                    # Hidden store for filtered data
                    dcc.Store(id="filtered-data-store"),
                    
                    # Overview stats
                    html.Div([
                        html.H4("Dashboard Overview", className="mb-3"),
                        dbc.Row([
                            dbc.Col(
                                create_stat_card(
                                    "Destinations",
                                    len(destinations_df),
                                    "fas fa-map-marker-alt",
                                    "primary"
                                ),
                                width=3
                            ),
                            dbc.Col(
                                create_stat_card(
                                    "Countries",
                                    destinations_df["country"].nunique(),
                                    "fas fa-globe",
                                    "success"
                                ),
                                width=3
                            ),
                            dbc.Col(
                                create_stat_card(
                                    "Avg Cost/Month",
                                    f"£{costs_df['monthly_living_cost'].mean():.0f}",
                                    "fas fa-coins",
                                    "warning"
                                ),
                                width=3
                            ),
                            dbc.Col(
                                create_stat_card(
                                    "Flight Options",
                                    len(flights_df),
                                    "fas fa-plane",
                                    "info"
                                ),
                                width=3
                            ),
                        ], className="mb-4"),
                    ], id="overview-stats"),
                    
                    # Tabs for different views
                    create_tabs(),
                    
                    # Tab content
                    html.Div(id="tab-content", className="mt-4"),
                ])
            ], width=9),
        ])
    ], fluid=True),
    
    create_footer(),
])


# Callback to update tab content
@app.callback(
    dash.Output("tab-content", "children"),
    dash.Input("main-tabs", "value")
)
def render_tab_content(active_tab):
    """
    Render content based on active tab.
    
    Args:
        active_tab: Currently active tab value
        
    Returns:
        Content for the active tab
    """
    if active_tab == "overview":
        return html.Div([
            html.H5("Welcome to Places2Go Dashboard", className="mb-3"),
            html.P([
                "This interactive dashboard helps you explore and compare travel destinations ",
                "from UK airports. Use the filters on the left to customize your view."
            ], className="text-muted"),
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    html.H6("Destinations Map", className="mb-3"),
                    dcc.Graph(id="destinations-map"),
                ], width=12),
            ]),
        ])
    
    elif active_tab == "map":
        return html.Div([
            html.H5("Destinations Map", className="mb-3"),
            html.P([
                "Interactive map showing all destinations with details. ",
                "Click on markers for more information."
            ], className="text-muted"),
            dcc.Graph(id="destinations-map"),
        ])
    
    elif active_tab == "weather":
        return html.Div([
            html.H5("Weather Forecast", className="mb-3"),
            html.P([
                "7-day weather forecast for all destinations including temperature trends, ",
                "rainfall, and comfort index."
            ], className="text-muted"),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="temperature-chart"),
                ], width=12, className="mb-4"),
                dbc.Col([
                    dcc.Graph(id="rainfall-chart"),
                ], width=12),
            ]),
        ])
    
    elif active_tab == "flights":
        return html.Div([
            html.H5("Flight Prices", className="mb-3"),
            html.P([
                "Flight price trends over time with price distribution and ",
                "duration vs cost analysis."
            ], className="text-muted"),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="flight-prices-chart"),
                ], width=12, className="mb-4"),
                dbc.Col([
                    dcc.Graph(id="flight-duration-scatter"),
                ], width=12),
            ]),
        ])
    
    elif active_tab == "costs":
        return html.Div([
            html.H5("Cost of Living Comparison", className="mb-3"),
            html.P([
                "Compare monthly living costs across destinations with detailed breakdowns ",
                "by category."
            ], className="text-muted"),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="cost-comparison-chart"),
                ], width=12, className="mb-4"),
                dbc.Col([
                    dcc.Graph(id="cost-breakdown-chart"),
                ], width=12),
            ]),
        ])
    
    return html.Div("Select a tab to view content")


# Register callbacks
register_filter_callbacks(app, loader)
register_chart_callbacks(app, loader)


if __name__ == "__main__":
    print("=" * 60)
    print("Places2Go Interactive Dashboard - Phase 4A")
    print("=" * 60)
    print("\nStarting Dash application...")
    print("Dashboard will be available at: http://127.0.0.1:8050")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    app.run(debug=True, host="127.0.0.1", port=8050)
