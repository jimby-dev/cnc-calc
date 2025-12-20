# CNC Calculator Backend

FastAPI backend for the CNC Calculator application.

## Setup

### Prerequisites

- Python 3.11+
- Poetry (recommended) or pip

### Installation

#### Using Poetry (Recommended)

```bash
# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

#### Using pip (Alternative)

```bash
pip install -r requirements.txt
```

## Development

### Running the Server

```bash
# Using Poetry
poetry run uvicorn main:app --reload

# Or using pip
uvicorn main:app --reload
```

### Database Migrations

```bash
# Run migrations
poetry run alembic upgrade head

# Create a new migration
poetry run alembic revision --autogenerate -m "description"
```

### Testing

```bash
# Run tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app --cov=services --cov-report=html
```

### Code Quality

```bash
# Format code
poetry run black .

# Sort imports
poetry run isort .

# Lint
poetry run flake8 .

# Type checking
poetry run mypy .
```

## Project Structure

```
backend/
├── alembic/              # Database migrations
├── engine/               # Decision engine (NEW)
│   ├── schemas/          # Domain models (Material, Machine, Policy, etc.)
│   ├── policies/         # Policy implementations (Safety, Tool Life, Time, Balanced)
│   ├── arbitration/      # Conflict detection and resolution
│   ├── constraints/      # Feasible range calculations
│   ├── signals/          # Risk assessment
│   ├── math/             # Feeds & speeds calculations
│   ├── explainability/   # Decision trace generation
│   └── engine.py         # Main decision engine pipeline
├── app/
│   ├── api/routers/      # API routes
│   │   ├── recommend.py  # Recommendation endpoint (primary)
│   │   ├── materials.py  # Materials endpoints
│   │   ├── machines.py   # Machines endpoints
│   │   ├── policies.py # Policies endpoints
│   │   ├── tools.py      # Tool management (legacy)
│   │   └── health.py     # Health checks
│   └── core/             # Core configuration
│       ├── auth.py       # API key authentication
│       ├── config.py     # Settings
│       ├── database.py   # Database setup
│       ├── exceptions.py # Custom exceptions
│       ├── rate_limit.py # Rate limiting (Redis-based)
│       └── redis_client.py # Redis connection
├── models/               # SQLAlchemy models
│   ├── tool.py           # Tool model (legacy)
│   ├── material.py       # Material model (NEW)
│   ├── machine.py        # Machine model (NEW)
│   ├── policy.py         # Policy model (NEW)
│   └── recommendation.py # Recommendation model (NEW)
├── schemas/              # Pydantic schemas (legacy tool schemas)
├── services/             # Business logic
│   ├── tool_service.py   # Tool CRUD operations
│   ├── export_service.py # Export functionality
│   └── validation_service.py # Tool validation
├── scripts/              # Utility scripts
│   └── seed_data.py      # Seed materials, machines, policies
├── tests/                # Test suite
└── main.py               # Application entry point
```

## Environment Variables

Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/cnc_calc

# Redis (for rate limiting)
REDIS_URL=redis://localhost:6379

# Security (REQUIRED in production)
SECRET_KEY=your-secret-key-change-in-production
API_KEY=your-api-key-here

# Application
ENVIRONMENT=development

# CORS (comma-separated)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

**Important**: 
- `API_KEY` is required for all API endpoints (except health checks)
- `SECRET_KEY` must be changed from default in production
- See `SECURITY_SETUP.md` for security configuration

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs (disabled in production)
- ReDoc: http://localhost:8000/redoc (disabled in production)

### Key Endpoints

**Decision Engine:**
- `POST /api/recommend` - Generate feeds & speeds recommendation
- `GET /api/materials` - List materials
- `GET /api/machines` - List machines
- `GET /api/policies` - List policies

**Tool Management:**
- `GET /api/tools` - List tools
- `POST /api/tools` - Create tool
- `GET /api/tools/{id}` - Get tool

**Note**: All endpoints require `X-API-Key` header except health checks.

## Database Setup

After installing dependencies:

```bash
# Run migrations
poetry run alembic upgrade head

# Seed initial data (materials, machines, policies)
python scripts/seed_data.py
```

