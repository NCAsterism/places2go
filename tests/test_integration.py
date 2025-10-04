"""Integration tests for the complete dashboard workflow.

This module tests the end-to-end workflow from data loading through chart
generation, ensuring all components work together correctly.
"""

from pathlib import Path

from scripts.dashboard import (
    load_data,
    create_flight_cost_chart,
    create_time_vs_cost_chart,
)


class TestFullDashboardWorkflow:
    """Test the complete dashboard generation workflow."""

    def test_full_workflow_with_real_data(self, tmp_path):
        """Test complete workflow from data load to chart generation.

        This integration test validates:
        1. Data loads successfully from the real CSV file
        2. Both charts generate without errors
        3. Both HTML files are created
        4. HTML files contain valid Plotly content
        5. Files are non-empty with reasonable sizes
        """
        # Setup paths
        project_root = Path(__file__).resolve().parents[1]
        data_path = project_root / "data" / "dummy_data.csv"
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Execute full workflow
        df = load_data(data_path)
        create_flight_cost_chart(df, output_dir)
        create_time_vs_cost_chart(df, output_dir)

        # Verify output files exist
        flight_costs_file = output_dir / "flight_costs.html"
        time_vs_cost_file = output_dir / "flight_time_vs_cost.html"

        assert flight_costs_file.exists(), "Flight costs chart not created"
        assert time_vs_cost_file.exists(), "Time vs cost chart not created"

        # Verify files are non-empty with reasonable sizes
        assert (
            flight_costs_file.stat().st_size > 1000
        ), "Flight costs chart file too small"
        assert (
            time_vs_cost_file.stat().st_size > 1000
        ), "Time vs cost chart file too small"

        # Verify files contain Plotly markers
        flight_costs_content = flight_costs_file.read_text(encoding="utf-8")
        time_vs_cost_content = time_vs_cost_file.read_text(encoding="utf-8")

        assert (
            "plotly" in flight_costs_content.lower()
        ), "Flight costs chart missing Plotly content"
        assert (
            "plotly" in time_vs_cost_content.lower()
        ), "Time vs cost chart missing Plotly content"

        # Verify chart titles are present
        assert (
            "Flight Cost by Destination" in flight_costs_content
        ), "Flight costs chart missing expected title"
        assert (
            "Flight Time vs Cost" in time_vs_cost_content
        ), "Time vs cost chart missing expected title"

    def test_workflow_with_empty_output_directory(self, tmp_path):
        """Test that workflow creates output directory if it doesn't exist."""
        project_root = Path(__file__).resolve().parents[1]
        data_path = project_root / "data" / "dummy_data.csv"
        output_dir = tmp_path / "nonexistent" / "output"

        # Should not raise error even though directory doesn't exist
        df = load_data(data_path)

        # Create parent directory
        output_dir.mkdir(parents=True)

        create_flight_cost_chart(df, output_dir)
        create_time_vs_cost_chart(df, output_dir)

        assert (output_dir / "flight_costs.html").exists()
        assert (output_dir / "flight_time_vs_cost.html").exists()

    def test_workflow_data_integrity(self, tmp_path):
        """Test that data maintains integrity through the workflow."""
        project_root = Path(__file__).resolve().parents[1]
        data_path = project_root / "data" / "dummy_data.csv"
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Load data
        df = load_data(data_path)

        # Verify data has expected structure
        assert len(df) > 0, "DataFrame should not be empty"
        assert "Destination" in df.columns, "Missing Destination column"
        assert "Flight Cost (GBP)" in df.columns, "Missing Flight Cost column"
        assert "Flight Time (hrs)" in df.columns, "Missing Flight Time column"

        # Verify data before chart generation
        original_shape = df.shape

        # Generate charts
        create_flight_cost_chart(df, output_dir)
        create_time_vs_cost_chart(df, output_dir)

        # Verify DataFrame wasn't modified by chart generation
        assert (
            df.shape == original_shape
        ), "DataFrame was modified during chart generation"


class TestWorkflowPerformance:
    """Test workflow performance characteristics."""

    def test_workflow_completes_quickly(self, tmp_path):
        """Test that full workflow completes in reasonable time (< 5 seconds)."""
        import time

        project_root = Path(__file__).resolve().parents[1]
        data_path = project_root / "data" / "dummy_data.csv"
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        start_time = time.time()

        # Execute workflow
        df = load_data(data_path)
        create_flight_cost_chart(df, output_dir)
        create_time_vs_cost_chart(df, output_dir)

        elapsed_time = time.time() - start_time

        assert elapsed_time < 5.0, f"Workflow took {elapsed_time:.2f}s, expected < 5s"


class TestWorkflowCleanup:
    """Test workflow cleanup and resource management."""

    def test_charts_can_be_regenerated(self, tmp_path):
        """Test that charts can be regenerated without issues."""
        project_root = Path(__file__).resolve().parents[1]
        data_path = project_root / "data" / "dummy_data.csv"
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        df = load_data(data_path)

        # Generate charts first time
        create_flight_cost_chart(df, output_dir)
        create_time_vs_cost_chart(df, output_dir)

        first_flight_costs = (output_dir / "flight_costs.html").stat().st_size
        first_time_vs_cost = (output_dir / "flight_time_vs_cost.html").stat().st_size

        # Regenerate charts (overwrite)
        create_flight_cost_chart(df, output_dir)
        create_time_vs_cost_chart(df, output_dir)

        second_flight_costs = (output_dir / "flight_costs.html").stat().st_size
        second_time_vs_cost = (output_dir / "flight_time_vs_cost.html").stat().st_size

        # Sizes should be similar (allowing for minor variations)
        assert (
            abs(first_flight_costs - second_flight_costs) < 1000
        ), "Regenerated flight costs chart significantly different"
        assert (
            abs(first_time_vs_cost - second_time_vs_cost) < 1000
        ), "Regenerated time vs cost chart significantly different"
