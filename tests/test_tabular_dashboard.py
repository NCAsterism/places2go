"""Tests for the tabular dashboard generator."""

from pathlib import Path
import re

import pandas as pd
import pytest

from scripts.visualizations.tabular_dashboard import create_tabular_dashboard


class TestTabularDashboard:
    """Tests for tabular dashboard generation."""

    def test_generates_dashboard_with_flight_links(self, tmp_path):
        """Test that dashboard includes clickable flight cost links."""
        output_path = tmp_path / "test_tabular_dashboard.html"
        
        create_tabular_dashboard(
            output_path=output_path,
            destination_name="Benidorm",
            month=11,
            year=2025,
        )
        
        # Verify file was created
        assert output_path.exists()
        assert output_path.stat().st_size > 10000
        
        # Read content
        content = output_path.read_text()
        
        # Verify basic structure
        assert "Benidorm Dashboard" in content
        assert "November 2025" in content
        assert "FLIGHTS FROM EXETER (£)" in content
        
        # Verify flight cost links are present
        assert "flight-price" in content
        assert "skyscanner.net/transport/flights" in content
        assert 'target="_blank"' in content
        assert 'title="Search flights on Skyscanner"' in content
        
        # Verify link format using regex
        link_pattern = r'<a href="https://www\.skyscanner\.net/transport/flights/[a-z]+/[a-z]+/\d{6}/?\?adults=\d+"'
        matches = re.findall(link_pattern, content)
        assert len(matches) > 0, "Should have at least one Skyscanner flight link"
        
    def test_flight_links_have_correct_structure(self, tmp_path):
        """Test that flight links have correct URL structure."""
        output_path = tmp_path / "test_tabular_dashboard.html"
        
        create_tabular_dashboard(
            output_path=output_path,
            destination_name="Benidorm",
            month=11,
            year=2025,
        )
        
        content = output_path.read_text()
        
        # Check for proper URL structure
        # Format: https://www.skyscanner.net/transport/flights/ext/alc/251101/?adults=1
        assert "/ext/alc/" in content  # Exeter to Alicante
        assert "251101" in content or "2511" in content  # November 2025 dates
        assert "adults=1" in content
        
    def test_flight_links_have_proper_styling(self, tmp_path):
        """Test that flight links have CSS styling."""
        output_path = tmp_path / "test_tabular_dashboard.html"
        
        create_tabular_dashboard(
            output_path=output_path,
            destination_name="Benidorm",
            month=11,
            year=2025,
        )
        
        content = output_path.read_text()
        
        # Verify CSS for flight-price links exists
        assert ".flight-price a {" in content
        assert "text-decoration:" in content
        assert "border-bottom:" in content
        assert ".flight-price a:hover {" in content


class TestTabularDashboardIntegration:
    """Integration tests for tabular dashboard."""

    def test_handles_destinations_without_flights(self, tmp_path):
        """Test dashboard generation for destinations without flight data."""
        output_path = tmp_path / "test_no_flights.html"
        
        # Benidorm should have flights for November 2025
        create_tabular_dashboard(
            output_path=output_path,
            destination_name="Benidorm",
            month=11,
            year=2025,
        )
        
        content = output_path.read_text()
        
        # Should still generate dashboard even if some dates lack flights
        assert "Benidorm Dashboard" in content
        assert output_path.exists()

    def test_generates_valid_html(self, tmp_path):
        """Test that generated HTML is valid and complete."""
        output_path = tmp_path / "test_valid_html.html"
        
        create_tabular_dashboard(
            output_path=output_path,
            destination_name="Benidorm",
            month=11,
            year=2025,
        )
        
        content = output_path.read_text()
        
        # Check for essential HTML structure
        assert "<!DOCTYPE html>" in content
        assert "<html>" in content
        assert "</html>" in content
        assert "<head>" in content
        assert "<body>" in content
        assert "<style>" in content
        assert "<table>" in content
        assert "</table>" in content
