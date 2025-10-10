"""
Example: Using Performance Utilities
=====================================

This example demonstrates how to use the performance optimization utilities
in a real-world scenario.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.core.data_loader import DataLoader
from scripts.core.performance import (
    cache_with_ttl,
    memoize,
    PerformanceTimer,
    get_profiler,
)


# Example 1: Caching expensive API calls
@cache_with_ttl(ttl=300)  # Cache for 5 minutes
def fetch_weather_forecast(destination_id: int):
    """
    Simulate fetching weather data from an API.
    In reality, this would make an HTTP request.
    """
    print(f"  → Fetching weather for destination {destination_id}...")
    loader = DataLoader()
    weather = loader.load_weather(data_source="demo1", forecast_only=True)
    return weather[weather["destination_id"] == destination_id]


# Example 2: Memoizing pure calculations
@memoize
def calculate_destination_score(
    avg_temp: float, flight_price: float, living_cost: float
) -> float:
    """
    Calculate a composite score for a destination.
    This is a pure function - output depends only on inputs.
    """
    print(f"  → Calculating score for temp={avg_temp}, price={flight_price}...")

    # Normalize values (dummy scoring logic)
    temp_score = min(avg_temp / 30, 1.0) * 100  # Prefer 30°C
    price_score = max(1 - (flight_price / 500), 0) * 100  # Lower is better
    cost_score = max(1 - (living_cost / 2000), 0) * 100  # Lower is better

    # Weighted average
    return temp_score * 0.3 + price_score * 0.4 + cost_score * 0.3


def main():
    """Demonstrate performance utilities usage."""
    print("=" * 70)
    print("Performance Utilities Demo")
    print("=" * 70)

    # Initialize profiler
    profiler = get_profiler()

    # Demo 1: Caching
    print("\n1. DEMONSTRATING TTL CACHE")
    print("-" * 70)

    print("\nFirst call (cache miss - slow):")
    with PerformanceTimer("fetch_weather_first"):
        weather1 = fetch_weather_forecast(1)
    print(f"   Loaded {len(weather1)} records")

    print("\nSecond call (cache hit - fast):")
    with PerformanceTimer("fetch_weather_second"):
        weather2 = fetch_weather_forecast(1)
    print(f"   Loaded {len(weather2)} records")

    # Show cache stats
    stats = fetch_weather_forecast.cache_stats()
    print(f"\n   Cache Statistics:")
    print(f"   - Hits: {stats['hits']}")
    print(f"   - Misses: {stats['misses']}")
    print(f"   - Hit Rate: {stats['hit_rate']:.1%}")

    # Demo 2: Memoization
    print("\n\n2. DEMONSTRATING MEMOIZATION")
    print("-" * 70)

    print("\nCalculating scores (first time):")
    with PerformanceTimer("calc_score_first"):
        score1 = calculate_destination_score(25.0, 150.0, 1200.0)
    print(f"   Score: {score1:.2f}")

    print("\nCalculating same score (memoized):")
    with PerformanceTimer("calc_score_second"):
        score2 = calculate_destination_score(25.0, 150.0, 1200.0)
    print(f"   Score: {score2:.2f}")

    # Demo 3: Profiling a workflow
    print("\n\n3. DEMONSTRATING PERFORMANCE PROFILING")
    print("-" * 70)

    print("\nRunning a complete data workflow...")

    with PerformanceTimer("complete_workflow"):
        # Load data
        profiler.start("load_all_data")
        loader = DataLoader()
        all_data = loader.load_all(data_source="demo1")
        profiler.end("load_all_data")

        # Calculate scores for each destination
        profiler.start("calculate_all_scores")
        scores = {}
        for _, row in all_data.head(6).iterrows():  # First 6 records
            dest = row["name"]
            if dest not in scores:
                score = calculate_destination_score(
                    row["temp_avg_c"], row["price"], row["monthly_living_cost"]
                )
                scores[dest] = score
        profiler.end("calculate_all_scores")

        print(f"\n   Processed {len(all_data)} records")
        print(f"   Calculated scores for {len(scores)} destinations")

    # Generate performance report
    print("\n\n4. PERFORMANCE REPORT")
    print("-" * 70)
    print(profiler.report())

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    workflow_stats = profiler.get_stats("complete_workflow")
    load_stats = profiler.get_stats("load_all_data")
    calc_stats = profiler.get_stats("calculate_all_scores")

    if workflow_stats and load_stats and calc_stats:
        print(f"\nComplete Workflow: {workflow_stats['total_ms']:.2f}ms")
        print(f"  - Data Loading: {load_stats['total_ms']:.2f}ms")
        print(f"  - Score Calculation: {calc_stats['total_ms']:.2f}ms")

    print("\n✅ All operations completed successfully!")
    print("\nKey Takeaways:")
    print("  • TTL caching speeds up repeated API calls")
    print("  • Memoization eliminates redundant calculations")
    print("  • Performance profiling identifies bottlenecks")
    print("  • Instrumentation adds minimal overhead")

    print("\n📚 For more information, see docs/PERFORMANCE.md")


if __name__ == "__main__":
    main()
