# Performance Optimization Guide

## Overview

This document provides comprehensive guidance on performance optimization for the Places2Go dashboard application, supporting Phase 4E objectives.

## Performance Utilities

The `scripts/core/performance.py` module provides a suite of utilities for optimizing application performance:

### 1. TTL Cache (`cache_with_ttl`)

Cache function results with automatic expiration:

```python
from scripts.core.performance import cache_with_ttl

@cache_with_ttl(ttl=300)  # Cache for 5 minutes
def fetch_flight_prices(origin: str, dest: str):
    """Expensive API call - results cached."""
    return api.get_flight_prices(origin, dest)
```

**Use Cases:**
- API response caching
- Database query results
- Expensive calculations with time-sensitive data

**Benefits:**
- Reduces API calls and database queries
- Configurable TTL per function
- Automatic cache invalidation
- LRU eviction when cache is full

### 2. Memoization (`memoize`)

Cache pure function results permanently:

```python
from scripts.core.performance import memoize

@memoize
def calculate_comfort_index(temp: float, humidity: float, wind: float) -> float:
    """Pure function - results never expire."""
    return complex_calculation(temp, humidity, wind)
```

**Use Cases:**
- Pure mathematical functions
- Deterministic transformations
- Configuration parsing
- Data validation

**Benefits:**
- Zero overhead after first call
- Unlimited cache lifetime
- Perfect for deterministic functions

### 3. Performance Timing (`PerformanceTimer`)

Measure execution time of code blocks:

```python
from scripts.core.performance import PerformanceTimer

with PerformanceTimer("load_large_dataset") as timer:
    data = pd.read_csv('large_file.csv')
    data = preprocess(data)

print(f"Loading took {timer.elapsed_ms:.2f}ms")
```

**Use Cases:**
- Measuring critical sections
- Identifying bottlenecks
- Performance regression testing
- Development profiling

### 4. Function Timing Decorator (`@timed`)

Automatically log function execution time:

```python
from scripts.core.performance import timed

@timed
def process_weather_data(df):
    """Function execution time logged automatically."""
    return df.groupby('destination').agg({
        'temperature': 'mean',
        'rainfall': 'sum'
    })
```

### 5. Performance Profiler (`PerformanceProfiler`)

Collect and analyze performance metrics:

```python
from scripts.core.performance import get_profiler

profiler = get_profiler()

# Start timing an operation
profiler.start("load_data")
data = load_data()
profiler.end("load_data")

# Record multiple instances
for destination in destinations:
    profiler.start("process_destination")
    process(destination)
    profiler.end("process_destination")

# Generate report
print(profiler.report())
```

**Report Output:**
```
Performance Profile Report
==================================================

load_data:
  Count: 5
  Total: 2534.56ms
  Avg:   506.91ms
  Min:   487.23ms
  Max:   542.18ms

process_destination:
  Count: 42
  Total: 1284.37ms
  Avg:   30.58ms
  Min:   24.12ms
  Max:   45.67ms
```

## Current Optimizations

### DataLoader Performance

The `DataLoader` class implements several optimizations:

1. **In-Memory Caching**
   - CSV files loaded once and cached
   - Subsequent calls return cached DataFrames
   - `reload=True` parameter forces refresh

2. **Performance Instrumentation**
   - All load operations timed automatically
   - Metrics recorded in global profiler
   - Enable debug logging to see timing

3. **Efficient Filtering**
   - Filtering done on cached DataFrames
   - No re-reading from disk
   - Copy-on-return prevents mutation

**Example Usage:**
```python
from scripts.core.data_loader import DataLoader
from scripts.core.performance import get_profiler

loader = DataLoader()

# First call - reads from disk (slower)
destinations = loader.load_destinations()

# Subsequent calls - from cache (fast)
destinations = loader.load_destinations()

# View performance metrics
profiler = get_profiler()
print(profiler.report())
```

## Phase 4A Dash App Optimizations

