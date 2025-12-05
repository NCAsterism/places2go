"""Sunlight visibility utilities for the "Beer in the sun" use case.

The helpers in this module provide a simple way to express whether a point is
in direct sunshine while accounting for surrounding obstructions such as
buildings, trees, or temporary structures. The geometry is intentionally
minimal: obstacles are modelled by the azimuth range they occupy around the
observer and the elevation angle they block above the horizon. If the Sun is
within the blocked azimuth range *and* below the obstacle's elevation angle,
the location is considered shaded; otherwise it is in sunshine.
"""

from dataclasses import dataclass
from typing import Iterable, List


def _normalise_azimuth(angle: float) -> float:
    """Normalise an azimuth angle to the range [0, 360).

    Args:
        angle: Raw azimuth angle in degrees. Positive and negative values are
            accepted.

    Returns:
        The input angle mapped onto the interval [0, 360).
    """

    return angle % 360


def _azimuth_in_range(angle: float, start: float, end: float) -> bool:
    """Check whether an angle lies within an azimuth span, handling wrap-around.

    The function works even when the azimuth window crosses north (e.g., a
    building running from 350° to 15°).

    Args:
        angle: Azimuth of interest in degrees.
        start: Start of the azimuth window in degrees.
        end: End of the azimuth window in degrees.

    Returns:
        True if the angle falls inside the azimuth range; otherwise False.
    """

    normalised_angle = _normalise_azimuth(angle)
    normalised_start = _normalise_azimuth(start)
    normalised_end = _normalise_azimuth(end)

    if normalised_start <= normalised_end:
        return normalised_start <= normalised_angle <= normalised_end

    # Range crosses north; treat it as two joined intervals.
    return normalised_angle >= normalised_start or normalised_angle <= normalised_end


@dataclass(frozen=True)
class SunPosition:
    """Represents the Sun's apparent position for a given moment in time."""

    azimuth: float
    altitude: float

    def is_above_horizon(self, threshold: float = 0.0) -> bool:
        """Return True when the Sun is above the specified altitude threshold."""

        return self.altitude > threshold


@dataclass(frozen=True)
class Obstacle:
    """A static obstruction described by its azimuth span and elevation angle."""

    azimuth_start: float
    azimuth_end: float
    elevation: float
    name: str = "obstacle"

    def blocks(self, sun_position: SunPosition) -> bool:
        """Determine whether this obstacle blocks direct sunshine.

        An obstacle blocks sunshine when the Sun is within its azimuth span and
        sits below the obstacle's elevation angle.
        """

        if sun_position.altitude > self.elevation:
            return False

        return _azimuth_in_range(
            sun_position.azimuth, self.azimuth_start, self.azimuth_end
        )


def is_in_sunshine(
    sun_position: SunPosition,
    obstacles: Iterable[Obstacle] | None = None,
    altitude_threshold: float = 0.0,
) -> bool:
    """Return True when the spot has direct sunshine.

    Args:
        sun_position: The Sun's azimuth and altitude at the observation point.
        obstacles: Any surrounding obstacles that may block the Sun.
        altitude_threshold: Minimum altitude (in degrees) that counts as
            sunshine. This helps ignore twilight conditions where shadows are
            effectively infinite.
    """

    if not sun_position.is_above_horizon(altitude_threshold):
        return False

    blocking_obstacles: List[Obstacle] = list(obstacles or [])

    return not any(obstacle.blocks(sun_position) for obstacle in blocking_obstacles)


def sunshine_ratio(
    sun_positions: Iterable[SunPosition],
    obstacles: Iterable[Obstacle] | None = None,
    altitude_threshold: float = 0.0,
) -> float:
    """Calculate the fraction of supplied moments that are in sunshine.

    Args:
        sun_positions: Sequence of Sun positions (for example, at five-minute
            intervals across an afternoon).
        obstacles: Surrounding obstacles to test against.
        altitude_threshold: Minimum altitude (in degrees) that counts as
            sunshine.

    Returns:
        A value between 0 and 1 indicating the proportion of moments that have
        sunshine.
    """

    sun_positions_list = list(sun_positions)
    if not sun_positions_list:
        return 0.0

    sunlit_count = sum(
        1
        for position in sun_positions_list
        if is_in_sunshine(
            position, obstacles=obstacles, altitude_threshold=altitude_threshold
        )
    )

    return sunlit_count / len(sun_positions_list)
