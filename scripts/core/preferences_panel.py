"""
Preferences panel generator for HTML visualizations.

This module provides utilities to inject a preferences panel into HTML
visualizations, allowing users to customize display settings.
"""

from typing import Optional
from scripts.core.user_preferences import (
    get_preferences_javascript,
    get_favorites_javascript,
    get_comparison_sets_javascript,
    get_share_javascript,
    get_recent_searches_javascript,
)


def get_preferences_panel_html() -> str:
    """
    Generate HTML for preferences panel.

    Returns:
        HTML string for preferences panel
    """
    return """
<div id="preferences-panel" class="preferences-panel">
    <div class="preferences-header">
        <h3>⚙️ Preferences</h3>
        <button class="close-btn" onclick="togglePreferencesPanel()">×</button>
    </div>
    <div class="preferences-content">
        <div class="preference-group">
            <label for="currency-select">Currency:</label>
            <select id="currency-select" onchange="updatePreference('currency', this.value)">
                <option value="GBP">£ GBP (British Pound)</option>
                <option value="USD">$ USD (US Dollar)</option>
                <option value="EUR">€ EUR (Euro)</option>
            </select>
        </div>
        
        <div class="preference-group">
            <label for="temp-unit-select">Temperature:</label>
            <select id="temp-unit-select" onchange="updatePreference('temp_unit', this.value)">
                <option value="C">°C (Celsius)</option>
                <option value="F">°F (Fahrenheit)</option>
            </select>
        </div>
        
        <div class="preference-group">
            <label for="theme-select">Theme:</label>
            <select id="theme-select" onchange="updatePreference('theme', this.value)">
                <option value="light">☀️ Light</option>
                <option value="dark">🌙 Dark</option>
            </select>
        </div>
        
        <div class="preference-group">
            <label for="date-format-select">Date Format:</label>
            <select id="date-format-select" onchange="updatePreference('date_format', this.value)">
                <option value="DD/MM/YYYY">DD/MM/YYYY</option>
                <option value="MM/DD/YYYY">MM/DD/YYYY</option>
                <option value="YYYY-MM-DD">YYYY-MM-DD</option>
            </select>
        </div>
        
        <div class="preference-actions">
            <button class="btn-reset" onclick="resetPreferences()">Reset to Defaults</button>
        </div>
    </div>
</div>

<div id="favorites-panel" class="side-panel">
    <div class="panel-header">
        <h3>⭐ Favorites</h3>
        <button class="close-btn" onclick="toggleFavoritesPanel()">×</button>
    </div>
    <div class="panel-content">
        <div id="favorites-list"></div>
        <div class="panel-empty" id="favorites-empty">
            <p>No favorites yet. Click ⭐ on destinations to add them.</p>
        </div>
    </div>
</div>

<div id="share-modal" class="modal">
    <div class="modal-content">
        <span class="close" onclick="closeShareModal()">&times;</span>
        <h2>📤 Share Dashboard</h2>
        <p>Copy this URL to share your current view:</p>
        <div class="share-url-container">
            <input type="text" id="share-url-input" readonly>
            <button onclick="copyShareUrl()">📋 Copy</button>
        </div>
        <div id="share-success" class="success-message" style="display: none;">
            ✅ URL copied to clipboard!
        </div>
    </div>
</div>

<div class="floating-buttons">
    <button class="fab" onclick="togglePreferencesPanel()" title="Preferences">
        ⚙️
    </button>
    <button class="fab" onclick="toggleFavoritesPanel()" title="Favorites">
        ⭐
    </button>
    <button class="fab" onclick="openShareModal()" title="Share">
        📤
    </button>
</div>
"""


