"""Tests for the URL generator module."""

from datetime import date

import pytest

from scripts.core.url_generator import (
    generate_flight_search_url,
    generate_google_flights_url,
    generate_skyscanner_url,
)


class TestSkyscannerURLGeneration:
    """Tests for Skyscanner URL generation."""

    def test_generates_round_trip_url(self):
        """Test generating a round-trip Skyscanner URL."""
        url = generate_skyscanner_url(
            origin_airport="EXT",
            destination_airport="ALC",
            departure_date=date(2025, 11, 15),
            return_date=date(2025, 11, 22),
        )

        expected = "https://www.skyscanner.net/transport/flights/ext/alc/251115/251122/?adults=1"
        assert url == expected

    def test_generates_one_way_url(self):
        """Test generating a one-way Skyscanner URL."""
        url = generate_skyscanner_url(
            origin_airport="EXT",
            destination_airport="ALC",
            departure_date=date(2025, 11, 15),
            return_date=None,
        )

        expected = "https://www.skyscanner.net/transport/flights/ext/alc/251115/?adults=1"
        assert url == expected

    def test_handles_multiple_adults(self):
        """Test generating URL with multiple adults."""
        url = generate_skyscanner_url(
            origin_airport="EXT",
            destination_airport="ALC",
            departure_date=date(2025, 11, 15),
            return_date=date(2025, 11, 22),
            adults=2,
        )

        assert "adults=2" in url

    def test_lowercase_airport_codes(self):
        """Test that airport codes are converted to lowercase."""
        url = generate_skyscanner_url(
            origin_airport="BRS",
            destination_airport="AGP",
            departure_date=date(2025, 10, 10),
        )

        assert "/brs/agp/" in url

    def test_date_format(self):
        """Test that dates are formatted correctly (YYMMDD)."""
        url = generate_skyscanner_url(
            origin_airport="EXT",
            destination_airport="ALC",
            departure_date=date(2025, 1, 5),  # Jan 5, 2025
            return_date=date(2025, 12, 31),  # Dec 31, 2025
        )

        assert "/250105/" in url
        assert "/251231/" in url


class TestGoogleFlightsURLGeneration:
    """Tests for Google Flights URL generation."""

    def test_generates_round_trip_url(self):
        """Test generating a round-trip Google Flights URL."""
        url = generate_google_flights_url(
            origin_airport="EXT",
            destination_airport="ALC",
            departure_date=date(2025, 11, 15),
            return_date=date(2025, 11, 22),
        )

        assert "google.com/travel/flights" in url
        assert "EXT" in url
        assert "ALC" in url
        assert "2025-11-15" in url
        assert "2025-11-22" in url

    def test_generates_one_way_url(self):
        """Test generating a one-way Google Flights URL."""
        url = generate_google_flights_url(
            origin_airport="EXT",
            destination_airport="ALC",
            departure_date=date(2025, 11, 15),
            return_date=None,
        )

        assert "google.com/travel/flights" in url
        assert "EXT" in url
        assert "ALC" in url
        assert "2025-11-15" in url
        assert "returning" not in url


class TestFlightSearchURL:
    """Tests for the generic flight search URL generator."""

    def test_defaults_to_skyscanner(self):
        """Test that default source is Skyscanner."""
        url = generate_flight_search_url(
            origin_airport="EXT",
            destination_airport="ALC",
            departure_date=date(2025, 11, 15),
        )

        assert "skyscanner.net" in url

    def test_skyscanner_source(self):
        """Test generating Skyscanner URL explicitly."""
        url = generate_flight_search_url(
            origin_airport="EXT",
            destination_airport="ALC",
            departure_date=date(2025, 11, 15),
            source="skyscanner",
        )

        assert "skyscanner.net" in url

    def test_google_source(self):
        """Test generating Google Flights URL."""
        url = generate_flight_search_url(
            origin_airport="EXT",
            destination_airport="ALC",
            departure_date=date(2025, 11, 15),
            source="google",
        )

        assert "google.com/travel/flights" in url

    def test_handles_skyscanner_data_source_name(self):
        """Test that data sources like 'skyscanner_oct2025' work."""
        url = generate_flight_search_url(
            origin_airport="EXT",
            destination_airport="ALC",
            departure_date=date(2025, 11, 15),
            source="skyscanner_oct2025",
        )

        assert "skyscanner.net" in url

    def test_handles_string_dates(self):
        """Test that string dates are converted properly."""
        url = generate_flight_search_url(
            origin_airport="EXT",
            destination_airport="ALC",
            departure_date="2025-11-15",
            return_date="2025-11-22",
            source="skyscanner",
        )

        assert "skyscanner.net" in url
        assert "/251115/" in url
        assert "/251122/" in url

    def test_passes_additional_kwargs_to_skyscanner(self):
        """Test that additional kwargs are passed to Skyscanner."""
        url = generate_flight_search_url(
            origin_airport="EXT",
            destination_airport="ALC",
            departure_date=date(2025, 11, 15),
            source="skyscanner",
            adults=3,
        )

        assert "adults=3" in url


class TestIntegrationWithRealData:
    """Integration tests using actual flight data structure."""

    def test_generates_url_from_flight_record(self):
        """Test generating URL from a typical flight record."""
        # Simulate a flight record
        flight = {
            "origin_airport": "EXT",
            "destination_id": 1,  # Would need to map to ALC
            "departure_date": date(2025, 10, 11),
            "return_date": date(2025, 10, 18),
            "data_source": "demo1",
        }

        # For this test, we'll assume destination_id 1 is Alicante (ALC)
        url = generate_flight_search_url(
            origin_airport=flight["origin_airport"],
            destination_airport="ALC",  # From destinations mapping
            departure_date=flight["departure_date"],
            return_date=flight["return_date"],
            source=flight["data_source"],
        )

        assert "skyscanner.net" in url
        assert "/ext/alc/" in url

    def test_handles_various_data_sources(self):
        """Test that different data sources generate valid URLs."""
        data_sources = ["demo1", "demo2", "skyscanner_oct2025", "live"]

        for source in data_sources:
            url = generate_flight_search_url(
                origin_airport="EXT",
                destination_airport="ALC",
                departure_date=date(2025, 11, 15),
                source=source,
            )

            # Should generate valid URL regardless of source
            assert url.startswith("https://")
            assert len(url) > 50
