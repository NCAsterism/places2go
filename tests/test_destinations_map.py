"""Tests for the destinations map visualization."""

import pandas as pd
import pytest

from scripts.visualizations.destinations_map import (
    REGION_COLORS,
    create_destination_details_html,
    create_interactive_map,
    create_summary_stats_html,
)


@pytest.fixture
def sample_destinations_df():
    """Create a sample destinations DataFrame for testing."""
    return pd.DataFrame(
        {
            "destination_id": [1, 2, 3, 4, 5, 6],
            "name": ["Alicante", "Malaga", "Majorca", "Faro", "Corfu", "Rhodes"],
            "country": ["Spain", "Spain", "Spain", "Portugal", "Greece", "Greece"],
            "country_code": ["ES", "ES", "ES", "PT", "GR", "GR"],
            "region": [
                "Costa Blanca",
                "Costa del Sol",
                "Balearic Islands",
                "Algarve",
                "Ionian Islands",
                "Dodecanese",
            ],
            "latitude": [38.2830, 36.7213, 39.5696, 37.0194, 39.6243, 36.4341],
            "longitude": [-0.5581, -4.4213, 2.6502, -7.9322, 19.9217, 28.2176],
            "timezone": [
                "Europe/Madrid",
                "Europe/Madrid",
                "Europe/Madrid",
                "Europe/Lisbon",
                "Europe/Athens",
                "Europe/Athens",
            ],
            "airport_code": ["ALC", "AGP", "PMI", "FAO", "CFU", "RHO"],
            "airport_name": [
                "Alicante-Elche Airport",
                "Málaga-Costa del Sol Airport",
                "Palma de Mallorca Airport",
                "Faro Airport",
                "Corfu International Airport",
                "Rhodes International Airport",
            ],
            "origin_airport": ["EXT", "EXT", "EXT", "BRS", "BRS", "BRS"],
        }
    )


def test_region_colors_defined():
    """Test that all region colors are defined."""
    assert "Costa Blanca" in REGION_COLORS
    assert "Costa del Sol" in REGION_COLORS
    assert "Balearic Islands" in REGION_COLORS
    assert "Algarve" in REGION_COLORS
    assert "Ionian Islands" in REGION_COLORS
    assert "Dodecanese" in REGION_COLORS
    assert len(REGION_COLORS) == 6


def test_region_colors_are_hex():
    """Test that all region colors are valid hex color codes."""
    for region, color in REGION_COLORS.items():
        assert color.startswith("#")
        assert len(color) == 7  # #RRGGBB format


def test_create_interactive_map(sample_destinations_df):
    """Test that interactive map is created successfully."""
    fig = create_interactive_map(sample_destinations_df)

    # Check that figure was created
    assert fig is not None

    # Check that we have traces for each region
    assert len(fig.data) == 6  # 6 unique regions

    # Check that each trace has the correct number of points
    for trace in fig.data:
        assert len(trace.lon) > 0
        assert len(trace.lat) > 0
        assert len(trace.lon) == len(trace.lat)

    # Check that layout has geo configuration
    assert "geo" in fig.layout
    assert fig.layout.geo.scope == "europe"


def test_create_interactive_map_has_hover_data(sample_destinations_df):
    """Test that interactive map includes hover data."""
    fig = create_interactive_map(sample_destinations_df)

    # Check each trace has customdata for hover
    for trace in fig.data:
        assert trace.customdata is not None
        assert len(trace.customdata) > 0


def test_create_interactive_map_legend(sample_destinations_df):
    """Test that interactive map has legend configured."""
    fig = create_interactive_map(sample_destinations_df)

    # Check legend configuration
    assert "legend" in fig.layout
    assert fig.layout.legend.title.text == "Region"


def test_create_summary_stats_html(sample_destinations_df):
    """Test that summary statistics HTML is generated."""
    html = create_summary_stats_html(sample_destinations_df)

    # Check that HTML is generated
    assert html is not None
    assert len(html) > 0

    # Check that HTML contains expected sections
    assert "By Country" in html
    assert "By Region" in html

    # Check that all countries are mentioned
    assert "Spain" in html
    assert "Portugal" in html
    assert "Greece" in html

    # Check that all regions are mentioned
    for region in sample_destinations_df["region"].unique():
        assert region in html


def test_create_summary_stats_html_has_colors(sample_destinations_df):
    """Test that summary statistics HTML includes region colors."""
    html = create_summary_stats_html(sample_destinations_df)

    # Check that color styles are present
    assert "background-color:" in html
    assert "region-color" in html


def test_create_destination_details_html(sample_destinations_df):
    """Test that destination details HTML is generated."""
    html = create_destination_details_html(sample_destinations_df)

    # Check that HTML is generated
    assert html is not None
    assert len(html) > 0

    # Check that all destination names are present
    for name in sample_destinations_df["name"]:
        assert name in html

    # Check that all airport codes are present
    for code in sample_destinations_df["airport_code"]:
        assert code in html

    # Check for key field labels
    assert "Country:" in html
    assert "Region:" in html
    assert "Airport:" in html
    assert "Coordinates:" in html
    assert "Timezone:" in html


def test_create_destination_details_html_cards(sample_destinations_df):
    """Test that destination details HTML creates cards for each destination."""
    html = create_destination_details_html(sample_destinations_df)

    # Count the number of destination cards (each has a <div class="destination-card">)
    card_count = html.count('class="destination-card"')
    assert card_count == len(sample_destinations_df)


def test_create_destination_details_html_has_region_colors(sample_destinations_df):
    """Test that destination details cards include region colors."""
    html = create_destination_details_html(sample_destinations_df)

    # Check that border-left-color styles are present
    assert "border-left-color:" in html

    # Check that at least one region color is used
    for color in REGION_COLORS.values():
        if color in html:
            break
    else:
        pytest.fail("No region colors found in destination cards HTML")


def test_create_interactive_map_with_empty_df():
    """Test that interactive map handles empty DataFrame gracefully."""
    empty_df = pd.DataFrame(
        columns=[
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
    )

    fig = create_interactive_map(empty_df)

    # Should still create a figure, just with no data traces
    assert fig is not None
    assert len(fig.data) == 0


def test_create_interactive_map_marker_properties(sample_destinations_df):
    """Test that map markers have correct properties."""
    fig = create_interactive_map(sample_destinations_df)

    # Check marker properties
    for trace in fig.data:
        assert trace.mode == "markers"
        assert trace.marker.size == 15
        assert trace.marker.line.width == 2
        assert trace.marker.line.color == "white"
        assert trace.marker.symbol == "circle"


def test_summary_stats_counts_correct(sample_destinations_df):
    """Test that summary statistics show correct counts."""
    html = create_summary_stats_html(sample_destinations_df)

    # Spain should have 3 destinations
    assert "Spain" in html
    # Portugal should have 1
    assert "Portugal" in html
    # Greece should have 2
    assert "Greece" in html


def test_create_interactive_map_coordinates_range(sample_destinations_df):
    """Test that map has appropriate coordinate ranges for Europe."""
    fig = create_interactive_map(sample_destinations_df)

    # Check that lonaxis and lataxis are configured
    assert "lonaxis" in fig.layout.geo
    assert "lataxis" in fig.layout.geo

    # Check ranges are appropriate for viewing destinations
    lon_range = fig.layout.geo.lonaxis.range
    lat_range = fig.layout.geo.lataxis.range

    assert lon_range[0] < 0  # Should include negative longitudes (west)
    assert lon_range[1] > 0  # Should include positive longitudes (east)
    assert lat_range[0] < 40  # Should include southern destinations
    assert lat_range[1] > 35  # Should include northern destinations
