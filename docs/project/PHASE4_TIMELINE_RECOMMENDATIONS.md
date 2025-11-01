# Phase 4 Timeline Recommendations

**Created:** November 1, 2025
**Purpose:** Address external critique recommendation on persistence timeline risk
**Recommendation Source:** [docs/critique.md](../critique.md)

## Summary

**Current plan:** Phase 5 (APIs) before Phase 6 (persistence)
**Recommendation:** Move persistence work into Phase 3/4 to establish stable internal storage before external API integrations
**Rationale:** Separate risks, ensure stable foundation before Dec deadline

## Current Timeline Analysis

### Phase 4: Interactive Features & Real-Time Data (4-6 weeks)
- 4A: Interactive Dashboard Framework (Dash migration)
- 4B: Real-Time Data Integration (API connections)
- 4C: User Features & Personalization
- 4D: Deployment & DevOps
- 4E: Performance & Optimization
- 4F: Advanced Features (Future)

### Phase 5: [Not yet documented]
Assumed to cover API integrations based on Phase 4B content.

### Phase 6: [Not yet documented]
Assumed to cover persistence layer (database setup, user data storage).

## Risk Assessment

### Current Approach Risks

**1. Late Persistence Introduction**
- **Risk:** Database setup happens after API integrations are complete
- **Impact:** Difficult to refactor working APIs to use persistence
- **Likelihood:** High - persistence is fundamental architecture change
- **Severity:** High - could require rework of Phases 4-5

**2. December Deadline Pressure**
- **Risk:** Persistence work compressed at end due to timeline slippage
- **Impact:** Poor database design, technical debt, rushed implementation
- **Likelihood:** Medium - typical project schedule drift
- **Severity:** High - affects long-term maintainability

**3. API-First Approach Complexity**
- **Risk:** Building caching/storage on top of APIs instead of database-first
- **Impact:** Temporary solutions become permanent, harder to refactor later
- **Likelihood:** High - workarounds accumulate
- **Severity:** Medium-High - reduces scalability

**4. Testing Complexity**
- **Risk:** Testing API integrations without persistence layer requires mocks
- **Impact:** Tests don't reflect production architecture
- **Likelihood:** High - common testing pattern
- **Severity:** Medium - increases bug risk in production

## Recommended Timeline Changes

### Option 1: Integrate Persistence into Phase 4B (Recommended)

**Revised Phase 4B: Data Layer & API Integration (2-3 weeks)**

Week 1: Database Foundation
- Set up PostgreSQL/SQLite database
- Design schema for destinations, weather, flights, costs
- Implement SQLAlchemy models
- Create database migrations (Alembic)
- Add database connection pooling

Week 2: API Integration with Persistence
- Implement API clients (Skyscanner, OpenWeatherMap, Teleport)
- Build data pipeline: API → Database → Dashboard
- Implement caching in database (not just Redis)
- Add data freshness tracking
- Background jobs for data refresh

Week 3: Testing & Optimization
- Integration tests with real database
- Performance testing (database queries)
- API fallback strategies
- Data validation and error handling

**Benefits:**
- Persistence layer ready before deployment (Phase 4D)
- APIs write to database from day 1
- Testing reflects production architecture
- Caching built into database, not separate layer
- Foundation for user data (Phase 4C)

**Drawbacks:**
- Adds 1 week to Phase 4B (from 1-2 weeks to 2-3 weeks)
- More complexity upfront
- Database setup learning curve

### Option 2: New Phase 3D: Data Persistence (Conservative)

**New Phase 3D: Data Persistence Foundation (1-2 weeks)**

Insert between Phase 3C (Complete) and Phase 4A:

Week 1: Database Setup
- Choose database (PostgreSQL recommended)
- Design schema for core entities
- Set up local development database
- Create migration framework
- Document database architecture

Week 2: Data Migration (if needed)
- Migrate CSV data to database
- Update DataLoader to read from database
- Add database tests
- Update documentation

