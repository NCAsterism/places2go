# Phase 3C Plan: Multi-Dataset Overlay Dashboard

**Status:** Planning
**Estimated Duration:** 8-10 hours
**Assigned To:** TBD (GitHub Copilot candidate)
**Dependencies:** Phase 3A ✅, Phase 3B ✅

## Overview

Create a comprehensive overlay dashboard that integrates all individual visualizations (weather, flights, costs, destinations) into a single interactive interface with cross-dataset filtering and comparison capabilities.

## Objectives

### Primary Goal
Build a unified dashboard that allows users to:
- View all datasets simultaneously
- Filter data by destination across all visualizations
- Compare multiple destinations side-by-side
- Navigate between different view modes
- Export and share insights

### Success Criteria
- [ ] Single HTML page combining all 4 visualizations
- [ ] Shared filtering mechanism (destination selector)
- [ ] Date range selector affecting time-series data
- [ ] Tabbed or panel-based navigation
- [ ] Consistent styling and color scheme
- [ ] Responsive design (desktop and mobile)
- [ ] Fast load time (< 5 seconds)
- [ ] Interactive cross-chart highlighting

## Technical Approach

### Architecture Options

#### Option 1: Static HTML with JavaScript (Recommended for MVP)
**Pros:**
- Consistent with Phase 3B approach
- No server required
- Can still be deployed to GitHub Pages
- Plotly has built-in interactivity

**Cons:**
- Limited cross-chart communication
- No real-time updates
- More complex state management

**Implementation:**
- Reuse existing chart generation functions from Phase 3B
- Add JavaScript for:
  - Shared destination filter
  - Tab/panel navigation
  - Cross-chart event handlers
- Use Plotly's `Plotly.restyle()` and `Plotly.relayout()` for updates

#### Option 2: Dash Framework (Future Consideration)
**Pros:**
- Built for interactive dashboards
- Python-based (consistent with codebase)
- Excellent callback system
- Built-in components

**Cons:**
- Requires Python server
- More complex deployment
- Different architecture from Phase 3B

**Decision:** Defer to Phase 4+

### Data Integration Strategy

1. **Load All Datasets**
   ```python
   loader = DataLoader()
   destinations = loader.load_destinations()
   costs = loader.load_costs(data_source='demo1')
   flights = loader.load_flights(data_source='demo1')
   weather = loader.load_weather(data_source='demo1', forecast_only=True)
   ```

2. **Merge Strategy**
   - Use `destination_id` as primary key
   - Handle missing data gracefully (show "N/A" or hide charts)
   - Filter all datasets simultaneously when user selects destinations

3. **Chart Reuse**
   - Import chart creation functions from individual visualization modules
   - Wrap in container divs with consistent IDs
   - Apply shared color palette

### UI/UX Design

#### Layout Structure
```
┌─────────────────────────────────────────────────────────────┐
│                    Header & Title                            │
│              Destination Dashboard Overview                   │
├─────────────────────────────────────────────────────────────┤
│  Controls Panel                                              │
│  [Destination Filter] [Date Range] [View Mode] [Export]     │
├──────────────┬──────────────────────────────────────────────┤
│              │                                               │
│  Navigation  │         Main Content Area                     │
│  Sidebar     │                                               │
│              │  Tab 1: Overview (Summary Cards)              │
│  • Overview  │  Tab 2: Destinations Map                      │
│  • Map       │  Tab 3: Weather Forecast                      │
│  • Weather   │  Tab 4: Flight Prices                         │
│  • Flights   │  Tab 5: Cost of Living                        │
│  • Costs     │  Tab 6: Comparison View                       │
│  • Compare   │                                               │
│              │                                               │
└──────────────┴──────────────────────────────────────────────┘
```

#### Color Palette (Consistent with Phase 3B)
```python
DESTINATION_COLORS = {
    'Alicante': '#1f77b4',  # Blue
    'Malaga': '#ff7f0e',    # Orange
    'Majorca': '#2ca02c',   # Green
    'Faro': '#d62728',      # Red
    'Corfu': '#9467bd',     # Purple
    'Rhodes': '#8c564b'     # Brown
}
```

