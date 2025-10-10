#!/usr/bin/env python3
"""
Demo script showing Phase 4C user preferences features.

This script demonstrates the key functionality of the user preferences
module without requiring a full visualization.
"""







from .core.user_preferences import (
    UserPreferences,
    convert_currency,
    convert_temperature,
    format_currency,
    format_temperature,
    CURRENCY_RATES,
)


def print_section(title: str) -> None:
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def demo_preferences() -> None:
    """Demonstrate UserPreferences class."""
    print_section("1. User Preferences")

    # Default preferences
    prefs = UserPreferences()
    print("Default preferences:")
    print(f"  Currency: {prefs.currency}")
    print(f"  Temperature Unit: {prefs.temp_unit}")
    print(f"  Theme: {prefs.theme}")
    print(f"  Date Format: {prefs.date_format}")

    # Custom preferences
    custom_prefs = UserPreferences(currency="USD", temp_unit="F", theme="dark")
    print("\nCustom preferences (US traveler):")
    print(f"  Currency: {custom_prefs.currency}")
    print(f"  Temperature Unit: {custom_prefs.temp_unit}")
    print(f"  Theme: {custom_prefs.theme}")

    # JSON serialization
    json_str = custom_prefs.to_json()
    print(f"\nJSON representation:\n  {json_str}")

    # Restore from JSON
    restored = UserPreferences.from_json(json_str)
    print(f"\nRestored from JSON:")
    print(f"  Currency: {restored.currency}")


def demo_currency_conversion() -> None:
    """Demonstrate currency conversion."""
    print_section("2. Currency Conversion")

    amounts = [100, 250, 1000]

    print("Exchange rates (base: GBP):")
    for currency, rate in CURRENCY_RATES.items():
        print(f"  1 GBP = {rate:.2f} {currency}")

    print("\nConversion examples:")
    for amount in amounts:
        usd = convert_currency(amount, "GBP", "USD")
        eur = convert_currency(amount, "GBP", "EUR")
        print(f"  £{amount} → ${usd:.2f} USD / €{eur:.2f} EUR")

    # Round-trip conversion
    print("\nRound-trip conversion (GBP → USD → GBP):")
    original = 100
    to_usd = convert_currency(original, "GBP", "USD")
    back_to_gbp = convert_currency(to_usd, "USD", "GBP")
    print(f"  £{original} → ${to_usd:.2f} → £{back_to_gbp:.2f}")


def demo_temperature_conversion() -> None:
    """Demonstrate temperature conversion."""
    print_section("3. Temperature Conversion")

    temps_c = [0, 10, 20, 25, 30]

    print("Temperature conversions:")
    for temp in temps_c:
        temp_f = convert_temperature(temp, "F")
        print(f"  {temp}°C = {temp_f:.1f}°F")

    # Formatting
    print("\nFormatted temperatures:")
    for temp in temps_c:
        temp_f = convert_temperature(temp, "F")
        print(
            f"  {format_temperature(temp, 'C')} = {format_temperature(temp_f, 'F')}"
        )


def demo_formatting() -> None:
    """Demonstrate formatting functions."""
    print_section("4. Formatting")

    amount = 1234.56
    temp = 22.7

    print("Currency formatting:")
    print(f"  {amount} → {format_currency(amount, 'GBP')}")
    print(f"  {amount} → {format_currency(amount, 'USD')}")
    print(f"  {amount} → {format_currency(amount, 'EUR')}")

    print("\nTemperature formatting:")
    print(f"  {temp} → {format_temperature(temp, 'C')}")
    print(f"  {temp} → {format_temperature(temp, 'F')}")


def demo_real_world_scenario() -> None:
    """Demonstrate a real-world scenario."""
    print_section("5. Real-World Scenario")

    print("Barcelona Trip Cost Comparison\n")

    # Trip costs in GBP
    flight_cost_gbp = 150
    hotel_per_night_gbp = 80
    daily_food_gbp = 40
    nights = 5

    total_gbp = flight_cost_gbp + (hotel_per_night_gbp * nights) + (daily_food_gbp * nights)

    # Average temperature in Barcelona (Celsius)
    avg_temp_c = 24

    # UK traveler (default preferences)
    print("UK Traveler (GBP, Celsius):")
    print(f"  Flight: {format_currency(flight_cost_gbp, 'GBP')}")
    print(f"  Hotel ({nights} nights): {format_currency(hotel_per_night_gbp * nights, 'GBP')}")
    print(f"  Food ({nights} days): {format_currency(daily_food_gbp * nights, 'GBP')}")
    print(f"  Total: {format_currency(total_gbp, 'GBP')}")
    print(f"  Average temp: {format_temperature(avg_temp_c, 'C')}")

    # US traveler (USD, Fahrenheit)
    print("\nUS Traveler (USD, Fahrenheit):")
    flight_cost_usd = convert_currency(flight_cost_gbp, "GBP", "USD")
    hotel_cost_usd = convert_currency(hotel_per_night_gbp * nights, "GBP", "USD")
    food_cost_usd = convert_currency(daily_food_gbp * nights, "GBP", "USD")
    total_usd = convert_currency(total_gbp, "GBP", "USD")
    avg_temp_f = convert_temperature(avg_temp_c, "F")

    print(f"  Flight: {format_currency(flight_cost_usd, 'USD')}")
    print(f"  Hotel ({nights} nights): {format_currency(hotel_cost_usd, 'USD')}")
    print(f"  Food ({nights} days): {format_currency(food_cost_usd, 'USD')}")
    print(f"  Total: {format_currency(total_usd, 'USD')}")
    print(f"  Average temp: {format_temperature(avg_temp_f, 'F')}")

    # European traveler (EUR, Celsius)
    print("\nEuropean Traveler (EUR, Celsius):")
    total_eur = convert_currency(total_gbp, "GBP", "EUR")
    print(f"  Total: {format_currency(total_eur, 'EUR')}")
    print(f"  Average temp: {format_temperature(avg_temp_c, 'C')}")


def main() -> None:
    """Run all demonstrations."""
    print("\n" + "=" * 60)
    print("  Phase 4C: User Preferences Demo")
    print("  Places2Go - Destination Dashboard")
    print("=" * 60)

    demo_preferences()
    demo_currency_conversion()
    demo_temperature_conversion()
    demo_formatting()
    demo_real_world_scenario()

    print("\n" + "=" * 60)
    print("  Demo Complete!")
    print("=" * 60)
    print("\nTry the enhanced visualization:")
    print("  python scripts/visualizations/weather_forecast_enhanced.py")
    print("  open .build/visualizations/weather_forecast_enhanced.html")
    print()


if __name__ == "__main__":
    main()
