"""Tests for the flight prices visualization."""

from pathlib import Path

import pandas as pd
import pytest

from scripts.visualizations.flight_prices import (
    create_airline_comparison_chart,
    create_duration_vs_cost_scatter,
    create_price_distribution_boxplot,
    create_price_trends_chart,
    create_weekly_heatmap,
    hex_to_rgba,
)


@pytest.fixture
def sample_flights_df():
    """Create a sample flights DataFrame for testing."""
    return pd.DataFrame(
        {
            "flight_id": [1, 2, 3, 4, 5, 6],
            "destination_id": [1, 1, 1, 2, 2, 2],
            "origin_airport": ["EXT", "EXT", "EXT", "EXT", "EXT", "EXT"],
            "search_date": pd.to_datetime(
                [
                    "2025-10-04",
                    "2025-10-04",
                    "2025-10-04",
                    "2025-10-04",
                    "2025-10-04",
                    "2025-10-04",
                ]
            ),
            "departure_date": pd.to_datetime(
                [
                    "2025-10-11",
                    "2025-10-12",
                    "2025-10-13",
                    "2025-10-11",
                    "2025-10-12",
                    "2025-10-13",
                ]
            ),
            "return_date": pd.to_datetime(
                [
                    "2025-10-18",
                    "2025-10-19",
                    "2025-10-20",
                    "2025-10-18",
                    "2025-10-19",
                    "2025-10-20",
                ]
            ),
            "price": [120.0, 115.0, 125.0, 150.0, 145.0, 155.0],
            "currency": ["GBP", "GBP", "GBP", "GBP", "GBP", "GBP"],
            "flight_duration_hours": [2.5, 2.5, 2.5, 2.7, 2.7, 2.7],
            "distance_km": [1245, 1245, 1245, 1620, 1620, 1620],
            "airline": [
                "Ryanair",
                "easyJet",
                "Ryanair",
                "Ryanair",
                "easyJet",
                "Ryanair",
            ],
            "direct_flight": [True, True, True, True, True, True],
            "data_source": ["demo1", "demo1", "demo1", "demo1", "demo1", "demo1"],
        }
    )


@pytest.fixture
def sample_destinations_df():
    """Create a sample destinations DataFrame for testing."""
    return pd.DataFrame(
        {
            "destination_id": [1, 2],
            "name": ["Alicante", "Malaga"],
            "country": ["Spain", "Spain"],
        }
    )


class TestHelperFunctions:
    """Tests for helper functions."""

    def test_hex_to_rgba_conversion(self):
        """Test hex to rgba color conversion."""
        result = hex_to_rgba("#1f77b4", 0.1)
        assert result == "rgba(31, 119, 180, 0.1)"

        result = hex_to_rgba("#ff7f0e", 0.5)
        assert result == "rgba(255, 127, 14, 0.5)"


class TestPriceTrendsChart:
    """Tests for price trends chart."""

    def test_creates_figure(self, sample_flights_df, sample_destinations_df):
        """Test that price trends chart creates a figure."""
        fig = create_price_trends_chart(sample_flights_df, sample_destinations_df)

        assert fig is not None
        assert len(fig.data) > 0

    def test_includes_all_destinations(self, sample_flights_df, sample_destinations_df):
        """Test that chart includes all destinations."""
        fig = create_price_trends_chart(sample_flights_df, sample_destinations_df)

        # Check that we have traces (destinations may have direct/indirect)
        assert len(fig.data) >= 2

    def test_has_correct_layout(self, sample_flights_df, sample_destinations_df):
        """Test that chart has proper layout settings."""
        fig = create_price_trends_chart(sample_flights_df, sample_destinations_df)

        assert "Price Trends Over Time" in fig.layout.title.text
        assert fig.layout.xaxis.title.text == "Departure Date"
        assert fig.layout.yaxis.title.text == "Price (GBP)"


class TestPriceDistributionBoxplot:
    """Tests for price distribution box plot."""

    def test_creates_figure(self, sample_flights_df, sample_destinations_df):
        """Test that price distribution boxplot creates a figure."""
        fig = create_price_distribution_boxplot(
            sample_flights_df, sample_destinations_df
        )

        assert fig is not None
        assert len(fig.data) > 0

    def test_includes_all_destinations(self, sample_flights_df, sample_destinations_df):
        """Test that boxplot includes all destinations."""
        fig = create_price_distribution_boxplot(
            sample_flights_df, sample_destinations_df
        )

        # Should have one box per destination
        assert len(fig.data) == 2

    def test_has_correct_layout(self, sample_flights_df, sample_destinations_df):
        """Test that boxplot has proper layout settings."""
        fig = create_price_distribution_boxplot(
            sample_flights_df, sample_destinations_df
        )

        assert "Price Distribution by Destination" in fig.layout.title.text
        assert fig.layout.yaxis.title.text == "Price (GBP)"


