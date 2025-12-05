# Beer in the sun

"Beer in the sun" is a lightweight concept for identifying spots that receive
direct sunshine—perfect for picking a sunny bench, beer garden table, or picnic
patch. The approach models how nearby buildings or trees cast shadows so that
we can answer the simple question: *is this spot in sunshine right now?*

## Problem statement

- Users want to know whether a given outdoor spot is currently sunlit.
- Buildings, walls, signage, and foliage all cast shadows that move throughout
  the day.
- A practical solution should work with limited inputs: the Sun's azimuth and
  altitude plus rough obstacle outlines.

## Modelling approach

1. **Sun position** — Represent the Sun at a moment in time as azimuth and
   altitude angles.
2. **Obstacles** — Describe obstructions by the azimuth span they occupy around
   the observer and the elevation angle they block above the horizon.
3. **Visibility check** — If the Sun sits within an obstacle's azimuth span *and*
   below its elevation angle, the spot is shaded; otherwise it is in sunshine.

This simplified geometry is fast to compute and works well with coarse obstacle
data (e.g., a skyline scan from a phone compass). It can be extended later with
polygons, time-dependent structures, or light-diffusion models.

## Implementation snippet

The module `scripts/core/sunlight.py` contains reusable helpers:

```python
from scripts.core.sunlight import Obstacle, SunPosition, is_in_sunshine

# Define a nearby office block that covers 150°–210° azimuth up to 20° elevation
office_block = Obstacle(azimuth_start=150, azimuth_end=210, elevation=20)

# Example Sun position at 14:30 (azimuth and altitude in degrees)
sun_now = SunPosition(azimuth=185, altitude=35)

if is_in_sunshine(sun_now, obstacles=[office_block], altitude_threshold=1.0):
    print("This bench is in sunshine.")
else:
    print("It is currently shaded.")
```

## Next steps

- Collect azimuth/elevation scans for common beer garden layouts to seed
  obstacle libraries.
- Integrate a solar position library (e.g., `astral`) to generate accurate
  `SunPosition` values by location and time.
- Pair with forecast data to surface "sunny hour" recommendations for each
  venue.
