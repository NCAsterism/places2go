"""
Cost of living data API client for fetching real-time cost data.

Supports Teleport Public API (free, no authentication required).
Implements caching (30 days), rate limiting, and fallback to CSV data.
"""

import logging
import os
from typing import List, Optional, Dict, Any

import pandas as pd
from dotenv import load_dotenv

from scripts.data.base_api import BaseAPIClient, with_cache
from scripts.core.data_loader import DataLoader

load_dotenv()
logger = logging.getLogger(__name__)


class CostDataFetcher(BaseAPIClient):
    """
    Fetches real-time cost of living data from Teleport Public API.

    Teleport API is free and doesn't require authentication.
    Provides fallback to CSV data if API calls fail.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        cache_ttl: int = 2592000,
    ):
        """
        Initialize cost data fetcher.

        Args:
            base_url: Base URL for Teleport API
            cache_ttl: Cache time-to-live in seconds (default: 30 days)
        """
        if base_url is None:
            base_url = os.getenv("COST_API_BASE_URL", "https://api.teleport.org/api")

        if cache_ttl is None:
            cache_ttl = int(os.getenv("COST_CACHE_TTL", "2592000"))

        super().__init__(
            base_url=base_url,
            api_key=None,  # Teleport API doesn't require authentication
            cache_ttl=cache_ttl,
            rate_limit=int(os.getenv("API_RATE_LIMIT", "50")),
            rate_period=int(os.getenv("API_RATE_PERIOD", "60")),
        )

        self.data_loader = DataLoader()

    @with_cache()
    def fetch_costs(self, destinations: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Fetch cost of living data for destinations.

        Args:
            destinations: List of destination dictionaries with city names

        Returns:
            DataFrame with cost of living data
        """
        try:
            logger.info("Fetching cost of living from Teleport API")

            all_costs = []

            for dest in destinations:
                try:
                    cost_data = self._fetch_for_city(
                        city_name=dest["name"],
                        country_code=dest["country_code"],
                        destination_id=dest["destination_id"],
                    )
                    if cost_data:
                        all_costs.append(cost_data)
                except Exception as e:
                    logger.error(f"Failed to fetch cost data for {dest['name']}: {e}")

            if not all_costs:
                logger.warning("No cost data fetched, using CSV fallback")
                return self._fallback_to_csv()

            return pd.DataFrame(all_costs)

        except Exception as e:
            logger.error(f"Failed to fetch cost data from API: {e}")
            return self._fallback_to_csv()

    def _fetch_for_city(
        self, city_name: str, country_code: str, destination_id: int
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch cost of living data for a specific city.

        Teleport API structure:
        1. Search for city by name
        2. Get urban area link
        3. Fetch cost of living details

        Args:
            city_name: Name of the city
            country_code: ISO country code
            destination_id: Destination ID

        Returns:
            Dictionary with cost data or None if not found
        """
        try:
            # Step 1: Search for city
            search_endpoint = "cities/"
            search_params = {"search": city_name}

            search_results = self._make_request(
                "GET", search_endpoint, params=search_params
            )

            # Find matching city
            city_link = None
            for result in search_results.get("_embedded", {}).get(
                "city:search-results", []
            ):
                if result.get("matching_full_name", "").startswith(city_name):
                    city_link = result["_links"]["city:item"]["href"]
                    break

            if not city_link:
                logger.warning(f"City not found in Teleport API: {city_name}")
                return None

            # Step 2: Get city details to find urban area
            # Extract endpoint from full URL
            city_endpoint = city_link.replace(self.base_url + "/", "")
            city_data = self._make_request("GET", city_endpoint)

            urban_area_link = (
                city_data.get("_links", {}).get("city:urban_area", {}).get("href")
            )
            if not urban_area_link:
                logger.warning(f"No urban area data for city: {city_name}")
                return None

            # Step 3: Get cost of living details
            cost_endpoint = urban_area_link.replace(self.base_url + "/", "") + "details"
            cost_data = self._make_request("GET", cost_endpoint)

            # Parse cost data
            categories = cost_data.get("categories", [])
            cost_info = {}

            for category in categories:
                if category["id"] == "COST-OF-LIVING":
                    for item in category.get("data", []):
                        cost_info[item["id"]] = item.get("currency_dollar_value")

            # Calculate monthly living cost estimate
            # Use available data points from Teleport
            rent = cost_info.get("APARTMENT-RENT-MEDIUM", 1000)
            groceries = (
                cost_info.get("MEAL-INEXPENSIVE-RESTAURANT-RANGE", 15) * 60
            )  # ~2 meals/day
            transport = cost_info.get("TRANSPORT-PUBLIC-MONTH", 50)

            monthly_cost = rent + groceries + transport

            return {
                "destination_id": destination_id,
                "monthly_living_cost": monthly_cost,
                "meal_inexpensive_restaurant": cost_info.get(
                    "MEAL-INEXPENSIVE-RESTAURANT-RANGE"
                ),
                "meal_midrange_restaurant": cost_info.get("MEAL-MIDRANGE-RESTAURANT"),
                "domestic_beer": cost_info.get("BEER-DOMESTIC"),
                "cappuccino": cost_info.get("CAPPUCCINO"),
                "apartment_rent": rent,
                "monthly_transport_pass": transport,
                "currency": "USD",
                "data_source": "teleport",
            }

        except Exception as e:
            logger.error(f"Failed to fetch cost data for {city_name}: {e}")
            return None

    def _fallback_to_csv(self) -> pd.DataFrame:
        """
        Fallback to loading cost of living data from CSV files.

        Returns:
            DataFrame with cost data from CSV
        """
        logger.info("Using CSV fallback for cost of living data")

        try:
            # Load cost data from CSV
            df = self.data_loader.load_costs(data_source="demo1")
            return df

        except Exception as e:
            logger.error(f"Failed to load CSV fallback data: {e}")
            return pd.DataFrame()

    def get_cost_comparison(
        self, destinations: Optional[List[Dict[str, Any]]] = None
    ) -> pd.DataFrame:
        """
        Get cost comparison across destinations.

        Args:
            destinations: Optional list of destinations to compare

        Returns:
            DataFrame with cost comparison
        """
        if destinations:
            df = self.fetch_costs(destinations)
        else:
            df = self._fallback_to_csv()

        if df.empty:
            return df

        # Sort by monthly living cost
        df = df.sort_values("monthly_living_cost").reset_index(drop=True)

        return df
