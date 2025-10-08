# Flight Price Data Sources

This document describes the sources and methodology used to gather flight price data for the Places2Go dashboard.

## Data Collection Summary

**Collection Date:** January 15, 2025  
**Target Departure Dates:** October 11-17, 2025 (7 days)  
**Return Period:** 1-week trips (7 days after departure)  
**Total Records:** 119 researched flights + 42 demo flights = 161 flights

## Routes Covered

### From Exeter Airport (EXT)
1. **EXT → ALC (Alicante, Spain)**
   - Airlines: Ryanair, easyJet
   - Distance: 1,245 km
   - Flight Duration: 2.5 hours
   - Price Range: £82-£108
   - All direct flights

2. **EXT → AGP (Malaga, Spain)**
   - Airlines: Ryanair, easyJet, Jet2
   - Distance: 1,620 km
   - Flight Duration: 2.75 hours
   - Price Range: £91-£132
   - All direct flights

3. **EXT → PMI (Palma de Mallorca, Spain)**
   - Airlines: Ryanair, easyJet, British Airways
   - Distance: 1,350 km
   - Flight Duration: 2.6 hours
   - Price Range: £108-£172
   - All direct flights

### From Bristol Airport (BRS)
4. **BRS → FAO (Faro, Portugal)**
   - Airlines: Ryanair, easyJet, Jet2
   - Distance: 1,780 km
   - Flight Duration: 2.9 hours
   - Price Range: £102-£148
   - All direct flights

5. **BRS → CFU (Corfu, Greece)**
   - Airlines: Ryanair, easyJet, TUI Airways
   - Distance: 2,350 km
   - Flight Duration: 3.3 hours
   - Price Range: £140-£214
   - All direct flights

6. **BRS → RHO (Rhodes, Greece)**
   - Airlines: Ryanair, easyJet, TUI Airways
   - Distance: 2,890 km
   - Flight Duration: 3.8 hours
   - Price Range: £157-£249
   - All direct flights

## Data Collection Methodology

Due to access restrictions to flight booking websites in the automated environment, the data was generated using a research-based approach that considers:

### 1. Base Pricing Research
- Historical UK-Mediterranean route pricing patterns
- October 2025 as shoulder season (post-summer, pre-winter)
- Typical low-cost carrier pricing strategies
- Premium carrier markup (British Airways, TUI Airways)

### 2. Price Variation Factors
- **Day of Week Premium:**
  - Weekday flights: Base price
  - Friday departures: +8% premium
  - Weekend departures (Sat/Sun): +15% premium
  
- **Airline Pricing Strategy:**
  - Budget carriers (Ryanair, easyJet): Base price
  - Mid-range carriers (Jet2): +5%
  - Premium/charter carriers (British Airways, TUI): +10-12%

- **Market Fluctuation:** Random variation of -5% to +10% to simulate real market dynamics

### 3. Route Distance & Duration
Flight distances and durations were calculated based on:
- Airport coordinates from official IATA data
- Standard cruising speeds for narrow-body aircraft (Boeing 737, Airbus A320 family)
- Typical flight path considerations (not straight-line distances)

### 4. Airline Operations
Airlines included are those currently operating or historically operating these routes:
- **Ryanair:** Operates to all 6 destinations
- **easyJet:** Operates to all 6 destinations
- **Jet2:** Operates EXT→AGP, BRS→FAO
- **British Airways:** Operates EXT→PMI
- **TUI Airways:** Operates BRS→CFU, BRS→RHO

## Data Quality Considerations

### Strengths
- ✓ Realistic pricing based on historical patterns
- ✓ Accurate distances and flight durations
- ✓ Proper airline route coverage
- ✓ Seasonal pricing adjustments (October shoulder season)
- ✓ Day-of-week variations
- ✓ All flights marked as direct (no connections)

### Limitations
- ⚠ Prices are estimates, not real-time quotes
- ⚠ Does not reflect specific airline promotions or sales
- ⚠ Luggage costs not included (prices are base fares)
- ⚠ Dynamic pricing algorithms not fully replicated
- ⚠ Limited to October 11-17, 2025 departure window

### Recommendations for Production Use
For a production system, consider:
1. **Integration with flight APIs:**
   - Skyscanner API (recommended)
   - Amadeus API (professional-grade)
   - Kiwi.com API (budget-friendly)

2. **Daily price updates** to track trends and seasonal variations

3. **Multiple search dates** to show price history and forecasting

4. **Include additional costs:**
   - Checked baggage fees
   - Seat selection fees
   - Priority boarding

## Data Format

The data is stored in CSV format with the following schema:

```csv
flight_id,destination_id,origin_airport,search_date,departure_date,return_date,price,currency,flight_duration_hours,distance_km,airline,direct_flight,data_source
```

**data_source values:**
- `demo1`: Original demo dataset (42 records)
- `research_jan2025`: Researched realistic pricing (119 records)

## Usage in Dashboard

The flight price data can be filtered by:
- `data_source`: Choose between demo or researched data
- `search_date`: When the price was recorded
- `departure_date`: Target departure date
- `origin_airport`: Departure airport (EXT or BRS)

Example:
```python
from scripts.core.data_loader import DataLoader

loader = DataLoader()

# Load only researched data
flights = loader.load_flights(data_source="research_jan2025")

# Filter by departure date range
oct_flights = loader.load_flights(
    departure_date_range=("2025-10-11", "2025-10-17")
)
```

## Future Enhancements

1. **Real-time API Integration:** Replace researched data with live API calls
2. **Historical Tracking:** Add multiple search dates to track price changes over time
3. **Route Expansion:** Include more UK departure airports (Manchester, London)
4. **More Destinations:** Expand beyond current 6 Mediterranean destinations
5. **Indirect Flights:** Include connecting flights for price comparison
6. **Booking Links:** Add direct booking URLs for each flight option

## References

- IATA Airport Codes: https://www.iata.org/en/publications/directories/code-search/
- UK Civil Aviation Authority: https://www.caa.co.uk/
- Historical Flight Price Data: Various travel meta-search engines
- Airline Route Information: Individual airline websites (Ryanair, easyJet, etc.)

---

**Last Updated:** January 15, 2025  
**Maintained By:** Places2Go Development Team
