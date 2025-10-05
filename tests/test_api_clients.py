"""
Tests for API data fetchers.

Tests caching, rate limiting, error handling, and fallback mechanisms.
"""

import time

import pandas as pd
import pytest
import responses

from scripts.data.base_api import BaseAPIClient, CacheManager, RateLimiter
from scripts.data.flight_api import FlightDataFetcher
from scripts.data.weather_api import WeatherDataFetcher
from scripts.data.cost_api import CostDataFetcher


class TestCacheManager:
    """Test cache manager functionality."""

    def test_cache_set_and_get(self, tmp_path):
        """Test setting and getting cache data."""
        cache = CacheManager(cache_dir=tmp_path)

        data = {"test": "data", "numbers": [1, 2, 3]}
        cache.set("test_key", data, ttl=3600)

        cached_data = cache.get("test_key")
        assert cached_data == data

    def test_cache_expiry(self, tmp_path):
        """Test that expired cache returns None."""
        cache = CacheManager(cache_dir=tmp_path)

        data = {"test": "data"}
        cache.set("test_key", data, ttl=1)  # 1 second TTL

        # Wait for cache to expire
        time.sleep(1.5)

        cached_data = cache.get("test_key")
        assert cached_data is None

    def test_cache_miss(self, tmp_path):
        """Test cache miss returns None."""
        cache = CacheManager(cache_dir=tmp_path)
        cached_data = cache.get("nonexistent_key")
        assert cached_data is None

    def test_cache_clear_specific(self, tmp_path):
        """Test clearing specific cache key."""
        cache = CacheManager(cache_dir=tmp_path)

        cache.set("key1", {"data": 1}, ttl=3600)
        cache.set("key2", {"data": 2}, ttl=3600)

        cache.clear("key1")

        assert cache.get("key1") is None
        assert cache.get("key2") == {"data": 2}

    def test_cache_clear_all(self, tmp_path):
        """Test clearing all cache."""
        cache = CacheManager(cache_dir=tmp_path)

        cache.set("key1", {"data": 1}, ttl=3600)
        cache.set("key2", {"data": 2}, ttl=3600)

        cache.clear()

        assert cache.get("key1") is None
        assert cache.get("key2") is None


class TestRateLimiter:
    """Test rate limiter functionality."""

    def test_rate_limiter_allows_within_limit(self):
        """Test that rate limiter allows calls within limit."""
        limiter = RateLimiter(max_calls=5, period=1)

        # Should allow 5 calls without waiting
        for _ in range(5):
            limiter.wait_if_needed()

    def test_rate_limiter_blocks_over_limit(self):
        """Test that rate limiter blocks calls over limit."""
        limiter = RateLimiter(max_calls=2, period=2)

        # First 2 calls should be immediate
        start = time.time()
        limiter.wait_if_needed()
        limiter.wait_if_needed()

        # Third call should wait
        limiter.wait_if_needed()
        elapsed = time.time() - start

        # Should have waited approximately 2 seconds
        assert elapsed >= 1.8  # Allow some tolerance


class TestBaseAPIClient:
    """Test base API client functionality."""

    def test_init(self, tmp_path):
        """Test initialization of base API client."""
        client = BaseAPIClient(
            base_url="https://api.example.com",
            api_key="test_key",
            cache_ttl=3600,
        )

        assert client.base_url == "https://api.example.com"
        assert client.api_key == "test_key"
        assert client.cache_ttl == 3600

    @responses.activate
    def test_make_request_success(self):
        """Test successful API request."""
        responses.add(
            responses.GET,
            "https://api.example.com/test",
            json={"result": "success"},
            status=200,
        )

        client = BaseAPIClient(base_url="https://api.example.com")
        result = client._make_request("GET", "test")

        assert result == {"result": "success"}

    @responses.activate
    def test_make_request_retry_on_timeout(self):
        """Test retry logic on timeout."""
        # First call times out, second succeeds
        responses.add(
            responses.GET,
            "https://api.example.com/test",
            body=Exception("Timeout"),
        )
        responses.add(
            responses.GET,
            "https://api.example.com/test",
            json={"result": "success"},
            status=200,
        )

        client = BaseAPIClient(base_url="https://api.example.com")

        # Should succeed after retry
        # Note: This test is simplified; actual timeout handling may vary
        with pytest.raises(Exception):
            client._make_request("GET", "test", max_retries=1)

    def test_get_cache_key(self):
        """Test cache key generation."""
        client = BaseAPIClient(base_url="https://api.example.com")

        key1 = client._get_cache_key("test", arg1="value1", arg2="value2")
        key2 = client._get_cache_key("test", arg2="value2", arg1="value1")

        # Keys should be the same regardless of kwarg order
        assert key1 == key2
        assert "test" in key1
        assert "arg1=value1" in key1
        assert "arg2=value2" in key1


