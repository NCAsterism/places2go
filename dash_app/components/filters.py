"""
Filter components for the dashboard.

Provides reusable filter controls including:
- Multi-select destination dropdown
- Date range picker
- Budget range slider
- Weather preference controls
- Flight preference controls
"""

from dash import dcc, html
import dash_bootstrap_components as dbc


def create_destination_filter(destinations):
    """
    Create multi-select destination dropdown.
    
    Args:
        destinations: List of destination names
        
    Returns:
        Dash component for destination filtering
    """
    return dbc.Card([
        dbc.CardBody([
            html.Label("Destinations", className="fw-bold mb-2"),
            dcc.Dropdown(
                id="destination-filter",
                options=[{"label": dest, "value": dest} for dest in destinations],
                value=destinations,  # All selected by default
                multi=True,
                placeholder="Select destinations...",
                className="mb-3"
            )
        ])
    ], className="mb-3")


def create_date_range_filter(min_date, max_date):
    """
    Create date range picker.
    
    Args:
        min_date: Minimum date (datetime or string)
        max_date: Maximum date (datetime or string)
        
    Returns:
        Dash component for date range filtering
    """
    return dbc.Card([
        dbc.CardBody([
            html.Label("Date Range", className="fw-bold mb-2"),
            dcc.DatePickerRange(
                id="date-range-filter",
                min_date_allowed=min_date,
                max_date_allowed=max_date,
                start_date=min_date,
                end_date=max_date,
                display_format="YYYY-MM-DD",
                className="mb-3"
            )
        ])
    ], className="mb-3")


def create_budget_filter(min_budget=0, max_budget=5000):
    """
    Create budget range slider.
    
    Args:
        min_budget: Minimum budget value
        max_budget: Maximum budget value
        
    Returns:
        Dash component for budget filtering
    """
    return dbc.Card([
        dbc.CardBody([
            html.Label("Budget Range (£)", className="fw-bold mb-2"),
            dcc.RangeSlider(
                id="budget-filter",
                min=min_budget,
                max=max_budget,
                step=100,
                value=[min_budget, max_budget],
                marks={
                    0: "£0",
                    1000: "£1K",
                    2000: "£2K",
                    3000: "£3K",
                    4000: "£4K",
                    5000: "£5K",
                },
                tooltip={"placement": "bottom", "always_visible": False},
                className="mb-3"
            )
        ])
    ], className="mb-3")


def create_weather_filter():
    """
    Create weather preference controls.
    
    Returns:
        Dash component for weather preferences
    """
    return dbc.Card([
        dbc.CardBody([
            html.Label("Weather Preferences", className="fw-bold mb-2"),
            html.Div([
                html.Label("Min Temperature (°C)", className="small"),
                dcc.Slider(
                    id="min-temp-filter",
                    min=0,
                    max=40,
                    step=1,
                    value=15,
                    marks={0: "0°C", 20: "20°C", 40: "40°C"},
                    tooltip={"placement": "bottom", "always_visible": False},
                    className="mb-3"
                ),
            ]),
            html.Div([
                html.Label("Max Temperature (°C)", className="small"),
                dcc.Slider(
                    id="max-temp-filter",
                    min=0,
                    max=40,
                    step=1,
                    value=35,
                    marks={0: "0°C", 20: "20°C", 40: "40°C"},
                    tooltip={"placement": "bottom", "always_visible": False},
                    className="mb-3"
                ),
            ])
        ])
    ], className="mb-3")


def create_flight_filter():
    """
    Create flight preference controls.
    
    Returns:
        Dash component for flight preferences
    """
    return dbc.Card([
        dbc.CardBody([
            html.Label("Flight Preferences", className="fw-bold mb-2"),
            html.Div([
                html.Label("Max Duration (hours)", className="small"),
                dcc.Slider(
                    id="max-duration-filter",
                    min=0,
                    max=12,
                    step=0.5,
                    value=12,
                    marks={0: "0h", 4: "4h", 8: "8h", 12: "12h"},
                    tooltip={"placement": "bottom", "always_visible": False},
                    className="mb-2"
                ),
            ]),
            dbc.Checklist(
                id="direct-flight-filter",
                options=[{"label": "Direct flights only", "value": "direct"}],
                value=[],
                className="mb-2"
            )
        ])
    ], className="mb-3")


def create_filters_panel(destinations, min_date, max_date):
    """
    Create complete filters panel with all filter controls.
    
    Args:
        destinations: List of destination names
        min_date: Minimum date for date picker
        max_date: Maximum date for date picker
        
    Returns:
        Complete filters panel component
    """
    return html.Div([
        html.H5("Filters", className="mb-3"),
        create_destination_filter(destinations),
        create_date_range_filter(min_date, max_date),
        create_budget_filter(),
        create_weather_filter(),
        create_flight_filter(),
    ])
