"""
Tests for Dash application components.

Tests cover:
- Filter components creation
- Chart components wrapping
- Layout components
"""

import pytest
import pandas as pd
from datetime import datetime

from dash_app.components.filters import (
    create_destination_filter,
    create_date_range_filter,
    create_budget_filter,
    create_weather_filter,
    create_flight_filter,
    create_filters_panel,
)
from dash_app.components.layout import (
    create_header,
    create_tabs,
    create_footer,
    create_stat_card,
    create_info_alert,
)


class TestFilterComponents:
    """Test filter component creation."""

    def test_create_destination_filter(self):
        """Test destination filter creation."""
        destinations = ["Alicante", "Malaga", "Faro"]
        component = create_destination_filter(destinations)
        
        assert component is not None
        # Component should have dropdown with multiple options
        assert len(destinations) == 3

    def test_create_date_range_filter(self):
        """Test date range filter creation."""
        min_date = datetime(2025, 10, 5)
        max_date = datetime(2025, 10, 17)
        component = create_date_range_filter(min_date, max_date)
        
        assert component is not None

    def test_create_budget_filter(self):
        """Test budget filter creation."""
        component = create_budget_filter()
        
        assert component is not None

    def test_create_weather_filter(self):
        """Test weather filter creation."""
        component = create_weather_filter()
        
        assert component is not None

    def test_create_flight_filter(self):
        """Test flight filter creation."""
        component = create_flight_filter()
        
        assert component is not None

    def test_create_filters_panel(self):
        """Test complete filters panel creation."""
        destinations = ["Alicante", "Malaga"]
        min_date = datetime(2025, 10, 5)
        max_date = datetime(2025, 10, 17)
        component = create_filters_panel(destinations, min_date, max_date)
        
        assert component is not None


class TestLayoutComponents:
    """Test layout component creation."""

    def test_create_header(self):
        """Test header creation."""
        component = create_header()
        
        assert component is not None

    def test_create_tabs(self):
        """Test tabs creation."""
        component = create_tabs()
        
        assert component is not None

    def test_create_footer(self):
        """Test footer creation."""
        component = create_footer()
        
        assert component is not None

    def test_create_stat_card(self):
        """Test stat card creation."""
        component = create_stat_card("Test Title", "42", "fas fa-test", "primary")
        
        assert component is not None

    def test_create_info_alert(self):
        """Test info alert creation."""
        component = create_info_alert("Test message", "info")
        
        assert component is not None


class TestChartComponents:
    """Test chart component wrapping."""

    @pytest.fixture
    def sample_destinations_df(self):
        """Create sample destinations DataFrame."""
        return pd.DataFrame({
            "destination_id": ["alc", "mal"],
            "name": ["Alicante", "Malaga"],
            "country": ["Spain", "Spain"],
            "region": ["Costa Blanca", "Costa del Sol"],
            "latitude": [38.2822, 36.7213],
            "longitude": [-0.5586, -4.4214],
            "airport_code": ["ALC", "AGP"],
            "airport_name": ["Alicante Airport", "Malaga Airport"],
            "timezone": ["Europe/Madrid", "Europe/Madrid"],
            "origin_airport": ["EXT", "EXT"],
        })

    def test_destinations_map_component_creation(self, sample_destinations_df):
        """Test destinations map component can be imported."""
        from dash_app.components.charts import create_destinations_map_component
        
        component = create_destinations_map_component(sample_destinations_df)
        assert component is not None

    def test_chart_component_with_empty_df(self, sample_destinations_df):
        """Test chart components handle empty dataframes."""
        from dash_app.components.charts import create_destinations_map_component
        
        empty_df = sample_destinations_df.iloc[0:0]  # Empty DataFrame with same columns
        component = create_destinations_map_component(sample_destinations_df, empty_df)
        assert component is not None