Then proceed with Phase 4A (Interactive Framework) which uses database.

**Benefits:**
- Clear separation of concerns
- No timeline pressure
- Database ready before any interactive features
- Can test database layer independently

**Drawbacks:**
- Delays Phase 4 start by 1-2 weeks
- December deadline impact
- Potential scope creep

### Option 3: Parallel Development (Risky)

Run persistence work in parallel with API integrations:
- Developer A: API clients (Phase 4B)
- Developer B: Database layer (Phase 3D/4B hybrid)
- Integrate in final week

**Benefits:**
- No timeline impact
- Both workstreams progress

**Drawbacks:**
- Requires 2+ developers
- High coordination overhead
- Integration complexity
- Potential conflicts/rework

## Recommendation: Option 1 (Persistence in Phase 4B)

### Why This Approach?

1. **Risk Separation:** Database and APIs developed together, not sequentially
2. **Timeline Impact:** Only +1 week to Phase 4, still before December
3. **Architecture First:** Persistence is fundamental, should drive API design
4. **Testing Quality:** Integration tests work with real production architecture
5. **Scalability:** Foundation ready for user data (Phase 4C) and future features

### Implementation Strategy

**Phase 4A: Interactive Framework (2 weeks) - No Changes**
- Dash migration
- Interactive filtering
- State management
- Still uses CSV data via DataLoader

**Phase 4B: Data Layer & API Integration (3 weeks) - REVISED**

Week 1: Database Foundation
```python
# New structure:
scripts/
  database/
    __init__.py
    models.py          # SQLAlchemy models
    connection.py      # Database connection
    migrations/        # Alembic migrations
      versions/
        001_initial_schema.py
        002_add_weather_cache.py
```

Week 2: API + Persistence
```python
scripts/
  data/
    api_clients/
      __init__.py
      flight_api.py    # Skyscanner client
      weather_api.py   # OpenWeatherMap client
      cost_api.py      # Teleport client
    pipeline.py        # API → DB → Dashboard
    cache_manager.py   # Database-backed caching
```

Week 3: Integration & Testing
- Update DataLoader to query database
- Implement background refresh jobs
- Add API fallback to CSV if database empty
- Integration tests with database
- Performance optimization

**Phase 4C: User Features (1 week) - EASIER NOW**
- User preferences stored in database (already set up)
- Favorites use database models (already designed)
- No additional database work needed

### Updated Phase 4 Timeline

**Month 1: Interactive Framework + Data Foundation**
- Week 1-2: Dash migration (Phase 4A)
- Week 3: Database setup (Phase 4B Week 1)
- Week 4: API integration (Phase 4B Week 2)

**Month 2: APIs, User Features, Deployment**
- Week 1: API testing & optimization (Phase 4B Week 3)
- Week 2: User preferences & favorites (Phase 4C)
- Week 3: Azure deployment (Phase 4D)
- Week 4: Performance optimization (Phase 4E)

**Total Duration:** 8 weeks (vs original 7 weeks)
**Completion Date:** Early January 2026 (vs late December 2025)
**December Deadline Impact:** Still achievable with MVP deployment end of Month 2

## Database Schema Recommendations

### Core Tables (Phase 4B Week 1)