### Features by Tab

#### Tab 1: Overview Dashboard
- Summary cards showing:
  - Total destinations analyzed
  - Average flight price
  - Average monthly cost
  - Best weather destination (highest avg temp)
  - Cheapest destination
  - Most expensive destination
- Mini-charts (sparklines) for quick trends
- Quick comparison table

#### Tab 2: Destinations Map
- Reuse `destinations_map.py` chart
- Add click handlers to filter other tabs
- Highlight selected destinations
- Show summary metrics in tooltip

#### Tab 3: Weather Forecast
- Reuse charts from `weather_forecast.py`
- Filter by selected destinations
- Add date range selector
- Highlight forecast vs historical data

#### Tab 4: Flight Prices
- Reuse charts from `flight_prices.py`
- Filter by selected destinations and date range
- Add airline filter
- Show price trends with predictions (future)

#### Tab 5: Cost of Living
- Reuse charts from `cost_comparison.py`
- Filter by selected destinations
- Add currency converter (future)
- Show cost breakdown

#### Tab 6: Comparison View
- Side-by-side comparison of 2-3 destinations
- Key metrics table
- Radar/spider chart comparing all dimensions
- Pros/cons summary

### JavaScript Implementation

```javascript
// Shared state management
const dashboardState = {
    selectedDestinations: ['Alicante', 'Malaga', 'Majorca', 'Faro', 'Corfu', 'Rhodes'],
    dateRange: { start: '2025-10-05', end: '2025-10-11' },
    activeTab: 'overview'
};

// Filter update handler
function updateFilters(destinations) {
    dashboardState.selectedDestinations = destinations;
    refreshAllCharts();
}

// Refresh all visible charts
function refreshAllCharts() {
    const activeTab = dashboardState.activeTab;

    // Use Plotly.restyle to update traces
    if (activeTab === 'weather') {
        updateWeatherCharts();
    } else if (activeTab === 'flights') {
        updateFlightCharts();
    }
    // ... etc
}
```

## File Structure

```
scripts/visualizations/
├── overlay_dashboard.py          # Main dashboard generator (NEW)
├── weather_forecast.py            # Existing
├── flight_prices.py               # Existing
├── cost_comparison.py             # Existing
├── destinations_map.py            # Existing
└── shared/                        # NEW
    ├── __init__.py
    ├── filters.py                 # Filter UI components
    ├── navigation.py              # Tab/navigation components
    └── theme.py                   # Shared styling constants

tests/
├── test_overlay_dashboard.py     # NEW
└── test_shared/                   # NEW
    ├── test_filters.py
    └── test_navigation.py

.build/visualizations/
└── overlay_dashboard.html         # Generated dashboard (NEW)
```

## Implementation Steps

### Phase 1: Setup & Infrastructure (1-2 hours)
1. Create `overlay_dashboard.py` with basic structure
2. Set up shared utilities (`shared/` directory)
3. Define color palette and theme constants
4. Create HTML template structure

### Phase 2: Chart Integration (2-3 hours)
5. Import and integrate destinations map
6. Import and integrate weather charts
7. Import and integrate flight charts
8. Import and integrate cost charts
9. Ensure consistent sizing and styling

### Phase 3: Interactivity (2-3 hours)
10. Implement destination filter component
11. Add date range selector
12. Create tab navigation system
13. Wire up filter event handlers
14. Test cross-chart updates

### Phase 4: Comparison View (1-2 hours)
15. Create side-by-side comparison layout
16. Build comparison metrics table
17. Add radar chart for multi-dimensional comparison
18. Implement destination selection for comparison

### Phase 5: Polish & Testing (2 hours)
19. Add loading indicators
20. Optimize performance
21. Test responsive design
22. Add export functionality (save as PDF/image)
23. Write comprehensive tests
24. Update documentation

