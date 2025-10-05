"""
DataLoader class for reading and managing destination dashboard data.

This module provides a unified interface for loading data from the new CSV structure
which separates destinations, cost of living, flight prices, and weather data into
dedicated files with proper normalization and time-series support.
"""

import logging
import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict, Union

from .performance import PerformanceTimer, get_profiler

logger = logging.getLogger(__name__)


class DataLoader:
    """
    Loads and manages destination dashboard data from CSV files.

    The DataLoader handles reading from the normalized CSV structure:
    - data/destinations/destinations.csv (static master data)
    - data/destinations/cost_of_living.csv (quarterly updates)
    - data/flights/flight_prices.csv (daily updates, time-series)
    - data/weather/weather_data.csv (daily updates, time-series)

    Supports filtering by data source (demo1, demo2, live) and provides
    methods for loading individual datasets or merged views.

    Attributes:
        data_dir (Path): Root directory containing CSV files
        destinations_df (pd.DataFrame): Cached destinations data
        costs_df (pd.DataFrame): Cached cost of living data
        flights_df (pd.DataFrame): Cached flight prices data
        weather_df (pd.DataFrame): Cached weather data

    Example:
        >>> loader = DataLoader()
        >>> destinations = loader.load_destinations()
        >>> all_data = loader.load_all()
        >>> demo_flights = loader.load_flights(data_source='demo1')
    """

    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize the DataLoader.

        Args:
            data_dir: Path to data directory. Defaults to 'data/' relative to project root.
        """
        if data_dir is None:
            # Default to data/ directory relative to this file
            project_root = Path(__file__).parent.parent.parent
            data_dir = project_root / "data"

        self.data_dir = Path(data_dir)

        # Cache for loaded dataframes
        self.destinations_df: Optional[pd.DataFrame] = None
        self.costs_df: Optional[pd.DataFrame] = None
        self.flights_df: Optional[pd.DataFrame] = None
        self.weather_df: Optional[pd.DataFrame] = None

    def load_destinations(self, reload: bool = False) -> pd.DataFrame:
        """
        Load destination master data.

        Args:
            reload: Force reload from CSV even if cached

        Returns:
            DataFrame with columns: destination_id, name, country, country_code,
            region, latitude, longitude, timezone, airport_code, airport_name, origin_airport

        Raises:
            FileNotFoundError: If destinations.csv doesn't exist
        """
        profiler = get_profiler()

        if self.destinations_df is None or reload:
            with PerformanceTimer("load_destinations", logging.DEBUG):
                csv_path = self.data_dir / "destinations" / "destinations.csv"
                if not csv_path.exists():
                    raise FileNotFoundError(f"Destinations file not found: {csv_path}")

                profiler.start("read_destinations_csv")
                self.destinations_df = pd.read_csv(csv_path)
                profiler.end("read_destinations_csv")

                # Ensure destination_id is integer
                self.destinations_df["destination_id"] = self.destinations_df[
                    "destination_id"
                ].astype(int)

        return self.destinations_df.copy()

    def load_costs(
        self, data_source: Optional[str] = None, reload: bool = False
    ) -> pd.DataFrame:
        """
        Load cost of living data.

        Args:
            data_source: Filter by data source (e.g., 'demo1', 'demo2', 'live', 'numbeo')
            reload: Force reload from CSV even if cached

        Returns:
            DataFrame with columns: destination_id, data_date, currency,
            monthly_living_cost, rent, food, transport, utilities, entertainment,
            meal_inexpensive, meal_mid_range, beer, coffee, public_transport,
            weed, data_source

        Raises:
            FileNotFoundError: If cost_of_living.csv doesn't exist
        """
        profiler = get_profiler()

        if self.costs_df is None or reload:
            with PerformanceTimer("load_costs", logging.DEBUG):
                csv_path = self.data_dir / "destinations" / "cost_of_living.csv"
                if not csv_path.exists():
                    raise FileNotFoundError(
                        f"Cost of living file not found: {csv_path}"
                    )

                profiler.start("read_costs_csv")
                self.costs_df = pd.read_csv(csv_path)
                profiler.end("read_costs_csv")

                # Parse dates
                self.costs_df["data_date"] = pd.to_datetime(self.costs_df["data_date"])

                # Ensure destination_id is integer
                self.costs_df["destination_id"] = self.costs_df[
                    "destination_id"
                ].astype(int)

        df = self.costs_df.copy()

        # Filter by data source if specified
        if data_source:
            df = df[df["data_source"] == data_source]

        return df

    def load_flights(
        self,
        data_source: Optional[str] = None,
        search_date: Optional[str] = None,
        departure_date_range: Optional[tuple] = None,
        reload: bool = False,
    ) -> pd.DataFrame:
        """
        Load flight price data with time-series support.

        Args:
            data_source: Filter by data source (e.g., 'demo1', 'skyscanner', 'live')
            search_date: Filter by specific search date (YYYY-MM-DD)
            departure_date_range: Tuple of (start_date, end_date) to filter departures
            reload: Force reload from CSV even if cached

        Returns:
            DataFrame with columns: flight_id, destination_id, origin_airport,
            search_date, departure_date, return_date, price, currency, duration_hours,
            distance_km, airline, direct_flight, data_source

        Raises:
            FileNotFoundError: If flight_prices.csv doesn't exist

        Example:
            >>> # Get demo flights searched on Oct 4
            >>> flights = loader.load_flights(
            ...     data_source='demo1',
            ...     search_date='2025-10-04'
            ... )
            >>>
            >>> # Get flights departing in October
            >>> oct_flights = loader.load_flights(
            ...     departure_date_range=('2025-10-01', '2025-10-31')
            ... )
        """
        if self.flights_df is None or reload:
            csv_path = self.data_dir / "flights" / "flight_prices.csv"
            if not csv_path.exists():
                raise FileNotFoundError(f"Flight prices file not found: {csv_path}")

            self.flights_df = pd.read_csv(csv_path)

            # Parse dates
            self.flights_df["search_date"] = pd.to_datetime(
                self.flights_df["search_date"]
            )
            self.flights_df["departure_date"] = pd.to_datetime(
                self.flights_df["departure_date"]
            )
            self.flights_df["return_date"] = pd.to_datetime(
                self.flights_df["return_date"]
            )

            # Ensure destination_id is integer and price is float
            self.flights_df["destination_id"] = self.flights_df[
                "destination_id"
            ].astype(int)
            self.flights_df["price"] = self.flights_df["price"].astype(float)

        df = self.flights_df.copy()

        # Apply filters
        if data_source:
            df = df[df["data_source"] == data_source]

        if search_date:
            filter_date = pd.to_datetime(search_date)
            df = df[df["search_date"] == filter_date]

        if departure_date_range:
            start_date = pd.to_datetime(departure_date_range[0])
            end_date = pd.to_datetime(departure_date_range[1])
            df = df[
                (df["departure_date"] >= start_date)
                & (df["departure_date"] <= end_date)
            ]

        return df

    def load_weather(
        self,
        data_source: Optional[str] = None,
        date_range: Optional[tuple] = None,
        forecast_only: bool = False,
        reload: bool = False,
    ) -> pd.DataFrame:
        """
        Load weather data with time-series support.

        Args:
            data_source: Filter by data source (e.g., 'demo1', 'openweather', 'live')
            date_range: Tuple of (start_date, end_date) to filter weather dates
            forecast_only: If True, only return forecast data (forecast_flag=TRUE)
            reload: Force reload from CSV even if cached

        Returns:
            DataFrame with columns: weather_id, destination_id, date, temp_high_c,
            temp_low_c, temp_avg_c, rainfall_mm, humidity_percent, sunshine_hours,
            wind_speed_kmh, conditions, uv_index, forecast_flag, data_source

        Raises:
            FileNotFoundError: If weather_data.csv doesn't exist

        Example:
            >>> # Get demo weather forecasts for next week
            >>> weather = loader.load_weather(
            ...     data_source='demo1',
            ...     forecast_only=True
            ... )
            >>>
            >>> # Get October weather observations
            >>> oct_weather = loader.load_weather(
            ...     date_range=('2025-10-01', '2025-10-31')
            ... )
        """
        if self.weather_df is None or reload:
            csv_path = self.data_dir / "weather" / "weather_data.csv"
            if not csv_path.exists():
                raise FileNotFoundError(f"Weather data file not found: {csv_path}")

            self.weather_df = pd.read_csv(csv_path)

            # Parse dates
            self.weather_df["date"] = pd.to_datetime(self.weather_df["date"])

            # Ensure destination_id is integer
            self.weather_df["destination_id"] = self.weather_df[
                "destination_id"
            ].astype(int)

            # Parse boolean
            self.weather_df["forecast_flag"] = self.weather_df["forecast_flag"].astype(
                bool
            )

        df = self.weather_df.copy()

        # Apply filters
        if data_source:
            df = df[df["data_source"] == data_source]

        if date_range:
            start_date = pd.to_datetime(date_range[0])
            end_date = pd.to_datetime(date_range[1])
            df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

        if forecast_only:
            df = df[df["forecast_flag"]]

        return df

    def load_all(
        self, data_source: Optional[str] = None, merge_strategy: str = "left"
    ) -> pd.DataFrame:
        """
        Load and merge all data sources into a single DataFrame.

        This creates a wide-format DataFrame with all information about each destination,
        including costs, flight prices, and weather. For time-series data (flights, weather),
        this may create multiple rows per destination.

        Args:
            data_source: Filter dynamic data by source (flights, weather, costs)
            merge_strategy: How to merge DataFrames ('left', 'inner', 'outer')
                - 'left': Keep all destinations even if missing data
                - 'inner': Only destinations with complete data
                - 'outer': Keep all records from all sources

        Returns:
            Merged DataFrame with all destination information

        Note:
            This returns the most recent cost data per destination if multiple
            dates exist. For flight and weather data, all records are included
            unless filtered by data_source.

        Example:
            >>> # Get complete demo dataset
            >>> all_data = loader.load_all(data_source='demo1')
            >>>
            >>> # Get all destinations with any available data
            >>> all_data = loader.load_all(merge_strategy='outer')
        """
        # Load base destination data
        destinations = self.load_destinations()

        # Load costs (take most recent per destination)
        costs = self.load_costs(data_source=data_source)
        if not costs.empty:
            # Get most recent cost data per destination
            costs = (
                costs.sort_values("data_date")
                .groupby("destination_id")
                .last()
                .reset_index()
            )

        # Load flights
        flights = self.load_flights(data_source=data_source)

        # Load weather
        weather = self.load_weather(data_source=data_source)

        # Start with destinations and merge costs
        result = destinations.merge(
            costs, on="destination_id", how=merge_strategy, suffixes=("", "_cost")
        )

        # Merge flights (may create multiple rows per destination)
        if not flights.empty:
            result = result.merge(
                flights,
                on="destination_id",
                how=merge_strategy,
                suffixes=("", "_flight"),
            )

        # Merge weather (aligned by date if flights are present)
        if not weather.empty:
            # If we have flights with departure dates, try to match weather to those dates
            if "departure_date" in result.columns:
                weather_aligned = weather.rename(columns={"date": "departure_date"})
                result = result.merge(
                    weather_aligned,
                    on=["destination_id", "departure_date"],
                    how=merge_strategy,
                    suffixes=("", "_weather"),
                )
            else:
                # No flights, just merge all weather data
                result = result.merge(
                    weather,
                    on="destination_id",
                    how=merge_strategy,
                    suffixes=("", "_weather"),
                )

        return result

    def get_aggregates(self, data_source: Optional[str] = None) -> pd.DataFrame:
        """
        Get aggregated statistics per destination.

        Computes summary statistics for each destination:
        - Average flight price
        - Min/max flight prices
        - Average temperature
        - Total rainfall
        - Average UV index

        Args:
            data_source: Filter by data source before aggregating

        Returns:
            DataFrame with one row per destination and aggregate columns

        Example:
            >>> aggregates = loader.get_aggregates(data_source='demo1')
            >>> print(aggregates[['name', 'avg_flight_price', 'avg_temp']])
        """
        destinations = self.load_destinations()
        costs = self.load_costs(data_source=data_source)
        flights = self.load_flights(data_source=data_source)
        weather = self.load_weather(data_source=data_source)

        # Start with destinations
        result = destinations[["destination_id", "name", "country"]].copy()

        # Add cost data (most recent)
        if not costs.empty:
            cost_latest = (
                costs.sort_values("data_date").groupby("destination_id").last()
            )
            result = result.merge(
                cost_latest[["monthly_living_cost"]], on="destination_id", how="left"
            )

        # Aggregate flight prices
        if not flights.empty:
            flight_agg = (
                flights.groupby("destination_id")
                .agg({"price": ["mean", "min", "max", "count"]})
                .round(2)
            )
            flight_agg.columns = [
                "avg_flight_price",
                "min_flight_price",
                "max_flight_price",
                "flight_count",
            ]
            result = result.merge(flight_agg, on="destination_id", how="left")

        # Aggregate weather
        if not weather.empty:
            weather_agg = (
                weather.groupby("destination_id")
                .agg(
                    {
                        "temp_avg_c": "mean",
                        "temp_high_c": "max",
                        "temp_low_c": "min",
                        "rainfall_mm": "sum",
                        "uv_index": "mean",
                        "sunshine_hours": "sum",
                    }
                )
                .round(2)
            )
            weather_agg.columns = [
                "avg_temp",
                "max_temp",
                "min_temp",
                "total_rainfall",
                "avg_uv_index",
                "total_sunshine_hours",
            ]
            result = result.merge(weather_agg, on="destination_id", how="left")

        return result

    def get_available_data_sources(self) -> Dict[str, List[str]]:
        """
        Get list of available data sources across all datasets.

        Returns:
            Dictionary mapping dataset names to lists of data sources found

        Example:
            >>> sources = loader.get_available_data_sources()
            >>> print(sources)
            {'costs': ['demo1'], 'flights': ['demo1'], 'weather': ['demo1']}
        """
        result = {}

        # Check costs
        try:
            costs = self.load_costs()
            if not costs.empty:
                result["costs"] = sorted(costs["data_source"].unique().tolist())
        except FileNotFoundError:
            pass

        # Check flights
        try:
            flights = self.load_flights()
            if not flights.empty:
                result["flights"] = sorted(flights["data_source"].unique().tolist())
        except FileNotFoundError:
            pass

        # Check weather
        try:
            weather = self.load_weather()
            if not weather.empty:
                result["weather"] = sorted(weather["data_source"].unique().tolist())
        except FileNotFoundError:
            pass

        return result

    def clear_cache(self) -> None:
        """Clear all cached DataFrames to force reload on next access."""
        self.destinations_df = None
        self.costs_df = None
        self.flights_df = None
        self.weather_df = None


# Convenience function for quick loading
def load_data(
    data_source: Optional[str] = None, merge: bool = True
) -> Union[DataLoader, pd.DataFrame]:
    """
    Convenience function to create a DataLoader and optionally load all data.

    Args:
        data_source: Filter by data source
        merge: If True, return merged data; if False, return DataLoader instance

    Returns:
        DataLoader instance or merged DataFrame

    Example:
        >>> # Get DataLoader instance
        >>> loader = load_data(merge=False)
        >>> destinations = loader.load_destinations()
        >>>
        >>> # Get merged data directly
        >>> data = load_data(data_source='demo1', merge=True)
    """
    loader = DataLoader()
    if merge:
        return loader.load_all(data_source=data_source)
    return loader
