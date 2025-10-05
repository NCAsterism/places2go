"""
Tests for user_preferences module.
"""

import pytest
import json
from scripts.core.user_preferences import (
    UserPreferences,
    convert_currency,
    convert_temperature,
    format_currency,
    format_temperature,
    CURRENCY_RATES,
)


class TestUserPreferences:
    """Tests for UserPreferences class."""

    def test_default_values(self):
        """Test that default preferences are set correctly."""
        prefs = UserPreferences()
        assert prefs.currency == "GBP"
        assert prefs.temp_unit == "C"
        assert prefs.theme == "light"
        assert prefs.date_format == "DD/MM/YYYY"

    def test_custom_values(self):
        """Test creating preferences with custom values."""
        prefs = UserPreferences(
            currency="USD", temp_unit="F", theme="dark", date_format="MM/DD/YYYY"
        )
        assert prefs.currency == "USD"
        assert prefs.temp_unit == "F"
        assert prefs.theme == "dark"
        assert prefs.date_format == "MM/DD/YYYY"

    def test_to_dict(self):
        """Test conversion to dictionary."""
        prefs = UserPreferences(currency="EUR", temp_unit="F")
        result = prefs.to_dict()
        assert result["currency"] == "EUR"
        assert result["temp_unit"] == "F"
        assert result["theme"] == "light"
        assert result["date_format"] == "DD/MM/YYYY"

    def test_to_json(self):
        """Test conversion to JSON string."""
        prefs = UserPreferences(currency="USD")
        json_str = prefs.to_json()
        parsed = json.loads(json_str)
        assert parsed["currency"] == "USD"
        assert parsed["temp_unit"] == "C"

    def test_from_dict(self):
        """Test creating preferences from dictionary."""
        data = {"currency": "EUR", "temp_unit": "F", "theme": "dark"}
        prefs = UserPreferences.from_dict(data)
        assert prefs.currency == "EUR"
        assert prefs.temp_unit == "F"
        assert prefs.theme == "dark"
        assert prefs.date_format == "DD/MM/YYYY"  # default

    def test_from_dict_partial(self):
        """Test creating preferences from partial dictionary."""
        data = {"currency": "USD"}
        prefs = UserPreferences.from_dict(data)
        assert prefs.currency == "USD"
        assert prefs.temp_unit == "C"  # default
        assert prefs.theme == "light"  # default

    def test_from_json(self):
        """Test creating preferences from JSON string."""
        json_str = '{"currency": "USD", "temp_unit": "F"}'
        prefs = UserPreferences.from_json(json_str)
        assert prefs.currency == "USD"
        assert prefs.temp_unit == "F"

    def test_from_json_invalid(self):
        """Test handling of invalid JSON."""
        with pytest.raises(json.JSONDecodeError):
            UserPreferences.from_json("invalid json")


class TestCurrencyConversion:
    """Tests for currency conversion functions."""

    def test_same_currency(self):
        """Test conversion to same currency."""
        result = convert_currency(100, "GBP", "GBP")
        assert result == 100.0

    def test_gbp_to_usd(self):
        """Test GBP to USD conversion."""
        result = convert_currency(100, "GBP", "USD")
        assert result == 127.0

    def test_usd_to_gbp(self):
        """Test USD to GBP conversion."""
        result = convert_currency(127, "USD", "GBP")
        assert result == 100.0

    def test_gbp_to_eur(self):
        """Test GBP to EUR conversion."""
        result = convert_currency(100, "GBP", "EUR")
        assert result == 117.0

    def test_eur_to_gbp(self):
        """Test EUR to GBP conversion."""
        result = convert_currency(117, "EUR", "GBP")
        assert result == 100.0

    def test_usd_to_eur(self):
        """Test USD to EUR conversion (via GBP)."""
        result = convert_currency(127, "USD", "EUR")
        # 127 USD -> 100 GBP -> 117 EUR
        assert result == 117.0

    def test_rounding(self):
        """Test that results are rounded to 2 decimal places."""
        result = convert_currency(10.50, "GBP", "USD")
        assert result == round(10.50 * CURRENCY_RATES["USD"], 2)


