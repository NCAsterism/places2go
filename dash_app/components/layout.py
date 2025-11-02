"""
Layout components for the dashboard.

Provides the main layout structure including:
- Header
- Navigation tabs
- Main content area
- Footer
"""

from dash import html, dcc
import dash_bootstrap_components as dbc


def create_header():
    """
    Create header component with title and description.
    
    Returns:
        Header component
    """
    return dbc.Navbar(
        dbc.Container([
            html.A(
                dbc.Row([
                    dbc.Col(html.I(className="fas fa-plane-departure me-2")),
                    dbc.Col(dbc.NavbarBrand("Places2Go", className="ms-2")),
                ], align="center", className="g-0"),
                href="/",
                style={"textDecoration": "none"},
            ),
            html.Div([
                html.Span("Interactive Travel Destination Dashboard", className="text-light small")
            ])
        ], fluid=True),
        color="primary",
        dark=True,
        className="mb-4"
    )


def create_tabs():
    """
    Create navigation tabs for different views.
    
    Returns:
        Tabs component
    """
    return dcc.Tabs(
        id="main-tabs",
        value="overview",
        children=[
            dcc.Tab(label="Overview", value="overview", className="custom-tab"),
            dcc.Tab(label="Destinations Map", value="map", className="custom-tab"),
            dcc.Tab(label="Weather", value="weather", className="custom-tab"),
            dcc.Tab(label="Flights", value="flights", className="custom-tab"),
            dcc.Tab(label="Costs", value="costs", className="custom-tab"),
        ],
        className="mb-4"
    )


def create_footer():
    """
    Create footer component with information.
    
    Returns:
        Footer component
    """
    return html.Footer([
        html.Hr(),
        dbc.Container([
            html.P([
                "Places2Go - Interactive Travel Destination Dashboard | ",
                html.A("GitHub", href="https://github.com/NCAsterism/places2go", target="_blank"),
                " | Phase 4A: Dash Migration"
            ], className="text-muted text-center small")
        ])
    ], className="mt-4")


def create_sidebar(children):
    """
    Create sidebar for filters.
    
    Args:
        children: Child components to place in sidebar
        
    Returns:
        Sidebar component
    """
    return html.Div(
        children,
        className="sidebar",
        style={
            "padding": "20px",
            "backgroundColor": "#f8f9fa",
            "borderRight": "1px solid #dee2e6",
            "height": "100vh",
            "position": "sticky",
            "top": "0",
            "overflowY": "auto",
        }
    )


def create_main_content(children):
    """
    Create main content area.
    
    Args:
        children: Child components to place in main content
        
    Returns:
        Main content component
    """
    return html.Div(
        children,
        style={
            "padding": "20px",
            "backgroundColor": "#ffffff",
        }
    )


def create_loading_spinner(component_id):
    """
    Create loading spinner for async content.
    
    Args:
        component_id: ID of the component to wrap with loading spinner
        
    Returns:
        Loading component
    """
    return dcc.Loading(
        id=f"loading-{component_id}",
        type="default",
        children=html.Div(id=component_id)
    )


def create_stat_card(title, value, icon=None, color="primary"):
    """
    Create a statistic card.
    
    Args:
        title: Card title
        value: Card value/content
        icon: Optional icon class
        color: Bootstrap color variant
        
    Returns:
        Stat card component
    """
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.I(className=f"{icon} fa-2x text-{color}") if icon else None,
            ], className="mb-2"),
            html.H4(value, className=f"text-{color}"),
            html.P(title, className="text-muted mb-0"),
        ])
    ], className="text-center mb-3")


def create_info_alert(message, type="info"):
    """
    Create an info alert box.
    
    Args:
        message: Alert message
        type: Alert type (info, warning, danger, success)
        
    Returns:
        Alert component
    """
    return dbc.Alert(
        message,
        color=type,
        dismissable=True,
        className="mb-3"
    )
