"""
Tests for the DataLoader class.

Tests cover loading individual datasets, filtering by data source,
merging data, and computing aggregates.
"""

import pytest
import pandas as pd
from scripts.core.data_loader import DataLoader, load_data


class TestDataLoader:
    """Test suite for DataLoader class."""

    @pytest.fixture
    def loader(self):
        """Create a DataLoader instance for testing."""
        return DataLoader()

    def test_init_default_path(self):
        """Test DataLoader initializes with default data path."""
        loader = DataLoader()
        assert loader.data_dir.name == "data"
        assert loader.destinations_df is None
        assert loader.costs_df is None
        assert loader.flights_df is None
        assert loader.weather_df is None

    def test_init_custom_path(self, tmp_path):
        """Test DataLoader can use custom data path."""
        loader = DataLoader(data_dir=tmp_path)
        assert loader.data_dir == tmp_path

    def test_load_destinations(self, loader):
        """Test loading destination master data."""
        df = loader.load_destinations()

        # Check data is loaded
        assert not df.empty
        assert len(df) == 6  # We have 6 destinations

        # Check required columns
        required_cols = [
            "destination_id",
            "name",
            "country",
            "country_code",
            "region",
            "latitude",
            "longitude",
            "timezone",
            "airport_code",
            "airport_name",
            "origin_airport",
        ]
        for col in required_cols:
            assert col in df.columns

        # Check data types
        assert df["destination_id"].dtype == int
        assert df["latitude"].dtype == float
        assert df["longitude"].dtype == float

        # Check specific destinations exist
        assert "Alicante" in df["name"].values
        assert "Malaga" in df["name"].values
        assert "Rhodes" in df["name"].values

    def test_load_destinations_caching(self, loader):
        """Test destinations data is cached after first load."""
        df1 = loader.load_destinations()
        df2 = loader.load_destinations()

        # Should return cached data (not the same object due to copy())
        assert df1.equals(df2)
        assert loader.destinations_df is not None

    def test_load_destinations_reload(self, loader):
        """Test forcing reload of destinations data."""
        df1 = loader.load_destinations()
        df2 = loader.load_destinations(reload=True)

        assert df1.equals(df2)
        assert loader.destinations_df is not None

    def test_load_costs(self, loader):
        """Test loading cost of living data."""
        df = loader.load_costs()

        # Check data is loaded
        assert not df.empty
        assert len(df) == 6  # One record per destination

        # Check required columns
        required_cols = [
            "destination_id",
            "data_date",
            "currency",
            "monthly_living_cost",
            "rent_1br_center",
            "monthly_food",
            "monthly_transport",
            "utilities",
            "data_source",
        ]
        for col in required_cols:
            assert col in df.columns

        # Check data types
        assert df["destination_id"].dtype == int
        assert pd.api.types.is_datetime64_any_dtype(df["data_date"])
        assert pd.api.types.is_numeric_dtype(df["monthly_living_cost"])

        # Check all have data_source
        assert df["data_source"].notna().all()

    def test_load_costs_filter_data_source(self, loader):
        """Test filtering costs by data source."""
        df_all = loader.load_costs()
        df_demo1 = loader.load_costs(data_source="demo1")

        # demo1 should be subset of all
        assert len(df_demo1) <= len(df_all)

        # All filtered records should be demo1
        assert (df_demo1["data_source"] == "demo1").all()

    def test_load_flights(self, loader):
        """Test loading flight price data."""
        df = loader.load_flights()

        # Check data is loaded
        assert not df.empty
        assert len(df) == 42  # 6 destinations × 7 days

        # Check required columns
        required_cols = [
            "flight_id",
            "destination_id",
            "origin_airport",
            "search_date",
            "departure_date",
            "return_date",
            "price",
            "currency",
            "airline",
            "data_source",
        ]
        for col in required_cols:
            assert col in df.columns

        # Check data types
        assert df["destination_id"].dtype == int
        assert pd.api.types.is_datetime64_any_dtype(df["search_date"])
        assert pd.api.types.is_datetime64_any_dtype(df["departure_date"])
        assert df["price"].dtype == float

        # Check price range is reasonable
        assert df["price"].min() >= 0
        assert df["price"].max() < 1000  # Assuming no flights over £1000

    def test_load_flights_filter_search_date(self, loader):
        """Test filtering flights by search date."""
        df = loader.load_flights(search_date="2025-10-04")

        # All should have same search date
        assert (df["search_date"] == pd.Timestamp("2025-10-04")).all()
        assert not df.empty

    def test_load_flights_filter_departure_range(self, loader):
        """Test filtering flights by departure date range."""
        df = loader.load_flights(departure_date_range=("2025-10-11", "2025-10-13"))

        # Should only have 3 days × 6 destinations = 18 flights
        assert len(df) <= 18

        # All departures should be in range
        assert (df["departure_date"] >= pd.Timestamp("2025-10-11")).all()
        assert (df["departure_date"] <= pd.Timestamp("2025-10-13")).all()

    def test_load_flights_filter_data_source(self, loader):
        """Test filtering flights by data source."""
        df = loader.load_flights(data_source="demo1")

        assert not df.empty
        assert (df["data_source"] == "demo1").all()

    def test_load_weather(self, loader):
        """Test loading weather data."""
        df = loader.load_weather()

        # Check data is loaded
        assert not df.empty
        assert len(df) == 42  # 6 destinations × 7 days

        # Check required columns
        required_cols = [
            "weather_id",
            "destination_id",
            "date",
            "temp_high_c",
            "temp_low_c",
            "temp_avg_c",
            "rainfall_mm",
            "humidity_percent",
            "conditions",
            "uv_index",
            "forecast_flag",
            "data_source",
        ]
        for col in required_cols:
            assert col in df.columns

        # Check data types
        assert df["destination_id"].dtype == int
        assert pd.api.types.is_datetime64_any_dtype(df["date"])
        assert pd.api.types.is_numeric_dtype(df["temp_avg_c"])
        assert df["forecast_flag"].dtype == bool

        # Check temperature values are reasonable (in Celsius)
        assert df["temp_avg_c"].min() > -50
        assert df["temp_avg_c"].max() < 60

    def test_load_weather_filter_date_range(self, loader):
        """Test filtering weather by date range."""
        df = loader.load_weather(date_range=("2025-10-05", "2025-10-07"))

        # Should have 3 days × 6 destinations = 18 records
        assert len(df) <= 18

        # All dates should be in range
        assert (df["date"] >= pd.Timestamp("2025-10-05")).all()
        assert (df["date"] <= pd.Timestamp("2025-10-07")).all()

    def test_load_weather_filter_forecast_only(self, loader):
        """Test filtering weather for forecasts only."""
        weather_data = pd.DataFrame(
            {
                "weather_id": [1, 2, 3],
                "destination_id": [1, 1, 1],
                "date": pd.to_datetime(
                    ["2025-10-05", "2025-10-06", "2025-10-07"]
                ),
                "temp_high_c": [26, 27, 25],
                "temp_low_c": [18, 19, 17],
                "temp_avg_c": [22, 23, 21],
                "rainfall_mm": [0, 0, 1],
                "humidity_percent": [65, 60, 70],
                "sunshine_hours": [9.5, 10.2, 8.5],
                "wind_speed_kmh": [12, 10, 15],
                "conditions": ["Sunny", "Clear", "Partly Cloudy"],
                "uv_index": [7, 7, 6],
                "forecast_flag": ["TRUE", "FALSE", True],
                "data_source": ["demo1", "demo1", "demo1"],
            }
        )

        # Inject custom weather data with mixed forecast flag representations
        loader.weather_df = weather_data

        df = loader.load_weather(forecast_only=True)

        assert len(df) == 2  # Only rows marked as forecast should remain
        assert df["forecast_flag"].dtype == bool
        assert df["forecast_flag"].all()

    def test_load_weather_filter_data_source(self, loader):
        """Test filtering weather by data source."""
        df = loader.load_weather(data_source="demo1")

        assert not df.empty
        assert (df["data_source"] == "demo1").all()

    def test_load_all(self, loader):
        """Test loading and merging all data."""
        df = loader.load_all()

        assert not df.empty

        # Should have destination columns
        assert "name" in df.columns
        assert "country" in df.columns

        # Should have cost columns
        assert "monthly_living_cost" in df.columns

        # Should have flight columns
        assert "price" in df.columns or "price_flight" in df.columns

        # Should have weather columns
        assert "temp_avg_c" in df.columns or "temp_avg_c_weather" in df.columns

    def test_load_all_filter_data_source(self, loader):
        """Test loading all data with data source filter."""
        df = loader.load_all(data_source="demo1")

        assert not df.empty

        # Check data sources where applicable
        if "data_source" in df.columns:
            assert (df["data_source"] == "demo1").all()

    def test_get_aggregates(self, loader):
        """Test computing aggregate statistics."""
        df = loader.get_aggregates()

        assert not df.empty
        assert len(df) == 6  # One row per destination

        # Check required columns
        assert "destination_id" in df.columns
        assert "name" in df.columns
        assert "country" in df.columns

        # Check aggregate columns exist
        if "avg_flight_price" in df.columns:
            assert df["avg_flight_price"].dtype == float
            assert (df["avg_flight_price"] > 0).any()

        if "avg_temp" in df.columns:
            assert df["avg_temp"].dtype == float
            # Reasonable temperature range
            assert df["avg_temp"].min() > 0
            assert df["avg_temp"].max() < 50

    def test_get_aggregates_with_data_source(self, loader):
        """Test aggregates filtered by data source."""
        df = loader.get_aggregates(data_source="demo1")

        assert not df.empty
        assert len(df) == 6

    def test_get_available_data_sources(self, loader):
        """Test getting list of available data sources."""
        sources = loader.get_available_data_sources()

        assert isinstance(sources, dict)

        # Should have some datasets
        assert len(sources) > 0

        # Each dataset should have a list of sources
        for dataset, source_list in sources.items():
            assert isinstance(source_list, list)
            assert len(source_list) > 0
            # demo1 should be in all sources
            assert "demo1" in source_list

    def test_clear_cache(self, loader):
        """Test clearing cached data."""
        # Load some data
        loader.load_destinations()
        loader.load_costs()

        # Verify cache is populated
        assert loader.destinations_df is not None
        assert loader.costs_df is not None

        # Clear cache
        loader.clear_cache()

        # Verify cache is cleared
        assert loader.destinations_df is None
        assert loader.costs_df is None
        assert loader.flights_df is None
        assert loader.weather_df is None

    def test_missing_file_error(self, tmp_path):
        """Test error handling when CSV file doesn't exist."""
        loader = DataLoader(data_dir=tmp_path)

        with pytest.raises(FileNotFoundError):
            loader.load_destinations()

    def test_load_data_convenience_function(self):
        """Test the convenience load_data function."""
        # Get loader instance
        loader = load_data(merge=False)
        assert isinstance(loader, DataLoader)

        # Get merged data
        data = load_data(data_source="demo1", merge=True)
        assert isinstance(data, pd.DataFrame)
        assert not data.empty