```sql
-- destinations (migrate from CSV)
CREATE TABLE destinations (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country VARCHAR(100),
    region VARCHAR(100),
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    description TEXT,
    timezone VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- weather_cache (API responses)
CREATE TABLE weather_forecasts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    destination_id VARCHAR(50) REFERENCES destinations(id),
    forecast_date DATE NOT NULL,
    temp_high DECIMAL(5,2),
    temp_low DECIMAL(5,2),
    precipitation_mm DECIMAL(5,2),
    humidity INT,
    wind_speed DECIMAL(5,2),
    conditions VARCHAR(100),
    fetched_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,
    UNIQUE(destination_id, forecast_date)
);

-- flight_price_cache (API responses)
CREATE TABLE flight_prices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    origin VARCHAR(3) NOT NULL,  -- airport code
    destination_id VARCHAR(50) REFERENCES destinations(id),
    departure_date DATE NOT NULL,
    return_date DATE,
    price_gbp DECIMAL(10,2),
    currency VARCHAR(3),
    airline VARCHAR(100),
    duration_minutes INT,
    direct BOOLEAN,
    fetched_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,
    INDEX idx_route_date (origin, destination_id, departure_date)
);

-- cost_of_living_cache (API responses, changes slowly)
CREATE TABLE cost_of_living (
    destination_id VARCHAR(50) PRIMARY KEY REFERENCES destinations(id),
    meal_inexpensive DECIMAL(8,2),
    meal_midrange DECIMAL(8,2),
    beer_domestic DECIMAL(8,2),
    coffee DECIMAL(8,2),
    accommodation_budget DECIMAL(8,2),
    accommodation_midrange DECIMAL(8,2),
    transport_daily DECIMAL(8,2),
    currency VARCHAR(3),
    fetched_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP
);
```

### User Tables (Phase 4C)

```sql
-- users (simple anonymous users initially)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_active_at TIMESTAMP DEFAULT NOW()
);

-- user_preferences
CREATE TABLE user_preferences (
    user_id UUID PRIMARY KEY REFERENCES users(id),
    currency VARCHAR(3) DEFAULT 'GBP',
    temp_unit CHAR(1) DEFAULT 'C',
    date_format VARCHAR(20) DEFAULT 'DD/MM/YYYY',
    theme VARCHAR(10) DEFAULT 'light',
    default_origin VARCHAR(3) DEFAULT 'EXT',
    updated_at TIMESTAMP DEFAULT NOW()
);

-- favorites
CREATE TABLE user_favorites (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    destination_id VARCHAR(50) REFERENCES destinations(id),
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, destination_id)
);

-- saved_comparisons
CREATE TABLE saved_comparisons (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    name VARCHAR(255),
    destination_ids TEXT[],  -- Array of destination IDs
    filters JSONB,           -- Saved filter state
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## Migration Path from CSV

### Step 1: Dual-Read Pattern (Phase 4B Week 1)

```python
# scripts/core/data_loader.py
class DataLoader:
    def __init__(self, use_database: bool = False):
        self.use_database = use_database
        if use_database:
            from scripts.database.connection import get_session
            self.db_session = get_session()

    def load_destinations(self) -> pd.DataFrame:
        if self.use_database:
            return self._load_destinations_from_db()
        else:
            return self._load_destinations_from_csv()  # Existing method
```

### Step 2: CSV → Database Migration Script (Phase 4B Week 1)

```python
# scripts/maintenance/migrate_csv_to_db.py
def migrate_destinations():
    """One-time migration of CSV data to database."""
    loader = DataLoader(use_database=False)
    df = loader.load_destinations()

    from scripts.database.models import Destination
    from scripts.database.connection import get_session

    session = get_session()
    for _, row in df.iterrows():
        dest = Destination(
            id=row['id'],
            name=row['name'],
            # ... map other fields
        )
        session.add(dest)
    session.commit()
```

### Step 3: Switch to Database (Phase 4B Week 2)

After migration script runs successfully:
1. Update DataLoader default: `use_database=True`
2. Keep CSV as backup/fallback
3. Add environment variable to control source

### Step 4: Database-First Development (Phase 4B Week 2+)

All new features read from database:
- API clients write to database
- Dashboard queries database
- CSV only used for:
  - Local development without database
  - Fallback if database unavailable
  - Historical reference

## Testing Strategy with Persistence

### Unit Tests (Fast, No Database)
```python
# tests/test_models.py
def test_destination_model():
    """Test SQLAlchemy model definitions."""
    dest = Destination(id='test', name='Test City')
    assert dest.id == 'test'
```

### Integration Tests (With Test Database)
```python
# tests/test_database_integration.py
@pytest.fixture
def test_db():
    """Create temporary test database."""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()

