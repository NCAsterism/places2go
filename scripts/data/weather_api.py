"""
Weather data API client for fetching real-time weather forecasts.

Supports OpenWeatherMap API with free tier (1000 calls/day).
Implements caching (6-12 hours), rate limiting, and fallback to CSV data.
"""

import logging
import os
from datetime import datetime
from typing import List, Optional, Dict, Any

import pandas as pd
from dotenv import load_dotenv

from scripts.data.base_api import BaseAPIClient, with_cache
from scripts.core.data_loader import DataLoader

load_dotenv()
logger = logging.getLogger(__name__)


class WeatherDataFetcher(BaseAPIClient):
    """
    Fetches real-time weather forecast data from OpenWeatherMap API.

    Provides fallback to CSV data if API calls fail.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        cache_ttl: int = 21600,
    ):
        """
        Initialize weather data fetcher.

        Args:
            api_key: OpenWeatherMap API key
            base_url: Base URL for OpenWeatherMap API
            cache_ttl: Cache time-to-live in seconds (default: 6 hours)
        """
        if api_key is None:
            api_key = os.getenv("WEATHER_API_KEY")

        if base_url is None:
            base_url = os.getenv(
                "WEATHER_API_BASE_URL", "https://api.openweathermap.org/data/2.5"
            )

        if cache_ttl is None:
            cache_ttl = int(os.getenv("WEATHER_CACHE_TTL", "21600"))

        super().__init__(
            base_url=base_url,
            api_key=api_key,
            cache_ttl=cache_ttl,
            rate_limit=int(os.getenv("API_RATE_LIMIT", "50")),
            rate_period=int(os.getenv("API_RATE_PERIOD", "60")),
        )

        self.data_loader = DataLoader()

    @with_cache()
    def fetch_forecast(
        self, destinations: List[Dict[str, Any]], days: int = 7
    ) -> pd.DataFrame:
        """
        Fetch weather forecast for destinations.

        Args:
            destinations: List of destination dictionaries with lat/lon/id
            days: Number of days to forecast (max 7 for free tier)

        Returns:
            DataFrame with weather forecast data
        """
        try:
            if not self.api_key:
                logger.warning("Weather API key not configured, using CSV fallback")
                return self._fallback_to_csv()

            logger.info("Fetching weather forecast from OpenWeatherMap API")

            all_forecasts = []

            for dest in destinations:
                try:
                    forecast = self._fetch_for_location(
                        lat=dest["latitude"],
                        lon=dest["longitude"],
                        destination_id=dest["destination_id"],
                        days=days,  # noqa: E501
                    )
                    all_forecasts.append(forecast)
                except Exception as e:
                    dest_id = dest["destination_id"]
                    logger.error(
                        f"Failed to fetch weather for destination {dest_id}: {e}"
                    )

            if not all_forecasts:
                logger.warning("No weather data fetched, using CSV fallback")
                return self._fallback_to_csv()

            return pd.concat(all_forecasts, ignore_index=True)

        except Exception as e:
            logger.error(f"Failed to fetch weather data from API: {e}")
            return self._fallback_to_csv()

    def _fetch_for_location(
        self, lat: float, lon: float, destination_id: int, days: int = 7
    ) -> pd.DataFrame:
        """
        Fetch weather forecast for a specific location.

        Uses OpenWeatherMap One Call API 3.0 or 5 Day / 3 Hour Forecast API.

        Args:
            lat: Latitude
            lon: Longitude
            destination_id: Destination ID for the location
            days: Number of days to forecast

        Returns:
            DataFrame with weather forecast
        """
        # Use 5 Day / 3 Hour Forecast API (available in free tier)
        endpoint = "forecast"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric",  # Celsius
            "cnt": min(days * 8, 40),  # 8 forecasts per day, max 40 (5 days)
        }

        try:
            response = self._make_request("GET", endpoint, params=params)

            # Parse response into DataFrame
            forecasts = []
            for item in response.get("list", []):
                forecast_date = datetime.fromtimestamp(item["dt"]).date()

                forecasts.append(
                    {
                        "destination_id": destination_id,
                        "date": forecast_date.isoformat(),
                        "temp_high_c": item["main"]["temp_max"],
                        "temp_low_c": item["main"]["temp_min"],
                        "temp_avg_c": item["main"]["temp"],
                        "rainfall_mm": item.get("rain", {}).get("3h", 0),
                        "humidity_percent": item["main"]["humidity"],
                        "sunshine_hours": None,  # Not available in API
                        "wind_speed_kmh": item["wind"]["speed"] * 3.6,  # m/s to km/h
                        "conditions": item["weather"][0]["main"],
                        "uv_index": None,  # Not available in free tier
                        "forecast_flag": True,
                        "data_source": "openweathermap",
                    }
                )

            # Aggregate by day (API returns 3-hour intervals)
            df = pd.DataFrame(forecasts)
            if not df.empty:
                df = (
                    df.groupby(["destination_id", "date"])
                    .agg(
                        {
                            "temp_high_c": "max",
                            "temp_low_c": "min",
                            "temp_avg_c": "mean",
                            "rainfall_mm": "sum",
                            "humidity_percent": "mean",
                            "wind_speed_kmh": "mean",
                            "conditions": "first",
                            "forecast_flag": "first",
                            "data_source": "first",
                        }
                    )
                    .reset_index()
                )

                # Add sunshine hours estimate (based on conditions)
                df["sunshine_hours"] = df["conditions"].apply(
                    lambda x: (
                        10
                        if "Clear" in x or "Sun" in x
                        else 8 if "Cloud" in x else 5 if "Rain" in x else 7
                    )
                )

                # Add UV index estimate (based on season and conditions)
                df["uv_index"] = df["conditions"].apply(
                    lambda x: 7 if "Clear" in x else 5 if "Cloud" in x else 3
                )

            return df

        except Exception as e:
            logger.error(f"Failed to fetch weather for location ({lat}, {lon}): {e}")
            return pd.DataFrame()

    def _fallback_to_csv(self) -> pd.DataFrame:
        """
        Fallback to loading weather data from CSV files.

        Returns:
            DataFrame with weather data from CSV
        """
        logger.info("Using CSV fallback for weather data")

        try:
            # Load weather data from CSV
            df = self.data_loader.load_weather(data_source="demo1", forecast_only=True)
            return df

        except Exception as e:
            logger.error(f"Failed to load CSV fallback data: {e}")
            return pd.DataFrame()

    def get_current_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Get current weather for a location.

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            Dictionary with current weather data
        """
        endpoint = "weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric",
        }

        try:
            response = self._make_request("GET", endpoint, params=params)

            return {
                "temp_c": response["main"]["temp"],
                "feels_like_c": response["main"]["feels_like"],
                "humidity_percent": response["main"]["humidity"],
                "wind_speed_kmh": response["wind"]["speed"] * 3.6,
                "conditions": response["weather"][0]["main"],
                "description": response["weather"][0]["description"],
            }

        except Exception as e:
            logger.error(f"Failed to fetch current weather: {e}")
            return {}
