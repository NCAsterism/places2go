# Data Directory

This directory contains all data files for the Places2Go dashboard, organized by data type and update frequency.

## Directory Structure

```
data/
├── destinations/          # Destination and cost data (static/semi-static)
│   ├── destinations.csv       # Core destination information
│   └── cost_of_living.csv     # Monthly living costs
├── flights/               # Flight price data (dynamic, time-series)
│   └── flight_prices.csv      # Historical and future flight prices
├── weather/               # Weather data (dynamic, time-series)
│   └── weather_data.csv       # Daily weather observations and forecasts
└── dummy_data.csv         # Legacy single-file dataset (deprecated)
```

## Data Files

### 1. destinations/destinations.csv (Static)

Core destination information that rarely changes.

**Update Frequency:** As needed (new destinations added)

**Fields:**
- `destination_id` (INTEGER) - Unique identifier
- `name` (TEXT) - Destination city name
- `country` (TEXT) - Country name
- `country_code` (TEXT) - ISO 3166-1 alpha-2 code
- `region` (TEXT) - Regional/local area name
- `latitude` (DECIMAL) - Latitude coordinate
- `longitude` (DECIMAL) - Longitude coordinate
- `timezone` (TEXT) - IANA timezone identifier
- `airport_code` (TEXT) - IATA 3-letter airport code
- `airport_name` (TEXT) - Full airport name
- `origin_airport` (TEXT) - Primary UK departure airport (EXT/BRS)

**Example:**
```csv
1,Alicante,Spain,ES,Costa Blanca,38.2830,-0.5581,Europe/Madrid,ALC,Alicante-Elche Airport,EXT
```

---

### 2. destinations/cost_of_living.csv (Semi-Static)

Monthly living costs and expenses per destination.

**Update Frequency:** Quarterly (Jan, Apr, Jul, Oct)

**Fields:**
- `destination_id` (INTEGER) - FK to destinations
- `data_date` (DATE) - When data was collected/valid
- `currency` (TEXT) - ISO 4217 currency code (GBP)
- `monthly_living_cost` (DECIMAL) - Total estimated monthly cost
- `rent_1br_center` (DECIMAL) - 1-bedroom apartment in city center
- `rent_1br_outside` (DECIMAL) - 1-bedroom apartment outside center
- `monthly_food` (DECIMAL) - Groceries for 1 person
- `monthly_transport` (DECIMAL) - Public transport pass
- `utilities` (DECIMAL) - Electricity, water, gas
- `internet` (DECIMAL) - Internet connection (60Mbps+)
- `meal_inexpensive` (DECIMAL) - Inexpensive restaurant meal
- `meal_mid_range` (DECIMAL) - 3-course meal for 2, mid-range
- `beer_domestic` (DECIMAL) - 0.5L domestic beer in restaurant
- `weed_cost_per_gram` (DECIMAL) - Cannabis cost (where legal)
- `data_source` (TEXT) - Source identifier (e.g., "demo1", "numbeo", "expatistan")

**Example:**
```csv
1,2025-10-01,GBP,800,440,330,200,40,90,25,10,28,3.0,10,demo1
```

---

### 3. flights/flight_prices.csv (Dynamic Time-Series)

Flight price data with search and departure dates for time-series analysis.

**Update Frequency:** Daily (for next 90 days)

**Fields:**
- `flight_id` (INTEGER) - Unique identifier
- `destination_id` (INTEGER) - FK to destinations
- `origin_airport` (TEXT) - IATA departure airport code
- `search_date` (DATE) - When price was found
- `departure_date` (DATE) - Flight departure date
- `return_date` (DATE) - Return flight date (NULL if one-way)
- `price` (DECIMAL) - Total return price
- `currency` (TEXT) - ISO 4217 currency code
- `flight_duration_hours` (DECIMAL) - Total flight time
- `distance_km` (INTEGER) - Flight distance
- `airline` (TEXT) - Operating airline
- `direct_flight` (BOOLEAN) - TRUE if direct, FALSE if stops
- `data_source` (TEXT) - Source identifier (e.g., "demo1", "skyscanner", "kayak")

**Example:**
```csv
1,1,EXT,2025-10-04,2025-10-11,2025-10-18,120,GBP,2.5,1245,Ryanair,TRUE,demo1
```

