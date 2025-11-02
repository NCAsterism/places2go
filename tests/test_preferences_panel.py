"""
Tests for preferences_panel module.
"""

from scripts.core.preferences_panel import (
    get_preferences_panel_html,
    get_preferences_panel_css,
    get_preferences_panel_js,
    inject_preferences_into_html,
)


class TestPreferencesPanelGeneration:
    """Tests for preferences panel generation."""

    def test_panel_html_contains_required_elements(self):
        """Test that HTML contains all required UI elements."""
        html = get_preferences_panel_html()

        # Check for main panels
        assert 'id="preferences-panel"' in html
        assert 'id="favorites-panel"' in html
        assert 'id="share-modal"' in html

        # Check for preference controls
        assert 'id="currency-select"' in html
        assert 'id="temp-unit-select"' in html
        assert 'id="theme-select"' in html
        assert 'id="date-format-select"' in html

        # Check for currency options
        assert "GBP" in html
        assert "USD" in html
        assert "EUR" in html

        # Check for temperature options
        assert "Celsius" in html
        assert "Fahrenheit" in html

        # Check for theme options
        assert "Light" in html
        assert "Dark" in html

    def test_panel_css_contains_styling(self):
        """Test that CSS contains styling rules."""
        css = get_preferences_panel_css()

        # Check for main classes
        assert ".preferences-panel" in css
        assert ".favorites-panel" in css or ".side-panel" in css
        assert ".floating-buttons" in css
        assert ".modal" in css

        # Check for theme support
        assert "dark-theme" in css

        # Check for responsive design
        assert "@media" in css

    def test_panel_js_contains_managers(self):
        """Test that JavaScript contains all manager objects."""
        js = get_preferences_panel_js()

        # Check for manager objects
        assert "PreferencesManager" in js
        assert "FavoritesManager" in js
        assert "ComparisonSetsManager" in js
        assert "ShareManager" in js
        assert "RecentSearchesManager" in js

        # Check for key functions
        assert "initializePreferences" in js
        assert "updatePreference" in js
        assert "toggleFavorite" in js
        assert "openShareModal" in js

        # Check for localStorage usage
        assert "localStorage" in js

    def test_inject_into_html_basic(self):
        """Test injecting preferences into basic HTML."""
        original_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <h1>Test Content</h1>
</body>
</html>
"""
        result = inject_preferences_into_html(original_html)

        # Check that original content is preserved
        assert "<h1>Test Content</h1>" in result

        # Check that new content is added
        assert "preferences-panel" in result
        assert "PreferencesManager" in result
        assert ".preferences-panel" in result

    def test_inject_preserves_existing_structure(self):
        """Test that injection preserves existing HTML structure."""
        original_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>My Dashboard</title>
    <style>
        body { margin: 0; }
    </style>
</head>
<body>
    <div id="content">
        <h1>Dashboard</h1>
        <div id="chart"></div>
    </div>
    <script>
        console.log('Original script');
    </script>
</body>
</html>
"""
        result = inject_preferences_into_html(original_html)

        # Check original content
        assert '<meta charset="utf-8">' in result
        assert "<h1>Dashboard</h1>" in result
        assert '<div id="chart"></div>' in result
        assert "console.log('Original script')" in result

        # Check new content
        assert "preferences-panel" in result
        assert "PreferencesManager" in result

    def test_inject_adds_to_head_and_body(self):
        """Test that injection adds CSS to head and HTML/JS to body."""
        original_html = """
<html>
<head></head>
<body></body>
</html>
"""
        result = inject_preferences_into_html(original_html)

        # CSS should be in head
        head_section = result.split("</head>")[0]
        assert "<style>" in head_section
        assert ".preferences-panel" in head_section

        # HTML and JS should be in body
        body_section = result.split("<body>")[1].split("</body>")[0]
        assert 'id="preferences-panel"' in body_section
        assert "<script>" in body_section
        assert "PreferencesManager" in body_section


class TestPreferencesPanelHTML:
    """Tests for specific HTML elements."""

    def test_currency_dropdown_has_all_options(self):
        """Test that currency dropdown has all required options."""
        html = get_preferences_panel_html()

        assert 'value="GBP"' in html
        assert 'value="USD"' in html
        assert 'value="EUR"' in html

    def test_temperature_dropdown_has_both_units(self):
        """Test that temperature dropdown has both units."""
        html = get_preferences_panel_html()

        assert 'value="C"' in html
        assert 'value="F"' in html

    def test_theme_dropdown_has_both_themes(self):
        """Test that theme dropdown has both themes."""
        html = get_preferences_panel_html()

        assert 'value="light"' in html
        assert 'value="dark"' in html

    def test_date_format_dropdown_has_all_formats(self):
        """Test that date format dropdown has all formats."""
        html = get_preferences_panel_html()

        assert 'value="DD/MM/YYYY"' in html
        assert 'value="MM/DD/YYYY"' in html
        assert 'value="YYYY-MM-DD"' in html

    def test_floating_action_buttons_present(self):
        """Test that floating action buttons are present."""
        html = get_preferences_panel_html()

        assert "floating-buttons" in html
        assert "togglePreferencesPanel" in html
        assert "toggleFavoritesPanel" in html
        assert "openShareModal" in html


class TestPreferencesPanelCSS:
    """Tests for CSS styling."""

    def test_responsive_design_rules(self):
        """Test that responsive design rules are included."""
        css = get_preferences_panel_css()

        assert "@media" in css
        assert "768px" in css or "max-width" in css

    def test_dark_theme_styles(self):
        """Test that dark theme styles are defined."""
        css = get_preferences_panel_css()

        assert "body.dark-theme" in css
        assert "dark-theme .preferences-panel" in css or "dark-theme" in css

    def test_panel_positioning(self):
        """Test that panels have positioning styles."""
        css = get_preferences_panel_css()

        assert "position: fixed" in css
        assert "z-index" in css


class TestPreferencesPanelJS:
    """Tests for JavaScript functionality."""

    def test_initialization_functions(self):
        """Test that initialization functions are present."""
        js = get_preferences_panel_js()

        assert "initializePreferences" in js
        assert "initializeFavorites" in js
        assert "DOMContentLoaded" in js

    def test_ui_interaction_functions(self):
        """Test that UI interaction functions are present."""
        js = get_preferences_panel_js()

        assert "togglePreferencesPanel" in js
        assert "toggleFavoritesPanel" in js
        assert "openShareModal" in js
        assert "closeShareModal" in js
        assert "copyShareUrl" in js

    def test_preference_update_function(self):
        """Test that preference update function is present."""
        js = get_preferences_panel_js()

        assert "updatePreference" in js
        assert "resetPreferences" in js

    def test_favorites_functions(self):
        """Test that favorites functions are present."""
        js = get_preferences_panel_js()

        assert "toggleFavorite" in js
        assert "removeFavorite" in js
        assert "renderFavoritesList" in js

    def test_state_management_functions(self):
        """Test that state management functions are present."""
        js = get_preferences_panel_js()

        assert "getCurrentState" in js
        assert "applyStateFromUrl" in js
