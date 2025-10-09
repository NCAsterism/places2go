"""
Tests to verify Alicante weather forecast data for Oct 11-17, 2025.

This test suite verifies that weather data for Alicante (destination_id=1)
exists for the period Oct 11-17, 2025 with all required fields as specified
in issue #48.
"""

import pytest
import pandas as pd
from scripts.core.data_loader import DataLoader


class TestAlicanteWeatherForecast:
    """Test suite for Alicante weather forecast data (Oct 11-17, 2025)."""

    @pytest.fixture
    def data_loader(self):
        """Create DataLoader instance."""
        return DataLoader()

    @pytest.fixture
    def alicante_weather(self, data_loader):
        """Load Alicante weather data for Oct 11-17, 2025."""
        weather_df = data_loader.load_weather(forecast_only=True)
        # Filter for Alicante (destination_id=1) Oct 11-17, 2025
        mask = (
            (weather_df["destination_id"] == 1)
            & (weather_df["date"] >= pd.to_datetime("2025-10-11"))
            & (weather_df["date"] <= pd.to_datetime("2025-10-17"))
        )
        return weather_df[mask].sort_values("date")

    def test_seven_days_of_data_exist(self, alicante_weather):
        """Verify exactly 7 days of forecast data exist."""
        assert len(alicante_weather) == 7, "Should have 7 days of forecast data"

    def test_date_range_is_correct(self, alicante_weather):
        """Verify the date range is Oct 11-17, 2025."""
        dates = alicante_weather["date"].dt.date.tolist()
        expected_dates = [
            pd.to_datetime(f"2025-10-{day}").date() for day in range(11, 18)
        ]
        assert dates == expected_dates, "Dates should be Oct 11-17, 2025"

    def test_all_required_fields_present(self, alicante_weather):
        """Verify all required fields are present and not null."""
        required_fields = [
            "temp_high_c",
            "temp_low_c",
            "temp_avg_c",
            "rainfall_mm",
            "humidity_percent",
            "sunshine_hours",
            "wind_speed_kmh",
            "conditions",
            "uv_index",
            "forecast_flag",
        ]

        for field in required_fields:
            assert field in alicante_weather.columns, f"Field {field} should exist"
            assert (
                not alicante_weather[field].isna().any()
            ), f"Field {field} should not have null values"

    def test_forecast_flag_is_true(self, alicante_weather):
        """Verify all records are marked as forecasts."""
        assert alicante_weather[
            "forecast_flag"
        ].all(), "All records should be forecasts (forecast_flag=True)"

    def test_destination_id_is_alicante(self, alicante_weather):
        """Verify all records are for Alicante (destination_id=1)."""
        assert (
            alicante_weather["destination_id"] == 1
        ).all(), "All records should be for Alicante (destination_id=1)"

    def test_temperature_values_are_reasonable(self, alicante_weather):
        """Verify temperature values are reasonable for Alicante in Oct."""
        # Based on climatological data for Alicante in October
        # High: typically 20-28°C, Low: typically 11-19°C
        assert (
            alicante_weather["temp_high_c"].min() >= 20
        ), "High temps should be at least 20°C"
        assert (
            alicante_weather["temp_high_c"].max() <= 30
        ), "High temps should be at most 30°C"
        assert (
            alicante_weather["temp_low_c"].min() >= 10
        ), "Low temps should be at least 10°C"
        assert (
            alicante_weather["temp_low_c"].max() <= 20
        ), "Low temps should be at most 20°C"

    def test_temperature_high_greater_than_low(self, alicante_weather):
        """Verify high temperature is greater than low temperature."""
        assert (
            alicante_weather["temp_high_c"] >= alicante_weather["temp_low_c"]
        ).all(), "High temp should be >= low temp"

    def test_humidity_in_valid_range(self, alicante_weather):
        """Verify humidity is between 0-100%."""
        assert (
            alicante_weather["humidity_percent"].min() >= 0
        ), "Humidity should be >= 0%"
        assert (
            alicante_weather["humidity_percent"].max() <= 100
        ), "Humidity should be <= 100%"

    def test_sunshine_hours_in_valid_range(self, alicante_weather):
        """Verify sunshine hours are between 0-24."""
        assert (
            alicante_weather["sunshine_hours"].min() >= 0
        ), "Sunshine hours should be >= 0"
        assert (
            alicante_weather["sunshine_hours"].max() <= 24
        ), "Sunshine hours should be <= 24"

    def test_uv_index_in_valid_range(self, alicante_weather):
        """Verify UV index is in valid range (0-11+)."""
        assert alicante_weather["uv_index"].min() >= 0, "UV index should be >= 0"
        # UV index can go above 11, but typically <= 15
        assert alicante_weather["uv_index"].max() <= 15, "UV index should be <= 15"

    def test_rainfall_is_non_negative(self, alicante_weather):
        """Verify rainfall is non-negative."""
        assert (alicante_weather["rainfall_mm"] >= 0).all(), "Rainfall should be >= 0"

    def test_wind_speed_is_positive(self, alicante_weather):
        """Verify wind speed is positive."""
        assert (
            alicante_weather["wind_speed_kmh"] > 0
        ).all(), "Wind speed should be > 0"

    def test_conditions_field_is_populated(self, alicante_weather):
        """Verify conditions field contains descriptions."""
        assert (
            not alicante_weather["conditions"].isna().any()
        ), "Conditions should not be null"
        assert (
            alicante_weather["conditions"].str.len() > 0
        ).all(), "Conditions should not be empty"

    def test_data_source_is_documented(self, alicante_weather):
        """Verify data source is specified."""
        assert (
            not alicante_weather["data_source"].isna().any()
        ), "Data source should not be null"
        # The data source should be "climatology_oct2025" based on the documentation
        assert (
            alicante_weather["data_source"].unique()[0] == "climatology_oct2025"
        ), "Data source should be climatology_oct2025"

    def test_weather_ids_are_unique(self, alicante_weather):
        """Verify each record has a unique weather_id."""
        weather_ids = alicante_weather["weather_id"].tolist()
        assert len(weather_ids) == len(
            set(weather_ids)
        ), "All weather_ids should be unique"

    def test_data_matches_climatological_expectations(self, alicante_weather):
        """Verify data aligns with Alicante October climate characteristics."""
        # Based on WEATHER_SOURCES_OCT2025.md:
        # Average High: 24°C, Average Low: 15°C, Humidity: 65%, UV: 6
        avg_high = alicante_weather["temp_high_c"].mean()
        avg_low = alicante_weather["temp_low_c"].mean()
        avg_humidity = alicante_weather["humidity_percent"].mean()

        # Allow reasonable variation (±3°C for temps, ±10% for humidity)
        assert 21 <= avg_high <= 27, f"Average high {avg_high:.1f}°C should be ~24°C"
        assert 12 <= avg_low <= 18, f"Average low {avg_low:.1f}°C should be ~15°C"
        assert (
            55 <= avg_humidity <= 75
        ), f"Average humidity {avg_humidity:.1f}% should be ~65%"
