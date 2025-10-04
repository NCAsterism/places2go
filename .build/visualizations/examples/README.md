# Examples and Screenshots

This directory contains screenshots and example outputs from the visualization pages.

## Screenshots

### Weather Forecast Dashboard

*(Screenshot to be added)*

The weather forecast dashboard shows:
- Temperature trends across all destinations
- Daily weather cards with icons and metrics
- Rainfall comparison bar chart
- UV index heatmap
- Weather conditions distribution
- Comfort index analysis

### Destinations Map

*(Screenshot to be added - when implemented)*

### Cost Comparison

*(Screenshot to be added - when implemented)*

### Flight Prices Time-Series

*(Screenshot to be added - when implemented)*

### Multi-Dataset Overlay

*(Screenshot to be added - future feature)*

## Adding Screenshots

To add a screenshot:

1. Generate the visualization
2. Open the HTML file in a browser
3. Take a screenshot (full page recommended)
4. Save as `<visualization_name>_screenshot.png` in this directory
5. Update this README with the screenshot reference

Example:
```markdown
![Weather Forecast Dashboard](weather_forecast_screenshot.png)
```

## Example Files

Example HTML outputs are not committed to git (they're regenerated), but you can generate them by running the visualization scripts:

```bash
python scripts/visualizations/weather_forecast.py
# Other scripts when available...
```

The generated HTML files will be in the parent directory (`.build/visualizations/`).
