"""Tests for the cost comparison visualization."""

from pathlib import Path

import pandas as pd
import pytest

from scripts.visualizations.cost_comparison import (
    create_category_comparison_chart,
    create_cost_dashboard,
    create_cost_breakdown_chart,
    create_cost_distribution_chart,
    create_total_cost_chart,
)


@pytest.fixture
def sample_costs_df():
    """Create a sample cost of living DataFrame for testing."""
    return pd.DataFrame(
        {
            "destination_id": [1, 2, 3],
            "data_date": pd.to_datetime(["2025-10-01", "2025-10-01", "2025-10-01"]),
            "currency": ["GBP", "GBP", "GBP"],
            "monthly_living_cost": [800, 850, 900],
            "rent_1br_center": [440, 475, 495],
            "rent_1br_outside": [330, 355, 375],
            "monthly_food": [200, 210, 225],
            "monthly_transport": [40, 45, 50],
            "utilities": [90, 95, 100],
            "internet": [25, 28, 30],
            "meal_inexpensive": [10, 12, 11],
            "meal_mid_range": [28, 32, 30],
            "beer_domestic": [3.0, 3.5, 3.2],
            "weed_cost_per_gram": [10, 12, 11],
            "data_source": ["demo1", "demo1", "demo1"],
        }
    )


@pytest.fixture
def sample_destinations_df():
    """Create a sample destinations DataFrame for testing."""
    return pd.DataFrame(
        {
            "destination_id": [1, 2, 3],
            "name": ["Alicante", "Malaga", "Majorca"],
            "country": ["Spain", "Spain", "Spain"],
        }
    )


class TestTotalCostChart:
    """Tests for total cost comparison chart."""

    def test_creates_figure(self, sample_costs_df, sample_destinations_df):
        """Test that total cost chart creates a figure."""
        fig = create_total_cost_chart(sample_costs_df, sample_destinations_df)
        assert fig is not None
        assert fig.layout.title.text == "Total Monthly Living Cost by Destination"

    def test_horizontal_bar_orientation(self, sample_costs_df, sample_destinations_df):
        """Test that chart uses horizontal bars."""
        fig = create_total_cost_chart(sample_costs_df, sample_destinations_df)
        assert len(fig.data) == 1
        assert fig.data[0].orientation == "h"

    def test_has_correct_axis_labels(self, sample_costs_df, sample_destinations_df):
        """Test that chart has correct axis labels."""
        fig = create_total_cost_chart(sample_costs_df, sample_destinations_df)
        assert fig.layout.xaxis.title.text == "Monthly Cost (£ GBP)"
        assert fig.layout.yaxis.title.text == "Destination"

    def test_contains_destination_names(self, sample_costs_df, sample_destinations_df):
        """Test that chart contains destination names."""
        fig = create_total_cost_chart(sample_costs_df, sample_destinations_df)
        y_values = fig.data[0].y
        assert "Alicante" in y_values
        assert "Malaga" in y_values
        assert "Majorca" in y_values


class TestCostBreakdownChart:
    """Tests for cost breakdown stacked chart."""

    def test_creates_figure(self, sample_costs_df, sample_destinations_df):
        """Test that cost breakdown chart creates a figure."""
        fig = create_cost_breakdown_chart(sample_costs_df, sample_destinations_df)
        assert fig is not None
        assert fig.layout.title.text == "Cost Breakdown by Category"

    def test_stacked_bar_mode(self, sample_costs_df, sample_destinations_df):
        """Test that chart uses stacked bar mode."""
        fig = create_cost_breakdown_chart(sample_costs_df, sample_destinations_df)
        assert fig.layout.barmode == "stack"

    def test_contains_all_categories(self, sample_costs_df, sample_destinations_df):
        """Test that chart contains all cost categories."""
        fig = create_cost_breakdown_chart(sample_costs_df, sample_destinations_df)
        # Should have 5 traces for: Rent, Food, Transport, Utilities, Internet
        assert len(fig.data) == 5

        # Check trace names
        trace_names = [trace.name for trace in fig.data]
        assert "Rent (Center)" in trace_names
        assert "Food" in trace_names
        assert "Transport" in trace_names
        assert "Utilities" in trace_names
        assert "Internet" in trace_names

    def test_has_correct_axis_labels(self, sample_costs_df, sample_destinations_df):
        """Test that chart has correct axis labels."""
        fig = create_cost_breakdown_chart(sample_costs_df, sample_destinations_df)
        assert fig.layout.xaxis.title.text == "Destination"
        assert fig.layout.yaxis.title.text == "Monthly Cost (£ GBP)"