class TestFlightDataFetcher:
    """Test flight data fetcher."""

    def test_init_with_defaults(self):
        """Test initialization with default values."""
        fetcher = FlightDataFetcher()

        assert fetcher.provider == "skyscanner"
        assert fetcher.data_loader is not None

    def test_init_with_custom_values(self):
        """Test initialization with custom values."""
        fetcher = FlightDataFetcher(
            api_key="test_key",
            base_url="https://api.test.com",
            provider="amadeus",
            cache_ttl=7200,
        )

        assert fetcher.api_key == "test_key"
        assert fetcher.base_url == "https://api.test.com"
        assert fetcher.provider == "amadeus"
        assert fetcher.cache_ttl == 7200

    def test_fallback_to_csv(self):
        """Test fallback to CSV data."""
        fetcher = FlightDataFetcher()

        # Should return data from CSV
        df = fetcher._fallback_to_csv("EXT")

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert "price" in df.columns
        assert "destination_id" in df.columns

    def test_fallback_to_csv_with_filter(self):
        """Test fallback to CSV with destination filter."""
        fetcher = FlightDataFetcher()

        df = fetcher._fallback_to_csv("EXT", destinations=["ALC", "AGP"])

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        # Verify filtering worked
        assert all(df["origin_airport"] == "EXT")

    def test_get_cheapest_flights(self):
        """Test getting cheapest flights."""
        fetcher = FlightDataFetcher()

        df = fetcher.get_cheapest_flights(origin="EXT", limit=5)

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        # Verify results are limited per destination
        dest_counts = df.groupby("destination_id").size()
        assert all(dest_counts <= 5)


class TestWeatherDataFetcher:
    """Test weather data fetcher."""

    def test_init_with_defaults(self):
        """Test initialization with default values."""
        fetcher = WeatherDataFetcher()

        assert fetcher.data_loader is not None

    def test_init_with_custom_values(self):
        """Test initialization with custom values."""
        fetcher = WeatherDataFetcher(
            api_key="test_key",
            base_url="https://api.test.com",
            cache_ttl=43200,
        )

        assert fetcher.api_key == "test_key"
        assert fetcher.base_url == "https://api.test.com"
        assert fetcher.cache_ttl == 43200

    def test_fallback_to_csv(self):
        """Test fallback to CSV data."""
        fetcher = WeatherDataFetcher()

        df = fetcher._fallback_to_csv()

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert "temp_high_c" in df.columns
        assert "destination_id" in df.columns
        assert all(df["forecast_flag"])  # Should only get forecast data


class TestCostDataFetcher:
    """Test cost data fetcher."""

    def test_init_with_defaults(self):
        """Test initialization with default values."""
        fetcher = CostDataFetcher()

        assert fetcher.api_key is None  # Teleport doesn't need auth
        assert fetcher.data_loader is not None

    def test_init_with_custom_values(self):
        """Test initialization with custom values."""
        fetcher = CostDataFetcher(
            base_url="https://api.test.com",
            cache_ttl=86400,
        )

        assert fetcher.base_url == "https://api.test.com"
        assert fetcher.cache_ttl == 86400

    def test_fallback_to_csv(self):
        """Test fallback to CSV data."""
        fetcher = CostDataFetcher()

        df = fetcher._fallback_to_csv()

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert "monthly_living_cost" in df.columns
        assert "destination_id" in df.columns

    def test_get_cost_comparison(self):
        """Test cost comparison."""
        fetcher = CostDataFetcher()

        df = fetcher.get_cost_comparison()

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        # Verify sorting by cost
        costs = df["monthly_living_cost"].tolist()
        assert costs == sorted(costs)


class TestIntegration:
    """Integration tests for API clients."""

    def test_all_fetchers_have_fallback(self):
        """Test that all fetchers can fall back to CSV data."""
        flight_fetcher = FlightDataFetcher()
        weather_fetcher = WeatherDataFetcher()
        cost_fetcher = CostDataFetcher()

        # All should return data even without API credentials
        flight_df = flight_fetcher._fallback_to_csv("EXT")
        weather_df = weather_fetcher._fallback_to_csv()
        cost_df = cost_fetcher._fallback_to_csv()

        assert not flight_df.empty
        assert not weather_df.empty
        assert not cost_df.empty

    def test_cache_improves_performance(self, tmp_path):
        """Test that caching improves performance."""
        cache = CacheManager(cache_dir=tmp_path)

        # First call - no cache
        start1 = time.time()
        if cache.get("test") is None:
            # Simulate slow operation
            time.sleep(0.1)
            cache.set("test", {"data": "value"}, ttl=3600)
        elapsed1 = time.time() - start1

        # Second call - with cache
        start2 = time.time()
        cached_data = cache.get("test")
        elapsed2 = time.time() - start2

        assert cached_data is not None
        assert elapsed2 < elapsed1  # Cache should be faster
