"""
performance.py
--------------

Performance optimization utilities for the Places2Go dashboard.

This module provides:
- Caching decorators with TTL support
- Memoization for expensive calculations
- Performance profiling tools
- Timing utilities
- Memory usage tracking

These utilities support the Phase 4E performance optimization objectives:
- Loading performance optimization
- Data query optimization
- Runtime performance improvements
"""

import functools
import logging
import time
from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, Optional, TypeVar

logger = logging.getLogger(__name__)

# Type variable for generic function decoration
F = TypeVar("F", bound=Callable[..., Any])


class CacheEntry:
    """Represents a cached value with expiration time."""

    def __init__(self, value: Any, ttl_seconds: int):
        self.value = value
        self.expiry = datetime.now() + timedelta(seconds=ttl_seconds)

    def is_expired(self) -> bool:
        """Check if the cache entry has expired."""
        return datetime.now() > self.expiry


class TTLCache:
    """
    Time-To-Live cache with automatic expiration.

    Args:
        max_size: Maximum number of entries to store (LRU eviction)
        default_ttl: Default time-to-live in seconds
    """

    def __init__(self, max_size: int = 128, default_ttl: int = 3600):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired."""
        if key in self._cache:
            entry = self._cache[key]
            if not entry.is_expired():
                # Move to end (most recently used)
                self._cache.move_to_end(key)
                self._hits += 1
                return entry.value
            else:
                # Remove expired entry
                del self._cache[key]

        self._misses += 1
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache with TTL."""
        if ttl is None:
            ttl = self.default_ttl

        # Remove oldest entry if cache is full
        if len(self._cache) >= self.max_size and key not in self._cache:
            self._cache.popitem(last=False)

        self._cache[key] = CacheEntry(value, ttl)
        self._cache.move_to_end(key)

    def clear(self):
        """Clear all cache entries."""
        self._cache.clear()
        self._hits = 0
        self._misses = 0

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_requests = self._hits + self._misses
        hit_rate = self._hits / total_requests if total_requests > 0 else 0

        return {
            "size": len(self._cache),
            "max_size": self.max_size,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": hit_rate,
        }


def cache_with_ttl(ttl: int = 3600, max_size: int = 128):
    """
    Decorator to cache function results with time-to-live.

    Args:
        ttl: Time-to-live in seconds (default: 1 hour)
        max_size: Maximum cache size (default: 128)

    Example:
        >>> @cache_with_ttl(ttl=300)  # Cache for 5 minutes
        ... def fetch_flight_prices(origin: str, dest: str):
        ...     return expensive_api_call(origin, dest)
    """

    def decorator(func: F) -> F:
        cache = TTLCache(max_size=max_size, default_ttl=ttl)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}:{str(args)}:{str(sorted(kwargs.items()))}"

            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return result

            # Cache miss - call function
            logger.debug(f"Cache miss for {func.__name__}")
            result = func(*args, **kwargs)

            # Store in cache
            cache.set(cache_key, result, ttl)

            return result

        # Add cache management methods
        wrapper.cache = cache  # type: ignore
        wrapper.clear_cache = cache.clear  # type: ignore
        wrapper.cache_stats = cache.get_stats  # type: ignore

        return wrapper  # type: ignore

    return decorator


def memoize(func: F) -> F:
    """
    Simple memoization decorator for deterministic functions.

    Unlike cache_with_ttl, this never expires entries (unlimited TTL).
    Use for pure functions with deterministic outputs.

    Example:
        >>> @memoize
        ... def calculate_comfort_index(temp: float, humidity: float) -> float:
        ...     return complex_calculation(temp, humidity)
    """
    cache: Dict[str, Any] = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cache_key = f"{str(args)}:{str(sorted(kwargs.items()))}"

        if cache_key not in cache:
            cache[cache_key] = func(*args, **kwargs)

        return cache[cache_key]

    wrapper.cache = cache  # type: ignore
    wrapper.clear_cache = cache.clear  # type: ignore

    return wrapper  # type: ignore


class PerformanceTimer:
    """
    Context manager for timing code blocks.

    Example:
        >>> with PerformanceTimer("data_loading") as timer:
        ...     data = load_large_dataset()
        >>> print(f"Took {timer.elapsed_ms:.2f}ms")
    """

    def __init__(self, name: str, log_level: int = logging.INFO):
        self.name = name
        self.log_level = log_level
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        logger.log(
            self.log_level,
            f"{self.name} took {self.elapsed_ms:.2f}ms",
        )

    @property
    def elapsed_seconds(self) -> float:
        """Get elapsed time in seconds."""
        if self.start_time is None or self.end_time is None:
            return 0.0
        return self.end_time - self.start_time

    @property
    def elapsed_ms(self) -> float:
        """Get elapsed time in milliseconds."""
        return self.elapsed_seconds * 1000


def timed(func: F) -> F:
    """
    Decorator to time function execution.

    Example:
        >>> @timed
        ... def process_data(df):
        ...     return df.groupby('destination').mean()
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000

        logger.info(f"{func.__name__} took {elapsed:.2f}ms")
        return result

    return wrapper  # type: ignore


class PerformanceProfiler:
    """
    Collects and reports performance metrics.

    Example:
        >>> profiler = PerformanceProfiler()
        >>> profiler.start("load_data")
        >>> data = load_data()
        >>> profiler.end("load_data")
        >>> profiler.report()
    """

    def __init__(self):
        self.metrics: Dict[str, list] = {}
        self.active_timers: Dict[str, float] = {}

    def start(self, operation: str):
        """Start timing an operation."""
        self.active_timers[operation] = time.perf_counter()

    def end(self, operation: str):
        """End timing an operation and record the duration."""
        if operation not in self.active_timers:
            logger.warning(f"No timer started for operation: {operation}")
            return

        elapsed = (time.perf_counter() - self.active_timers[operation]) * 1000
        del self.active_timers[operation]

        if operation not in self.metrics:
            self.metrics[operation] = []

        self.metrics[operation].append(elapsed)

    def record(self, operation: str, duration_ms: float):
        """Manually record a duration for an operation."""
        if operation not in self.metrics:
            self.metrics[operation] = []

        self.metrics[operation].append(duration_ms)

    def get_stats(self, operation: str) -> Optional[Dict[str, float]]:
        """Get statistics for a specific operation."""
        if operation not in self.metrics or not self.metrics[operation]:
            return None

        durations = self.metrics[operation]
        return {
            "count": len(durations),
            "total_ms": sum(durations),
            "avg_ms": sum(durations) / len(durations),
            "min_ms": min(durations),
            "max_ms": max(durations),
        }

    def report(self) -> str:
        """Generate a performance report."""
        lines = ["Performance Profile Report", "=" * 50]

        for operation in sorted(self.metrics.keys()):
            stats = self.get_stats(operation)
            if stats:
                lines.append(f"\n{operation}:")
                lines.append(f"  Count: {stats['count']}")
                lines.append(f"  Total: {stats['total_ms']:.2f}ms")
                lines.append(f"  Avg:   {stats['avg_ms']:.2f}ms")
                lines.append(f"  Min:   {stats['min_ms']:.2f}ms")
                lines.append(f"  Max:   {stats['max_ms']:.2f}ms")

        return "\n".join(lines)

    def clear(self):
        """Clear all recorded metrics."""
        self.metrics.clear()
        self.active_timers.clear()


# Global profiler instance
_global_profiler = PerformanceProfiler()


def get_profiler() -> PerformanceProfiler:
    """Get the global performance profiler instance."""
    return _global_profiler
