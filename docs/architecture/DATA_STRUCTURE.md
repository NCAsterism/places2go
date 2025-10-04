# Data Structure Design

**Version:** 2.0
**Date:** October 4, 2025
**Status:** Proposed

---

## Overview

This document defines the new data structure for Places2Go, separating different data types for better organization and maintainability.

---

## Design Principles

1. **Separate Static from Dynamic** - Destination info vs. time-series data
2. **Single Responsibility** - Each CSV has one clear purpose
3. **Normalized Data** - Avoid duplication, use relationships
4. **Easy Updates** - Update one file without affecting others
5. **Version Control Friendly** - Smaller files, fewer conflicts
6. **Clear Schema** - Well-documented fields and constraints

---

## Current Structure (v1.0)

### dummy_data.csv
```csv
Destination,Country,Airport,Flight Cost (£),Flight Time (hours),Distance (km),Monthly Living Cost (£),Monthly Sunshine Hours
Alicante,Spain,ALC,45.23,2.5,1245,850,280
```

**Problems:**
- ❌ Mixes static and dynamic data
- ❌ Flight prices change over time (no date)
- ❌ Weather data is seasonal (no temporal dimension)
- ❌ Hard to update one aspect without touching all
- ❌ Can't track historical trends
- ❌ No data provenance (source, date collected)

---

## Proposed Structure (v2.0)

### 1. destinations.csv (Static Data)

**Purpose:** Core destination information that rarely changes

```csv
destination_id,name,country,country_code,region,latitude,longitude,timezone,population,airport_code,airport_name
1,Alicante,Spain,ES,Costa Blanca,38.2830,-0.5581,Europe/Madrid,334887,ALC,Alicante-Elche Airport
2,Malaga,Spain,ES,Costa del Sol,36.7213,-4.4213,Europe/Madrid,578460,AGP,Málaga-Costa del Sol Airport
3,Faro,Portugal,PT,Algarve,37.0194,-7.9322,Europe/Lisbon,64560,FAO,Faro Airport
```

**Schema:**
| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| destination_id | INTEGER | Yes | Unique identifier | 1 |
| name | TEXT | Yes | Destination name | Alicante |
| country | TEXT | Yes | Country name | Spain |
| country_code | TEXT(2) | Yes | ISO 3166-1 alpha-2 | ES |
| region | TEXT | No | Regional name | Costa Blanca |
| latitude | DECIMAL(8,6) | Yes | Latitude | 38.2830 |
| longitude | DECIMAL(9,6) | Yes | Longitude | -0.5581 |
| timezone | TEXT | Yes | IANA timezone | Europe/Madrid |
| population | INTEGER | No | City population | 334887 |
| airport_code | TEXT(3) | Yes | IATA airport code | ALC |
| airport_name | TEXT | Yes | Full airport name | Alicante-Elche Airport |

**Constraints:**
- PRIMARY KEY: destination_id
- UNIQUE: name, airport_code
- CHECK: latitude BETWEEN -90 AND 90
- CHECK: longitude BETWEEN -180 AND 180

---

### 2. cost_of_living.csv (Semi-Static Data)

**Purpose:** Monthly living costs per destination (updated quarterly)

```csv
destination_id,data_date,currency,rent_1br_center,rent_1br_outside,monthly_food,monthly_transport,utilities,internet,gym,healthcare_monthly,meal_inexpensive,meal_mid_range,beer_domestic,coffee,data_source,source_url
1,2025-10-01,GBP,650,480,250,50,120,30,35,40,12,35,3.50,2.80,Numbeo,https://www.numbeo.com/cost-of-living/in/Alicante
2,2025-10-01,GBP,720,550,280,55,130,35,40,45,13,38,3.80,3.00,Numbeo,https://www.numbeo.com/cost-of-living/in/Malaga
```