class TestCategoryComparisonChart:
    """Tests for category comparison grouped chart."""

    def test_creates_figure(self, sample_costs_df, sample_destinations_df):
        """Test that category comparison chart creates a figure."""
        fig = create_category_comparison_chart(sample_costs_df, sample_destinations_df)
        assert fig is not None
        assert fig.layout.title.text == "Dining & Leisure Cost Comparison"

    def test_grouped_bar_mode(self, sample_costs_df, sample_destinations_df):
        """Test that chart uses grouped bar mode."""
        fig = create_category_comparison_chart(sample_costs_df, sample_destinations_df)
        assert fig.layout.barmode == "group"

    def test_contains_dining_categories(self, sample_costs_df, sample_destinations_df):
        """Test that chart contains dining and leisure categories."""
        fig = create_category_comparison_chart(sample_costs_df, sample_destinations_df)
        # Should have 3 traces for: Meal (Inexpensive), Meal (Mid-range), Beer
        assert len(fig.data) == 3

        trace_names = [trace.name for trace in fig.data]
        assert "Meal (Inexpensive)" in trace_names
        assert "Meal (Mid-range)" in trace_names
        assert "Beer (Domestic)" in trace_names


class TestCostDistributionChart:
    """Tests for cost distribution box plot."""

    def test_creates_figure(self, sample_costs_df, sample_destinations_df):
        """Test that cost distribution chart creates a figure."""
        fig = create_cost_distribution_chart(sample_costs_df, sample_destinations_df)
        assert fig is not None
        assert fig.layout.title.text == "Cost Distribution by Category"

    def test_uses_box_traces(self, sample_costs_df, sample_destinations_df):
        """Test that chart uses box plot traces."""
        fig = create_cost_distribution_chart(sample_costs_df, sample_destinations_df)
        # Should have 6 box plots for different cost categories
        assert len(fig.data) == 6
        assert all(trace.type == "box" for trace in fig.data)

    def test_contains_all_categories(self, sample_costs_df, sample_destinations_df):
        """Test that chart contains all cost categories."""
        fig = create_cost_distribution_chart(sample_costs_df, sample_destinations_df)
        trace_names = [trace.name for trace in fig.data]
        assert "Rent (Center)" in trace_names
        assert "Rent (Outside)" in trace_names
        assert "Food" in trace_names
        assert "Transport" in trace_names
        assert "Utilities" in trace_names
        assert "Internet" in trace_names


