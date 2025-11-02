"""
profile_performance.py
---------------------

Performance profiling script for Places2Go dashboard.

This script measures and reports performance metrics for:
- Data loading operations
- Chart generation
- Cache effectiveness
- Overall workflow timing

Run this script to generate a performance baseline report.
"""

import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.core.data_loader import DataLoader
from scripts.core.performance import (
    PerformanceTimer,
    get_profiler,
    cache_with_ttl,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def profile_data_loading():
    """Profile data loading operations."""
    logger.info("=" * 60)
    logger.info("PROFILING DATA LOADING")
    logger.info("=" * 60)

    loader = DataLoader()
    profiler = get_profiler()

    # Test 1: Cold load (first time, from disk)
    logger.info("\n1. Cold Load (from disk)...")
    with PerformanceTimer("cold_load_destinations"):
        destinations = loader.load_destinations()
    logger.info(f"   Loaded {len(destinations)} destinations")

    with PerformanceTimer("cold_load_costs"):
        costs = loader.load_costs(data_source="demo1")
    logger.info(f"   Loaded {len(costs)} cost records")

    with PerformanceTimer("cold_load_flights"):
        flights = loader.load_flights(data_source="demo1")
    logger.info(f"   Loaded {len(flights)} flight records")

    with PerformanceTimer("cold_load_weather"):
        weather = loader.load_weather(data_source="demo1", forecast_only=True)
    logger.info(f"   Loaded {len(weather)} weather records")

    # Test 2: Warm load (from cache)
    logger.info("\n2. Warm Load (from cache)...")
    with PerformanceTimer("warm_load_destinations"):
        destinations = loader.load_destinations()

    with PerformanceTimer("warm_load_costs"):
        costs = loader.load_costs(data_source="demo1")

    with PerformanceTimer("warm_load_flights"):
        flights = loader.load_flights(data_source="demo1")

    with PerformanceTimer("warm_load_weather"):
        weather = loader.load_weather(data_source="demo1", forecast_only=True)

    # Test 3: Load all data
    logger.info("\n3. Load All Data (merged view)...")
    with PerformanceTimer("load_all_data"):
        all_data = loader.load_all(data_source="demo1")
    logger.info(f"   Merged dataset: {len(all_data)} records")

    # Test 4: Aggregates
    logger.info("\n4. Calculate Aggregates...")
    with PerformanceTimer("calculate_aggregates"):
        stats = loader.get_aggregates(data_source="demo1")
    logger.info(f"   Generated {len(stats)} aggregate statistics")

    return profiler


def profile_caching():
    """Profile caching effectiveness."""
    logger.info("\n" + "=" * 60)
    logger.info("PROFILING CACHE EFFECTIVENESS")
    logger.info("=" * 60)

    # Simulate an expensive function with caching
    call_count = {"count": 0}

    @cache_with_ttl(ttl=60)
    def expensive_calculation(x: int) -> int:
        """Simulate expensive calculation."""
        call_count["count"] += 1
        import time

        time.sleep(0.01)  # Simulate work
        return x * x

    # Test cache hits
    logger.info("\n1. Testing cache hits...")

    with PerformanceTimer("first_call"):
        result1 = expensive_calculation(10)
    logger.info(f"   First call: {result1}, calls: {call_count['count']}")

    with PerformanceTimer("second_call"):
        result2 = expensive_calculation(10)  # Should be cached
    logger.info(f"   Second call: {result2}, calls: {call_count['count']}")

    with PerformanceTimer("third_call"):
        result3 = expensive_calculation(20)  # Different arg, new call
    logger.info(f"   Third call: {result3}, calls: {call_count['count']}")

    # Show cache statistics
    stats = expensive_calculation.cache_stats()
    logger.info("\n2. Cache Statistics:")
    logger.info(f"   Size: {stats['size']}/{stats['max_size']}")
    logger.info(f"   Hits: {stats['hits']}")
    logger.info(f"   Misses: {stats['misses']}")
    logger.info(f"   Hit Rate: {stats['hit_rate']:.2%}")


def profile_full_workflow():
    """Profile a complete workflow."""
    logger.info("\n" + "=" * 60)
    logger.info("PROFILING FULL WORKFLOW")
    logger.info("=" * 60)

    with PerformanceTimer("full_workflow"):
        # Step 1: Load all data
        logger.info("\n1. Loading all data...")
        loader = DataLoader()

        with PerformanceTimer("workflow_load_data"):
            all_data = loader.load_all(data_source="demo1")
        logger.info(f"   Loaded {len(all_data)} records")

        # Step 2: Calculate statistics
        logger.info("\n2. Calculating statistics...")
        with PerformanceTimer("workflow_calculate_stats"):
            stats = loader.get_aggregates(data_source="demo1")
        logger.info(f"   Calculated {len(stats)} metrics")

        # Step 3: Filter data
        logger.info("\n3. Filtering data...")
        with PerformanceTimer("workflow_filter_data"):
            filtered = all_data[all_data["name"].isin(["Alicante", "Malaga"])]
        logger.info(f"   Filtered to {len(filtered)} records")

        # Step 4: Group and aggregate
        logger.info("\n4. Grouping and aggregating...")
        with PerformanceTimer("workflow_group_aggregate"):
            grouped = filtered.groupby("name").agg(
                {
                    "temp_avg_c": "mean",
                    "price": "mean",
                    "monthly_living_cost": "mean",
                }
            )
        logger.info(f"   Grouped into {len(grouped)} destination summaries")


def generate_report():
    """Generate final performance report."""
    profiler = get_profiler()

    logger.info("\n" + "=" * 60)
    logger.info("PERFORMANCE REPORT")
    logger.info("=" * 60)
    logger.info("\n" + profiler.report())

    # Calculate and display key metrics
    logger.info("\n" + "=" * 60)
    logger.info("KEY PERFORMANCE METRICS")
    logger.info("=" * 60)

    # Cold vs warm load comparison
    cold_stats = profiler.get_stats("cold_load_destinations")
    warm_stats = profiler.get_stats("warm_load_destinations")

    if cold_stats and warm_stats:
        speedup = cold_stats["avg_ms"] / warm_stats["avg_ms"]
        logger.info(
            f"\nCache Speedup: {speedup:.1f}x faster "
            f"({cold_stats['avg_ms']:.2f}ms → {warm_stats['avg_ms']:.2f}ms)"
        )

    # Full workflow timing
    workflow_stats = profiler.get_stats("full_workflow")
    if workflow_stats:
        logger.info(
            f"\nFull Workflow: {workflow_stats['total_ms']:.2f}ms "
            f"(avg: {workflow_stats['avg_ms']:.2f}ms)"
        )

    # Phase 4E targets
    logger.info("\n" + "=" * 60)
    logger.info("PHASE 4E TARGET METRICS")
    logger.info("=" * 60)
    logger.info("\nCurrent Status:")

    if workflow_stats:
        workflow_seconds = workflow_stats["avg_ms"] / 1000
        logger.info(f"  ✓ Data Loading: {workflow_seconds:.2f}s (target: < 1s)")

    logger.info("\nFuture Metrics (Phase 4A - Dash App):")
    logger.info("  - First Contentful Paint: < 1.5s")
    logger.info("  - Time to Interactive: < 3s")
    logger.info("  - Lighthouse Score: > 90")
    logger.info("  - All interactions: < 100ms")

    logger.info("\n" + "=" * 60)


def main():
    """Run all performance profiling tests."""
    logger.info("Starting Performance Profiling...")
    logger.info("This will measure baseline performance for optimization.\n")

    try:
        # Run profiling tests
        profile_data_loading()
        profile_caching()
        profile_full_workflow()

        # Generate final report
        generate_report()

        logger.info("\n✅ Performance profiling completed successfully!")
        logger.info(
            "\nTo optimize further, review the report above and apply "
            "the strategies in docs/PERFORMANCE.md"
        )

    except Exception as e:
        logger.error(f"\n❌ Error during profiling: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