**Schema:**
| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| destination_id | INTEGER | Yes | FK to destinations | 1 |
| data_date | DATE | Yes | When data collected | 2025-10-01 |
| currency | TEXT(3) | Yes | ISO 4217 code | GBP |
| rent_1br_center | DECIMAL(10,2) | Yes | 1BR apt city center | 650.00 |
| rent_1br_outside | DECIMAL(10,2) | Yes | 1BR apt outside center | 480.00 |
| monthly_food | DECIMAL(10,2) | Yes | Groceries for 1 person | 250.00 |
| monthly_transport | DECIMAL(10,2) | Yes | Public transport pass | 50.00 |
| utilities | DECIMAL(10,2) | Yes | Electric, water, gas | 120.00 |
| internet | DECIMAL(10,2) | Yes | Internet 60Mbps+ | 30.00 |
| gym | DECIMAL(10,2) | No | Gym membership | 35.00 |
| healthcare_monthly | DECIMAL(10,2) | No | Health insurance | 40.00 |
| meal_inexpensive | DECIMAL(10,2) | No | Inexpensive restaurant | 12.00 |
| meal_mid_range | DECIMAL(10,2) | No | 3-course for 2 | 35.00 |
| beer_domestic | DECIMAL(10,2) | No | 0.5L domestic beer | 3.50 |
| coffee | DECIMAL(10,2) | No | Cappuccino | 2.80 |
| data_source | TEXT | Yes | Data provider | Numbeo |
| source_url | TEXT | No | URL to source | https://... |

**Constraints:**
- FOREIGN KEY: destination_id REFERENCES destinations(destination_id)
- PRIMARY KEY: (destination_id, data_date)
- CHECK: All cost fields >= 0

**Update Frequency:** Quarterly (Jan, Apr, Jul, Oct)

---

### 3. flight_prices.csv (Dynamic Time-Series Data)

**Purpose:** Historical and current flight prices (updated daily/weekly)

```csv
flight_id,destination_id,origin_airport,search_date,departure_date,return_date,price,currency,flight_duration_hours,distance_km,airline,direct_flight,booking_url,data_source
1,1,LHR,2025-10-04,2025-12-15,2025-12-22,45.23,GBP,2.5,1245,Ryanair,TRUE,https://...,Skyscanner
2,1,LHR,2025-10-04,2025-11-10,2025-11-17,38.50,GBP,2.5,1245,easyJet,TRUE,https://...,Skyscanner
3,2,LHR,2025-10-04,2025-12-15,2025-12-22,52.80,GBP,2.75,1620,British Airways,TRUE,https://...,Skyscanner
```

**Schema:**
| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| flight_id | INTEGER | Yes | Unique identifier | 1 |
| destination_id | INTEGER | Yes | FK to destinations | 1 |
| origin_airport | TEXT(3) | Yes | IATA origin code | LHR |
| search_date | DATE | Yes | When price was found | 2025-10-04 |
| departure_date | DATE | Yes | Flight departure | 2025-12-15 |
| return_date | DATE | No | Return flight (NULL if one-way) | 2025-12-22 |
| price | DECIMAL(10,2) | Yes | Total price | 45.23 |
| currency | TEXT(3) | Yes | ISO 4217 code | GBP |
| flight_duration_hours | DECIMAL(4,2) | Yes | Total flight time | 2.5 |
| distance_km | INTEGER | Yes | Flight distance | 1245 |
| airline | TEXT | No | Operating airline | Ryanair |
| direct_flight | BOOLEAN | Yes | Direct or with stops | TRUE |
| booking_url | TEXT | No | Link to book | https://... |
| data_source | TEXT | Yes | API/scraper used | Skyscanner |

**Constraints:**
- FOREIGN KEY: destination_id REFERENCES destinations(destination_id)
- PRIMARY KEY: flight_id
- UNIQUE: (destination_id, origin_airport, search_date, departure_date)
- CHECK: price >= 0
- CHECK: flight_duration_hours > 0
- CHECK: departure_date >= search_date

**Update Frequency:** Daily for next 90 days

---

### 4. weather_data.csv (Dynamic Time-Series Data)

**Purpose:** Historical and forecast weather data

```csv
weather_id,destination_id,date,temp_high_c,temp_low_c,temp_avg_c,rainfall_mm,humidity_percent,sunshine_hours,wind_speed_kmh,conditions,forecast_flag,data_source
1,1,2025-10-04,26,18,22,0,65,9.5,12,Sunny,FALSE,OpenWeather
2,1,2025-10-05,27,19,23,0,60,10.2,10,Clear,TRUE,OpenWeather
3,2,2025-10-04,28,20,24,2,70,8.8,15,Partly Cloudy,FALSE,OpenWeather
```