When implementing the Dash framework (Phase 4A), apply these optimizations:

### 1. Callback Optimization

**Debounce Filter Inputs:**
```python
from dash import Input, Output, State
from dash.exceptions import PreventUpdate

@app.callback(
    Output('graph', 'figure'),
    Input('filter-input', 'value'),
    prevent_initial_call=True
)
def update_graph(filter_value):
    """Debounced via Dash's built-in mechanisms."""
    if not filter_value:
        raise PreventUpdate
    
    return create_figure(filter_value)
```

**Use `prevent_initial_call`:**
```python
@app.callback(
    Output('expensive-graph', 'figure'),
    Input('trigger', 'n_clicks'),
    prevent_initial_call=True  # Don't run on page load
)
def update_expensive_graph(n_clicks):
    return expensive_calculation()
```

### 2. Data Loading Strategy

**Pre-load Common Data:**
```python
from scripts.core.performance import cache_with_ttl

# Cache shared data for all callbacks
@cache_with_ttl(ttl=3600)  # 1 hour
def get_destinations_data():
    loader = DataLoader()
    return loader.load_all(data_source='live')

@app.callback(...)
def update_chart_1(...):
    data = get_destinations_data()  # From cache
    return process_chart_1(data)

@app.callback(...)
def update_chart_2(...):
    data = get_destinations_data()  # From cache
    return process_chart_2(data)
```

### 3. Lazy Loading Charts

**Load Charts on Tab Selection:**
```python
@app.callback(
    Output('tab-content', 'children'),
    Input('tabs', 'value')
)
def render_tab_content(active_tab):
    """Only render active tab's charts."""
    if active_tab == 'weather':
        return generate_weather_charts()
    elif active_tab == 'flights':
        return generate_flight_charts()
    # Other tabs not rendered until selected
```

### 4. Memoization in Callbacks

**Cache Expensive Calculations:**
```python
from scripts.core.performance import memoize

@memoize
def calculate_destination_scores(filters):
    """Expensive calculation - memoized."""
    scores = {}
    for dest in destinations:
        scores[dest] = complex_scoring(dest, filters)
    return scores

@app.callback(...)
def update_rankings(filters):
    scores = calculate_destination_scores(tuple(filters))  # Cached
    return create_ranking_table(scores)
```

## Target Metrics (Phase 4E)

### Loading Performance
- **First Contentful Paint:** < 1.5s
- **Time to Interactive:** < 3s
- **Lighthouse Score:** > 90

**Optimization Strategies:**
1. Code splitting (separate bundle per route)
2. Lazy loading of Plotly charts
3. Minified CSS/JS assets
4. gzip/brotli compression on server

### Data Performance
- **Query response time:** < 100ms for cached data
- **API calls:** < 2s with 5-minute cache
- **Database queries:** < 50ms with proper indexing

**Optimization Strategies:**
1. Aggressive caching with TTL
2. Database indexes on frequently queried columns
3. Pagination for large result sets
4. CDN for static assets

### Runtime Performance
- **Filter updates:** < 100ms
- **Chart rendering:** < 500ms
- **All interactions:** < 100ms

**Optimization Strategies:**
1. Debounced filter inputs (300ms delay)
2. Memoization of calculations
3. Virtual scrolling for long lists
4. Web Workers for heavy processing (future)

## Measuring Performance

### Development Profiling

```python
from scripts.core.performance import get_profiler, PerformanceTimer

# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run your code
with PerformanceTimer("full_workflow"):
    loader = DataLoader()
    data = loader.load_all(data_source='demo1')
    charts = generate_all_charts(data)

# View profiling report
profiler = get_profiler()
print(profiler.report())
```

### Production Monitoring

For Phase 4D deployment, integrate monitoring:

1. **Application Insights** (Azure)
   - Track response times
   - Monitor error rates
   - User session tracking

2. **Custom Metrics**
   - Cache hit rates
   - Query execution times
   - API call latency

