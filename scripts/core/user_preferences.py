"""
User preferences management for the Places2Go dashboard.

This module provides functionality for managing user preferences including:
- Currency selection (USD, EUR, GBP)
- Temperature units (Celsius/Fahrenheit)
- Theme selection (light/dark)
- Date format preferences

For Phase 4C, preferences are stored client-side using browser localStorage.
This module provides the data structures and conversion utilities used by
the visualization scripts to support user-configurable settings.
"""

from dataclasses import dataclass, asdict
import json
from typing import Dict, Any, Optional, Literal


CurrencyType = Literal["USD", "EUR", "GBP"]
TempUnitType = Literal["C", "F"]
ThemeType = Literal["light", "dark"]
DateFormatType = Literal["DD/MM/YYYY", "MM/DD/YYYY", "YYYY-MM-DD"]


@dataclass
class UserPreferences:
    """
    User preferences for dashboard customization.

    Attributes:
        currency: Preferred currency for cost display (USD, EUR, GBP)
        temp_unit: Temperature unit preference (C for Celsius, F for Fahrenheit)
        theme: Visual theme preference (light or dark)
        date_format: Date display format preference
    """

    currency: CurrencyType = "GBP"
    temp_unit: TempUnitType = "C"
    theme: ThemeType = "light"
    date_format: DateFormatType = "DD/MM/YYYY"

    def to_dict(self) -> Dict[str, str]:
        """
        Convert preferences to dictionary.

        Returns:
            Dictionary representation of preferences
        """
        return asdict(self)

    def to_json(self) -> str:
        """
        Convert preferences to JSON string.

        Returns:
            JSON string representation of preferences
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserPreferences":
        """
        Create UserPreferences from dictionary.

        Args:
            data: Dictionary containing preference values

        Returns:
            UserPreferences instance

        Example:
            >>> prefs = UserPreferences.from_dict({
            ...     'currency': 'USD',
            ...     'temp_unit': 'F'
            ... })
        """
        return cls(
            currency=data.get("currency", "GBP"),
            temp_unit=data.get("temp_unit", "C"),
            theme=data.get("theme", "light"),
            date_format=data.get("date_format", "DD/MM/YYYY"),
        )

    @classmethod
    def from_json(cls, json_str: str) -> "UserPreferences":
        """
        Create UserPreferences from JSON string.

        Args:
            json_str: JSON string containing preferences

        Returns:
            UserPreferences instance

        Raises:
            json.JSONDecodeError: If JSON string is invalid
        """
        data = json.loads(json_str)
        return cls.from_dict(data)


# Currency conversion rates (base: GBP)
# In production, these would be fetched from an API
CURRENCY_RATES: Dict[str, float] = {
    "GBP": 1.0,
    "USD": 1.27,  # 1 GBP = ~1.27 USD
    "EUR": 1.17,  # 1 GBP = ~1.17 EUR
}


def convert_currency(
    amount: float, from_currency: CurrencyType, to_currency: CurrencyType
) -> float:
    """
    Convert amount between currencies.

    Args:
        amount: Amount to convert
        from_currency: Source currency code
        to_currency: Target currency code

    Returns:
        Converted amount rounded to 2 decimal places

    Example:
        >>> convert_currency(100, 'GBP', 'USD')
        127.0
        >>> convert_currency(127, 'USD', 'GBP')
        100.0
    """
    if from_currency == to_currency:
        return round(amount, 2)

    # Convert to GBP first, then to target currency
    amount_in_gbp = amount / CURRENCY_RATES[from_currency]
    converted = amount_in_gbp * CURRENCY_RATES[to_currency]
    return round(converted, 2)


def convert_temperature(temp_c: float, to_unit: TempUnitType) -> float:
    """
    Convert temperature between Celsius and Fahrenheit.

    Args:
        temp_c: Temperature in Celsius
        to_unit: Target unit ('C' or 'F')

    Returns:
        Temperature in target unit, rounded to 1 decimal place

    Example:
        >>> convert_temperature(20, 'F')
        68.0
        >>> convert_temperature(20, 'C')
        20.0
    """
    if to_unit == "C":
        return round(temp_c, 1)
    else:  # F
        return round((temp_c * 9 / 5) + 32, 1)


def format_currency(amount: float, currency: CurrencyType) -> str:
    """
    Format currency amount with appropriate symbol.

    Args:
        amount: Amount to format
        currency: Currency code

    Returns:
        Formatted currency string

    Example:
        >>> format_currency(100.50, 'GBP')
        '£100.50'
        >>> format_currency(127.00, 'USD')
        '$127.00'
    """
    symbols = {"GBP": "£", "USD": "$", "EUR": "€"}
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:.2f}"


def format_temperature(temp: float, unit: TempUnitType) -> str:
    """
    Format temperature with unit symbol.

    Args:
        temp: Temperature value
        unit: Temperature unit

    Returns:
        Formatted temperature string

    Example:
        >>> format_temperature(20.5, 'C')
        '20.5°C'
        >>> format_temperature(68.9, 'F')
        '68.9°F'
    """
    return f"{temp:.1f}°{unit}"


def get_preferences_javascript() -> str:
    """
    Generate JavaScript code for localStorage preferences management.

    This function returns JavaScript code that can be embedded in HTML
    visualizations to provide client-side preference management.

    Returns:
        JavaScript code as a string
    """
    return """