**Schema:**
| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| weather_id | INTEGER | Yes | Unique identifier | 1 |
| destination_id | INTEGER | Yes | FK to destinations | 1 |
| date | DATE | Yes | Weather date | 2025-10-04 |
| temp_high_c | DECIMAL(4,1) | Yes | High temperature Celsius | 26.0 |
| temp_low_c | DECIMAL(4,1) | Yes | Low temperature Celsius | 18.0 |
| temp_avg_c | DECIMAL(4,1) | Yes | Average temperature | 22.0 |
| rainfall_mm | DECIMAL(5,1) | Yes | Precipitation | 0.0 |
| humidity_percent | INTEGER | No | Relative humidity | 65 |
| sunshine_hours | DECIMAL(4,1) | No | Hours of sunshine | 9.5 |
| wind_speed_kmh | DECIMAL(4,1) | No | Average wind speed | 12.0 |
| conditions | TEXT | No | Weather description | Sunny |
| forecast_flag | BOOLEAN | Yes | TRUE if forecast, FALSE if actual | FALSE |
| data_source | TEXT | Yes | API used | OpenWeather |

**Constraints:**
- FOREIGN KEY: destination_id REFERENCES destinations(destination_id)
- PRIMARY KEY: weather_id
- UNIQUE: (destination_id, date)
- CHECK: temp_high_c >= temp_low_c
- CHECK: humidity_percent BETWEEN 0 AND 100
- CHECK: sunshine_hours BETWEEN 0 AND 24

**Update Frequency:**
- Historical: Once (immutable)
- Forecast: Daily for next 14 days

---

## Calculated/Derived Fields

These are computed on-the-fly, not stored:

### Monthly Total Cost
```python
def calculate_monthly_cost(cost_data, rent_type='center'):
    rent = cost_data['rent_1br_center'] if rent_type == 'center' else cost_data['rent_1br_outside']
    return (
        rent +
        cost_data['monthly_food'] +
        cost_data['monthly_transport'] +
        cost_data['utilities'] +
        cost_data['internet']
    )
```

### Annual Sunshine Hours
```python
def calculate_annual_sunshine(weather_data):
    # Average daily sunshine * 365
    return weather_data.groupby('destination_id')['sunshine_hours'].mean() * 365
```

### Average Flight Price
```python
def calculate_avg_flight_price(flight_data, days_ahead=30):
    # Average price for flights in next N days
    cutoff = datetime.now() + timedelta(days=days_ahead)
    return flight_data[flight_data['departure_date'] <= cutoff]['price'].mean()
```

---

## Data Relationships

```
destinations (1) ----< (many) cost_of_living
                |
                |
                ----< (many) flight_prices
                |
                |
                ----< (many) weather_data
```

**ERD:**
```
┌─────────────────┐
│  destinations   │
│─────────────────│
│ destination_id  │──┐
│ name            │  │
│ country         │  │
│ airport_code    │  │
│ ...             │  │
└─────────────────┘  │
                     │
        ┌────────────┼────────────┬────────────┐
        │            │            │            │
        ▼            ▼            ▼            ▼
┌─────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│cost_of_living flight_prices weather_data ...       │
│─────────────│ │──────────│ │──────────│ │──────────│
│dest_id (FK) │ │dest_id   │ │dest_id   │ │dest_id   │
│data_date    │ │search_   │ │date      │ │...       │
│rent_...     │ │date      │ │temp_...  │ │          │
│...          │ │price     │ │rainfall  │ │          │
└─────────────┘ └──────────┘ └──────────┘ └──────────┘
```

---

## Sample Queries

### Get full destination profile
```sql
SELECT
    d.*,
    c.rent_1br_center,
    c.monthly_food,
    AVG(f.price) as avg_flight_price,
    AVG(w.temp_avg_c) as avg_temperature,
    SUM(w.sunshine_hours)/COUNT(w.date) as avg_daily_sunshine
FROM destinations d
LEFT JOIN cost_of_living c ON d.destination_id = c.destination_id
LEFT JOIN flight_prices f ON d.destination_id = f.destination_id
LEFT JOIN weather_data w ON d.destination_id = w.destination_id
WHERE d.destination_id = 1
GROUP BY d.destination_id;
```