def get_preferences_panel_css() -> str:
    """
    Generate CSS for preferences panel.

    Returns:
        CSS string for preferences panel styling
    """
    return """
/* Preferences Panel Styles */
.preferences-panel {
    position: fixed;
    top: 80px;
    right: -350px;
    width: 320px;
    background: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: -2px 2px 10px rgba(0,0,0,0.1);
    z-index: 1000;
    transition: right 0.3s ease;
}

.preferences-panel.open {
    right: 20px;
}

.preferences-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
    border-bottom: 1px solid #eee;
    background: #f8f9fa;
    border-radius: 8px 8px 0 0;
}

.preferences-header h3 {
    margin: 0;
    font-size: 18px;
    color: #333;
}

.close-btn {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #666;
    padding: 0;
    width: 30px;
    height: 30px;
    line-height: 1;
}

.close-btn:hover {
    color: #333;
}

.preferences-content {
    padding: 20px;
}

.preference-group {
    margin-bottom: 15px;
}

.preference-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
    color: #555;
}

.preference-group select {
    width: 100%;
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
    background: white;
}

.preference-actions {
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #eee;
}

.btn-reset {
    width: 100%;
    padding: 10px;
    background: #6c757d;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
}

.btn-reset:hover {
    background: #5a6268;
}

/* Side Panel (Favorites) */
.side-panel {
    position: fixed;
    top: 80px;
    right: -350px;
    width: 320px;
    height: calc(100vh - 100px);
    background: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: -2px 2px 10px rgba(0,0,0,0.1);
    z-index: 999;
    transition: right 0.3s ease;
    overflow-y: auto;
}

.side-panel.open {
    right: 20px;
}

.panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
    border-bottom: 1px solid #eee;
    background: #f8f9fa;
    position: sticky;
    top: 0;
    border-radius: 8px 8px 0 0;
}

.panel-header h3 {
    margin: 0;
    font-size: 18px;
    color: #333;
}

.panel-content {
    padding: 20px;
}

.panel-empty {
    text-align: center;
    color: #999;
    padding: 40px 20px;
}

.favorite-item {
    padding: 12px;
    margin-bottom: 10px;
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 6px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.favorite-item:hover {
    background: #e9ecef;
}

.favorite-name {
    font-weight: 500;
    color: #333;
}

.btn-remove-favorite {
    background: #dc3545;
    color: white;
    border: none;
    padding: 4px 12px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
}

.btn-remove-favorite:hover {
    background: #c82333;
}

/* Floating Action Buttons */
.floating-buttons {
    position: fixed;
    bottom: 30px;
    right: 30px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    z-index: 998;
}

.fab {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: #007bff;
    color: white;
    border: none;
    font-size: 24px;
    cursor: pointer;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
}

.fab:hover {
    background: #0056b3;
    transform: scale(1.1);
}

/* Share Modal */
.modal {
    display: none;
    position: fixed;
    z-index: 1001;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.4);
}

.modal.open {
    display: block;
}

.modal-content {
    background-color: #fefefe;
    margin: 15% auto;
    padding: 30px;
    border: 1px solid #888;
    border-radius: 8px;
    width: 80%;
    max-width: 500px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}

.modal-content h2 {
    margin-top: 0;
    color: #333;
}

.close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
}

.close:hover {
    color: #000;
}

.share-url-container {
    display: flex;
    gap: 10px;
    margin: 20px 0;
}

#share-url-input {
    flex: 1;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
}

.share-url-container button {
    padding: 10px 20px;
    background: #28a745;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
}

.share-url-container button:hover {
    background: #218838;
}

.success-message {
    color: #28a745;
    padding: 10px;
    text-align: center;
    font-weight: 500;
}

/* Dark Theme */
body.dark-theme {
    background: #1a1a1a;
    color: #e0e0e0;
}

body.dark-theme .preferences-panel,
body.dark-theme .side-panel,
body.dark-theme .modal-content {
    background: #2d2d2d;
    border-color: #404040;
    color: #e0e0e0;
}

body.dark-theme .preferences-header,
body.dark-theme .panel-header {
    background: #1f1f1f;
    border-color: #404040;
}

body.dark-theme .preferences-header h3,
body.dark-theme .panel-header h3 {
    color: #e0e0e0;
}

body.dark-theme select,
body.dark-theme input {
    background: #1a1a1a;
    border-color: #404040;
    color: #e0e0e0;
}

body.dark-theme .favorite-item {
    background: #1f1f1f;
    border-color: #404040;
}

body.dark-theme .favorite-item:hover {
    background: #262626;
}

/* Favorite Star Button */
.favorite-star {
    cursor: pointer;
    font-size: 20px;
    color: #ddd;
    transition: color 0.2s;
}

.favorite-star:hover {
    color: #ffc107;
}

.favorite-star.favorited {
    color: #ffc107;
}

/* Responsive */
@media (max-width: 768px) {
    .preferences-panel,
    .side-panel {
        width: calc(100% - 40px);
        right: -100%;
    }
    
    .preferences-panel.open,
    .side-panel.open {
        right: 20px;
    }
    
    .floating-buttons {
        bottom: 20px;
        right: 20px;
    }
    
    .fab {
        width: 48px;
        height: 48px;
        font-size: 20px;
    }
}
"""