// User Preferences Management for Places2Go
// Uses localStorage for persistent browser-based storage

const PreferencesManager = {
    STORAGE_KEY: 'places2go_preferences',
    
    // Default preferences
    defaults: {
        currency: 'GBP',
        temp_unit: 'C',
        theme: 'light',
        date_format: 'DD/MM/YYYY'
    },
    
    // Load preferences from localStorage
    load: function() {
        try {
            const stored = localStorage.getItem(this.STORAGE_KEY);
            if (stored) {
                return { ...this.defaults, ...JSON.parse(stored) };
            }
        } catch (e) {
            console.warn('Failed to load preferences:', e);
        }
        return { ...this.defaults };
    },
    
    // Save preferences to localStorage
    save: function(preferences) {
        try {
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(preferences));
            return true;
        } catch (e) {
            console.error('Failed to save preferences:', e);
            return false;
        }
    },
    
    // Update a single preference
    update: function(key, value) {
        const prefs = this.load();
        prefs[key] = value;
        return this.save(prefs);
    },
    
    // Reset to defaults
    reset: function() {
        return this.save(this.defaults);
    },
    
    // Currency conversion rates (base: GBP)
    currencyRates: {
        'GBP': 1.0,
        'USD': 1.27,
        'EUR': 1.17
    },
    
    // Convert currency amount
    convertCurrency: function(amount, fromCurrency, toCurrency) {
        if (fromCurrency === toCurrency) return amount;
        const amountInGBP = amount / this.currencyRates[fromCurrency];
        return amountInGBP * this.currencyRates[toCurrency];
    },
    
    // Convert temperature
    convertTemperature: function(tempC, toUnit) {
        if (toUnit === 'C') return tempC;
        return (tempC * 9 / 5) + 32;
    },
    
    // Format currency with symbol
    formatCurrency: function(amount, currency) {
        const symbols = { 'GBP': '£', 'USD': '$', 'EUR': '€' };
        const symbol = symbols[currency] || currency;
        return symbol + amount.toFixed(2);
    },
    
    // Format temperature with unit
    formatTemperature: function(temp, unit) {
        return temp.toFixed(1) + '°' + unit;
    }
};
"""


def get_favorites_javascript() -> str:
    """
    Generate JavaScript code for favorites management.

    Returns:
        JavaScript code as a string
    """
    return """
// Favorites Management for Places2Go

