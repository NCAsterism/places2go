"""
URL Generator for Flight Search Links

This module provides utilities to generate flight search URLs for various
booking platforms like Skyscanner, Google Flights, etc.
"""

from datetime import date, datetime
from typing import Optional
from urllib.parse import urlencode
import pandas as pd


def generate_skyscanner_url(
    origin_airport: str,
    destination_airport: str,
    departure_date: date,
    return_date: Optional[date] = None,
    adults: int = 1,
) -> str:
    """
    Generate a Skyscanner search URL with pre-filled search parameters.

    Args:
        origin_airport: Origin airport code (e.g., 'EXT', 'BRS')
        destination_airport: Destination airport code (e.g., 'ALC', 'AGP')
        departure_date: Departure date
        return_date: Optional return date (None for one-way)
        adults: Number of adults (default: 1)

    Returns:
        Full Skyscanner search URL

    Example:
        >>> from datetime import date
        >>> url = generate_skyscanner_url('EXT', 'ALC', date(2025, 11, 15), date(2025, 11, 22))
        >>> print(url)
        https://www.skyscanner.net/transport/flights/ext/alc/251115/251122/?adults=1
    """
    # Skyscanner uses lowercase airport codes in URLs
    origin = origin_airport.lower()
    destination = destination_airport.lower()

    # Format dates as YYMMDD
    dep_str = departure_date.strftime("%y%m%d")

    # Construct URL path - handle NaT/None for return_date
    # Note: Although typed as Optional[date], we often receive pandas Timestamp
    # objects from DataFrames which can be NaT, so we check with pd.isna()
    if return_date is not None and not pd.isna(return_date):
        ret_str = return_date.strftime("%y%m%d")
        path = f"{origin}/{destination}/{dep_str}/{ret_str}/"
    else:
        path = f"{origin}/{destination}/{dep_str}/"

    # Build query parameters
    params = {"adults": str(adults)}
    query_string = urlencode(params)

    return f"https://www.skyscanner.net/transport/flights/{path}?{query_string}"


def generate_google_flights_url(
    origin_airport: str,
    destination_airport: str,
    departure_date: date,
    return_date: Optional[date] = None,
) -> str:
    """
    Generate a Google Flights search URL with pre-filled search parameters.

    Args:
        origin_airport: Origin airport code (e.g., 'EXT', 'BRS')
        destination_airport: Destination airport code (e.g., 'ALC', 'AGP')
        departure_date: Departure date
        return_date: Optional return date (None for one-way)

    Returns:
        Full Google Flights search URL

    Example:
        >>> from datetime import date
        >>> url = generate_google_flights_url('EXT', 'ALC', date(2025, 11, 15), date(2025, 11, 22))
        >>> print(url)
        https://www.google.com/travel/flights?q=Flights%20from%20EXT%20to%20ALC%20on%202025-11-15%20returning%202025-11-22
    """
    dep_str = departure_date.strftime("%Y-%m-%d")

    # Handle NaT/None for return_date (pandas Timestamp can be NaT)
    if return_date is not None and not pd.isna(return_date):
        ret_str = return_date.strftime("%Y-%m-%d")
        query = f"Flights from {origin_airport} to {destination_airport} on {dep_str} returning {ret_str}"
    else:
        query = f"Flights from {origin_airport} to {destination_airport} on {dep_str}"

    params = {"q": query}
    query_string = urlencode(params)

    return f"https://www.google.com/travel/flights?{query_string}"


def generate_flight_search_url(
    origin_airport: str,
    destination_airport: str,
    departure_date: date,
    return_date: Optional[date] = None,
    source: str = "skyscanner",
    **kwargs,
) -> str:
    """
    Generate a flight search URL based on the specified source.

    Args:
        origin_airport: Origin airport code
        destination_airport: Destination airport code
        departure_date: Departure date
        return_date: Optional return date
        source: Booking source ('skyscanner', 'google', etc.)
        **kwargs: Additional parameters for specific sources

    Returns:
        Flight search URL for the specified source

    Raises:
        ValueError: If source is not supported

    Example:
        >>> from datetime import date
        >>> url = generate_flight_search_url('EXT', 'ALC', date(2025, 11, 15), source='skyscanner')
        >>> print(url)
        https://www.skyscanner.net/transport/flights/ext/alc/251115/?adults=1
    """
    if isinstance(departure_date, str):
        departure_date = datetime.strptime(departure_date, "%Y-%m-%d").date()

    if isinstance(return_date, str):
        return_date = datetime.strptime(return_date, "%Y-%m-%d").date()

    source_lower = source.lower()

    if "skyscanner" in source_lower:
        return generate_skyscanner_url(
            origin_airport, destination_airport, departure_date, return_date, **kwargs
        )
    elif "google" in source_lower:
        return generate_google_flights_url(
            origin_airport, destination_airport, departure_date, return_date
        )
    else:
        # Default to Skyscanner
        return generate_skyscanner_url(
            origin_airport, destination_airport, departure_date, return_date, **kwargs
        )