## Testing Strategy

### Unit Tests
- Test filter logic
- Test data merging functions
- Test chart generation with different filter states
- Test navigation state management

### Integration Tests
- Test full dashboard generation
- Test filtering across all charts
- Test date range selection
- Test tab navigation

### Manual Testing Checklist
- [ ] All charts render correctly
- [ ] Filters update all charts simultaneously
- [ ] Date range affects time-series charts only
- [ ] Navigation works smoothly
- [ ] Comparison view shows accurate data
- [ ] Responsive design works on mobile
- [ ] Export functionality works
- [ ] Performance is acceptable (< 5s load)
- [ ] No console errors
- [ ] Memory usage is reasonable

## Performance Considerations

### Optimization Strategies
1. **Lazy Loading**
   - Only load charts for active tab
   - Defer rendering of hidden tabs

2. **Data Caching**
   - Cache filtered datasets
   - Avoid recomputing on every update

3. **Chart Recycling**
   - Use `Plotly.react()` instead of recreating charts
   - Update data without full re-render

4. **Code Splitting**
   - Load Plotly from CDN
   - Minify custom JavaScript

### Target Metrics
- First Contentful Paint: < 1s
- Time to Interactive: < 3s
- Full Load Time: < 5s
- Chart Update Time: < 500ms

## Documentation Requirements

### User Documentation
- How to use the dashboard
- Filter and navigation guide
- Comparison view explanation
- Export instructions

### Developer Documentation
- Architecture overview
- Adding new visualizations
- Customizing filters
- Extending comparison features

## Success Metrics

### Quantitative
- Load time < 5 seconds
- All 73+ tests passing
- 100% code coverage on new modules
- File size < 500 KB (excluding Plotly CDN)

### Qualitative
- Intuitive navigation
- Consistent visual design
- Smooth interactions
- Clear data presentation
- Useful comparison insights

## Future Enhancements (Phase 4+)

1. **Real-Time Data**
   - Live flight price updates
   - Current weather conditions
   - Dynamic cost calculations

2. **Advanced Filtering**
   - Budget range slider
   - Weather preferences (min temp, max rainfall)
   - Flight preferences (max duration, direct only)
   - Multi-criteria scoring

3. **Personalization**
   - Save favorite destinations
   - Custom comparison sets
   - User preferences (currency, units)
   - Sharing/bookmarking

4. **AI/ML Features**
   - Price predictions
   - Best time to book recommendations
   - Destination recommendations based on preferences
   - Anomaly detection (unusual prices/weather)

5. **Social Features**
   - Share dashboard links
   - Export reports
   - Embed widgets
   - Public/private views

## Risk Assessment

### Technical Risks
- **Performance with all charts loaded:** Mitigated by lazy loading
- **Browser compatibility:** Test on major browsers (Chrome, Firefox, Safari, Edge)
- **Mobile performance:** Optimize chart sizes and interactions
- **JavaScript complexity:** Keep state management simple

### Scope Risks
- **Feature creep:** Stick to MVP, defer enhancements to Phase 4
- **Over-engineering:** Use simplest solution that works
- **Timeline pressure:** Focus on core features first

## Resources Required

### Development
- Time: 8-10 hours
- Developer: 1 (or GitHub Copilot)
- Testing: Manual + automated

### Tools & Libraries
- Python 3.9+
- Plotly
- DataLoader (existing)
- No additional dependencies needed

## Timeline

**Week 1:** Planning and setup (this document)
**Week 2:** Implementation (8-10 hours over 2-3 days)
**Week 3:** Testing and refinement
**Week 4:** Documentation and release

## Approval & Sign-off

- [ ] Technical design approved
- [ ] UI/UX mockup approved
- [ ] Timeline agreed
- [ ] Success criteria defined
- [ ] Ready to assign to Copilot

---

**Status:** Ready for Implementation
**Next Action:** Assign Issue #21 to GitHub Copilot
**Target Completion:** Week of October 7-14, 2025
