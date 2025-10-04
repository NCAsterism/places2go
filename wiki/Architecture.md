# Architecture Overview

Technical architecture and design decisions for Places2Go.

---

## System Overview

Places2Go is a Python-based data visualization dashboard for comparing travel destinations. The system processes destination data and generates interactive charts for analysis.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                       │
│  ┌─────────────────┐         ┌──────────────────────┐       │
│  │  Plotly Charts  │         │  Streamlit UI        │       │
│  │  (Phase 1)      │         │  (Phase 4)           │       │
│  └─────────────────┘         └──────────────────────┘       │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────────────────────────────────────┐
│                  Application Logic Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │  Dashboard   │  │   Data       │  │   Validation    │   │
│  │  Generator   │  │   Processor  │  │   Layer         │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                               │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │  CSV Files   │  │  External    │  │   Database      │   │
│  │  (Phase 1)   │  │  APIs        │  │   (Phase 6)     │   │
│  │              │  │  (Phase 5)   │  │                 │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Design

### Current Architecture (Phase 1)

**Simplified single-script design:**

```python
# scripts/dashboard.py

┌─────────────────────────────────────────────────┐
│                  dashboard.py                    │
│                                                  │
│  1. load_data()                                 │
│     ├── Read CSV file                           │
│     ├── Parse DataFrame                         │
│     └── Return data                             │
│                                                  │
│  2. create_flight_cost_chart()                  │
│     ├── Process data                            │
│     ├── Generate Plotly chart                   │
│     └── Save HTML                               │
│                                                  │
│  3. create_time_vs_cost_chart()                 │
│     ├── Process data                            │
│     ├── Generate scatter plot                   │
│     └── Save HTML                               │
│                                                  │
│  4. main()                                      │
│     ├── Call load_data()                        │
│     ├── Call chart generators                   │
│     └── Save outputs                            │
└─────────────────────────────────────────────────┘
```

### Future Architecture (Phase 3+)

**Modular, scalable design:**

```
src/
├── data/
│   ├── loader.py           # Data loading
│   ├── models.py           # Pydantic models
│   ├── validator.py        # Data validation
│   └── repository.py       # Data access layer
│
├── dashboard/
│   ├── charts.py           # Chart generation
│   ├── streamlit_app.py    # Web interface
│   └── filters.py          # Filter logic
│
├── api/
│   ├── flights.py          # Flight data API
│   ├── weather.py          # Weather API
│   └── costs.py            # Cost of living API
│
├── services/
│   ├── data_service.py     # Business logic
│   ├── cache_service.py    # Caching layer
│   └── auth_service.py     # Authentication
│
└── utils/
    ├── logger.py           # Logging
    ├── exceptions.py       # Custom exceptions
    └── config.py           # Configuration
```

---

## Data Flow

### Phase 1: Static Data Flow

```
CSV File → Pandas DataFrame → Chart Generator → HTML Output
```

**Detailed Flow:**

```
1. User runs: python scripts/dashboard.py

2. load_data() reads data/dummy_data.csv
   ├── Path resolution: PROJECT_ROOT / "data" / "dummy_data.csv"
   ├── Pandas read_csv()
   └── Returns: DataFrame with 6 destinations

3. create_flight_cost_chart(df)
   ├── Sort by flight cost
   ├── Create Plotly bar chart
   │   ├── X-axis: Destination + Airport
   │   └── Y-axis: Flight Cost (GBP)
   ├── Update layout (title, labels, colors)
   └── Save: output/flight_costs.html

4. create_time_vs_cost_chart(df)
   ├── Create scatter plot
   │   ├── X-axis: Flight Time (hours)
   │   ├── Y-axis: Flight Cost (GBP)
   │   └── Marker size: Temperature
   ├── Update layout
   └── Save: output/flight_time_vs_cost.html

5. Output generated successfully
```

### Phase 5: Dynamic Data Flow

```
API Request → Cache Check → External API → Data Processing → 
Database Store → Validation → Chart Generation → Web UI
```

---

## Data Models

### Current Data Structure (Phase 1)

**CSV Format:**
```csv
Destination,Origin Airport,Flight Cost (GBP),Flight Time (hours),Temperature (C)
Alicante, Spain,Exeter,120,2.5,28
```

**DataFrame Schema:**
```python
{
    "Destination": str,       # "Alicante, Spain"
    "Origin Airport": str,    # "Exeter"
    "Flight Cost (GBP)": int, # 120
    "Flight Time (hours)": float,  # 2.5
    "Temperature (C)": int    # 28
}
```

### Future Data Models (Phase 3)

**Pydantic Models:**