class TestTemperatureConversion:
    """Tests for temperature conversion functions."""

    def test_celsius_to_celsius(self):
        """Test C to C conversion (no change)."""
        result = convert_temperature(20.0, "C")
        assert result == 20.0

    def test_celsius_to_fahrenheit(self):
        """Test C to F conversion."""
        result = convert_temperature(0.0, "F")
        assert result == 32.0

    def test_celsius_to_fahrenheit_typical(self):
        """Test typical C to F conversion."""
        result = convert_temperature(20.0, "F")
        assert result == 68.0

    def test_negative_temperature(self):
        """Test conversion of negative temperature."""
        result = convert_temperature(-10.0, "F")
        assert result == 14.0

    def test_rounding(self):
        """Test that results are rounded to 1 decimal place."""
        result = convert_temperature(25.55, "F")
        assert result == round((25.55 * 9 / 5) + 32, 1)


class TestFormatCurrency:
    """Tests for currency formatting functions."""

    def test_format_gbp(self):
        """Test GBP formatting."""
        result = format_currency(100.50, "GBP")
        assert result == "£100.50"

    def test_format_usd(self):
        """Test USD formatting."""
        result = format_currency(127.00, "USD")
        assert result == "$127.00"

    def test_format_eur(self):
        """Test EUR formatting."""
        result = format_currency(117.00, "EUR")
        assert result == "€117.00"

    def test_format_whole_number(self):
        """Test formatting whole number."""
        result = format_currency(100, "GBP")
        assert result == "£100.00"

    def test_format_many_decimals(self):
        """Test that decimals are limited to 2 places."""
        result = format_currency(100.999, "USD")
        assert result == "$101.00"


class TestFormatTemperature:
    """Tests for temperature formatting functions."""

    def test_format_celsius(self):
        """Test Celsius formatting."""
        result = format_temperature(20.5, "C")
        assert result == "20.5°C"

    def test_format_fahrenheit(self):
        """Test Fahrenheit formatting."""
        result = format_temperature(68.9, "F")
        assert result == "68.9°F"

    def test_format_negative(self):
        """Test negative temperature formatting."""
        result = format_temperature(-10.2, "C")
        assert result == "-10.2°C"

    def test_format_zero(self):
        """Test zero temperature formatting."""
        result = format_temperature(0.0, "C")
        assert result == "0.0°C"


class TestJavaScriptGeneration:
    """Tests for JavaScript code generation functions."""

    def test_preferences_javascript_not_empty(self):
        """Test that preferences JavaScript is generated."""
        from scripts.core.user_preferences import get_preferences_javascript

        result = get_preferences_javascript()
        assert len(result) > 0
        assert "PreferencesManager" in result
        assert "localStorage" in result

    def test_favorites_javascript_not_empty(self):
        """Test that favorites JavaScript is generated."""
        from scripts.core.user_preferences import get_favorites_javascript

        result = get_favorites_javascript()
        assert len(result) > 0
        assert "FavoritesManager" in result
        assert "localStorage" in result

    def test_comparison_sets_javascript_not_empty(self):
        """Test that comparison sets JavaScript is generated."""
        from scripts.core.user_preferences import get_comparison_sets_javascript

        result = get_comparison_sets_javascript()
        assert len(result) > 0
        assert "ComparisonSetsManager" in result
        assert "localStorage" in result

    def test_share_javascript_not_empty(self):
        """Test that share JavaScript is generated."""
        from scripts.core.user_preferences import get_share_javascript

        result = get_share_javascript()
        assert len(result) > 0
        assert "ShareManager" in result
        assert "URLSearchParams" in result

    def test_recent_searches_javascript_not_empty(self):
        """Test that recent searches JavaScript is generated."""
        from scripts.core.user_preferences import get_recent_searches_javascript

        result = get_recent_searches_javascript()
        assert len(result) > 0
        assert "RecentSearchesManager" in result
        assert "localStorage" in result