### Find cheapest flights next month
```sql
SELECT
    d.name,
    f.departure_date,
    f.price,
    f.airline
FROM flight_prices f
JOIN destinations d ON f.destination_id = d.destination_id
WHERE f.departure_date BETWEEN '2025-11-01' AND '2025-11-30'
ORDER BY f.price ASC
LIMIT 10;
```

### Compare monthly costs
```sql
SELECT
    d.name,
    c.rent_1br_center + c.monthly_food + c.monthly_transport + c.utilities as total_cost
FROM destinations d
JOIN cost_of_living c ON d.destination_id = c.destination_id
WHERE c.data_date = (SELECT MAX(data_date) FROM cost_of_living)
ORDER BY total_cost ASC;
```

---

## Data Loading (Python)

### Load all data
```python
import pandas as pd
from pathlib import Path

class DataLoader:
    def __init__(self, data_dir='data'):
        self.data_dir = Path(data_dir)

    def load_destinations(self):
        """Load static destination data"""
        return pd.read_csv(
            self.data_dir / 'destinations' / 'destinations.csv',
            parse_dates=['data_date']
        )

    def load_cost_of_living(self, latest_only=True):
        """Load cost of living data"""
        df = pd.read_csv(
            self.data_dir / 'destinations' / 'cost_of_living.csv',
            parse_dates=['data_date']
        )
        if latest_only:
            # Get most recent data for each destination
            df = df.sort_values('data_date').groupby('destination_id').tail(1)
        return df

    def load_flight_prices(self, days_ahead=90):
        """Load flight prices for next N days"""
        df = pd.read_csv(
            self.data_dir / 'flights' / 'flight_prices.csv',
            parse_dates=['search_date', 'departure_date', 'return_date']
        )
        # Filter to relevant date range
        cutoff = pd.Timestamp.now() + pd.Timedelta(days=days_ahead)
        return df[df['departure_date'] <= cutoff]

    def load_weather_data(self, historical_days=30, forecast_days=14):
        """Load weather data (historical + forecast)"""
        df = pd.read_csv(
            self.data_dir / 'weather' / 'weather_data.csv',
            parse_dates=['date']
        )
        start_date = pd.Timestamp.now() - pd.Timedelta(days=historical_days)
        end_date = pd.Timestamp.now() + pd.Timedelta(days=forecast_days)
        return df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    def load_all(self):
        """Load and merge all data"""
        destinations = self.load_destinations()
        costs = self.load_cost_of_living()
        flights = self.load_flight_prices()
        weather = self.load_weather_data()

        # Merge on destination_id
        data = destinations.merge(costs, on='destination_id', how='left')

        # Aggregate flight prices
        flight_agg = flights.groupby('destination_id').agg({
            'price': 'mean',
            'flight_duration_hours': 'mean',
            'distance_km': 'first'
        }).reset_index()
        flight_agg.columns = ['destination_id', 'avg_flight_price',
                              'flight_duration', 'distance_km']
        data = data.merge(flight_agg, on='destination_id', how='left')

        # Aggregate weather
        weather_agg = weather[~weather['forecast_flag']].groupby('destination_id').agg({
            'temp_avg_c': 'mean',
            'sunshine_hours': 'sum',
            'rainfall_mm': 'sum'
        }).reset_index()
        weather_agg.columns = ['destination_id', 'avg_temp',
                               'total_sunshine_hours', 'total_rainfall']
        data = data.merge(weather_agg, on='destination_id', how='left')

        return data
```

---

## Migration Strategy

### Step 1: Create new CSV files from existing data