class TestCostComparisonIntegration:
    """Integration tests for cost comparison visualization."""

    def test_generates_html_file(self):
        """Test that main script generates HTML file."""
        from scripts.visualizations.cost_comparison import main

        # Run main and check file creation
        main()

        # Check that file exists (using same path resolution as in main)
        import scripts.visualizations.cost_comparison as cc_module

        project_root = Path(cc_module.__file__).resolve().parents[2]
        output_file = (
            project_root / ".build" / "visualizations" / "cost_comparison.html"
        )
        assert output_file.exists()

    def test_html_contains_plotly(self):
        """Test that generated HTML contains Plotly."""
        from scripts.visualizations.cost_comparison import main

        main()

        import scripts.visualizations.cost_comparison as cc_module

        project_root = Path(cc_module.__file__).resolve().parents[2]
        output_file = (
            project_root / ".build" / "visualizations" / "cost_comparison.html"
        )
        content = output_file.read_text()

        # Check for Plotly markers
        assert "plotly" in content.lower()
        assert "Cost of Living Comparison" in content

    def test_html_contains_all_charts(self):
        """Test that HTML contains all expected charts."""
        from scripts.visualizations.cost_comparison import main

        main()

        import scripts.visualizations.cost_comparison as cc_module

        project_root = Path(cc_module.__file__).resolve().parents[2]
        output_file = (
            project_root / ".build" / "visualizations" / "cost_comparison.html"
        )
        content = output_file.read_text()

        # Check for chart titles
        assert "Total Monthly Living Cost by Destination" in content
        assert "Cost Breakdown by Category" in content
        assert "Dining & Leisure Cost Comparison" in content
        assert "Cost Distribution by Category" in content

    def test_html_contains_all_6_destinations(self):
        """Test that HTML displays all 6 destinations."""
        from scripts.visualizations.cost_comparison import main

        main()

        import scripts.visualizations.cost_comparison as cc_module

        project_root = Path(cc_module.__file__).resolve().parents[2]
        output_file = (
            project_root / ".build" / "visualizations" / "cost_comparison.html"
        )
        content = output_file.read_text()

        # Check for all 6 destination names
        destinations = ["Alicante", "Malaga", "Majorca", "Faro", "Corfu", "Rhodes"]
        for dest in destinations:
            assert dest in content

    def test_html_shows_currency_and_data_source(self):
        """Test that HTML shows currency and data source information."""
        from scripts.visualizations.cost_comparison import main

        main()

        import scripts.visualizations.cost_comparison as cc_module

        project_root = Path(cc_module.__file__).resolve().parents[2]
        output_file = (
            project_root / ".build" / "visualizations" / "cost_comparison.html"
        )
        content = output_file.read_text()

        # Check for currency and data source
        assert "GBP" in content
        assert "demo1" in content
        assert "2025-10-01" in content

    def test_html_contains_summary_statistics(self):
        """Test that HTML contains summary statistics."""
        from scripts.visualizations.cost_comparison import main

        main()

        import scripts.visualizations.cost_comparison as cc_module

        project_root = Path(cc_module.__file__).resolve().parents[2]
        output_file = (
            project_root / ".build" / "visualizations" / "cost_comparison.html"
        )
        content = output_file.read_text()

        # Check for stats cards
        assert "Average Cost" in content
        assert "Most Affordable" in content
        assert "Most Expensive" in content
        assert "Cost Range" in content

    def test_create_cost_dashboard_handles_empty_dataframe(
        self, tmp_path, sample_destinations_df
    ):
        """Test that dashboard generation handles empty cost data gracefully."""

        empty_df = pd.DataFrame(
            {
                "destination_id": pd.Series(dtype="int64"),
                "data_date": pd.Series(dtype="datetime64[ns]"),
                "data_source": pd.Series(dtype="object"),
                "currency": pd.Series(dtype="object"),
                "monthly_living_cost": pd.Series(dtype="float64"),
                "rent_1br_center": pd.Series(dtype="float64"),
                "rent_1br_outside": pd.Series(dtype="float64"),
                "monthly_food": pd.Series(dtype="float64"),
                "monthly_transport": pd.Series(dtype="float64"),
                "utilities": pd.Series(dtype="float64"),
                "internet": pd.Series(dtype="float64"),
                "meal_inexpensive": pd.Series(dtype="float64"),
                "meal_mid_range": pd.Series(dtype="float64"),
                "beer_domestic": pd.Series(dtype="float64"),
                "weed_cost_per_gram": pd.Series(dtype="float64"),
            }
        )

        output_path = tmp_path / "cost_comparison_empty.html"

        create_cost_dashboard(output_path, empty_df, sample_destinations_df)

        assert output_path.exists()
        content = output_path.read_text()
        assert "N/A" in content
