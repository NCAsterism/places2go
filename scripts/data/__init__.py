"""
Data API module for fetching real-time data from external sources.

This module provides API clients for:
- Flight prices (Skyscanner/Amadeus)
- Weather forecasts (OpenWeatherMap)
- Cost of living (Teleport Public API)

All API clients implement caching, rate limiting, and fallback to CSV data.
"""

from scripts.data.base_api import BaseAPIClient, CacheManager
from scripts.data.flight_api import FlightDataFetcher
from scripts.data.weather_api import WeatherDataFetcher
from scripts.data.cost_api import CostDataFetcher

__all__ = [
    "BaseAPIClient",
    "CacheManager",
    "FlightDataFetcher",
    "WeatherDataFetcher",
    "CostDataFetcher",
]