def get_preferences_panel_js() -> str:
    """
    Generate JavaScript for preferences panel functionality.

    Returns:
        JavaScript string for preferences panel
    """
    # Combine all JavaScript modules
    all_js = "\n\n".join(
        [
            get_preferences_javascript(),
            get_favorites_javascript(),
            get_comparison_sets_javascript(),
            get_share_javascript(),
            get_recent_searches_javascript(),
        ]
    )

    # Add UI interaction functions
    ui_js = """

// UI Interaction Functions

// Initialize preferences on page load
document.addEventListener('DOMContentLoaded', function() {
    initializePreferences();
    initializeFavorites();
    applyStateFromUrl();
});

function initializePreferences() {
    const prefs = PreferencesManager.load();
    
    // Set select values
    document.getElementById('currency-select').value = prefs.currency;
    document.getElementById('temp-unit-select').value = prefs.temp_unit;
    document.getElementById('theme-select').value = prefs.theme;
    document.getElementById('date-format-select').value = prefs.date_format;
    
    // Apply theme
    applyTheme(prefs.theme);
    
    // Apply preferences to data (if applicable)
    if (typeof applyPreferencesToData === 'function') {
        applyPreferencesToData(prefs);
    }
}

function updatePreference(key, value) {
    if (PreferencesManager.update(key, value)) {
        if (key === 'theme') {
            applyTheme(value);
        }
        
        // Reload data with new preferences
        if (typeof applyPreferencesToData === 'function') {
            const prefs = PreferencesManager.load();
            applyPreferencesToData(prefs);
        }
    }
}

function resetPreferences() {
    if (confirm('Reset all preferences to defaults?')) {
        PreferencesManager.reset();
        initializePreferences();
    }
}

function applyTheme(theme) {
    if (theme === 'dark') {
        document.body.classList.add('dark-theme');
    } else {
        document.body.classList.remove('dark-theme');
    }
}

function togglePreferencesPanel() {
    const panel = document.getElementById('preferences-panel');
    const favPanel = document.getElementById('favorites-panel');
    
    // Close favorites if open
    if (favPanel.classList.contains('open')) {
        favPanel.classList.remove('open');
    }
    
    panel.classList.toggle('open');
}

function initializeFavorites() {
    renderFavoritesList();
}

function renderFavoritesList() {
    const favorites = FavoritesManager.load();
    const container = document.getElementById('favorites-list');
    const emptyMsg = document.getElementById('favorites-empty');
    
    if (favorites.length === 0) {
        container.innerHTML = '';
        emptyMsg.style.display = 'block';
    } else {
        emptyMsg.style.display = 'none';
        container.innerHTML = favorites.map(fav => `
            <div class="favorite-item">
                <span class="favorite-name">${fav.name}</span>
                <button class="btn-remove-favorite" onclick="removeFavorite('${fav.id}')">
                    Remove
                </button>
            </div>
        `).join('');
    }
}

function toggleFavorite(destinationId, destinationName) {
    FavoritesManager.toggle(destinationId, destinationName);
    renderFavoritesList();
    
    // Update star icon if it exists
    const star = document.querySelector(`[data-destination-id="${destinationId}"] .favorite-star`);
    if (star) {
        if (FavoritesManager.isFavorite(destinationId)) {
            star.classList.add('favorited');
        } else {
            star.classList.remove('favorited');
        }
    }
}

function removeFavorite(destinationId) {
    FavoritesManager.remove(destinationId);
    renderFavoritesList();
    
    // Update star icon if it exists
    const star = document.querySelector(`[data-destination-id="${destinationId}"] .favorite-star`);
    if (star) {
        star.classList.remove('favorited');
    }
}

function toggleFavoritesPanel() {
    const panel = document.getElementById('favorites-panel');
    const prefPanel = document.getElementById('preferences-panel');
    
    // Close preferences if open
    if (prefPanel.classList.contains('open')) {
        prefPanel.classList.remove('open');
    }
    
    panel.classList.toggle('open');
}

function openShareModal() {
    const modal = document.getElementById('share-modal');
    const urlInput = document.getElementById('share-url-input');
    
    // Get current state
    const state = getCurrentState();
    const shareUrl = ShareManager.getShareableUrl(state);
    
    urlInput.value = shareUrl;
    modal.classList.add('open');
}

function closeShareModal() {
    const modal = document.getElementById('share-modal');
    modal.classList.remove('open');
    document.getElementById('share-success').style.display = 'none';
}

function copyShareUrl() {
    const urlInput = document.getElementById('share-url-input');
    const successMsg = document.getElementById('share-success');
    
    const state = getCurrentState();
    ShareManager.copyShareableUrl(state).then(success => {
        if (success) {
            successMsg.style.display = 'block';
            setTimeout(() => {
                successMsg.style.display = 'none';
            }, 3000);
        } else {
            alert('Failed to copy URL to clipboard');
        }
    });
}

function getCurrentState() {
    // This should be customized per visualization
    // Override this function in individual visualizations
    return {
        preferences: PreferencesManager.load(),
        destinations: [],
        filters: {}
    };
}

function applyStateFromUrl() {
    const state = ShareManager.applyFromUrl();
    
    // Apply preferences if present
    if (Object.keys(state.preferences).length > 0) {
        const currentPrefs = PreferencesManager.load();
        const mergedPrefs = { ...currentPrefs, ...state.preferences };
        PreferencesManager.save(mergedPrefs);
        initializePreferences();
    }
    
    // Apply other state (destinations, filters)
    // This should be customized per visualization
    if (typeof applyStateToVisualization === 'function') {
        applyStateToVisualization(state);
    }
}

// Close modals when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('share-modal');
    if (event.target === modal) {
        closeShareModal();
    }
}
"""

    return all_js + ui_js


def inject_preferences_into_html(
    html_content: str, title: Optional[str] = None
) -> str:
    """
    Inject preferences panel into existing HTML content.

    Args:
        html_content: Original HTML content
        title: Optional title for the visualization

    Returns:
        Modified HTML with preferences panel
    """
    # Generate all components
    panel_html = get_preferences_panel_html()
    panel_css = get_preferences_panel_css()
    panel_js = get_preferences_panel_js()

    # Find the closing </head> tag and inject CSS
    css_injection = f"<style>\n{panel_css}\n</style>\n</head>"
    html_content = html_content.replace("</head>", css_injection)

    # Find the closing </body> tag and inject HTML and JS
    body_injection = f"""
{panel_html}
<script>
{panel_js}
</script>
</body>"""
    html_content = html_content.replace("</body>", body_injection)

    return html_content
