"""Tests for the dashboard chart generation functions.

These tests verify that chart generation functions create valid HTML files
with Plotly charts and handle error cases appropriately.
"""

import pandas as pd
import pytest

from scripts.dashboard import create_flight_cost_chart, create_time_vs_cost_chart


@pytest.fixture
def sample_df():
    """Create a sample DataFrame for testing chart functions."""
    data = {
        "Destination": ["Alicante", "Malaga", "Faro"],
        "Airport": ["Exeter", "Exeter", "Bristol"],
        "Flight Cost (GBP)": [120, 150, 180],
        "Flight Time (hrs)": [2.5, 2.7, 2.9],
        "Avg Temp (°C)": [25, 28, 24],
        "UV Index": [7, 8, 6],
        "Monthly Living Cost (GBP)": [800, 850, 750],
        "Meal Cost (GBP)": [10, 12, 8],
        "Beer Cost (GBP)": [3, 3.5, 2.8],
        "Weed Cost (GBP per gram)": [10, 12, 9],
    }
    return pd.DataFrame(data)


@pytest.fixture
def empty_df():
    """Create an empty DataFrame with correct columns for testing error handling."""
    columns = [
        "Destination",
        "Airport",
        "Flight Cost (GBP)",
        "Flight Time (hrs)",
        "Avg Temp (°C)",
        "UV Index",
        "Monthly Living Cost (GBP)",
        "Meal Cost (GBP)",
        "Beer Cost (GBP)",
        "Weed Cost (GBP per gram)",
    ]
    return pd.DataFrame(columns=columns)


class TestCreateFlightCostChart:
    """Tests for create_flight_cost_chart function."""

    def test_creates_html_file(self, tmp_path, sample_df):
        """Test that chart function creates HTML file in correct location."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        create_flight_cost_chart(sample_df, output_dir)

        output_file = output_dir / "flight_costs.html"
        assert output_file.exists(), "HTML file should be created"
        assert output_file.stat().st_size > 0, "HTML file should not be empty"

    def test_html_contains_plotly_structure(self, tmp_path, sample_df):
        """Test that generated HTML contains expected Plotly chart structure."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        create_flight_cost_chart(sample_df, output_dir)

        output_file = output_dir / "flight_costs.html"
        content = output_file.read_text()

        # Check for Plotly markers
        assert "plotly" in content.lower(), "HTML should contain Plotly library"
        assert (
            "Flight Cost by Destination and Airport" in content
        ), "Chart title should be present"

    def test_chart_contains_data_points(self, tmp_path, sample_df):
        """Test that chart has correct data points from DataFrame."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        create_flight_cost_chart(sample_df, output_dir)

        output_file = output_dir / "flight_costs.html"
        content = output_file.read_text()

        # Check that destination names appear in the HTML
        assert "Alicante" in content, "Destination 'Alicante' should appear in chart"
        assert "Malaga" in content, "Destination 'Malaga' should appear in chart"
        assert "Faro" in content, "Destination 'Faro' should appear in chart"

    def test_handles_empty_dataframe(self, tmp_path, empty_df):
        """Test error handling for empty DataFrame.

        Note: Plotly can handle empty DataFrames, so this should not raise an error,
        but should create a valid HTML file with an empty chart.
        """
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # This should not raise an exception
        create_flight_cost_chart(empty_df, output_dir)

        output_file = output_dir / "flight_costs.html"
        assert (
            output_file.exists()
        ), "HTML file should be created even for empty DataFrame"

    def test_output_directory_created_if_missing(self, tmp_path, sample_df):
        """Test that function works when output directory doesn't exist yet.

        Note: The current implementation doesn't create the directory automatically,
        so this test documents the expected behavior. If directory doesn't exist,
        an error will be raised by Plotly's write_html.
        """
        output_dir = tmp_path / "nonexistent_output"

        with pytest.raises(FileNotFoundError):
            create_flight_cost_chart(sample_df, output_dir)


class TestCreateTimeVsCostChart:
    """Tests for create_time_vs_cost_chart function."""

    def test_creates_html_file(self, tmp_path, sample_df):
        """Test that chart function creates HTML file."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        create_time_vs_cost_chart(sample_df, output_dir)

        output_file = output_dir / "flight_time_vs_cost.html"
        assert output_file.exists(), "HTML file should be created"
        assert output_file.stat().st_size > 0, "HTML file should not be empty"

    def test_html_contains_plotly_structure(self, tmp_path, sample_df):
        """Test that generated HTML contains expected Plotly chart structure."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        create_time_vs_cost_chart(sample_df, output_dir)

        output_file = output_dir / "flight_time_vs_cost.html"
        content = output_file.read_text()

        # Check for Plotly markers
        assert "plotly" in content.lower(), "HTML should contain Plotly library"
        assert "Flight Time vs Cost" in content, "Chart title should be present"

    def test_bubble_size_mapping(self, tmp_path, sample_df):
        """Test that bubble size mapping is correct (based on Monthly Living Cost)."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        create_time_vs_cost_chart(sample_df, output_dir)

        output_file = output_dir / "flight_time_vs_cost.html"
        content = output_file.read_text()

        # Verify that the size parameter references Monthly Living Cost
        # The data should be embedded in the HTML
        assert (
            "Monthly Living Cost" in content
        ), "Size mapping should reference Monthly Living Cost"

    def test_color_mapping_per_destination(self, tmp_path, sample_df):
        """Test that color mapping per destination is present."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        create_time_vs_cost_chart(sample_df, output_dir)

        output_file = output_dir / "flight_time_vs_cost.html"
        content = output_file.read_text()

        # Check that destinations are used for coloring
        assert "Alicante" in content, "Destination 'Alicante' should appear in chart"
        assert "Malaga" in content, "Destination 'Malaga' should appear in chart"
        assert "Faro" in content, "Destination 'Faro' should appear in chart"

    def test_hover_text_contains_expected_fields(self, tmp_path, sample_df):
        """Test that hover text contains expected fields (destination name)."""
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        create_time_vs_cost_chart(sample_df, output_dir)

        output_file = output_dir / "flight_time_vs_cost.html"
        content = output_file.read_text()

        # The hover_name parameter uses Destination, so destinations should appear
        # in the hover data
        assert "Alicante" in content, "Hover text should include destination"

    def test_handles_missing_columns(self, tmp_path):
        """Test error handling for missing columns.

        When required columns are missing, Plotly should raise a ValueError.
        """
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Create DataFrame missing required columns
        incomplete_df = pd.DataFrame(
            {
                "Destination": ["Alicante"],
                "Airport": ["Exeter"],
            }
        )

        with pytest.raises((ValueError, KeyError)):
            create_time_vs_cost_chart(incomplete_df, output_dir)

    def test_handles_empty_dataframe(self, tmp_path, empty_df):
        """Test error handling for empty DataFrame.

        Note: Plotly can handle empty DataFrames, so this should not raise an error,
        but should create a valid HTML file with an empty chart.
        """
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # This should not raise an exception
        create_time_vs_cost_chart(empty_df, output_dir)

        output_file = output_dir / "flight_time_vs_cost.html"
        assert (
            output_file.exists()
        ), "HTML file should be created even for empty DataFrame"
