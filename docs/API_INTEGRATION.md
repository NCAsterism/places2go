# API Data Integration

This module provides real-time data integration for the Places2Go application through external APIs.

## Overview

The API integration layer provides:
- **Flight Prices**: Real-time flight pricing from Skyscanner/Amadeus APIs
- **Weather Forecasts**: 7-day weather forecasts from OpenWeatherMap API
- **Cost of Living**: City cost data from Teleport Public API

All API clients implement:
- File-based caching with configurable TTL
- Rate limiting to stay within API quotas
- Automatic retry with exponential backoff
- Graceful fallback to CSV data on failures
- Zero API key exposure (via environment variables)

## Architecture

```
scripts/data/
├── __init__.py           # Module exports
├── base_api.py           # Base API client with common functionality
├── flight_api.py         # Flight data fetcher
├── weather_api.py        # Weather data fetcher
└── cost_api.py           # Cost of living data fetcher
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env`:
```bash
# Weather API (OpenWeatherMap)
WEATHER_API_KEY=your_openweathermap_api_key_here

# Flight API (optional - falls back to CSV)
FLIGHT_API_KEY=your_flight_api_key_here
FLIGHT_API_PROVIDER=skyscanner

# Cost API (Teleport - no key needed)
# Free and open, no configuration required
```

### 3. Use the API Clients

```python
from scripts.data import FlightDataFetcher, WeatherDataFetcher, CostDataFetcher

# Fetch flight prices
flight_fetcher = FlightDataFetcher()
flights = flight_fetcher.fetch_prices(
    origin="EXT",
    destinations=["ALC", "AGP", "PMI"],
    departure_date="2025-10-15",
    return_date="2025-10-22"
)

# Fetch weather forecasts
weather_fetcher = WeatherDataFetcher()
destinations = [
    {"destination_id": 1, "latitude": 38.2830, "longitude": -0.5581},
    {"destination_id": 2, "latitude": 36.7213, "longitude": -4.4213},
]
weather = weather_fetcher.fetch_forecast(destinations, days=7)

# Fetch cost of living data
cost_fetcher = CostDataFetcher()
destinations = [
    {"destination_id": 1, "name": "Alicante", "country_code": "ES"},
    {"destination_id": 2, "name": "Malaga", "country_code": "ES"},
]
costs = cost_fetcher.fetch_costs(destinations)
```

## API Details

### Flight Data API

**Provider**: Skyscanner (via RapidAPI) or Amadeus
**Cache TTL**: 1 hour (configurable)
**Rate Limit**: 50 calls/minute
**Fallback**: CSV flight data

```python
from scripts.data import FlightDataFetcher

fetcher = FlightDataFetcher(
    api_key="your_key",
    provider="skyscanner",
    cache_ttl=3600
)

# Get cheapest flights
cheapest = fetcher.get_cheapest_flights(
    origin="EXT",
    destinations=["ALC", "AGP"],
    limit=5
)
```

**Note**: Flight API integration is currently a stub implementation. The actual API calls need to be implemented based on your chosen provider's API documentation.

### Weather Data API

**Provider**: OpenWeatherMap
**Cache TTL**: 6 hours (configurable)
**Rate Limit**: 1000 calls/day (free tier)
**Fallback**: CSV weather data

```python
from scripts.data import WeatherDataFetcher

fetcher = WeatherDataFetcher(api_key="your_openweathermap_key")

# Fetch 7-day forecast
weather = fetcher.fetch_forecast(destinations, days=7)

# Get current weather
current = fetcher.get_current_weather(lat=38.2830, lon=-0.5581)
```

**OpenWeatherMap API**: Get free API key at https://openweathermap.org/api
- Free tier: 1000 calls/day
- 5-day forecast available
- Historical data available

### Cost of Living API

**Provider**: Teleport Public API
**Cache TTL**: 30 days (costs change slowly)
**Rate Limit**: 50 calls/minute
**Fallback**: CSV cost data

```python
from scripts.data import CostDataFetcher

fetcher = CostDataFetcher()  # No API key needed

# Fetch cost data
costs = fetcher.fetch_costs(destinations)

# Get cost comparison
comparison = fetcher.get_cost_comparison()
```

