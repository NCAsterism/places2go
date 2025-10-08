"""Tests for the weather forecast visualization."""

from pathlib import Path

import pandas as pd
import pytest

from scripts.visualizations.weather_forecast import (
    create_comfort_index_chart,
    create_conditions_pie_chart,
    create_rainfall_chart,
    create_temperature_trends_chart,
    create_uv_index_heatmap,
    create_weather_cards_html,
    get_weather_icon,
    hex_to_rgba,
)


@pytest.fixture
def sample_weather_df():
    """Create a sample weather DataFrame for testing."""
    return pd.DataFrame(
        {
            "weather_id": [1, 2, 3],
            "destination_id": [1, 1, 2],
            "date": pd.to_datetime(["2025-10-05", "2025-10-06", "2025-10-05"]),
            "temp_high_c": [26, 27, 29],
            "temp_low_c": [18, 19, 21],
            "temp_avg_c": [22, 23, 25],
            "rainfall_mm": [0, 0, 0],
            "humidity_percent": [65, 60, 68],
            "sunshine_hours": [9.5, 10.2, 9.0],
            "wind_speed_kmh": [12, 10, 14],
            "conditions": ["Sunny", "Clear", "Sunny"],
            "uv_index": [7, 7, 8],
            "forecast_flag": [True, True, True],
            "data_source": ["demo1", "demo1", "demo1"],
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

    def test_get_weather_icon_known_condition(self):
        """Test weather icon mapping for known conditions."""
        assert get_weather_icon("Sunny") == "☀️"
        assert get_weather_icon("Clear") == "🌤️"
        assert get_weather_icon("Rain") == "🌧️"

    def test_get_weather_icon_unknown_condition(self):
        """Test weather icon mapping for unknown conditions."""
        assert get_weather_icon("Unknown") == "🌡️"

    def test_hex_to_rgba_conversion(self):
        """Test hex to rgba color conversion."""
        result = hex_to_rgba("#1f77b4", 0.1)
        assert result == "rgba(31, 119, 180, 0.1)"

        result = hex_to_rgba("#ff7f0e", 0.5)
        assert result == "rgba(255, 127, 14, 0.5)"


class TestTemperatureTrendsChart:
    """Tests for temperature trends chart."""

    def test_creates_figure(self, sample_weather_df, sample_destinations_df):
        """Test that temperature trends chart creates a figure."""
        fig = create_temperature_trends_chart(sample_weather_df, sample_destinations_df)
        assert fig is not None
        assert fig.layout.title.text == "Temperature Trends (7-Day Forecast)"

    def test_contains_temperature_data(self, sample_weather_df, sample_destinations_df):
        """Test that chart contains temperature data traces."""
        fig = create_temperature_trends_chart(sample_weather_df, sample_destinations_df)
        # Should have 3 traces per destination (high, low, avg) * 2 destinations = 6 traces
        assert len(fig.data) == 6

    def test_has_correct_axis_labels(self, sample_weather_df, sample_destinations_df):
        """Test that chart has correct axis labels."""
        fig = create_temperature_trends_chart(sample_weather_df, sample_destinations_df)
        assert fig.layout.xaxis.title.text == "Date"
        assert fig.layout.yaxis.title.text == "Temperature (°C)"


class TestRainfallChart:
    """Tests for rainfall chart."""

    def test_creates_figure(self, sample_weather_df, sample_destinations_df):
        """Test that rainfall chart creates a figure."""
        fig = create_rainfall_chart(sample_weather_df, sample_destinations_df)
        assert fig is not None
        assert fig.layout.title.text == "Daily Rainfall by Destination"

    def test_has_bar_mode(self, sample_weather_df, sample_destinations_df):
        """Test that chart uses grouped bar mode."""
        fig = create_rainfall_chart(sample_weather_df, sample_destinations_df)
        assert fig.layout.barmode == "group"


class TestUVIndexHeatmap:
    """Tests for UV index heatmap."""

    def test_creates_figure(self, sample_weather_df, sample_destinations_df):
        """Test that UV heatmap creates a figure."""
        fig = create_uv_index_heatmap(sample_weather_df, sample_destinations_df)
        assert fig is not None
        assert fig.layout.title.text == "UV Index Heatmap"

    def test_uses_heatmap_trace(self, sample_weather_df, sample_destinations_df):
        """Test that chart uses heatmap trace type."""
        fig = create_uv_index_heatmap(sample_weather_df, sample_destinations_df)
        assert len(fig.data) == 1
        assert fig.data[0].type == "heatmap"


class TestConditionsPieChart:
    """Tests for conditions pie chart."""

    def test_creates_figure(self, sample_weather_df, sample_destinations_df):
        """Test that conditions pie chart creates a figure."""
        fig = create_conditions_pie_chart(sample_weather_df, sample_destinations_df)
        assert fig is not None
        assert fig.layout.title.text == "Weather Conditions Distribution"

    def test_uses_pie_trace(self, sample_weather_df, sample_destinations_df):
        """Test that chart uses pie trace type."""
        fig = create_conditions_pie_chart(sample_weather_df, sample_destinations_df)
        assert len(fig.data) == 1
        assert fig.data[0].type == "pie"

    def test_includes_emojis_in_labels(self, sample_weather_df, sample_destinations_df):
        """Test that pie chart labels include emojis."""
        fig = create_conditions_pie_chart(sample_weather_df, sample_destinations_df)
        # Check that at least one label contains an emoji
        labels = fig.data[0].labels
        assert any("☀️" in label or "🌤️" in label for label in labels)


class TestComfortIndexChart:
    """Tests for comfort index chart."""

    def test_creates_figure(self, sample_weather_df, sample_destinations_df):
        """Test that comfort index chart creates a figure."""
        fig = create_comfort_index_chart(sample_weather_df, sample_destinations_df)
        assert fig is not None
        assert "Comfort Index" in fig.layout.title.text

    def test_scatter_mode(self, sample_weather_df, sample_destinations_df):
        """Test that chart uses scatter traces."""
        fig = create_comfort_index_chart(sample_weather_df, sample_destinations_df)
        assert len(fig.data) == 2  # Two destinations
        assert all(trace.type == "scatter" for trace in fig.data)


class TestWeatherCardsHTML:
    """Tests for weather cards HTML generation."""

    def test_creates_html_string(self, sample_weather_df, sample_destinations_df):
        """Test that weather cards creates HTML string."""
        html = create_weather_cards_html(sample_weather_df, sample_destinations_df)
        assert isinstance(html, str)
        assert len(html) > 0

    def test_contains_destination_names(
        self, sample_weather_df, sample_destinations_df
    ):
        """Test that HTML contains destination names."""
        html = create_weather_cards_html(sample_weather_df, sample_destinations_df)
        assert "Alicante" in html
        assert "Malaga" in html

    def test_contains_weather_data(self, sample_weather_df, sample_destinations_df):
        """Test that HTML contains weather data."""
        html = create_weather_cards_html(sample_weather_df, sample_destinations_df)
        # Check for temperature, humidity, rainfall, UV index emojis
        assert "🌡️" in html
        assert "💧" in html
        assert "🌧️" in html
        assert "☀️" in html

    def test_contains_weather_icons(self, sample_weather_df, sample_destinations_df):
        """Test that HTML contains weather condition icons."""
        html = create_weather_cards_html(sample_weather_df, sample_destinations_df)
        # Should contain Sunny or Clear emojis
        assert "☀️" in html or "🌤️" in html


class TestWeatherForecastIntegration:
    """Integration tests for weather forecast visualization."""

    def test_generates_html_file(self):
        """Test that main script generates HTML file."""
        from scripts.visualizations.weather_forecast import main

        # Run main and check file creation
        main()

        # Check that file exists (using same path resolution as in main)
        import scripts.visualizations.weather_forecast as wf_module

        project_root = Path(wf_module.__file__).resolve().parents[2]
        output_file = (
            project_root / ".build" / "visualizations" / "weather_forecast.html"
        )
        assert output_file.exists()

    def test_html_contains_plotly(self):
        """Test that generated HTML contains Plotly."""
        from scripts.visualizations.weather_forecast import main

        main()

        import scripts.visualizations.weather_forecast as wf_module

        project_root = Path(wf_module.__file__).resolve().parents[2]
        output_file = (
            project_root / ".build" / "visualizations" / "weather_forecast.html"
        )
        content = output_file.read_text()

        # Check for Plotly markers
        assert "plotly" in content.lower()
        assert "Weather Forecast Dashboard" in content

    def test_html_contains_all_charts(self):
        """Test that HTML contains all expected charts."""
        from scripts.visualizations.weather_forecast import main

        main()

        import scripts.visualizations.weather_forecast as wf_module

        project_root = Path(wf_module.__file__).resolve().parents[2]
        output_file = (
            project_root / ".build" / "visualizations" / "weather_forecast.html"
        )
        content = output_file.read_text()

        # Check for chart titles
        assert "Temperature Trends" in content
        assert "Daily Rainfall" in content
        assert "UV Index Heatmap" in content
        assert "Weather Conditions Distribution" in content
        assert "Comfort Index" in content

    def test_html_contains_all_42_records(self):
        """Test that HTML displays all 42 weather records."""
        from scripts.visualizations.weather_forecast import main

        main()

        import scripts.visualizations.weather_forecast as wf_module

        project_root = Path(wf_module.__file__).resolve().parents[2]
        output_file = (
            project_root / ".build" / "visualizations" / "weather_forecast.html"
        )
        content = output_file.read_text()

        # Check for data overview showing 78 records
        assert "78 total forecast records" in content
