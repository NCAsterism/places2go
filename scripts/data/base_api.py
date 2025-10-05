"""
Base API client with caching, rate limiting, and error handling.

Provides common functionality for all API clients:
- File-based caching with TTL
- Rate limiting
- Retry logic with exponential backoff
- Error handling and logging
"""

import json
import logging
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional, Callable
from functools import wraps

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class CacheManager:
    """
    File-based cache manager with TTL support.

    Stores cached data in JSON files with metadata including expiry time.
    """

    def __init__(self, cache_dir: Optional[Path] = None):
        """
        Initialize cache manager.

        Args:
            cache_dir: Directory to store cache files. Defaults to .cache/
        """
        if cache_dir is None:
            cache_dir = Path(os.getenv("CACHE_DIR", ".cache"))

        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get(self, key: str) -> Optional[Any]:
        """
        Get cached data if not expired.

        Args:
            key: Cache key

        Returns:
            Cached data if found and not expired, None otherwise
        """
        import pandas as pd

        cache_file = self.cache_dir / f"{key}.json"

        if not cache_file.exists():
            return None

        try:
            with open(cache_file, "r") as f:
                cache_data = json.load(f)

            # Check if cache has expired
            expiry = datetime.fromisoformat(cache_data["expiry"])
            if datetime.now() > expiry:
                logger.info(f"Cache expired for key: {key}")
                cache_file.unlink()  # Delete expired cache
                return None

            logger.info(f"Cache hit for key: {key}")

            # Handle DataFrame deserialization
            data = cache_data["data"]
            if isinstance(data, dict) and data.get("_type") == "dataframe":
                return pd.DataFrame(data["_data"], columns=data["_columns"])

            return data

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.warning(f"Invalid cache file for key {key}: {e}")
            cache_file.unlink()  # Delete corrupted cache
            return None

    def set(self, key: str, data: Any, ttl: int) -> None:
        """
        Store data in cache with TTL.

        Args:
            key: Cache key
            data: Data to cache (supports pandas DataFrames)
            ttl: Time to live in seconds
        """
        import pandas as pd

        cache_file = self.cache_dir / f"{key}.json"
        expiry = datetime.now() + timedelta(seconds=ttl)

        # Convert DataFrame to records format for JSON serialization
        if isinstance(data, pd.DataFrame):
            # Convert to dict with date strings to avoid timestamp issues
            data_dict = data.to_dict("records")
            # Convert any datetime objects to ISO format strings
            for record in data_dict:
                for key_name, value in record.items():
                    if isinstance(value, (pd.Timestamp, datetime)):
                        record[key_name] = value.isoformat()

            data_to_cache = {
                "_type": "dataframe",
                "_data": data_dict,
                "_columns": list(data.columns),
            }
        else:
            data_to_cache = data

        cache_data = {
            "data": data_to_cache,
            "expiry": expiry.isoformat(),
            "created_at": datetime.now().isoformat(),
        }

        try:
            with open(cache_file, "w") as f:
                json.dump(cache_data, f, indent=2)
            logger.info(f"Cache set for key: {key} (TTL: {ttl}s)")
        except Exception as e:
            logger.error(f"Failed to write cache for key {key}: {e}")

    def clear(self, key: Optional[str] = None) -> None:
        """
        Clear cache for specific key or all cache.

        Args:
            key: Cache key to clear. If None, clears all cache.
        """
        if key:
            cache_file = self.cache_dir / f"{key}.json"
            if cache_file.exists():
                cache_file.unlink()
                logger.info(f"Cleared cache for key: {key}")
        else:
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
            logger.info("Cleared all cache")


