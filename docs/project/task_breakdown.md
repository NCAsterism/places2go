# Task Breakdown

This document outlines the initial tasks required to evolve the Destination Dashboard from a proof‑of‑concept into a fully featured, production‑ready application.  Each task can be tracked as a GitHub issue and assigned to team members or GitHub agents.

## 1. Layout & UI (Dashboard)

* **Task:** Design and implement the user interface for the dashboard.
* **Feature Branch:** `feature/dashboard-ui`
* **Description:** Choose a web framework (e.g. Dash, Streamlit, or a React front‑end with a Python backend) and build the layout.  The UI should allow users to select an origin airport (Exeter or Bristol), choose destinations, and filter by metrics such as date or cost.  It should display charts and tables created by the data‑retrieval modules.  Aim for a responsive design that works on desktop and mobile devices.

## 2. Flight Data Retrieval

* **Task:** Implement modules to fetch flight prices and times from APIs.
* **Feature Branch:** `feature/flight-data`
* **Description:** Identify and integrate with a flight search API (e.g. Skyscanner, Kiwi or Amadeus).  The module should take origin and destination airports along with dates and return the lowest available price and typical flight duration.  Write tests that mock API responses to ensure the module handles success, empty results, and error scenarios gracefully.

## 3. Weather & UV Data Retrieval

* **Task:** Add weather and UV information for each destination.
* **Feature Branch:** `feature/weather-data`
* **Description:** Use a weather API (such as OpenWeatherMap or Weatherbit) to fetch current weather, average temperatures, and UV index.  Provide functions to retrieve data by city name or coordinates.  Include tests that simulate API responses.

## 4. Cost of Living & Local Expenses

* **Task:** Gather and present cost‑of‑living data.
* **Feature Branch:** `feature/cost-of-living`
* **Description:** Research reliable sources for monthly living costs, food prices, drink prices, and cannabis prices for each destination.  Where APIs are not available, identify publicly available datasets or scrape data (respecting terms of service).  Convert prices to GBP and normalise units.  Write tests to verify data cleaning routines and handle missing values.

## 5. Automated Updates & Refresh Mechanism

* **Task:** Implement a scheduler to refresh data periodically.
* **Feature Branch:** `feature/data-refresh`
* **Description:** Set up a task scheduler (e.g. `cron`, `APScheduler`, or background tasks in Dash) to automatically update data daily or weekly.  Ensure that the dashboard reflects new data without requiring manual intervention.  Write tests to confirm that the scheduler triggers and logs updates as expected.

## 6. Testing Infrastructure

* **Task:** Set up unit and integration tests across the project.
* **Feature Branch:** `feature/test-infra`
* **Description:** Install `pytest` and set up a `pytest.ini` configuration file.  Configure code coverage reporting.  Integrate with GitHub Actions to run tests and linting on every pull request.  Enforce a minimum coverage threshold for merging.

## 7. Documentation & Contribution Guidelines

* **Task:** Expand the documentation.
* **Feature Branch:** `feature/documentation`
* **Description:** Flesh out the `docs/` directory with setup instructions, API usage examples, architecture diagrams and a contributors’ guide.  Include instructions on how to set up API keys securely (e.g. using environment variables or `.env` files).

Each task is intended to be independent and can proceed in parallel once the PoC is in place.  As tasks are completed, additional issues can be opened to extend functionality (e.g. adding more airports, destinations, or metrics).
