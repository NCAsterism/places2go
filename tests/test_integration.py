"""Integration tests for the full dashboard workflow.

This test validates the complete workflow from data loading through chart
generation, ensuring all components work together properly.
"""

from pathlib import Path

from scripts.dashboard import (
    load_data,
    create_flight_cost_chart,
    create_time_vs_cost_chart,
)


def test_full_dashboard_workflow(tmp_path):
    """Test complete workflow from data load to chart generation."""
    # Setup
    project_root = Path(__file__).resolve().parents[1]
    data_path = project_root / "data" / "dummy_data.csv"
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # Execute full workflow
    df = load_data(data_path)
    create_flight_cost_chart(df, output_dir)
    create_time_vs_cost_chart(df, output_dir)

    # Verify both HTML files exist
    flight_costs_path = output_dir / "flight_costs.html"
    time_vs_cost_path = output_dir / "flight_time_vs_cost.html"

    assert flight_costs_path.exists(), "flight_costs.html should exist"
    assert time_vs_cost_path.exists(), "flight_time_vs_cost.html should exist"

    # Verify files are non-empty (greater than 1000 bytes)
    assert (
        flight_costs_path.stat().st_size > 1000
    ), "flight_costs.html should be greater than 1000 bytes"
    assert (
        time_vs_cost_path.stat().st_size > 1000
    ), "flight_time_vs_cost.html should be greater than 1000 bytes"

    # Verify files contain Plotly chart markers
    flight_costs_content = flight_costs_path.read_text()
    time_vs_cost_content = time_vs_cost_path.read_text()

    # Check for Plotly markers (both files should contain these)
    assert (
        "plotly" in flight_costs_content.lower()
    ), "flight_costs.html should contain Plotly markers"
    assert (
        "plotly" in time_vs_cost_content.lower()
    ), "flight_time_vs_cost.html should contain Plotly markers"

    # Additional verification: check for expected chart titles
    assert (
        "Flight Cost by Destination and Airport" in flight_costs_content
    ), "flight_costs.html should contain the expected chart title"
    assert (
        "Flight Time vs Cost" in time_vs_cost_content
    ), "flight_time_vs_cost.html should contain the expected chart title"