const FavoritesManager = {
    STORAGE_KEY: 'places2go_favorites',
    
    // Load favorites from localStorage
    load: function() {
        try {
            const stored = localStorage.getItem(this.STORAGE_KEY);
            return stored ? JSON.parse(stored) : [];
        } catch (e) {
            console.warn('Failed to load favorites:', e);
            return [];
        }
    },
    
    // Save favorites to localStorage
    save: function(favorites) {
        try {
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(favorites));
            return true;
        } catch (e) {
            console.error('Failed to save favorites:', e);
            return false;
        }
    },
    
    // Add a destination to favorites
    add: function(destinationId, destinationName) {
        const favorites = this.load();
        if (!favorites.find(f => f.id === destinationId)) {
            favorites.push({
                id: destinationId,
                name: destinationName,
                addedAt: new Date().toISOString()
            });
            return this.save(favorites);
        }
        return false; // Already in favorites
    },
    
    // Remove a destination from favorites
    remove: function(destinationId) {
        let favorites = this.load();
        const initialLength = favorites.length;
        favorites = favorites.filter(f => f.id !== destinationId);
        if (favorites.length < initialLength) {
            return this.save(favorites);
        }
        return false; // Not found
    },
    
    // Check if destination is favorited
    isFavorite: function(destinationId) {
        const favorites = this.load();
        return favorites.some(f => f.id === destinationId);
    },
    
    // Toggle favorite status
    toggle: function(destinationId, destinationName) {
        if (this.isFavorite(destinationId)) {
            return this.remove(destinationId);
        } else {
            return this.add(destinationId, destinationName);
        }
    },
    
    // Get all favorite destination IDs
    getIds: function() {
        return this.load().map(f => f.id);
    },
    
    // Clear all favorites
    clear: function() {
        return this.save([]);
    }
};
"""


def get_comparison_sets_javascript() -> str:
    """
    Generate JavaScript code for comparison sets (trip plans) management.

    Returns:
        JavaScript code as a string
    """
    return """
// Comparison Sets (Trip Plans) Management for Places2Go

const ComparisonSetsManager = {
    STORAGE_KEY: 'places2go_comparison_sets',
    
    // Load all comparison sets
    load: function() {
        try {
            const stored = localStorage.getItem(this.STORAGE_KEY);
            return stored ? JSON.parse(stored) : [];
        } catch (e) {
            console.warn('Failed to load comparison sets:', e);
            return [];
        }
    },
    
    // Save all comparison sets
    save: function(sets) {
        try {
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(sets));
            return true;
        } catch (e) {
            console.error('Failed to save comparison sets:', e);
            return false;
        }
    },
    
    // Create a new comparison set
    create: function(name, destinationIds, filters = {}) {
        const sets = this.load();
        const newSet = {
            id: Date.now().toString(),
            name: name,
            destinations: destinationIds,
            filters: filters,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString()
        };
        sets.push(newSet);
        return this.save(sets) ? newSet.id : null;
    },
    
    // Update an existing comparison set
    update: function(id, updates) {
        const sets = this.load();
        const index = sets.findIndex(s => s.id === id);
        if (index !== -1) {
            sets[index] = {
                ...sets[index],
                ...updates,
                updatedAt: new Date().toISOString()
            };
            return this.save(sets);
        }
        return false;
    },
    
    // Delete a comparison set
    delete: function(id) {
        let sets = this.load();
        const initialLength = sets.length;
        sets = sets.filter(s => s.id !== id);
        if (sets.length < initialLength) {
            return this.save(sets);
        }
        return false;
    },
    
    // Get a specific comparison set
    get: function(id) {
        const sets = this.load();
        return sets.find(s => s.id === id);
    },
    
    // Get all comparison set names and IDs
    list: function() {
        const sets = this.load();
        return sets.map(s => ({ id: s.id, name: s.name, createdAt: s.createdAt }));
    }
};
"""


def get_share_javascript() -> str:
    """
    Generate JavaScript code for URL sharing functionality.

    Returns:
        JavaScript code as a string
    """
    return """
// URL Sharing for Places2Go
// Encode/decode dashboard state in URL parameters