```python
def migrate_dummy_data():
    """Split dummy_data.csv into new structure"""
    df = pd.read_csv('data/dummy_data.csv')

    # 1. Create destinations.csv
    destinations = df[['Destination', 'Country', 'Airport', 'Distance (km)']].copy()
    destinations['destination_id'] = range(1, len(destinations) + 1)
    destinations.rename(columns={
        'Destination': 'name',
        'Country': 'country',
        'Airport': 'airport_code',
        'Distance (km)': 'distance_km'
    }, inplace=True)
    # Add missing fields (lookup or estimate)
    destinations['country_code'] = destinations['country'].map({'Spain': 'ES', 'Portugal': 'PT'})
    # ... add lat/lon, timezone, etc.
    destinations.to_csv('data/destinations/destinations.csv', index=False)

    # 2. Create cost_of_living.csv
    costs = df[['Destination', 'Monthly Living Cost (£)']].copy()
    costs['destination_id'] = range(1, len(costs) + 1)
    costs['data_date'] = '2025-10-01'
    costs['currency'] = 'GBP'
    # Split total into components (estimate)
    costs['rent_1br_center'] = costs['Monthly Living Cost (£)'] * 0.55
    costs['monthly_food'] = costs['Monthly Living Cost (£)'] * 0.25
    # ... etc.
    costs.to_csv('data/destinations/cost_of_living.csv', index=False)

    # 3. Create flight_prices.csv
    flights = df[['Destination', 'Airport', 'Flight Cost (£)', 'Flight Time (hours)', 'Distance (km)']].copy()
    flights['flight_id'] = range(1, len(flights) + 1)
    flights['destination_id'] = range(1, len(flights) + 1)
    flights['origin_airport'] = 'LHR'
    flights['search_date'] = pd.Timestamp.now().date()
    flights['departure_date'] = pd.Timestamp.now().date() + pd.Timedelta(days=30)
    # ... etc.
    flights.to_csv('data/flights/flight_prices.csv', index=False)

    # 4. Create weather_data.csv
    weather = df[['Destination', 'Monthly Sunshine Hours']].copy()
    weather['destination_id'] = range(1, len(weather) + 1)
    # Estimate daily from monthly
    weather['sunshine_hours'] = weather['Monthly Sunshine Hours'] / 30
    # ... generate dates, add temp/rainfall estimates
    weather.to_csv('data/weather/weather_data.csv', index=False)
```

### Step 2: Update data_loader.py

```python
# Old version
def load_data():
    return pd.read_csv('data/dummy_data.csv')

# New version
def load_data():
    loader = DataLoader()
    return loader.load_all()
```

### Step 3: Test compatibility

```bash
pytest tests/ -v
python scripts/dashboard.py
# Compare outputs
```

---

## Data Quality & Validation

### Validation rules
```python
def validate_destinations(df):
    assert df['destination_id'].is_unique, "destination_id must be unique"
    assert df['latitude'].between(-90, 90).all(), "Invalid latitude"
    assert df['longitude'].between(-180, 180).all(), "Invalid longitude"
    assert df['airport_code'].str.len().eq(3).all(), "Airport codes must be 3 chars"

def validate_cost_of_living(df):
    assert (df[df.columns[df.columns.str.contains('rent|cost|price')]] >= 0).all().all(), \
        "Costs must be non-negative"
    assert df['currency'].isin(['GBP', 'EUR', 'USD']).all(), "Invalid currency"

def validate_flight_prices(df):
    assert (df['departure_date'] >= df['search_date']).all(), \
        "departure_date must be >= search_date"
    assert (df['price'] > 0).all(), "Prices must be positive"
```

---

## Future Enhancements

1. **Recreational Data** (Phase 4)
   - `data/recreation/activities.csv`
   - Beach quality, nightlife, sports facilities

2. **Safety & Healthcare** (Phase 5)
   - `data/safety/crime_stats.csv`
   - `data/healthcare/facilities.csv`

3. **Expat Community** (Phase 6)
   - `data/community/expat_stats.csv`
   - Forum activity, meetup groups

4. **Historical Trends** (Phase 7)
   - Keep all historical data for trend analysis
   - Machine learning for price prediction

---

## Summary

**Key Improvements:**
- ✅ Separated static from dynamic data
- ✅ Time-series capability for flights & weather
- ✅ Normalized structure (no duplication)
- ✅ Data provenance (source tracking)
- ✅ Flexible for future expansion
- ✅ Better version control (smaller files)
- ✅ Clear schema and relationships

**Next Steps:**
1. Review and approve schema
2. Create migration script
3. Generate initial CSV files
4. Update data loader
5. Test thoroughly
6. Document in wiki

---

**Questions?** Create an issue with label `data-structure`.