class TestAirlineComparisonChart:
    """Tests for airline comparison chart."""

    def test_creates_figure(self, sample_flights_df, sample_destinations_df):
        """Test that airline comparison chart creates a figure."""
        fig = create_airline_comparison_chart(sample_flights_df, sample_destinations_df)

        assert fig is not None
        assert len(fig.data) > 0

    def test_includes_airlines(self, sample_flights_df, sample_destinations_df):
        """Test that chart includes airlines."""
        fig = create_airline_comparison_chart(sample_flights_df, sample_destinations_df)

        # Should have traces for airlines
        assert len(fig.data) >= 2

    def test_has_correct_layout(self, sample_flights_df, sample_destinations_df):
        """Test that chart has proper layout settings."""
        fig = create_airline_comparison_chart(sample_flights_df, sample_destinations_df)

        assert "Average Price by Airline" in fig.layout.title.text
        assert fig.layout.xaxis.title.text == "Destination"
        assert fig.layout.yaxis.title.text == "Average Price (GBP)"


class TestDurationVsCostScatter:
    """Tests for duration vs cost scatter plot."""

    def test_creates_figure(self, sample_flights_df, sample_destinations_df):
        """Test that duration vs cost scatter creates a figure."""
        fig = create_duration_vs_cost_scatter(sample_flights_df, sample_destinations_df)

        assert fig is not None
        assert len(fig.data) > 0

    def test_includes_destinations(self, sample_flights_df, sample_destinations_df):
        """Test that scatter plot includes destinations."""
        fig = create_duration_vs_cost_scatter(sample_flights_df, sample_destinations_df)

        # Should have one trace per destination
        assert len(fig.data) == 2

    def test_has_correct_layout(self, sample_flights_df, sample_destinations_df):
        """Test that scatter plot has proper layout settings."""
        fig = create_duration_vs_cost_scatter(sample_flights_df, sample_destinations_df)

        assert "Flight Duration vs Cost" in fig.layout.title.text
        assert fig.layout.xaxis.title.text == "Duration (hours)"
        assert fig.layout.yaxis.title.text == "Price (GBP)"


class TestWeeklyHeatmap:
    """Tests for weekly calendar heatmap."""

    def test_creates_figure(self, sample_flights_df, sample_destinations_df):
        """Test that weekly heatmap creates a figure."""
        fig = create_weekly_heatmap(sample_flights_df, sample_destinations_df)

        assert fig is not None
        assert len(fig.data) > 0

    def test_has_correct_layout(self, sample_flights_df, sample_destinations_df):
        """Test that heatmap has proper layout settings."""
        fig = create_weekly_heatmap(sample_flights_df, sample_destinations_df)

        assert "Average Price Calendar Heatmap" in fig.layout.title.text
        assert fig.layout.xaxis.title.text == "Departure Date"
        assert fig.layout.yaxis.title.text == "Destination"


class TestIntegration:
    """Integration tests using actual data."""

    def test_generates_dashboard_with_real_data(self, tmp_path):
        """Test that dashboard can be generated with real data."""
        from scripts.core.data_loader import DataLoader
        from scripts.visualizations.flight_prices import create_flight_dashboard

        loader = DataLoader()
        flights_df = loader.load_flights(data_source="demo1")
        destinations_df = loader.load_destinations()

        output_path = tmp_path / "test_flight_prices.html"
        create_flight_dashboard(output_path, flights_df, destinations_df)

        # Verify file was created
        assert output_path.exists()
        assert output_path.stat().st_size > 10000  # Should be substantial

        # Verify content
        content = output_path.read_text()
        assert "Flight Prices Dashboard" in content
        assert "Price Trends Over Time" in content
        assert "Price Distribution" in content
        assert "Airline Comparison" in content
        assert "Duration vs Cost" in content
        assert "Weekly Price Heatmap" in content

    def test_handles_all_42_records(self):
        """Test that visualization handles all 42 flight records correctly."""
        from scripts.core.data_loader import DataLoader

        loader = DataLoader()
        flights_df = loader.load_flights(data_source="demo1")

        assert len(flights_df) == 42

        # Test all chart functions with full dataset
        destinations_df = loader.load_destinations()

        price_trends = create_price_trends_chart(flights_df, destinations_df)
        assert price_trends is not None
        assert len(price_trends.data) > 0

        price_dist = create_price_distribution_boxplot(flights_df, destinations_df)
        assert price_dist is not None
        assert len(price_dist.data) == 6  # 6 destinations

        airline_comp = create_airline_comparison_chart(flights_df, destinations_df)
        assert airline_comp is not None
        assert len(airline_comp.data) >= 2  # At least 2 airlines

        duration_scatter = create_duration_vs_cost_scatter(flights_df, destinations_df)
        assert duration_scatter is not None
        assert len(duration_scatter.data) == 6  # 6 destinations

        weekly_heatmap = create_weekly_heatmap(flights_df, destinations_df)
        assert weekly_heatmap is not None
        assert len(weekly_heatmap.data) > 0