class TestDataIntegrity:
    """Test data integrity and relationships."""

    @pytest.fixture
    def loader(self):
        """Create a DataLoader instance for testing."""
        return DataLoader()

    def test_destination_ids_consistent(self, loader):
        """Test destination_id is consistent across all datasets."""
        destinations = loader.load_destinations()
        costs = loader.load_costs()
        flights = loader.load_flights()
        weather = loader.load_weather()

        dest_ids = set(destinations["destination_id"])

        # All cost destination_ids should exist in destinations
        assert set(costs["destination_id"]).issubset(dest_ids)

        # All flight destination_ids should exist in destinations
        assert set(flights["destination_id"]).issubset(dest_ids)

        # All weather destination_ids should exist in destinations
        assert set(weather["destination_id"]).issubset(dest_ids)

    def test_no_duplicate_destination_ids(self, loader):
        """Test destination_id is unique in destinations table."""
        destinations = loader.load_destinations()
        assert not destinations["destination_id"].duplicated().any()

    def test_flight_dates_valid(self, loader):
        """Test flight date relationships are valid."""
        flights = loader.load_flights()

        # Departure should be after or equal to search date
        assert (flights["departure_date"] >= flights["search_date"]).all()

        # Return should be after departure
        assert (flights["return_date"] > flights["departure_date"]).all()

    def test_weather_dates_are_future(self, loader):
        """Test weather forecast dates are reasonable."""
        weather = loader.load_weather(forecast_only=True)

        # Forecast dates should not be too far in the past
        # (allowing some flexibility for test data)
        oldest_date = weather["date"].min()
        # Should be within reasonable range (not ancient history)
        assert oldest_date.year >= 2025

    def test_prices_positive(self, loader):
        """Test all prices are positive numbers."""
        costs = loader.load_costs()
        flights = loader.load_flights()

        # Cost of living should be positive
        assert (costs["monthly_living_cost"] > 0).all()

        # Flight prices should be positive
        assert (flights["price"] > 0).all()

    def test_temperatures_reasonable(self, loader):
        """Test temperature values are in reasonable range."""
        weather = loader.load_weather()

        # Temperatures should be in Celsius range
        assert (weather["temp_low_c"] >= -50).all()
        assert (weather["temp_high_c"] <= 60).all()

        # High should be >= low
        assert (weather["temp_high_c"] >= weather["temp_low_c"]).all()

        # Average should be between low and high
        assert (weather["temp_avg_c"] >= weather["temp_low_c"]).all()
        assert (weather["temp_avg_c"] <= weather["temp_high_c"]).all()

    def test_humidity_valid_percentage(self, loader):
        """Test humidity is valid percentage (0-100)."""
        weather = loader.load_weather()

        assert (weather["humidity_percent"] >= 0).all()
        assert (weather["humidity_percent"] <= 100).all()

    def test_uv_index_valid_range(self, loader):
        """Test UV index is in valid range (0-11+)."""
        weather = loader.load_weather()

        assert (weather["uv_index"] >= 0).all()
        # UV index typically goes up to 11 (extreme), but allow higher
        assert (weather["uv_index"] <= 15).all()
