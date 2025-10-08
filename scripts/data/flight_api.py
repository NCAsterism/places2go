"""
Flight data API client for fetching real-time flight prices.

Supports multiple providers:
- Skyscanner API (via RapidAPI)
- Amadeus API

Implements caching (1-6 hours), rate limiting, and fallback to CSV data.
"""

import logging
import os
from typing import List, Optional

import pandas as pd
from dotenv import load_dotenv

from scripts.data.base_api import BaseAPIClient, with_cache
from scripts.core.data_loader import DataLoader

load_dotenv()
logger = logging.getLogger(__name__)


class FlightDataFetcher(BaseAPIClient):
    """
    Fetches real-time flight price data from various APIs.

    Provides fallback to CSV data if API calls fail.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        provider: str = "skyscanner",
        cache_ttl: int = 3600,
    ):
        """
        Initialize flight data fetcher.

        Args:
            api_key: API key for authentication
            base_url: Base URL for the API
            provider: API provider (skyscanner, amadeus)
            cache_ttl: Cache time-to-live in seconds (default: 1 hour)
        """
        if api_key is None:
            api_key = os.getenv("FLIGHT_API_KEY")

        if base_url is None:
            base_url = os.getenv("FLIGHT_API_BASE_URL", "")

        if cache_ttl is None:
            cache_ttl = int(os.getenv("FLIGHT_CACHE_TTL", "3600"))

        super().__init__(
            base_url=base_url,
            api_key=api_key,
            cache_ttl=cache_ttl,
            rate_limit=int(os.getenv("API_RATE_LIMIT", "50")),
            rate_period=int(os.getenv("API_RATE_PERIOD", "60")),
        )

        self.provider = provider
        self.data_loader = DataLoader()

    @with_cache()
    def fetch_prices(
        self,
        origin: str,
        destinations: List[str],
        departure_date: str,
        return_date: str,
    ) -> pd.DataFrame:
        """
        Fetch flight prices for destinations.

        Args:
            origin: Origin airport code (e.g., 'EXT', 'BRS')
            destinations: List of destination airport codes
            departure_date: Departure date (YYYY-MM-DD)
            return_date: Return date (YYYY-MM-DD)

        Returns:
            DataFrame with flight price data
        """
        try:
            if not self.api_key or not self.base_url:
                logger.warning("API credentials not configured, using CSV fallback")
                return self._fallback_to_csv(origin, destinations)

            logger.info(
                f"Fetching flight prices from {self.provider} API: "
                f"{origin} -> {destinations}"
            )

            if self.provider == "skyscanner":
                return self._fetch_from_skyscanner(
                    origin, destinations, departure_date, return_date
                )
            elif self.provider == "amadeus":
                return self._fetch_from_amadeus(
                    origin, destinations, departure_date, return_date
                )
            else:
                logger.error(f"Unknown provider: {self.provider}")
                return self._fallback_to_csv(origin, destinations)

        except Exception as e:
            logger.error(f"Failed to fetch flight data from API: {e}")
            return self._fallback_to_csv(origin, destinations)

    def _fetch_from_skyscanner(
        self,
        origin: str,
        destinations: List[str],
        departure_date: str,
        return_date: str,
    ) -> pd.DataFrame:
        """
        Fetch flight prices from Skyscanner API.

        This is a stub implementation. In production, you would:
        1. Make request to Skyscanner API endpoint
        2. Parse the response
        3. Convert to standardized DataFrame format

        Args:
            origin: Origin airport code
            destinations: List of destination airport codes
            departure_date: Departure date
            return_date: Return date

        Returns:
            DataFrame with flight price data
        """
        # Stub: In production, implement actual API call
        # Example endpoint: /flights/search
        # Response would include: prices, airlines, durations, etc.

        logger.info("Skyscanner API integration is a stub - using CSV fallback")
        return self._fallback_to_csv(origin, destinations)

    def _fetch_from_amadeus(
        self,
        origin: str,
        destinations: List[str],
        departure_date: str,
        return_date: str,
    ) -> pd.DataFrame:
        """
        Fetch flight prices from Amadeus API.

        This is a stub implementation. In production, you would:
        1. Authenticate with Amadeus API
        2. Make flight offers search request
        3. Parse response and convert to DataFrame

        Args:
            origin: Origin airport code
            destinations: List of destination airport codes
            departure_date: Departure date
            return_date: Return date

        Returns:
            DataFrame with flight price data
        """
        # Stub: In production, implement actual API call
        # Example: POST /shopping/flight-offers

        logger.info("Amadeus API integration is a stub - using CSV fallback")
        return self._fallback_to_csv(origin, destinations)

    def _fallback_to_csv(
        self, origin: str, destinations: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Fallback to loading flight data from CSV files.

        Args:
            origin: Origin airport code
            destinations: Optional list of destination airport codes to filter

        Returns:
            DataFrame with flight price data from CSV
        """
        logger.info("Using CSV fallback for flight data")

        try:
            # Load flight data from CSV
            df = self.data_loader.load_flights(data_source="demo1")

            # Filter by origin
            df = df[df["origin_airport"] == origin]

            # Filter by destinations if provided
            if destinations:
                # Get destination IDs for the airport codes
                dest_df = self.data_loader.load_destinations()
                dest_ids = dest_df[dest_df["airport_code"].isin(destinations)][
                    "destination_id"
                ].tolist()
                df = df[df["destination_id"].isin(dest_ids)]

            return df

        except Exception as e:
            logger.error(f"Failed to load CSV fallback data: {e}")
            return pd.DataFrame()

    def get_cheapest_flights(
        self,
        origin: str,
        destinations: Optional[List[str]] = None,
        departure_date: Optional[str] = None,
        return_date: Optional[str] = None,
        limit: int = 10,
    ) -> pd.DataFrame:
        """
        Get cheapest flights for each destination.

        Args:
            origin: Origin airport code
            destinations: Optional list of destination airport codes
            departure_date: Optional departure date filter
            return_date: Optional return date filter
            limit: Maximum number of results per destination

        Returns:
            DataFrame with cheapest flights
        """
        if departure_date and return_date:
            df = self.fetch_prices(
                origin, destinations or [], departure_date, return_date
            )
        else:
            df = self._fallback_to_csv(origin, destinations)

        if df.empty:
            return df

        # Group by destination and get cheapest flights
        df = df.sort_values("price")
        df = df.groupby("destination_id").head(limit).reset_index(drop=True)

        return df
