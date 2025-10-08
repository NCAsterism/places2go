#!/usr/bin/env python3
"""
API Integration Demo Script

Demonstrates how to use the API data fetchers with fallback to CSV.
Run this script to test API integration functionality.
"""

import logging

from scripts.data import FlightDataFetcher, WeatherDataFetcher, CostDataFetcher
from scripts.core.data_loader import DataLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def demo_flight_api():
    """Demonstrate flight data fetcher."""
    print("\n" + "=" * 70)
    print("Flight Data API Demo")
    print("=" * 70)

    fetcher = FlightDataFetcher()

    # Get cheapest flights (will use CSV fallback without API key)
    print("\nFetching cheapest flights from EXT...")
    flights = fetcher.get_cheapest_flights(origin="EXT", limit=3)

    if not flights.empty:
        print(f"\nFound {len(flights)} flight options:")
        for _, flight in flights.head(5).iterrows():
            print(
                f"  - Destination ID {flight['destination_id']}: "
                f"£{flight['price']} ({flight.get('airline', 'N/A')})"
            )
    else:
        print("  No flight data available")


def demo_weather_api():
    """Demonstrate weather data fetcher."""
    print("\n" + "=" * 70)
    print("Weather Data API Demo")
    print("=" * 70)

    fetcher = WeatherDataFetcher()
    loader = DataLoader()

    # Get destination info
    destinations_df = loader.load_destinations()
    destinations = destinations_df.head(3).to_dict("records")

    print(f"\nFetching weather forecast for {len(destinations)} destinations...")
    weather = fetcher.fetch_forecast(destinations, days=7)

    if not weather.empty:
        print(f"\nForecast for next 7 days ({len(weather)} records):")
        for dest_id in weather["destination_id"].unique():
            dest_weather = weather[weather["destination_id"] == dest_id]
            dest_name = destinations_df[
                destinations_df["destination_id"] == dest_id
            ].iloc[0]["name"]
            avg_temp = dest_weather["temp_avg_c"].mean()
            print(f"  - {dest_name}: Average {avg_temp:.1f}°C")
    else:
        print("  No weather data available")


def demo_cost_api():
    """Demonstrate cost of living data fetcher."""
    print("\n" + "=" * 70)
    print("Cost of Living API Demo")
    print("=" * 70)

    fetcher = CostDataFetcher()
    loader = DataLoader()

    # Get destination info
    destinations_df = loader.load_destinations()
    destinations = destinations_df.head(3).to_dict("records")

    print(f"\nFetching cost of living for {len(destinations)} destinations...")
    costs = fetcher.fetch_costs(destinations)

    if not costs.empty:
        print(f"\nCost of living comparison ({len(costs)} destinations):")
        comparison = fetcher.get_cost_comparison()
        for _, row in comparison.head(5).iterrows():
            dest_name = destinations_df[
                destinations_df["destination_id"] == row["destination_id"]
            ].iloc[0]["name"]
            cost = row["monthly_living_cost"]
            print(f"  - {dest_name}: £{cost:,.0f}/month")
    else:
        print("  No cost data available")


def demo_caching():
    """Demonstrate caching behavior."""
    print("\n" + "=" * 70)
    print("Caching Demo")
    print("=" * 70)

    from scripts.data.base_api import CacheManager
    import time

    cache = CacheManager()

    print("\nTesting cache functionality...")

    # Set cache
    print("  1. Setting cache with 2 second TTL...")
    cache.set("demo_key", {"test": "data"}, ttl=2)

    # Get cache immediately
    print("  2. Getting cache immediately...")
    cached = cache.get("demo_key")
    print(f"     Result: {cached}")

    # Wait for expiry
    print("  3. Waiting 3 seconds for cache to expire...")
    time.sleep(3)

    # Try to get expired cache
    print("  4. Getting expired cache...")
    cached = cache.get("demo_key")
    print(f"     Result: {cached} (should be None)")

    # Clean up
    cache.clear()
    print("  5. Cache cleared")


def main():
    """Run all demos."""
    print("\n" + "=" * 70)
    print("API Integration Demo")
    print("=" * 70)
    print("\nThis demo shows how to use the API data fetchers.")
    print("Without API keys configured, data will fall back to CSV files.")
    print("\nTo enable real API calls:")
    print("  1. Copy .env.example to .env")
    print("  2. Add your API keys")
    print("  3. Run this script again")

    try:
        demo_flight_api()
        demo_weather_api()
        demo_cost_api()
        demo_caching()

        print("\n" + "=" * 70)
        print("Demo Complete!")
        print("=" * 70)
        print("\nNext steps:")
        print("  - Configure API keys in .env file")
        print("  - Read docs/API_INTEGRATION.md for detailed documentation")
        print("  - Run tests: pytest tests/test_api_clients.py -v")
        print()

    except Exception as e:
        logger.error(f"Demo failed: {e}", exc_info=True)
        print(f"\nError: {e}")
        print(
            "Make sure all dependencies are installed: pip install -r requirements.txt"
        )


if __name__ == "__main__":
    main()
