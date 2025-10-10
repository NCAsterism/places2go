# Data Collection GitHub Issues

Created: October 8, 2025

## Overview

We've created 21 GitHub issues to track real data collection for the Places2Go project. These issues are structured as 3 parent issues with 18 sub-tasks (6 per data type).

## Parent Issues

| Issue | Title | Sub-tasks | Labels |
|-------|-------|-----------|--------|
| [#46](https://github.com/NCAsterism/places2go/issues/46) | Research and gather real flight price data | #51-#56 | `data-collection`, `flights`, `parent-issue` |
| [#47](https://github.com/NCAsterism/places2go/issues/47) | Research and gather real weather forecast data | #57-#62 | `data-collection`, `weather`, `parent-issue` |
| [#50](https://github.com/NCAsterism/places2go/issues/50) | Research and gather real cost of living data | #63-#68 | `data-collection`, `costs`, `parent-issue` |

## Sub-tasks by Category

### Flight Prices (#51-#56)
Each sub-task covers one destination and requires:
- Price (GBP)
- Airline
- Flight duration (hours)
- Direct flight flag
- Distance (km)

Sources: Skyscanner, Google Flights, airline websites

- #51: Alicante (EXT → ALC)
- #52: Malaga (EXT → AGP)
- #53: Majorca (EXT → PMI)
- #54: Faro (BRS → FAO)
- #55: Corfu (BRS → CFU)
- #56: Rhodes (BRS → RHO)

### Weather Forecasts (#57-#62)
Each sub-task covers 7-day forecast (Oct 11-17, 2025) with:
- Temperature (high, low, avg)
- Rainfall
- Humidity
- Sunshine hours
- Wind speed
- Conditions
- UV index

Sources: OpenWeatherMap, Weather.com, BBC Weather, Met Office

- #57: Alicante
- #58: Malaga
- #59: Majorca
- #60: Faro
- #61: Corfu
- #62: Rhodes

### Cost of Living (#63-#68)
Each sub-task covers 11 cost metrics in EUR:
- Monthly living cost
- Rent (center & outside)
- Food, transport, utilities, internet
- Meal prices (inexpensive & mid-range)
- Beer (0.5L draught)
- Cannabis per gram

Sources: Numbeo, Expatistan, Idealista, local forums

- #63: Alicante
- #64: Malaga
- #65: Majorca
- #66: Faro
- #67: Corfu
- #68: Rhodes

## GitHub CLI Commands

### View Issues by Category

```powershell
# All data collection issues
gh issue list --label "data-collection"

# Flight sub-tasks only
gh issue list --label "flights,sub-task"

# Weather sub-tasks only
gh issue list --label "weather,sub-task"

# Cost sub-tasks only
gh issue list --label "costs,sub-task"

# Parent issues only
gh issue list --label "parent-issue"
```

### Assign Issues to Bots/Users

```powershell
# Assign a single issue
gh issue edit 51 --add-assignee username

# Assign multiple issues
gh issue edit 51 52 53 --add-assignee username

# View issue details
gh issue view 51
```

### Track Progress

```powershell
# Check open data collection issues
gh issue list --label "data-collection" --state open

# Check completed issues
gh issue list --label "data-collection" --state closed

# View specific parent issue with sub-tasks
gh issue view 46
```

## Data Output Files

When completing these issues, update the following CSV files:

- **Flights**: `data/flights/flight_prices.csv`
- **Weather**: `data/weather/weather_data.csv`
- **Costs**: `data/destinations/cost_of_living.csv`

## CSV Tracking

The `data/issues.csv` file tracks issues #9-#11 as references to these GitHub issues:
- Issue #9 → GitHub #46 (Flights)
- Issue #10 → GitHub #47 (Weather)
- Issue #11 → GitHub #50 (Costs)

## Next Steps

1. Assign sub-tasks to bots or team members
2. Bots perform web searches and gather real data
3. Update CSV files with real data
4. Close sub-tasks as completed
5. Close parent issues when all sub-tasks are done
6. Regenerate dashboards with real data

## Labels Reference

- `data-collection` - All data gathering issues
- `flights` - Flight price data
- `weather` - Weather forecast data
- `costs` - Cost of living data
- `parent-issue` - Parent tracking issue
- `sub-task` - Individual data collection task