3. **Alerting**
   - Response time > 5s
   - Error rate > 1%
   - Cache hit rate < 80%

## Best Practices

### 1. Cache Appropriately

✅ **DO:**
- Cache API responses (TTL: 5-60 minutes)
- Cache database queries (TTL: 1-10 minutes)
- Memoize pure calculations (no TTL)
- Cache user preferences (TTL: 1 hour)

❌ **DON'T:**
- Cache real-time data too long
- Cache user-specific data globally
- Over-cache (wastes memory)

### 2. Measure Before Optimizing

✅ **DO:**
- Profile first to identify bottlenecks
- Use PerformanceTimer for critical paths
- Track metrics over time
- Set performance budgets

❌ **DON'T:**
- Optimize without measuring
- Assume what's slow
- Optimize prematurely

### 3. Optimize Incrementally

✅ **DO:**
- Fix biggest bottlenecks first
- Measure impact of each change
- Keep optimizations simple
- Document performance decisions

❌ **DON'T:**
- Over-engineer solutions
- Sacrifice code clarity
- Optimize everything at once

## Performance Testing

Add performance tests to catch regressions:

```python
import pytest
from scripts.core.performance import PerformanceTimer

def test_data_loading_performance():
    """Ensure data loading stays under threshold."""
    with PerformanceTimer("test_load") as timer:
        loader = DataLoader()
        data = loader.load_all(data_source='demo1')
    
    # Should load in under 1 second
    assert timer.elapsed_seconds < 1.0

def test_chart_generation_performance():
    """Ensure chart generation is fast enough."""
    with PerformanceTimer("test_chart") as timer:
        chart = create_weather_chart(sample_data)
    
    # Should generate in under 500ms
    assert timer.elapsed_ms < 500
```

## Future Enhancements

### Phase 5: Advanced Optimizations

1. **Database Indexing**
   ```sql
   CREATE INDEX idx_destinations_cost ON destinations(flight_cost_gbp);
   CREATE INDEX idx_weather_date ON weather_data(forecast_date);
   CREATE INDEX idx_flights_departure ON flight_prices(departure_date);
   ```

2. **Async Data Loading**
   ```python
   import asyncio
   import httpx

   async def fetch_all_destinations():
       async with httpx.AsyncClient() as client:
           tasks = [fetch_destination(client, dest) for dest in dests]
           return await asyncio.gather(*tasks)
   ```

3. **Web Workers** (for browser-side processing)
   ```javascript
   // Heavy calculation in Web Worker
   const worker = new Worker('calculations.js');
   worker.postMessage(largeDataset);
   worker.onmessage = (e) => {
       updateChart(e.data);
   };
   ```

4. **Service Workers** (for offline caching)
   ```javascript
   // Cache API responses for offline use
   self.addEventListener('fetch', (event) => {
       event.respondWith(
           caches.match(event.request).then((response) => {
               return response || fetch(event.request);
           })
       );
   });
   ```

## Resources

- **Plotly Performance:** https://plotly.com/python/performance/
- **Dash Performance:** https://dash.plotly.com/performance
- **Python Performance Tips:** https://wiki.python.org/moin/PythonSpeed
- **Web Performance Best Practices:** https://web.dev/fast/

## Monitoring Dashboard (Future)

For Phase 4D, create a performance monitoring dashboard:

```python
# Performance metrics endpoint
@app.route('/api/metrics')
def get_metrics():
    profiler = get_profiler()
    
    # Get cache statistics
    cache_stats = {
        'destinations': loader.load_destinations.cache_stats(),
        'flights': fetch_flights.cache_stats(),
    }
    
    return {
        'profiler': profiler.report(),
        'cache': cache_stats,
        'memory': get_memory_usage(),
    }
```

Display in admin dashboard:
- Response time trends
- Cache hit rates
- Error rates
- User experience metrics

---

**Last Updated:** Phase 4E Implementation  
**Next Review:** After Phase 4A (Dash app) completion
