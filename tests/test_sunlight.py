"""Unit tests for the sunlight visibility helpers."""

from scripts.core.sunlight import (
    Obstacle,
    SunPosition,
    _azimuth_in_range,
    is_in_sunshine,
    sunshine_ratio,
)


def test_azimuth_range_wraps_north():
    """Ranges that cross north should still match values on either side."""

    assert _azimuth_in_range(355, 350, 10)
    assert _azimuth_in_range(5, 350, 10)
    assert not _azimuth_in_range(45, 350, 10)


def test_obstacle_blocks_low_sun():
    """Buildings with sufficient elevation should block low-altitude sun."""

    sun = SunPosition(azimuth=180, altitude=12)
    building = Obstacle(azimuth_start=150, azimuth_end=210, elevation=20, name="office")

    assert not is_in_sunshine(sun, obstacles=[building])


def test_sunshine_when_above_obstacle():
    """A taller Sun altitude than the obstacle height should not be blocked."""

    sun = SunPosition(azimuth=185, altitude=35)
    building = Obstacle(azimuth_start=150, azimuth_end=210, elevation=20, name="office")

    assert is_in_sunshine(sun, obstacles=[building])


def test_sunshine_ratio_counts_multiple_positions():
    """The sunshine ratio should reflect the share of unblocked moments."""

    building = Obstacle(azimuth_start=260, azimuth_end=310, elevation=25, name="tower")
    sun_positions = [
        SunPosition(azimuth=270, altitude=15),  # blocked by tower
        SunPosition(azimuth=240, altitude=15),  # clear
        SunPosition(azimuth=90, altitude=5),  # clear
        SunPosition(azimuth=300, altitude=30),  # above tower
    ]

    assert (
        sunshine_ratio(sun_positions, obstacles=[building], altitude_threshold=1.0)
        == 0.75
    )
