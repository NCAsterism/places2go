#!/usr/bin/env python3
"""
DataLoader demonstration script.

Shows how to use the DataLoader class to load and work with the new CSV structure.
Run this script to see examples of all DataLoader features.
"""

from scripts.core.data_loader import DataLoader, load_data


def main():
    """Demonstrate DataLoader features."""
    print("=" * 70)
    print("DataLoader Demonstration")
    print("=" * 70)
    print()

    # Initialize loader
    print("1. Initializing DataLoader...")
    loader = DataLoader()
    print("   ✓ DataLoader initialized")
    print()

    # Load destinations
    print("2. Loading destinations...")
    destinations = loader.load_destinations()
    print(f"   ✓ Loaded {len(destinations)} destinations:")
    for _, dest in destinations.iterrows():
        print(f"     - {dest['name']}, {dest['country']} ({dest['airport_code']})")
    print()

    # Load costs
    print("3. Loading cost of living data...")
    costs = loader.load_costs(data_source="demo1")
    print(f"   ✓ Loaded costs for {len(costs)} destinations")
    print(f"   Average monthly cost: £{costs['monthly_living_cost'].mean():.0f}")
    print(
        f"   Range: £{costs['monthly_living_cost'].min():.0f} - £{costs['monthly_living_cost'].max():.0f}"
    )
    print()

    # Load flights
    print("4. Loading flight data...")
    flights = loader.load_flights(data_source="demo1")
    print(f"   ✓ Loaded {len(flights)} flight records")
    print(f"   Average price: £{flights['price'].mean():.2f}")
    print(f"   Cheapest: £{flights['price'].min():.2f}")
    print(f"   Most expensive: £{flights['price'].max():.2f}")
    print()

    # Load weather
    print("5. Loading weather data...")
    weather = loader.load_weather(data_source="demo1", forecast_only=True)
    print(f"   ✓ Loaded {len(weather)} weather forecasts")
    print(
        f"   Temperature range: {weather['temp_low_c'].min()}°C - {weather['temp_high_c'].max()}°C"
    )
    print(f"   Average: {weather['temp_avg_c'].mean():.1f}°C")
    print()

    # Filter flights by date
    print("6. Filtering flights by departure date...")
    oct_11_13 = loader.load_flights(
        data_source="demo1", departure_date_range=("2025-10-11", "2025-10-13")
    )
    print(f"   ✓ Found {len(oct_11_13)} flights departing Oct 11-13")
    print(f"   Average price for this period: £{oct_11_13['price'].mean():.2f}")
    print()

    # Get aggregates
    print("7. Computing aggregate statistics...")
    aggregates = loader.get_aggregates(data_source="demo1")
    print(f"   ✓ Computed stats for {len(aggregates)} destinations")
    print()
    print("   Destination Summary:")
    print("   " + "-" * 66)
    print(f"   {'Destination':<20} {'Avg Flight':<12} {'Avg Temp':<12} {'Cost/Mo':<12}")
    print("   " + "-" * 66)
    for _, row in aggregates.iterrows():
        avg_price = (
            f"£{row.get('avg_flight_price', 0):.0f}"
            if "avg_flight_price" in row
            else "N/A"
        )
        avg_temp = f"{row.get('avg_temp', 0):.1f}°C" if "avg_temp" in row else "N/A"
        cost = (
            f"£{row.get('monthly_living_cost', 0):.0f}"
            if "monthly_living_cost" in row
            else "N/A"
        )
        print(f"   {row['name']:<20} {avg_price:<12} {avg_temp:<12} {cost:<12}")
    print()

    # Load all data merged
    print("8. Loading merged dataset...")
    all_data = loader.load_all(data_source="demo1")
    print(f"   ✓ Merged dataset has {len(all_data)} rows")
    print(f"   ✓ Contains {len(all_data.columns)} columns")
    print()

    # Check available data sources
    print("9. Checking available data sources...")
    sources = loader.get_available_data_sources()
    print("   ✓ Available data sources:")
    for dataset, source_list in sources.items():
        print(f"     - {dataset}: {', '.join(source_list)}")
    print()

    # Convenience function
    print("10. Using convenience function...")
    quick_data = load_data(data_source="demo1", merge=True)
    print(
        f"    ✓ Quick load: {len(quick_data)} rows, {len(quick_data.columns)} columns"
    )
    print()

    print("=" * 70)
    print("Demonstration complete!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  - Explore the DataLoader API in scripts/core/data_loader.py")
    print("  - Read data/README.md for schema documentation")
    print("  - Run tests with: pytest tests/test_data_loader.py -v")
    print()


if __name__ == "__main__":
    main()
