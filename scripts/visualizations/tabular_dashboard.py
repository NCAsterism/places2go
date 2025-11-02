"""
Tabular Dashboard Generator

Creates a spreadsheet-style dashboard view with dates as columns
and key metrics (weather, flights, costs) as rows.
"""

import logging
from pathlib import Path
from datetime import datetime

from scripts.core.data_loader import DataLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_tabular_dashboard(
    output_path: Path,
    destination_name: str = "Benidorm",
    month: int = 11,
    year: int = 2025,
):
    """Create a tabular dashboard for a specific destination and month."""
    logger.info(f"Creating tabular dashboard for {destination_name} - {month}/{year}")

    loader = DataLoader()
    destinations_df = loader.load_destinations()

    # Get destination ID
    dest = destinations_df[destinations_df["name"] == destination_name]
    if dest.empty:
        raise ValueError(f"Destination {destination_name} not found")

    dest_id = dest.iloc[0]["destination_id"]

    # Load data
    weather_df = loader.load_weather()
    weather_df = weather_df[weather_df["destination_id"] == dest_id]
    weather_df["date"] = weather_df["date"].dt.date

    flights_df = loader.load_flights()
    flights_df = flights_df[flights_df["destination_id"] == dest_id]
    if "departure_date" in flights_df.columns:
        flights_df["departure_date"] = flights_df["departure_date"].dt.date

    costs_df = loader.load_costs()
    costs_df = costs_df[costs_df["destination_id"] == dest_id]

    # Filter for the specified month
    weather_df = weather_df[
        (weather_df["date"].apply(lambda x: x.month) == month)
        & (weather_df["date"].apply(lambda x: x.year) == year)
    ]

    if not flights_df.empty and "departure_date" in flights_df.columns:
        flights_df = flights_df[
            (flights_df["departure_date"].apply(lambda x: x.month) == month)
            & (flights_df["departure_date"].apply(lambda x: x.year) == year)
        ]

    # Sort by date
    weather_df = weather_df.sort_values("date")
    if not flights_df.empty and "departure_date" in flights_df.columns:
        flights_df = flights_df.sort_values("departure_date")

    # Get unique dates
    dates = sorted(weather_df["date"].unique())

    # Build HTML
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{destination_name} Dashboard - {month}/{year}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 100%;
            overflow-x: auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        .subtitle {{
            color: #7f8c8d;
            margin-bottom: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 11px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
            white-space: nowrap;
        }}
        th {{
            background-color: #34495e;
            color: white;
            font-weight: 600;
            position: sticky;
            top: 0;
            z-index: 10;
        }}
        .row-header {{
            background-color: #ecf0f1;
            font-weight: 600;
            text-align: left;
            position: sticky;
            left: 0;
            z-index: 5;
        }}
        .section-header {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
            text-align: left;
        }}
        /* Temperature gradient: cold (blue) to hot (red) */
        .temp-cold {{
            background-color: #bbdefb;
            color: #01579b;
        }}
        .temp-cool {{
            background-color: #e3f2fd;
            color: #0277bd;
        }}
        .temp-mild {{
            background-color: #fff9c4;
            color: #f57f17;
        }}
        .temp-warm {{
            background-color: #ffcc80;
            color: #e65100;
        }}
        .temp-hot {{
            background-color: #ef9a9a;
            color: #b71c1c;
        }}
        /* Rainfall gradient: dry (light) to heavy (dark blue) */
        .rain-none {{
            background-color: #ffffff;
            color: #666666;
        }}
        .rain-light {{
            background-color: #e1f5fe;
            color: #01579b;
        }}
        .rain-moderate {{
            background-color: #81d4fa;
            color: #01579b;
        }}
        .rain-heavy {{
            background-color: #039be5;
            color: #ffffff;
        }}
        .rain-very-heavy {{
            background-color: #0277bd;
            color: #ffffff;
        }}
        .cost {{
            background-color: #fff9e6;
        }}
        /* Flight price gradient: cheap (green) to expensive (red) */
        .flight-cheap {{
            background-color: #c8e6c9;
            color: #1b5e20;
        }}
        .flight-reasonable {{
            background-color: #fff9c4;
            color: #f57f17;
        }}
        .flight-moderate {{
            background-color: #ffcc80;
            color: #e65100;
        }}
        .flight-expensive {{
            background-color: #ef9a9a;
            color: #b71c1c;
        }}
        .flight-very-expensive {{
            background-color: #d32f2f;
            color: #ffffff;
        }}
        .weekend {{
            background-color: #f0f0f0;
        }}
        .uv-low {{
            background-color: #c8e6c9;
            color: #1b5e20;
        }}
        .uv-moderate {{
            background-color: #fff9c4;
            color: #f57f17;
        }}
        .uv-high {{
            background-color: #ffcc80;
            color: #e65100;
        }}
        .uv-very-high {{
            background-color: #ef9a9a;
            color: #b71c1c;
        }}
        .uv-extreme {{
            background-color: #ce93d8;
            color: #4a148c;
        }}
        .summary {{
            margin-top: 20px;
            padding: 15px;
            background: #ecf0f1;
            border-radius: 4px;
        }}
        .summary-item {{
            display: inline-block;
            margin-right: 30px;
            margin-bottom: 10px;
        }}
        .summary-label {{
            font-weight: 600;
            color: #2c3e50;
        }}
        .summary-value {{
            color: #3498db;
            font-size: 18px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{destination_name} Dashboard</h1>
        <p class="subtitle">{datetime(year, month, 1).strftime('%B %Y')}</p>

        <table>
            <thead>
                <tr>
                    <th class="row-header">Metric</th>
"""

    # Add date headers
    for date in dates:
        day_name = datetime(date.year, date.month, date.day).strftime("%a")
        html += (
            f"                    <th>{date.day:02d}-{month:02d}<br>{day_name}</th>\n"
        )

    html += """                </tr>
            </thead>
            <tbody>
                <!-- Weather Section -->
                <tr>
                    <td class="section-header" colspan="999">WEATHER</td>
                </tr>
"""

    # Temperature High
    html += '                <tr>\n                    <td class="row-header">Max Temp (°C)</td>\n'
    for date in dates:
        day_weather = weather_df[weather_df["date"] == date]
        if not day_weather.empty:
            temp = day_weather.iloc[0]["temp_high_c"]
            # Temperature gradient: <10 cold, 10-15 cool, 15-20 mild, 20-25 warm, >25 hot
            if temp < 10:
                temp_class = "temp-cold"
            elif temp < 15:
                temp_class = "temp-cool"
            elif temp < 20:
                temp_class = "temp-mild"
            elif temp < 25:
                temp_class = "temp-warm"
            else:
                temp_class = "temp-hot"
            html += f'                    <td class="{temp_class}">{temp:.1f}</td>\n'
        else:
            html += "                    <td>-</td>\n"
    html += "                </tr>\n"

    # Temperature Low
    html += '                <tr>\n                    <td class="row-header">Min Temp (°C)</td>\n'
    for date in dates:
        day_weather = weather_df[weather_df["date"] == date]
        if not day_weather.empty:
            temp = day_weather.iloc[0]["temp_low_c"]
            # Temperature gradient: <5 cold, 5-10 cool, 10-15 mild, 15-20 warm, >20 hot
            if temp < 5:
                temp_class = "temp-cold"
            elif temp < 10:
                temp_class = "temp-cool"
            elif temp < 15:
                temp_class = "temp-mild"
            elif temp < 20:
                temp_class = "temp-warm"
            else:
                temp_class = "temp-hot"
            html += f'                    <td class="{temp_class}">{temp:.1f}</td>\n'
        else:
            html += "                    <td>-</td>\n"
    html += "                </tr>\n"

    # Rainfall
    html += '                <tr>\n                    <td class="row-header">Rainfall (mm)</td>\n'
    for date in dates:
        day_weather = weather_df[weather_df["date"] == date]
        if not day_weather.empty:
            rain = day_weather.iloc[0]["rainfall_mm"]
            # Rainfall gradient: 0 none, 0-2 light, 2-5 moderate, 5-10 heavy, >10 very heavy
            if rain == 0:
                rain_class = "rain-none"
            elif rain < 2:
                rain_class = "rain-light"
            elif rain < 5:
                rain_class = "rain-moderate"
            elif rain < 10:
                rain_class = "rain-heavy"
            else:
                rain_class = "rain-very-heavy"
            html += f'                    <td class="{rain_class}">{rain:.1f}</td>\n'
        else:
            html += "                    <td>-</td>\n"
    html += "                </tr>\n"

    # Humidity
    html += '                <tr>\n                    <td class="row-header">Humidity (%)</td>\n'
    for date in dates:
        day_weather = weather_df[weather_df["date"] == date]
        if not day_weather.empty:
            humidity = day_weather.iloc[0]["humidity_percent"]
            html += f"                    <td>{humidity:.0f}</td>\n"
        else:
            html += "                    <td>-</td>\n"
    html += "                </tr>\n"

    # Sunshine Hours
    html += '                <tr>\n                    <td class="row-header">Hours of Sunshine</td>\n'
    for date in dates:
        day_weather = weather_df[weather_df["date"] == date]
        if not day_weather.empty:
            sunshine = day_weather.iloc[0]["sunshine_hours"]
            html += f"                    <td>{sunshine:.2f}</td>\n"
        else:
            html += "                    <td>-</td>\n"
    html += "                </tr>\n"

    # Wind Speed
    html += '                <tr>\n                    <td class="row-header">Wind (km/h)</td>\n'
    for date in dates:
        day_weather = weather_df[weather_df["date"] == date]
        if not day_weather.empty:
            wind = day_weather.iloc[0]["wind_speed_kmh"]
            html += f"                    <td>{wind:.1f}</td>\n"
        else:
            html += "                    <td>-</td>\n"
    html += "                </tr>\n"

    # UV Index
    html += '                <tr>\n                    <td class="row-header">UV Index</td>\n'
    for date in dates:
        day_weather = weather_df[weather_df["date"] == date]
        if not day_weather.empty:
            uv = day_weather.iloc[0]["uv_index"]
            # Determine UV class based on level
            if uv <= 2:
                uv_class = "uv-low"
            elif uv <= 5:
                uv_class = "uv-moderate"
            elif uv <= 7:
                uv_class = "uv-high"
            elif uv <= 10:
                uv_class = "uv-very-high"
            else:
                uv_class = "uv-extreme"
            html += f'                    <td class="{uv_class}">{uv:.0f}</td>\n'
        else:
            html += "                    <td>-</td>\n"
    html += "                </tr>\n"

    # Sunrise/Sunset placeholders
    html += '                <tr>\n                    <td class="row-header">Sunrise</td>\n'
    for date in dates:
        html += "                    <td>08:00</td>\n"
    html += "                </tr>\n"

    html += (
        '                <tr>\n                    <td class="row-header">Sunset</td>\n'
    )
    for date in dates:
        html += "                    <td>16:00</td>\n"
    html += "                </tr>\n"

    # Flight Prices Section
    if not flights_df.empty and "departure_date" in flights_df.columns:
        html += """                <!-- Flight Prices Section -->
                <tr>
                    <td class="section-header" colspan="999">FLIGHTS (£)</td>
                </tr>
"""
        # Exeter flights
        html += '                <tr>\n                    <td class="row-header">Cost from Exeter (£)</td>\n'
        for date in dates:
            day_flights = flights_df[
                (flights_df["departure_date"] == date)
                & (flights_df["origin_airport"] == "EXT")
            ]
            if not day_flights.empty:
                min_price = day_flights["price"].min()
                # Flight price gradient: <35 cheap, 35-45 reasonable, 45-55 moderate, 55-70 expensive, >70 very expensive
                if min_price < 35:
                    price_class = "flight-cheap"
                elif min_price < 45:
                    price_class = "flight-reasonable"
                elif min_price < 55:
                    price_class = "flight-moderate"
                elif min_price < 70:
                    price_class = "flight-expensive"
                else:
                    price_class = "flight-very-expensive"
                html += f'                    <td class="{price_class}">{min_price:.0f}</td>\n'
            else:
                html += "                    <td>-</td>\n"
        html += "                </tr>\n"

        # Bristol flights
        html += '                <tr>\n                    <td class="row-header">Cost from Bristol (£)</td>\n'
        for date in dates:
            day_flights = flights_df[
                (flights_df["departure_date"] == date)
                & (flights_df["origin_airport"] == "BRS")
            ]
            if not day_flights.empty:
                min_price = day_flights["price"].min()
                # Flight price gradient: <35 cheap, 35-45 reasonable, 45-55 moderate, 55-70 expensive, >70 very expensive
                if min_price < 35:
                    price_class = "flight-cheap"
                elif min_price < 45:
                    price_class = "flight-reasonable"
                elif min_price < 55:
                    price_class = "flight-moderate"
                elif min_price < 70:
                    price_class = "flight-expensive"
                else:
                    price_class = "flight-very-expensive"
                html += f'                    <td class="{price_class}">{min_price:.0f}</td>\n'
            else:
                html += "                    <td>-</td>\n"
        html += "                </tr>\n"

    # Costs Section (static per month)
    if not costs_df.empty:
        html += """                <!-- Cost of Living Section -->
                <tr>
                    <td class="section-header" colspan="999">COSTS</td>
                </tr>
"""
        html += '                <tr>\n                    <td class="row-header">Cost from Bristol (£)</td>\n'
        for _ in dates:
            html += '                    <td class="cost">-</td>\n'
        html += "                </tr>\n"

    html += """            </tbody>
        </table>

        <div class="summary">
            <h3>Summary</h3>
"""

    # Add summary statistics
    if not weather_df.empty:
        avg_high = weather_df["temp_high_c"].mean()
        avg_low = weather_df["temp_low_c"].mean()
        total_rain = weather_df["rainfall_mm"].sum()
        avg_sunshine = weather_df["sunshine_hours"].mean()

        html += f"""            <div class="summary-item">
                <span class="summary-label">Avg High:</span>
                <span class="summary-value">{avg_high:.1f}°C</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">Avg Low:</span>
                <span class="summary-value">{avg_low:.1f}°C</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">Total Rain:</span>
                <span class="summary-value">{total_rain:.1f}mm</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">Avg Sunshine:</span>
                <span class="summary-value">{avg_sunshine:.1f}hrs/day</span>
            </div>
"""

    if not flights_df.empty and "price" in flights_df.columns:
        min_flight = flights_df["price"].min()
        max_flight = flights_df["price"].max()
        avg_flight = flights_df["price"].mean()

        html += f"""            <div class="summary-item">
                <span class="summary-label">Min Flight:</span>
                <span class="summary-value">£{min_flight:.0f}</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">Max Flight:</span>
                <span class="summary-value">£{max_flight:.0f}</span>
            </div>
            <div class="summary-item">
                <span class="summary-label">Avg Flight:</span>
                <span class="summary-value">£{avg_flight:.0f}</span>
            </div>
"""

    html += """        </div>
    </div>
</body>
</html>
"""

    # Write to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    logger.info(f"Tabular dashboard saved to {output_path}")


def main():
    """Main entry point."""
    logger.info("Starting tabular dashboard generation")

    # Get project root (2 levels up from this script)
    project_root = Path(__file__).resolve().parents[2]
    output_dir = project_root / ".build" / "visualizations"
    output_path = output_dir / "tabular_dashboard.html"

    create_tabular_dashboard(
        output_path, destination_name="Benidorm", month=11, year=2025
    )

    logger.info("Tabular dashboard generation completed successfully")
    logger.info(f"View dashboard at: {output_path}")


if __name__ == "__main__":
    main()
