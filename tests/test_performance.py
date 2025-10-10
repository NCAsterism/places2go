"""
Tests for performance optimization utilities.
"""

import time
from scripts.core.performance import (
    TTLCache,
    cache_with_ttl,
    memoize,
    PerformanceTimer,
    timed,
    PerformanceProfiler,
    get_profiler,
)


class TestTTLCache:
    """Tests for TTLCache class."""

    def test_cache_basic_operations(self):
        """Test basic get/set operations."""
        cache = TTLCache(max_size=10, default_ttl=60)

        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"

    def test_cache_miss(self):
        """Test cache miss returns None."""
        cache = TTLCache()
        assert cache.get("nonexistent") is None

    def test_cache_expiration(self):
        """Test that entries expire after TTL."""
        cache = TTLCache(default_ttl=1)

        cache.set("key1", "value1", ttl=1)
        assert cache.get("key1") == "value1"

        # Wait for expiration
        time.sleep(1.1)
        assert cache.get("key1") is None

    def test_cache_max_size(self):
        """Test that cache respects max_size limit."""
        cache = TTLCache(max_size=2)

        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")  # Should evict key1

        assert cache.get("key1") is None
        assert cache.get("key2") == "value2"
        assert cache.get("key3") == "value3"

    def test_cache_stats(self):
        """Test cache statistics tracking."""
        cache = TTLCache()

        # Generate some hits and misses
        cache.set("key1", "value1")
        cache.get("key1")  # Hit
        cache.get("key2")  # Miss
        cache.get("key1")  # Hit

        stats = cache.get_stats()
        assert stats["hits"] == 2
        assert stats["misses"] == 1
        assert stats["hit_rate"] == 2 / 3

    def test_cache_clear(self):
        """Test clearing the cache."""
        cache = TTLCache()

        cache.set("key1", "value1")
        cache.set("key2", "value2")
        assert cache.get("key1") == "value1"

        cache.clear()
        assert cache.get("key1") is None
        assert cache.get("key2") is None


class TestCacheDecorator:
    """Tests for cache_with_ttl decorator."""

    def test_caches_function_results(self):
        """Test that function results are cached."""
        call_count = {"count": 0}

        @cache_with_ttl(ttl=60)
        def expensive_function(x):
            call_count["count"] += 1
            return x * 2

        result1 = expensive_function(5)
        result2 = expensive_function(5)

        assert result1 == 10
        assert result2 == 10
        assert call_count["count"] == 1  # Only called once

    def test_different_args_different_cache(self):
        """Test that different arguments create different cache entries."""

        @cache_with_ttl(ttl=60)
        def add(a, b):
            return a + b

        result1 = add(1, 2)
        result2 = add(2, 3)

        assert result1 == 3
        assert result2 == 5

    def test_cache_expiration_decorator(self):
        """Test that cached results expire."""
        call_count = {"count": 0}

        @cache_with_ttl(ttl=1)
        def get_value():
            call_count["count"] += 1
            return 42

        result1 = get_value()
        assert result1 == 42
        assert call_count["count"] == 1

        # Wait for cache to expire
        time.sleep(1.1)

        result2 = get_value()
        assert result2 == 42
        assert call_count["count"] == 2  # Called again after expiration

    def test_cache_clear_method(self):
        """Test clearing the cache via decorator."""

        @cache_with_ttl(ttl=60)
        def get_value(x):
            return x * 3

        result1 = get_value(5)
        assert result1 == 15

        get_value.clear_cache()

        # Should still work after clearing
        result2 = get_value(5)
        assert result2 == 15


class TestMemoizeDecorator:
    """Tests for memoize decorator."""

    def test_memoizes_results(self):
        """Test that results are memoized."""
        call_count = {"count": 0}

        @memoize
        def calculate(x, y):
            call_count["count"] += 1
            return x + y

        result1 = calculate(3, 4)
        result2 = calculate(3, 4)

        assert result1 == 7
        assert result2 == 7
        assert call_count["count"] == 1

    def test_different_args_call_function(self):
        """Test that different arguments call function again."""
        call_count = {"count": 0}

        @memoize
        def multiply(x, y):
            call_count["count"] += 1
            return x * y

        result1 = multiply(2, 3)
        result2 = multiply(4, 5)

        assert result1 == 6
        assert result2 == 20
        assert call_count["count"] == 2


class TestPerformanceTimer:
    """Tests for PerformanceTimer context manager."""

    def test_timer_measures_time(self):
        """Test that timer measures elapsed time."""
        with PerformanceTimer("test_operation") as timer:
            time.sleep(0.1)

        assert timer.elapsed_seconds >= 0.1
        assert timer.elapsed_ms >= 100

    def test_timer_with_no_time(self):
        """Test timer before context execution."""
        timer = PerformanceTimer("test")
        assert timer.elapsed_seconds == 0.0
        assert timer.elapsed_ms == 0.0


class TestTimedDecorator:
    """Tests for timed decorator."""

    def test_timed_function_executes(self):
        """Test that timed function executes correctly."""

        @timed
        def slow_function(x):
            time.sleep(0.01)
            return x * 2

        result = slow_function(5)
        assert result == 10


class TestPerformanceProfiler:
    """Tests for PerformanceProfiler class."""

    def test_profiler_start_end(self):
        """Test starting and ending operations."""
        profiler = PerformanceProfiler()

        profiler.start("operation1")
        time.sleep(0.01)
        profiler.end("operation1")

        stats = profiler.get_stats("operation1")
        assert stats is not None
        assert stats["count"] == 1
        assert stats["avg_ms"] >= 10

    def test_profiler_multiple_recordings(self):
        """Test recording multiple instances of same operation."""
        profiler = PerformanceProfiler()

        profiler.record("operation1", 100)
        profiler.record("operation1", 200)
        profiler.record("operation1", 150)

        stats = profiler.get_stats("operation1")
        assert stats is not None
        assert stats["count"] == 3
        assert stats["avg_ms"] == 150
        assert stats["min_ms"] == 100
        assert stats["max_ms"] == 200

    def test_profiler_report(self):
        """Test generating a performance report."""
        profiler = PerformanceProfiler()

        profiler.record("load_data", 500)
        profiler.record("process_data", 300)

        report = profiler.report()
        assert "load_data" in report
        assert "process_data" in report
        assert "500.00ms" in report
        assert "300.00ms" in report

    def test_profiler_clear(self):
        """Test clearing profiler metrics."""
        profiler = PerformanceProfiler()

        profiler.record("operation1", 100)
        assert profiler.get_stats("operation1") is not None

        profiler.clear()
        assert profiler.get_stats("operation1") is None

    def test_global_profiler(self):
        """Test getting the global profiler instance."""
        profiler1 = get_profiler()
        profiler2 = get_profiler()

        assert profiler1 is profiler2  # Same instance


class TestIntegration:
    """Integration tests for performance utilities."""

    def test_cached_function_with_profiler(self):
        """Test using cache and profiler together."""
        profiler = PerformanceProfiler()

        @cache_with_ttl(ttl=60)
        def expensive_calc(x):
            profiler.start("expensive_calc")
            time.sleep(0.01)
            result = x * 2
            profiler.end("expensive_calc")
            return result

        # First call - should be slow
        result1 = expensive_calc(5)
        assert result1 == 10

        stats1 = profiler.get_stats("expensive_calc")
        assert stats1 is not None
        assert stats1["count"] == 1

        # Second call - should be cached (fast)
        result2 = expensive_calc(5)
        assert result2 == 10

        stats2 = profiler.get_stats("expensive_calc")
        # Still only 1 execution because second call was cached
        assert stats2["count"] == 1
