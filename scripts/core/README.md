# Performance Utilities

This directory contains core utilities for performance optimization in the Places2Go dashboard.

## Files

### `performance.py`
Performance optimization utilities including:
- **TTL Cache**: Time-to-live cache with automatic expiration
- **Memoization**: Permanent caching for pure functions
- **Performance Timing**: Context managers and decorators for timing code
- **Profiling**: Collect and report performance metrics

### `data_loader.py`
Enhanced DataLoader with performance instrumentation:
- In-memory caching of CSV data
- Performance timing on all load operations
- Automatic profiler integration

## Quick Start

### Using TTL Cache

```python
from scripts.core.performance import cache_with_ttl

@cache_with_ttl(ttl=300)  # Cache for 5 minutes
def fetch_api_data(endpoint):
    return expensive_api_call(endpoint)

# First call - fetches from API
data = fetch_api_data("/flights")

# Second call - returns from cache
data = fetch_api_data("/flights")  # Fast!
```

### Using Memoization

```python
from scripts.core.performance import memoize

@memoize
def calculate_score(temp, humidity, price):
    """Pure function - results cached forever."""
    return complex_calculation(temp, humidity, price)
```

### Timing Code

```python
from scripts.core.performance import PerformanceTimer

with PerformanceTimer("data_processing") as timer:
    result = process_large_dataset()

print(f"Processing took {timer.elapsed_ms:.2f}ms")
```

### Performance Profiling

```python
from scripts.core.performance import get_profiler

profiler = get_profiler()

profiler.start("load_data")
data = load_data()
profiler.end("load_data")

# Generate report
print(profiler.report())
```

## Running Performance Profiling

To generate a performance baseline report:

```bash
python scripts/profile_performance.py
```

This will:
1. Profile data loading (cold and warm loads)
2. Test cache effectiveness
3. Profile a complete workflow
4. Generate a comprehensive report

## Documentation

For comprehensive performance optimization guidance, see:
- `docs/PERFORMANCE.md` - Complete performance guide
- `tests/test_performance.py` - Usage examples and tests

## Phase 4E Integration

These utilities support Phase 4E objectives:
- ✅ Data caching with TTL
- ✅ Performance measurement and profiling
- ✅ Optimization framework ready for Dash app
- ⏳ Future: Debouncing, lazy loading (Phase 4A required)

## Testing

All performance utilities have comprehensive test coverage:

```bash
pytest tests/test_performance.py -v
```

Coverage: 99% (147/149 statements)
