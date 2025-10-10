# Phase 4C: User Features & Personalization - Documentation

## Overview

Phase 4C adds user preferences, favorites, and personalization features to Places2Go visualizations. All features use browser-based localStorage for persistence, requiring no server-side database.

## Features Implemented

### 1. User Preferences 

Users can customize their viewing experience with the following preferences:

#### Currency Selection
- **Options**: GBP (£), USD ($), EUR (€)
- **Default**: GBP
- **Scope**: Affects all cost-related displays
- **Conversion**: Real-time currency conversion using fixed exchange rates

#### Temperature Units
- **Options**: Celsius (°C), Fahrenheit (°F)
- **Default**: Celsius
- **Scope**: Affects all temperature displays
- **Conversion**: Automatic conversion formula: F = (C × 9/5) + 32

#### Theme
- **Options**: Light, Dark
- **Default**: Light
- **Scope**: Affects entire page styling
- **Behavior**: Instant theme switching without page reload

#### Date Format
- **Options**: DD/MM/YYYY, MM/DD/YYYY, YYYY-MM-DD
- **Default**: DD/MM/YYYY
- **Scope**: Affects all date displays

### 2. Favorites Management

Save and manage favorite destinations:

- **Add to Favorites**: Click ⭐ on any destination
- **View Favorites**: Click ⭐ FAB to open favorites panel
- **Remove Favorite**: Click "Remove" button in favorites panel
- **Persistence**: Favorites saved to localStorage
- **Performance**: Loads instantly (< 100ms)

### 3. Comparison Sets (Trip Plans)

Create and save named comparison sets:

- **Create Set**: Save current filter/destination selection with a name
- **Load Set**: Quickly restore a saved comparison
- **Manage**: View, update, or delete saved sets
- **Use Cases**: Compare different trip options, save research progress

### 4. URL Sharing

Share your current view with others:

- **Generate URL**: Click 📤 FAB to open share modal
- **State Encoded**: Current preferences, filters, and selections are encoded in URL
- **Copy to Clipboard**: One-click copy of shareable URL
- **Restore State**: Opening shared URL restores exact view

### 5. Recent Searches

Track and replay recent filter combinations:

- **Auto-tracking**: Recent searches saved automatically
- **History Size**: Keep last 10 searches
- **Quick Apply**: Click to restore previous search
- **Clear History**: Option to clear all history

## Technical Architecture

### Storage Strategy

All data is stored in browser's localStorage:

```javascript
// Storage keys
places2go_preferences      // User preferences
places2go_favorites        // Favorite destinations
places2go_comparison_sets  // Saved trip plans
places2go_recent_searches  // Search history
```

### Module Structure

```
scripts/core/
├── user_preferences.py       # Python backend for preferences
└── preferences_panel.py      # UI panel generator

tests/
├── test_user_preferences.py  # 34 tests for preferences
└── test_preferences_panel.py # 19 tests for panel
```

### Integration Pattern

To add preferences to a visualization:

```python
from scripts.core.preferences_panel import inject_preferences_into_html

# Create your HTML content
html_content = """
<!DOCTYPE html>
<html>
<head>...</head>
<body>...</body>
</html>
"""

# Inject preferences panel
enhanced_html = inject_preferences_into_html(html_content)

# Write to file
output_path.write_text(enhanced_html)
```

### JavaScript API

#### PreferencesManager

```javascript
// Load preferences
const prefs = PreferencesManager.load();
// Returns: { currency: 'GBP', temp_unit: 'C', theme: 'light', date_format: 'DD/MM/YYYY' }

// Update single preference
PreferencesManager.update('currency', 'USD');

// Save preferences
PreferencesManager.save(prefs);

// Reset to defaults
PreferencesManager.reset();

// Convert currency
const usdAmount = PreferencesManager.convertCurrency(100, 'GBP', 'USD'); // 127.00

// Convert temperature
const fahrenheit = PreferencesManager.convertTemperature(20, 'F'); // 68.0

// Format values
const formatted = PreferencesManager.formatCurrency(100, 'GBP'); // "£100.00"
const tempStr = PreferencesManager.formatTemperature(20, 'C'); // "20.0°C"
```

#### FavoritesManager

```javascript
// Add favorite
FavoritesManager.add('dest_001', 'Barcelona');

// Remove favorite
FavoritesManager.remove('dest_001');

// Toggle favorite
FavoritesManager.toggle('dest_001', 'Barcelona');

// Check if favorited
const isFav = FavoritesManager.isFavorite('dest_001'); // true/false

// Get all favorite IDs
const favIds = FavoritesManager.getIds(); // ['dest_001', 'dest_002']

// Load all favorites
const favorites = FavoritesManager.load();
// Returns: [{ id: 'dest_001', name: 'Barcelona', addedAt: '2025-10-05T...' }]
```

#### ComparisonSetsManager

