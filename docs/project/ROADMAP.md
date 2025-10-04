# Places2Go Development Roadmap

## Current Status: Phase 1 Complete ✅
**Version:** 0.1.0
**Date:** October 4, 2025
**Branch:** develop

### Phase 1 Achievements
- ✅ Project structure established
- ✅ Build tooling configured (pytest, black, flake8)
- ✅ CI/CD pipeline ready (GitHub Actions)
- ✅ Basic dashboard with dummy data working
- ✅ Test infrastructure in place
- ✅ Git repository initialized with GitFlow branching
- ✅ Documentation complete (README, branching strategy, task breakdown)

---

## Phase 2: Enhanced Testing & Code Quality
**Target:** Version 0.2.0
**Timeline:** 1-2 weeks
**Branch:** feature/enhanced-testing

### Objectives
Improve test coverage and code quality before building new features.

### Tasks

#### 2.1 Increase Test Coverage (Priority: High)
- [ ] Add tests for `create_flight_cost_chart()` function
  - Verify HTML file is created
  - Check chart structure and data
  - Test error handling for empty dataframes
- [ ] Add tests for `create_time_vs_cost_chart()` function
  - Similar to flight cost chart tests
  - Verify bubble size mapping
- [ ] Add integration test for full dashboard workflow
  - Load data → Generate both charts → Verify outputs exist
- [ ] Target: Achieve 80%+ code coverage

#### 2.2 Code Quality Improvements (Priority: Medium)
- [ ] Add type hints to all functions in `dashboard.py`
- [ ] Add docstring examples and update documentation
- [ ] Configure and run mypy for static type checking
- [ ] Add pre-commit hooks for black and flake8
- [ ] Create CONTRIBUTING.md with code standards

#### 2.3 Error Handling (Priority: High)
- [ ] Add proper error handling for missing CSV file
- [ ] Add validation for required columns in dataframe
- [ ] Add logging instead of print statements
- [ ] Create custom exceptions for domain-specific errors

### Success Criteria
- All tests passing with 80%+ coverage
- No flake8 warnings or errors
- All code formatted with black
- Type checking passes with mypy
- Error handling documented and tested

---

## Phase 3: Data Module Architecture
**Target:** Version 0.3.0
**Timeline:** 2-3 weeks
**Branch:** feature/data-modules

### Objectives
Create modular data retrieval system to replace dummy data.

### Tasks

#### 3.1 Base Data Module (Priority: High)
- [ ] Create `src/data/` directory structure
- [ ] Implement abstract base class `DataSource`
  - Define interface for all data sources
  - Methods: `fetch()`, `validate()`, `cache()`
- [ ] Create data models with Pydantic or dataclasses
  - `Destination`, `FlightInfo`, `WeatherInfo`, etc.

#### 3.2 CSV Data Source (Priority: High)
- [ ] Implement `CSVDataSource` class
- [ ] Migrate existing CSV loading logic
- [ ] Add data validation and cleaning
- [ ] Write comprehensive tests

#### 3.3 API Integration Framework (Priority: Medium)
- [ ] Set up API client base class
- [ ] Implement rate limiting and retry logic
- [ ] Add API response caching (local file or Redis)
- [ ] Create mock API responses for testing
- [ ] Add API key management using python-dotenv

#### 3.4 Weather Data Source (Priority: Medium)
- [ ] Research and select weather API (OpenWeatherMap recommended)
- [ ] Implement `WeatherAPIDataSource`
- [ ] Add UV index retrieval
- [ ] Write tests with mocked API responses
- [ ] Update `.env.example` with weather API keys

#### 3.5 Flight Data Source (Priority: Low)
- [ ] Research flight APIs (Skyscanner, Kiwi, Amadeus)
- [ ] Implement basic `FlightAPIDataSource` (stub for now)
- [ ] Document API selection rationale
- [ ] Plan for future implementation

### Success Criteria
- Modular, testable data architecture
- All data sources implement common interface
- CSV source working with existing data
- Weather API integrated (optional for phase completion)
- 100% test coverage for data modules

---

## Phase 4: Interactive Dashboard Framework
**Target:** Version 0.4.0
**Timeline:** 2-3 weeks
**Branch:** feature/dashboard-framework

### Objectives
Upgrade from static HTML to interactive web dashboard.

### Tasks

#### 4.1 Framework Selection & Setup (Priority: High)
- [ ] Evaluate frameworks: Streamlit vs Dash vs Flask+Plotly
  - **Recommendation:** Streamlit for rapid development
- [ ] Set up basic Streamlit app structure
- [ ] Migrate existing charts to Streamlit
- [ ] Add to requirements.txt and CI/CD pipeline

#### 4.2 Interactive Features (Priority: High)
- [ ] Add airport selector (Exeter/Bristol)
- [ ] Add destination multi-select
- [ ] Add date range picker (for future real data)
- [ ] Add metric filters (cost range, temperature, etc.)
- [ ] Implement real-time chart updates