class RateLimiter:
    """
    Simple rate limiter using token bucket algorithm.
    """

    def __init__(self, max_calls: int, period: int):
        """
        Initialize rate limiter.

        Args:
            max_calls: Maximum number of calls allowed
            period: Time period in seconds
        """
        self.max_calls = max_calls
        self.period = period
        self.calls = []

    def wait_if_needed(self) -> None:
        """
        Wait if rate limit would be exceeded.
        """
        now = time.time()

        # Remove calls outside the current period
        self.calls = [
            call_time for call_time in self.calls if now - call_time < self.period
        ]

        if len(self.calls) >= self.max_calls:
            # Calculate wait time
            oldest_call = min(self.calls)
            wait_time = self.period - (now - oldest_call)
            if wait_time > 0:
                logger.info(f"Rate limit reached, waiting {wait_time:.2f}s")
                time.sleep(wait_time)
                self.calls = []

        self.calls.append(time.time())


class BaseAPIClient:
    """
    Base class for all API clients with common functionality.
    """

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        cache_ttl: int = 3600,
        rate_limit: Optional[int] = None,
        rate_period: int = 60,
    ):
        """
        Initialize API client.

        Args:
            base_url: Base URL for the API
            api_key: API key for authentication (if required)
            cache_ttl: Cache time-to-live in seconds
            rate_limit: Maximum API calls per period
            rate_period: Rate limit period in seconds
        """
        self.base_url = base_url
        self.api_key = api_key
        self.cache_ttl = cache_ttl

        self.cache = CacheManager()

        if rate_limit:
            self.rate_limiter = RateLimiter(rate_limit, rate_period)
        else:
            self.rate_limiter = None

        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Places2Go/1.0"})

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        max_retries: int = 3,
    ) -> Dict[str, Any]:
        """
        Make HTTP request with retry logic.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Query parameters
            data: Request body data
            headers: Additional headers
            max_retries: Maximum number of retries

        Returns:
            Response data as dictionary

        Raises:
            requests.RequestException: If request fails after retries
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        # Apply rate limiting
        if self.rate_limiter:
            self.rate_limiter.wait_if_needed()

        # Prepare headers
        req_headers = {}
        if self.api_key:
            req_headers["Authorization"] = f"Bearer {self.api_key}"
        if headers:
            req_headers.update(headers)

        # Retry logic with exponential backoff
        for attempt in range(max_retries):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    headers=req_headers,
                    timeout=10,
                )
                response.raise_for_status()
                return response.json()

            except requests.exceptions.Timeout:
                logger.warning(f"Request timeout (attempt {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    time.sleep(2**attempt)  # Exponential backoff
                else:
                    raise

            except requests.exceptions.HTTPError as e:
                logger.error(f"HTTP error: {e}")
                if e.response.status_code >= 500 and attempt < max_retries - 1:
                    # Retry on server errors
                    time.sleep(2**attempt)
                else:
                    raise

            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2**attempt)
                else:
                    raise

        raise requests.RequestException("Max retries exceeded")

    def _get_cache_key(self, *args: Any, **kwargs: Any) -> str:
        """
        Generate cache key from arguments.

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Cache key string
        """
        import hashlib

        key_parts = [self.__class__.__name__]
        key_parts.extend(str(arg) for arg in args)
        key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
        key_str = "_".join(key_parts)

        # If key is too long for filesystem, use hash
        if len(key_str) > 200:
            key_hash = hashlib.md5(key_str.encode()).hexdigest()
            return f"{self.__class__.__name__}_{key_hash}"

        return key_str.replace(" ", "_").replace("/", "_")


def with_cache(ttl: Optional[int] = None) -> Callable:
    """
    Decorator to add caching to API methods.

    Args:
        ttl: Cache time-to-live in seconds (overrides client default)
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self: BaseAPIClient, *args: Any, **kwargs: Any) -> Any:
            # Generate cache key
            cache_key = self._get_cache_key(func.__name__, *args, **kwargs)

            # Try to get from cache
            cached_data = self.cache.get(cache_key)
            if cached_data is not None:
                return cached_data

            # Call the actual function
            result = func(self, *args, **kwargs)

            # Cache the result
            cache_ttl = ttl if ttl is not None else self.cache_ttl
            self.cache.set(cache_key, result, cache_ttl)

            return result

        return wrapper

    return decorator
