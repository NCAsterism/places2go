# Phase 4C Implementation: User Features & Personalization

## Quick Start

### Running the Enhanced Demo

```bash
# Generate enhanced weather visualization with preferences
python scripts/visualizations/weather_forecast_enhanced.py

# Open in browser
open .build/visualizations/weather_forecast_enhanced.html
```

### Adding Preferences to Your Visualization

```python
from scripts.core.preferences_panel import inject_preferences_into_html

# Your existing HTML generation code
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>My Visualization</title>
</head>
<body>
    <h1>My Chart</h1>
    <div id="chart"></div>
</body>
</html>
"""

# Inject preferences panel
enhanced_html = inject_preferences_into_html(html_content)

# Save
with open('output.html', 'w') as f:
    f.write(enhanced_html)
```

## Features Overview

### 1. User Preferences ⚙️

**Available Settings:**
- Currency: GBP, USD, EUR
- Temperature: Celsius, Fahrenheit  
- Theme: Light, Dark
- Date Format: DD/MM/YYYY, MM/DD/YYYY, YYYY-MM-DD

**How to Use:**
1. Click ⚙️ button (bottom-right)
2. Select your preferences
3. Changes apply instantly
4. Preferences saved automatically

### 2. Favorites ⭐

**Save Destinations:**
- Click ⭐ on any destination card
- View all favorites: Click ⭐ FAB
- Remove: Use "Remove" button in panel

**Use Cases:**
- Mark destinations to research further
- Quick filter to favorite locations
- Track places you've visited

### 3. URL Sharing 📤

**Share Your View:**
1. Set up your preferences and filters
2. Click 📤 button
3. Copy the generated URL
4. Share with others

**What's Shared:**
- Currency/temperature preferences
- Selected destinations
- Active filters
- Comparison state

### 4. Comparison Sets

**Save Trip Plans:**
- Create named comparison groups
- Save multiple scenarios
- Compare side-by-side

**Example:**
- "Summer 2025 - Budget"
- "Winter Getaway - Luxury"
- "Family Trip Options"

### 5. Recent Searches

**Quick Access:**
- Last 10 searches saved
- One-click to restore
- Clear history option

## Implementation Details

### Python Modules

#### `scripts/core/user_preferences.py`

Core preferences management:
- UserPreferences dataclass
- Currency conversion functions
- Temperature conversion functions
- Format helpers

```python
from scripts.core.user_preferences import (
    UserPreferences,
    convert_currency,
    convert_temperature,
    format_currency,
    format_temperature
)

# Create preferences
prefs = UserPreferences(currency='USD', temp_unit='F')

# Convert values
usd_amount = convert_currency(100, 'GBP', 'USD')  # 127.00
fahrenheit = convert_temperature(20, 'F')  # 68.0

# Format for display
print(format_currency(127, 'USD'))  # "$127.00"
print(format_temperature(68, 'F'))  # "68.0°F"
```

#### `scripts/core/preferences_panel.py`

UI panel generator:
- HTML generation
- CSS styling (light/dark themes)
- JavaScript for interactions
- Injection utility

```python
from scripts.core.preferences_panel import (
    get_preferences_panel_html,
    get_preferences_panel_css,
    get_preferences_panel_js,
    inject_preferences_into_html
)

# Get individual components
html = get_preferences_panel_html()
css = get_preferences_panel_css()
js = get_preferences_panel_js()

# Or inject all at once
enhanced = inject_preferences_into_html(original_html)
```

### JavaScript API

All JavaScript managers are automatically included when using `inject_preferences_into_html()`.

#### PreferencesManager

```javascript
// Load/save preferences
const prefs = PreferencesManager.load();
PreferencesManager.save({ currency: 'USD', temp_unit: 'F' });
PreferencesManager.update('theme', 'dark');

// Convert values
const usd = PreferencesManager.convertCurrency(100, 'GBP', 'USD');
const fahrenheit = PreferencesManager.convertTemperature(20, 'F');

// Format for display
const price = PreferencesManager.formatCurrency(127, 'USD');
const temp = PreferencesManager.formatTemperature(68, 'F');
```

#### FavoritesManager

```javascript
// Manage favorites
FavoritesManager.add('dest_001', 'Barcelona');
FavoritesManager.remove('dest_001');
FavoritesManager.toggle('dest_001', 'Barcelona');

// Query favorites
const isFav = FavoritesManager.isFavorite('dest_001');
const favIds = FavoritesManager.getIds();
const allFavs = FavoritesManager.load();
```