#### 4.3 Enhanced Visualizations (Priority: Medium)
- [ ] Add map view showing destinations
- [ ] Create comparison table view
- [ ] Add export functionality (CSV, PDF)
- [ ] Implement dark mode toggle
- [ ] Add responsive design for mobile

#### 4.4 User Experience (Priority: Medium)
- [ ] Add loading states for data fetching
- [ ] Implement error messages for users
- [ ] Add helpful tooltips and explanations
- [ ] Create "About" page with methodology

### Success Criteria
- Functional interactive dashboard running locally
- All existing functionality preserved
- User can filter and explore data dynamically
- Mobile-responsive design
- No console errors in browser

---

## Phase 5: Cost of Living & Extended Metrics
**Target:** Version 0.5.0
**Timeline:** 3-4 weeks
**Branch:** feature/cost-of-living

### Objectives
Add comprehensive cost of living data and recreational metrics.

### Tasks

#### 5.1 Cost Data Collection (Priority: High)
- [ ] Research data sources:
  - Numbeo API
  - Expatistan
  - Government statistics
- [ ] Implement cost data retrieval
- [ ] Normalize all prices to GBP
- [ ] Add data quality indicators

#### 5.2 Recreational Cannabis Data (Priority: Low)
- [ ] Research legal/ethical data sources
- [ ] Implement data collection for legal jurisdictions only
- [ ] Add legal status indicator per destination
- [ ] Include disclaimers and warnings

#### 5.3 Extended Metrics (Priority: Medium)
- [ ] Public transport costs and quality
- [ ] Internet speeds and availability
- [ ] Healthcare quality indicators
- [ ] Safety and crime statistics
- [ ] Expat community size

#### 5.4 Dashboard Integration (Priority: High)
- [ ] Create dedicated "Cost of Living" page
- [ ] Add comparison calculator
- [ ] Implement "your budget" tool
- [ ] Create cost breakdown visualizations

### Success Criteria
- Comprehensive cost data for all destinations
- Data from reliable sources with citations
- User can estimate monthly living costs
- All data regularly updated (automation planned)

---

## Phase 6: Deployment & Scaling
**Target:** Version 1.0.0
**Timeline:** 2-3 weeks
**Branch:** release/1.0

### Objectives
Deploy application and prepare for public use.

### Tasks

#### 6.1 Production Deployment (Priority: High)
- [ ] Choose hosting platform (Streamlit Cloud, Heroku, Railway)
- [ ] Set up production environment variables
- [ ] Configure production database (if needed)
- [ ] Set up domain and SSL
- [ ] Configure CDN for assets

#### 6.2 Performance Optimization (Priority: High)
- [ ] Implement caching strategy
- [ ] Optimize data loading and queries
- [ ] Add background job scheduler for data updates
- [ ] Implement lazy loading for large datasets
- [ ] Profile and optimize slow functions

#### 6.3 Monitoring & Analytics (Priority: Medium)
- [ ] Add application monitoring (Sentry)
- [ ] Implement usage analytics (privacy-respecting)
- [ ] Set up uptime monitoring
- [ ] Create admin dashboard for maintenance

#### 6.4 Documentation & Community (Priority: High)
- [ ] Create user guide and FAQ
- [ ] Write API documentation
- [ ] Set up GitHub issues templates
- [ ] Create contributor guidelines
- [ ] Write deployment guide

### Success Criteria
- Application publicly accessible
- Sub-2 second page load times
- 99.9% uptime
- Comprehensive documentation
- Community engagement plan

---

## Future Enhancements (Post-1.0)

### User Accounts & Personalization
- User profiles and saved searches
- Customizable destination lists
- Email alerts for price changes
- Community ratings and reviews

### Advanced Features
- AI-powered destination recommendations
- "Find similar destinations" tool
- Historical data and trends
- Multi-destination trip planning
- Budget optimizer

### Data Expansion
- Visa requirements and processes
- Language difficulty ratings
- Timezone considerations
- Climate predictions
- Local events and festivals

### Mobile App
- Native iOS/Android apps
- Offline mode
- Push notifications
- Location-based suggestions

---

## Release Schedule

| Version | Phase | Target Date | Status |
|---------|-------|-------------|--------|
| 0.1.0 | Project Setup | Oct 4, 2025 | ✅ Complete |
| 0.2.0 | Enhanced Testing | Oct 18, 2025 | 📋 Planned |
| 0.3.0 | Data Modules | Nov 8, 2025 | 📋 Planned |
| 0.4.0 | Interactive Dashboard | Dec 1, 2025 | 📋 Planned |
| 0.5.0 | Cost of Living | Jan 5, 2026 | 📋 Planned |
| 1.0.0 | Production Release | Feb 1, 2026 | 📋 Planned |

---

## Contributing to the Roadmap

This roadmap is a living document. If you have suggestions or want to contribute:

1. Open an issue with the `roadmap` label
2. Discuss in our community channels
3. Submit a PR to update this document
4. Join the planning discussions

Last Updated: October 4, 2025