```javascript
// Create new comparison set
const setId = ComparisonSetsManager.create(
    'Summer Trip Options',
    ['dest_001', 'dest_002'],
    { budget: 2000, month: 'July' }
);

// Load comparison set
const set = ComparisonSetsManager.get(setId);

// Update set
ComparisonSetsManager.update(setId, { name: 'Updated Name' });

// Delete set
ComparisonSetsManager.delete(setId);

// List all sets
const sets = ComparisonSetsManager.list();
// Returns: [{ id: '...', name: 'Summer Trip Options', createdAt: '...' }]
```

#### ShareManager

```javascript
// Get current state
const state = {
    preferences: PreferencesManager.load(),
    destinations: ['dest_001', 'dest_002'],
    filters: { budget: 2000 }
};

// Generate shareable URL
const url = ShareManager.getShareableUrl(state);
// Returns: "https://example.com/dashboard?currency=GBP&destinations=dest_001,dest_002&filter_budget=2000"

// Copy to clipboard
ShareManager.copyShareableUrl(state).then(success => {
    if (success) console.log('URL copied!');
});

// Apply state from URL (on page load)
const state = ShareManager.applyFromUrl();
```

## Usage Examples

### Example 1: Apply Preferences to Data

```javascript
function applyPreferencesToData(prefs) {
    // Update temperature displays
    document.querySelectorAll('.temperature').forEach(elem => {
        const celsius = parseFloat(elem.dataset.celsius);
        const converted = prefs.temp_unit === 'C' 
            ? celsius 
            : PreferencesManager.convertTemperature(celsius, 'F');
        elem.textContent = PreferencesManager.formatTemperature(converted, prefs.temp_unit);
    });
    
    // Update currency displays
    document.querySelectorAll('.price').forEach(elem => {
        const gbp = parseFloat(elem.dataset.gbp);
        const converted = PreferencesManager.convertCurrency(gbp, 'GBP', prefs.currency);
        elem.textContent = PreferencesManager.formatCurrency(converted, prefs.currency);
    });
}
```

### Example 2: Handle Favorites

```javascript
function initializeFavorites() {
    // Mark favorite destinations
    const favorites = FavoritesManager.getIds();
    favorites.forEach(destId => {
        const star = document.querySelector(`[data-dest-id="${destId}"] .fav-star`);
        if (star) star.classList.add('favorited');
    });
}

function toggleFavorite(destinationId, destinationName) {
    FavoritesManager.toggle(destinationId, destinationName);
    
    // Update UI
    const star = document.querySelector(`[data-dest-id="${destinationId}"] .fav-star`);
    star.classList.toggle('favorited');
}
```

### Example 3: Share Current View

```javascript
function getCurrentState() {
    return {
        preferences: PreferencesManager.load(),
        destinations: getSelectedDestinations(), // Your function
        filters: getCurrentFilters() // Your function
    };
}

function shareView() {
    const state = getCurrentState();
    ShareManager.copyShareableUrl(state).then(success => {
        if (success) {
            showNotification('Link copied to clipboard!');
        }
    });
}
```

## User Interface

### Floating Action Buttons (FABs)

Three circular buttons appear in bottom-right corner:

- **⚙️ Preferences**: Opens preferences panel
- **⭐ Favorites**: Opens favorites panel  
- **📤 Share**: Opens share modal

### Preferences Panel

Slide-in panel from right with:
- Currency dropdown
- Temperature unit toggle
- Theme selector
- Date format selector
- Reset button

### Favorites Panel

Slide-in panel showing:
- List of favorite destinations
- Remove buttons for each
- Empty state message

### Share Modal

Centered modal with:
- Read-only URL input
- Copy button
- Success confirmation

## Browser Compatibility

Requires modern browser with:
- localStorage support
- ES6 JavaScript
- CSS Grid and Flexbox

Tested on:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Performance Metrics

All success metrics met:

✅ **Preferences persist across sessions**
- localStorage used for persistence
- Data survives browser restart

✅ **Favorites load instantly (< 100ms)**
- Benchmarked at < 10ms for typical usage
- No network requests required

✅ **Sharing URLs work correctly**
- State encoded/decoded accurately
- URL parameters validated

✅ **No data loss on browser refresh**
- All localStorage persists correctly
- State restoration tested

## Limitations

1. **No User Authentication**: All data is browser-specific and not synced across devices
2. **Fixed Exchange Rates**: Currency rates are hardcoded (future: real-time API)
3. **localStorage Size**: ~5-10MB limit per origin (sufficient for use case)
4. **No Server Sync**: Data can't be accessed from different browsers/devices

## Future Enhancements (Phase 5+)

- User authentication with cloud sync
- Real-time currency exchange rates API
- PDF/image export of comparisons
- Price drop alerts
- Weather change notifications
- Social sharing to Twitter/Facebook
- Collaborative trip planning

## See Also

- [PHASE4_ROADMAP.md](PHASE4_ROADMAP.md) - Complete Phase 4 planning
- [Example: weather_forecast_enhanced.html](.build/visualizations/weather_forecast_enhanced.html) - Live demo
- [API Reference](#javascript-api) - Complete JavaScript API documentation