```python
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class Airport(BaseModel):
    """Airport information."""
    code: str = Field(..., min_length=3, max_length=3)
    name: str
    city: str
    country: str
    
class Destination(BaseModel):
    """Travel destination with pricing and weather."""
    id: Optional[int] = None
    city: str
    country: str
    origin_airport: Airport
    flight_cost_gbp: float = Field(..., gt=0)
    flight_time_hours: float = Field(..., gt=0)
    temperature_c: float
    humidity_percent: Optional[float] = Field(None, ge=0, le=100)
    uv_index: Optional[int] = Field(None, ge=0, le=11)
    cost_of_living_monthly: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    @validator("flight_cost_gbp")
    def validate_cost(cls, v):
        if v > 10000:
            raise ValueError("Flight cost seems unrealistic")
        return v
    
    class Config:
        orm_mode = True

class FlightQuery(BaseModel):
    """Search criteria for flights."""
    origin_airports: List[str]
    max_cost: Optional[float] = None
    max_flight_time: Optional[float] = None
    min_temperature: Optional[float] = None
    max_temperature: Optional[float] = None
    date_range: Optional[tuple[datetime, datetime]] = None
```

---

## Technology Stack

### Core Technologies

| Layer | Technology | Purpose | Phase |
|-------|-----------|---------|-------|
| **Language** | Python 3.9-3.12 | Core language | 1 |
| **Data Processing** | Pandas | DataFrame manipulation | 1 |
| **Visualization** | Plotly | Interactive charts | 1 |
| **Testing** | pytest | Unit testing | 1 |
| **Formatting** | Black | Code formatting | 1 |
| **Linting** | Flake8 | Code quality | 1 |
| **Type Checking** | mypy | Static type analysis | 2 |
| **Validation** | Pydantic | Data models | 3 |
| **Web Framework** | Streamlit | Interactive UI | 4 |
| **APIs** | httpx/aiohttp | HTTP client | 5 |
| **Database** | PostgreSQL | Data storage | 6 |
| **ORM** | SQLAlchemy | Database ORM | 6 |
| **Caching** | Redis | Performance | 6 |

### Development Tools

| Tool | Purpose | Phase |
|------|---------|-------|
| **Git** | Version control | 1 |
| **GitHub Actions** | CI/CD | 1 |
| **pre-commit** | Git hooks | 2 |
| **pytest-cov** | Coverage reports | 2 |
| **python-dotenv** | Environment config | 1 |
| **Docker** | Containerization | 6 |

---

## Design Patterns

### Current Patterns (Phase 1)

**Functional Programming:**
- Pure functions for data processing
- Immutable DataFrames
- Function composition

```python
def load_data(file_path: Path) -> pd.DataFrame:
    """Pure function - no side effects."""
    return pd.read_csv(file_path)

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transformation without mutation."""
    return df.sort_values("Flight Cost (GBP)")
```

### Future Patterns (Phase 3+)

**Repository Pattern:**
```python
class DestinationRepository:
    """Data access abstraction."""
    
    def get_all(self) -> List[Destination]:
        pass
    
    def get_by_id(self, id: int) -> Optional[Destination]:
        pass
    
    def create(self, destination: Destination) -> Destination:
        pass
```

**Service Layer:**
```python
class DataService:
    """Business logic layer."""
    
    def __init__(self, repo: DestinationRepository):
        self.repo = repo
    
    def search_destinations(
        self, 
        criteria: FlightQuery
    ) -> List[Destination]:
        # Business logic here
        pass
```

**Factory Pattern:**
```python
class ChartFactory:
    """Create different chart types."""
    
    @staticmethod
    def create(chart_type: str, data: pd.DataFrame):
        if chart_type == "bar":
            return BarChart(data)
        elif chart_type == "scatter":
            return ScatterChart(data)
```

---

## Error Handling

### Current Approach (Phase 1)

Basic exception handling:

```python
try:
    df = pd.read_csv(data_path)
except FileNotFoundError:
    print(f"Error: Data file not found at {data_path}")
    sys.exit(1)
```

### Future Approach (Phase 2+)

**Custom Exceptions:**

```python
# src/utils/exceptions.py

class Places2GoException(Exception):
    """Base exception for Places2Go."""
    pass

class DataLoadError(Places2GoException):
    """Error loading data."""
    pass

class DataValidationError(Places2GoException):
    """Data validation failed."""
    pass

class APIError(Places2GoException):
    """External API error."""
    pass

class ConfigurationError(Places2GoException):
    """Configuration error."""
    pass
```

**Usage with Logging:**