def test_api_to_database_pipeline(test_db):
    """Test API client writes to database correctly."""
    client = WeatherAPIClient()
    client.fetch_and_store('Bangkok')

    session = Session(test_db)
    forecasts = session.query(WeatherForecast).all()
    assert len(forecasts) > 0
```

### End-to-End Tests (Full Stack)
```python
# tests/test_e2e.py
def test_dashboard_displays_api_data():
    """Test full pipeline: API → DB → Dashboard."""
    # Trigger API fetch
    # Verify database updated
    # Check dashboard renders data
```

## Rollback Plan

If database integration causes significant delays:

1. **Phase 4B Week 1 Milestone:** Database schema + models complete
   - If not done: Skip database, continue with Redis caching (original plan)
   - Impact: Return to Phase 6 for persistence (original timeline)

2. **Phase 4B Week 2 Milestone:** API clients writing to database
   - If blocked: Use file-based caching temporarily
   - Impact: Refactor needed in Phase 6

3. **Phase 4B Week 3 Milestone:** Dashboard reading from database
   - If issues: Keep CSV as primary source, database as cache
   - Impact: Reduced benefit but still functional

## Success Criteria for Revised Phase 4B

### Week 1: Database Foundation
- [x] PostgreSQL/SQLite installed and running locally
- [x] All core tables created (destinations, weather, flights, costs)
- [x] SQLAlchemy models defined and tested
- [x] Alembic migrations working
- [x] CSV data migrated to database
- [x] Database connection pooling configured

### Week 2: API + Persistence
- [x] Weather API client fetches and stores data
- [x] Flight API client fetches and stores data
- [x] Cost API client fetches and stores data
- [x] Cache expiry logic working (stale data refreshed)
- [x] Background refresh jobs configured
- [x] DataLoader reads from database

### Week 3: Testing & Optimization
- [x] Integration tests passing with database
- [x] Database queries optimized (< 100ms)
- [x] CSV fallback working if database unavailable
- [x] Error handling for API failures
- [x] Data validation preventing bad data in database

## Monitoring & Observability

Add database monitoring from day 1:

```python
# scripts/database/monitoring.py
def log_query_performance():
    """Track slow queries for optimization."""
    # Log queries > 500ms

def check_data_freshness():
    """Alert if cached data expired."""
    # Check expires_at timestamps

def monitor_api_usage():
    """Track API calls vs cache hits."""
    # Calculate cache hit ratio
```

## Documentation Updates Required

1. **Architecture Diagram:** Add database layer between APIs and Dashboard
2. **Setup Guide:** Include database installation steps
3. **Development Workflow:** Document database migrations
4. **Testing Guide:** Explain test database setup
5. **Deployment Guide:** Add database provisioning (Azure PostgreSQL)

## Cost Impact

**Development Environment:**
- PostgreSQL local: Free
- SQLite local: Free

**Production (Azure):**
- Azure Database for PostgreSQL: ~£15-30/month (Basic tier)
- Alternative: SQLite in Azure Files: ~£5/month (limited scalability)

**Recommendation:** Start with SQLite for MVP, migrate to PostgreSQL if scaling needed.

## Next Steps

1. **Review with Team:** Discuss timeline trade-offs (1 week delay vs risk mitigation)
2. **Update Phase 4 Roadmap:** Incorporate revised Phase 4B timeline
3. **Database Technology Decision:** PostgreSQL vs SQLite for development
4. **Create Task Breakdown:** Detail Phase 4B database tasks in issues.csv
5. **Prototype Schema:** Create initial SQLAlchemy models for validation

## References

- [PHASE4_ROADMAP.md](PHASE4_ROADMAP.md) - Original Phase 4 plan
- [docs/critique.md](../critique.md) - External AI recommendations
- [data/issues.csv](../../data/issues.csv) - Task 48: Implement critique recommendations

---

**Recommendation Status:** Proposed
**Decision Required By:** Before Phase 4A starts
**Impact Assessment:** +1 week to Phase 4, significantly reduced architectural risk