const ShareManager = {
    
    // Encode state to URL parameters
    encodeState: function(state) {
        const params = new URLSearchParams();
        
        // Add preferences
        if (state.preferences) {
            params.set('currency', state.preferences.currency);
            params.set('temp_unit', state.preferences.temp_unit);
            params.set('theme', state.preferences.theme);
        }
        
        // Add selected destinations
        if (state.destinations && state.destinations.length > 0) {
            params.set('destinations', state.destinations.join(','));
        }
        
        // Add filters
        if (state.filters) {
            Object.keys(state.filters).forEach(key => {
                params.set('filter_' + key, state.filters[key]);
            });
        }
        
        return params.toString();
    },
    
    // Decode URL parameters to state
    decodeState: function(urlParams) {
        const params = new URLSearchParams(urlParams || window.location.search);
        const state = {
            preferences: {},
            destinations: [],
            filters: {}
        };
        
        // Extract preferences
        if (params.has('currency')) {
            state.preferences.currency = params.get('currency');
        }
        if (params.has('temp_unit')) {
            state.preferences.temp_unit = params.get('temp_unit');
        }
        if (params.has('theme')) {
            state.preferences.theme = params.get('theme');
        }
        
        // Extract destinations
        if (params.has('destinations')) {
            state.destinations = params.get('destinations').split(',');
        }
        
        // Extract filters
        params.forEach((value, key) => {
            if (key.startsWith('filter_')) {
                state.filters[key.replace('filter_', '')] = value;
            }
        });
        
        return state;
    },
    
    // Generate shareable URL
    getShareableUrl: function(state) {
        const baseUrl = window.location.origin + window.location.pathname;
        const params = this.encodeState(state);
        return baseUrl + (params ? '?' + params : '');
    },
    
    // Copy shareable URL to clipboard
    copyShareableUrl: function(state) {
        const url = this.getShareableUrl(state);
        if (navigator.clipboard && navigator.clipboard.writeText) {
            return navigator.clipboard.writeText(url)
                .then(() => true)
                .catch(e => {
                    console.error('Failed to copy URL:', e);
                    return false;
                });
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = url;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            document.body.appendChild(textArea);
            textArea.select();
            try {
                document.execCommand('copy');
                document.body.removeChild(textArea);
                return Promise.resolve(true);
            } catch (e) {
                document.body.removeChild(textArea);
                console.error('Failed to copy URL:', e);
                return Promise.resolve(false);
            }
        }
    },
    
    // Apply state from URL on page load
    applyFromUrl: function() {
        return this.decodeState();
    }
};
"""


def get_recent_searches_javascript() -> str:
    """
    Generate JavaScript code for recent searches history.

    Returns:
        JavaScript code as a string
    """
    return """
// Recent Searches History for Places2Go

const RecentSearchesManager = {
    STORAGE_KEY: 'places2go_recent_searches',
    MAX_ITEMS: 10,
    
    // Load recent searches
    load: function() {
        try {
            const stored = localStorage.getItem(this.STORAGE_KEY);
            return stored ? JSON.parse(stored) : [];
        } catch (e) {
            console.warn('Failed to load recent searches:', e);
            return [];
        }
    },
    
    // Save recent searches
    save: function(searches) {
        try {
            // Keep only the most recent MAX_ITEMS
            const trimmed = searches.slice(0, this.MAX_ITEMS);
            localStorage.setItem(this.STORAGE_KEY, JSON.stringify(trimmed));
            return true;
        } catch (e) {
            console.error('Failed to save recent searches:', e);
            return false;
        }
    },
    
    // Add a new search to history
    add: function(searchParams) {
        const searches = this.load();
        
        // Create search entry
        const entry = {
            id: Date.now().toString(),
            params: searchParams,
            timestamp: new Date().toISOString()
        };
        
        // Remove duplicates (same parameters)
        const filtered = searches.filter(s => 
            JSON.stringify(s.params) !== JSON.stringify(searchParams)
        );
        
        // Add to front of list
        filtered.unshift(entry);
        
        return this.save(filtered);
    },
    
    // Remove a search from history
    remove: function(id) {
        let searches = this.load();
        searches = searches.filter(s => s.id !== id);
        return this.save(searches);
    },
    
    // Clear all history
    clear: function() {
        return this.save([]);
    },
    
    // Get formatted list of recent searches
    list: function() {
        return this.load();
    }
};
"""