**Time-Series Usage:**
- Track price changes over time by comparing `search_date` for same `departure_date`
- Analyze price trends by departure day of week
- Find cheapest times to travel

---

### 4. weather/weather_data.csv (Dynamic Time-Series)

Daily weather observations and forecasts per destination.

**Update Frequency:** Daily
- Historical data: Immutable once recorded
- Forecast data: Updated daily for next 14 days

**Fields:**
- `weather_id` (INTEGER) - Unique identifier
- `destination_id` (INTEGER) - FK to destinations
- `date` (DATE) - Weather observation date
- `temp_high_c` (DECIMAL) - High temperature (Celsius)
- `temp_low_c` (DECIMAL) - Low temperature (Celsius)
- `temp_avg_c` (DECIMAL) - Average temperature (Celsius)
- `rainfall_mm` (DECIMAL) - Precipitation in millimeters
- `humidity_percent` (INTEGER) - Relative humidity (0-100)
- `sunshine_hours` (DECIMAL) - Hours of sunshine (0-24)
- `wind_speed_kmh` (DECIMAL) - Average wind speed
- `conditions` (TEXT) - Weather description
- `uv_index` (INTEGER) - UV index (0-11+)
- `forecast_flag` (BOOLEAN) - TRUE if forecast, FALSE if actual
- `data_source` (TEXT) - Source identifier (e.g., "demo1", "openweather", "weatherapi")

**Example:**
```csv
1,1,2025-10-05,26,18,22,0,65,9.5,12,Sunny,7,TRUE,demo1
```

**Time-Series Usage:**
- Calculate seasonal averages
- Identify best travel months
- Compare current weather to historical patterns

---

## Data Source Tracking

All dynamic data includes a `data_source` column to track where data came from:

| Source Value | Description |
|--------------|-------------|
| `demo1` | Demo/dummy data for testing |
| `demo2` | Alternative demo dataset |
| `live` | Real-time production data |
| `numbeo` | Numbeo cost of living API |
| `skyscanner` | Skyscanner flight API |
| `openweather` | OpenWeather API |
| `manual` | Manually entered data |

This allows mixing demo and live data during development and testing.

---

## Relationships

```
destinations (1) ----< (many) cost_of_living
             (1) ----< (many) flight_prices
             (1) ----< (many) weather_data
```

All data files reference `destinations.destination_id` as the primary key.

---

## Usage Example

### Loading All Data

```python
import pandas as pd
from pathlib import Path

data_dir = Path('data')

# Load static data
destinations = pd.read_csv(data_dir / 'destinations' / 'destinations.csv')
costs = pd.read_csv(data_dir / 'destinations' / 'cost_of_living.csv', parse_dates=['data_date'])

# Load time-series data
flights = pd.read_csv(data_dir / 'flights' / 'flight_prices.csv',
                      parse_dates=['search_date', 'departure_date', 'return_date'])
weather = pd.read_csv(data_dir / 'weather' / 'weather_data.csv',
                      parse_dates=['date'])

# Merge for analysis
data = destinations.merge(costs, on='destination_id', how='left')
```

### Filtering by Data Source

```python
# Get only demo data
demo_flights = flights[flights['data_source'] == 'demo1']

# Get only live data
live_weather = weather[weather['data_source'] == 'live']

# Mix demo and live
mixed_data = flights[flights['data_source'].isin(['demo1', 'live'])]
```

---

## Migration from Legacy Format

The old `dummy_data.csv` file has been split into these new files:
- Static info → `destinations/destinations.csv`
- Costs → `destinations/cost_of_living.csv`
- Flight prices → `flights/flight_prices.csv` (now time-series)
- Weather → `weather/weather_data.csv` (now time-series)

The legacy file is kept for backward compatibility but will be removed in a future version.

---

## Future Enhancements

Planned additional data files:
- `destinations/activities.csv` - Recreation and activities
- `destinations/safety.csv` - Safety and crime statistics
- `flights/airlines.csv` - Airline information and ratings
- `weather/climate_normals.csv` - Historical climate averages

---

**Last Updated:** October 4, 2025
**Data Format Version:** 2.0