```python
import logging
from src.utils.exceptions import DataLoadError

logger = logging.getLogger(__name__)

def load_data(file_path: Path) -> pd.DataFrame:
    try:
        logger.info(f"Loading data from {file_path}")
        df = pd.read_csv(file_path)
        logger.info(f"Loaded {len(df)} destinations")
        return df
    except FileNotFoundError as e:
        logger.error(f"File not found: {file_path}")
        raise DataLoadError(f"Could not load data file: {file_path}") from e
    except pd.errors.EmptyDataError as e:
        logger.error(f"Empty CSV file: {file_path}")
        raise DataLoadError("CSV file is empty") from e
```

---

## Performance Considerations

### Current Performance (Phase 1)

- **Data Size:** < 100 destinations (negligible)
- **Processing Time:** < 1 second
- **Memory Usage:** < 50MB
- **No caching needed**

### Future Optimizations (Phase 5-6)

**Caching Strategy:**
```python
# API response caching
@cache(ttl=3600)  # 1 hour
def fetch_flight_prices(origin: str, dest: str) -> FlightData:
    pass

# Database query caching
@cache(ttl=300)  # 5 minutes
def get_destinations_by_criteria(criteria: FlightQuery) -> List[Destination]:
    pass
```

**Database Indexing:**
```sql
-- Optimize common queries
CREATE INDEX idx_destinations_origin ON destinations(origin_airport);
CREATE INDEX idx_destinations_cost ON destinations(flight_cost_gbp);
CREATE INDEX idx_destinations_temp ON destinations(temperature_c);
```

**Async Operations:**
```python
import asyncio
import httpx

async def fetch_all_data(destinations: List[str]) -> List[DestinationData]:
    """Fetch data for multiple destinations concurrently."""
    async with httpx.AsyncClient() as client:
        tasks = [fetch_destination_data(client, dest) for dest in destinations]
        return await asyncio.gather(*tasks)
```

---

## Security Considerations

### Current Security (Phase 1)

- No authentication needed (local-only)
- No sensitive data
- No external connections

### Future Security (Phase 5-6)

**API Key Management:**
```python
# .env
FLIGHT_API_KEY=your_api_key_here
WEATHER_API_KEY=your_api_key_here

# config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    flight_api_key: str
    weather_api_key: str
    
    class Config:
        env_file = ".env"
```

**Input Validation:**
```python
from pydantic import validator

class FlightQuery(BaseModel):
    max_cost: float
    
    @validator("max_cost")
    def validate_cost(cls, v):
        if v < 0:
            raise ValueError("Cost must be positive")
        if v > 50000:
            raise ValueError("Cost exceeds reasonable limit")
        return v
```

---

## Deployment Architecture

### Local Development (Phase 1-4)

```
Developer Machine
├── Python venv
├── Local CSV files
└── HTML output files
```

### Production (Phase 6)

```
┌─────────────────────────────────────────────┐
│           Load Balancer (nginx)              │
└─────────────────────────────────────────────┘
                    ▼
┌─────────────────────────────────────────────┐
│       Streamlit App (Docker Container)       │
│              Python 3.11                     │
└─────────────────────────────────────────────┘
                    ▼
┌─────────────────────────────────────────────┐
│         PostgreSQL Database                  │
│         (Persistent Storage)                 │
└─────────────────────────────────────────────┘
                    ▼
┌─────────────────────────────────────────────┐
│              Redis Cache                     │
│           (Session & Query Cache)            │
└─────────────────────────────────────────────┘
```

---

## Testing Architecture

### Test Organization

```
tests/
├── unit/                 # Unit tests
│   ├── test_data.py
│   ├── test_charts.py
│   └── test_models.py
├── integration/          # Integration tests
│   ├── test_api.py
│   └── test_database.py
├── e2e/                  # End-to-end tests
│   └── test_dashboard.py
└── fixtures/             # Test data
    └── sample_data.csv
```

### Testing Strategy

| Level | Coverage | Tools | Phase |
|-------|----------|-------|-------|
| **Unit** | 90%+ | pytest | 2 |
| **Integration** | 80%+ | pytest | 3 |
| **E2E** | Key flows | Selenium | 4 |
| **Performance** | Load testing | Locust | 6 |

---

## Next Steps

- 📊 [Roadmap](Roadmap) - Development timeline
- 🛠️ [Development Guide](Development-Guide) - Start contributing
- 🧪 [Testing Guide](Testing) - Write tests
- 📖 [API Reference](API-Reference) - API documentation

---

**Questions?** See [FAQ](FAQ) or open a [discussion](https://github.com/NCAsterism/places2go/discussions).