#### ShareManager

```javascript
// Generate shareable URL
const state = getCurrentState();
const url = ShareManager.getShareableUrl(state);

// Copy to clipboard
ShareManager.copyShareableUrl(state);

// Restore from URL
const state = ShareManager.applyFromUrl();
```

## Customizing for Your Visualization

### 1. Override State Management

Provide custom `getCurrentState()` function:

```javascript
function getCurrentState() {
    return {
        preferences: PreferencesManager.load(),
        destinations: getSelectedDestinations(),
        filters: {
            budget: document.getElementById('budget').value,
            month: document.getElementById('month').value
        }
    };
}
```

### 2. Apply Preferences to Data

Provide custom `applyPreferencesToData()` function:

```javascript
function applyPreferencesToData(prefs) {
    // Update temperature displays
    updateTemperatures(prefs.temp_unit);
    
    // Update currency displays  
    updatePrices(prefs.currency);
    
    // Refresh charts
    refreshCharts(prefs);
}
```

### 3. Handle URL State

Provide custom `applyStateToVisualization()` function:

```javascript
function applyStateToVisualization(state) {
    // Apply destinations filter
    if (state.destinations.length > 0) {
        filterDestinations(state.destinations);
    }
    
    // Apply custom filters
    if (state.filters.budget) {
        setBudgetFilter(state.filters.budget);
    }
}
```

## Testing

### Run All Tests

```bash
# All preference-related tests
pytest tests/test_user_preferences.py tests/test_preferences_panel.py -v

# With coverage
pytest tests/test_user_preferences.py tests/test_preferences_panel.py --cov
```

### Test Coverage

- `test_user_preferences.py`: 34 tests
- `test_preferences_panel.py`: 19 tests
- Total: 53 tests
- Coverage: 100% on both modules

### Manual Testing

1. **Preferences Persistence**
   - Set preferences → Refresh page → Verify persistence

2. **Currency Conversion**
   - Switch currency → Verify values update correctly

3. **Temperature Conversion**
   - Switch to Fahrenheit → Verify conversion accuracy

4. **Theme Switching**
   - Toggle dark theme → Verify all elements styled

5. **Favorites**
   - Add favorite → Refresh → Verify still favorited

6. **URL Sharing**
   - Set state → Copy URL → Open in new tab → Verify state restored

## File Structure

```
scripts/
├── core/
│   ├── user_preferences.py        # 51 statements, 100% coverage
│   └── preferences_panel.py       # 19 statements, 100% coverage
└── visualizations/
    └── weather_forecast_enhanced.py  # Demo integration

tests/
├── test_user_preferences.py       # 34 tests
└── test_preferences_panel.py      # 19 tests

docs/
└── project/
    └── PHASE4C_GUIDE.md           # Full documentation
```

## Browser Requirements

- **localStorage**: Required for persistence
- **ES6 JavaScript**: Arrow functions, template literals
- **CSS Grid/Flexbox**: For responsive layout
- **Modern Browser**: Chrome 90+, Firefox 88+, Safari 14+

## Performance

All success metrics achieved:

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Preferences persist | Yes | Yes | ✅ |
| Favorites load time | < 100ms | < 10ms | ✅ |
| Sharing URLs work | Yes | Yes | ✅ |
| No data loss on refresh | Yes | Yes | ✅ |

## Known Limitations

1. **Browser-Specific Storage**: Data not synced across browsers/devices
2. **Fixed Exchange Rates**: Hardcoded rates (future: API integration)
3. **No Authentication**: No user accounts (future: Phase 5)
4. **localStorage Limits**: ~5-10MB per domain (sufficient for use case)

## Future Improvements

- [ ] Real-time currency API integration
- [ ] User authentication with cloud sync
- [ ] PDF/image export
- [ ] Price alerts
- [ ] Weather notifications
- [ ] Social media sharing

## Examples

See working example:
- `weather_forecast_enhanced.py` - Source code
- `.build/visualizations/weather_forecast_enhanced.html` - Generated output

## Support

- Documentation: `docs/project/PHASE4C_GUIDE.md`
- Issues: GitHub issue tracker
- Examples: `scripts/visualizations/weather_forecast_enhanced.py`

## License

MIT License - See LICENSE file for details