**Teleport API**: https://developers.teleport.org/api/
- Free and open
- No authentication required
- Limited city coverage

## Caching Strategy

All API responses are cached to minimize API calls and improve performance:

| Data Type | Cache TTL | Rationale |
|-----------|-----------|-----------|
| Flight Prices | 1-6 hours | Prices change frequently |
| Weather Forecasts | 6-12 hours | Moderate update frequency |
| Cost of Living | 30 days | Costs change slowly |

Cache files are stored in `.cache/` directory (configurable via `CACHE_DIR` env var).

### Cache Management

```python
from scripts.data.base_api import CacheManager

cache = CacheManager()

# Clear specific cache
cache.clear("flight_prices_key")

# Clear all cache
cache.clear()
```

## Rate Limiting

Rate limiting is implemented using a token bucket algorithm:

```python
from scripts.data.base_api import RateLimiter

limiter = RateLimiter(max_calls=50, period=60)  # 50 calls per minute
limiter.wait_if_needed()  # Automatically waits if limit exceeded
```

Rate limits are configured via environment variables:
- `API_RATE_LIMIT`: Maximum calls (default: 50)
- `API_RATE_PERIOD`: Time period in seconds (default: 60)

## Error Handling

All API clients implement automatic fallback to CSV data on failures:

```python
try:
    data = fetcher.fetch_prices(...)
except Exception as e:
    # Automatically falls back to CSV data
    logger.error(f"API failed, using CSV fallback: {e}")
    data = fetcher._fallback_to_csv(...)
```

Error scenarios handled:
- API key missing/invalid
- Network timeouts
- Rate limit exceeded
- HTTP errors (4xx, 5xx)
- Invalid response format

## Configuration

All configuration is done via environment variables in `.env`:

```bash
# API Keys
WEATHER_API_KEY=your_key
FLIGHT_API_KEY=your_key
FLIGHT_API_PROVIDER=skyscanner

# Base URLs (optional)
WEATHER_API_BASE_URL=https://api.openweathermap.org/data/2.5
FLIGHT_API_BASE_URL=your_endpoint
COST_API_BASE_URL=https://api.teleport.org/api

# Caching
CACHE_DIR=.cache
FLIGHT_CACHE_TTL=3600
WEATHER_CACHE_TTL=21600
COST_CACHE_TTL=2592000

# Rate Limiting
API_RATE_LIMIT=50
API_RATE_PERIOD=60

# Application
APP_ENV=development
DEBUG=True
```

## Testing

Comprehensive tests are provided in `tests/test_api_clients.py`:

```bash
# Run all API tests
pytest tests/test_api_clients.py -v

# Run specific test class
pytest tests/test_api_clients.py::TestFlightDataFetcher -v

# Run with coverage
pytest tests/test_api_clients.py --cov=scripts/data --cov-report=html
```

Tests cover:
- Cache functionality (set, get, expiry, clear)
- Rate limiting
- API request/retry logic
- Fallback mechanisms
- Integration scenarios

## Best Practices

1. **API Keys**: Never commit API keys to version control
2. **Caching**: Use appropriate TTLs for each data type
3. **Rate Limits**: Monitor API usage to stay within quotas
4. **Error Handling**: Always provide fallback mechanisms
5. **Logging**: Enable logging to track API calls and errors

## Troubleshooting

### No data returned

Check that:
1. API keys are correctly configured in `.env`
2. API endpoints are accessible
3. Rate limits haven't been exceeded
4. CSV fallback data exists

### Cache not working

Check that:
1. `.cache/` directory exists and is writable
2. Cache TTL is appropriate for your use case
3. Cache files aren't corrupted

### Rate limit exceeded

Options:
1. Increase cache TTL to reduce API calls
2. Implement request queuing
3. Upgrade to higher API tier

## Future Enhancements

- [ ] Redis caching for distributed systems
- [ ] Background refresh jobs
- [ ] API response validation with Pydantic
- [ ] Metrics and monitoring
- [ ] Async API calls with asyncio
- [ ] GraphQL API support

## License

MIT License - See LICENSE file for details
