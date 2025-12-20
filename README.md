# Machining Decision Engine

A policy-driven machining decision engine that generates explainable feeds & speeds recommendations for CNC machining. Built to be portfolio-grade for DevOps/platform engineering.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm 9+
- Python 3.11+
- Docker (optional, for containerized development)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cnccalc
   ```

2. **Complete setup**
   ```bash
   make setup
   ```

3. **Start development environment**
   ```bash
   make dev
   ```

4. **Open your browser**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📋 Features

### Decision Engine
- **Policy-Driven Recommendations**: Generate feeds & speeds based on optimization goals (tool life, time, safety)
- **Explainable Results**: Complete decision trace showing why each parameter was chosen
- **Multiple Policies**: Apply and arbitrate between multiple policies simultaneously
- **Risk Assessment**: Automatic risk scoring for tool wear, chatter, surface finish, and more

### Scenario Builder
- **5-Step Workflow**: Tool → Material → Machine → Operation → Policies
- **Fusion 360 Import**: Import tool profiles from Fusion 360 JSON
- **Policy Weighting**: Adjust optimization priorities with interactive sliders
- **Real-time Validation**: Instant feedback on parameter feasibility

### Export & Integration
- **Fusion 360 Presets**: Export recommendations as Fusion-compatible presets
- **Tool Library**: Manage tool profiles for reuse across scenarios
- **Unit Conversion**: All calculations in metric (mm), UI supports inch/mm toggle

## 🏗️ Architecture

### Frontend (Next.js)
- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS with custom components
- **State Management**: React hooks with SWR for data fetching
- **Validation**: Zod schemas with real-time validation
- **3D Visualization**: Three.js for optional 3D tool preview

### Backend (FastAPI)
- **Framework**: FastAPI with async/await support
- **Decision Engine**: Policy-driven recommendation system with explainability
- **Database**: PostgreSQL with SQLAlchemy ORM (JSONB for flexible schemas)
- **Caching**: Redis for rate limiting and session management
- **Validation**: Pydantic v2 models with comprehensive validation
- **Security**: API key authentication, rate limiting, IP whitelisting

### Infrastructure
- **Development**: Docker Compose for local services
- **Production**: AWS ECS with RDS PostgreSQL
- **CI/CD**: GitHub Actions with automated testing
- **Monitoring**: Grafana dashboards with Prometheus metrics

## 🛠️ Development

### Available Commands

```bash
# Setup & Development
make setup          # Complete project setup
make dev            # Start development environment
make build          # Build both frontend and backend
make test           # Run all tests
make clean          # Clean build artifacts

# Database & Services
make db-up          # Start local database
make db-seed        # Seed database with sample data
make docker-up      # Start all services
make docker-down    # Stop all services

# Code Quality
make lint           # Lint all code
make format         # Format all code
make type-check     # Type checking
make security-scan  # Security vulnerability scan

# Deployment
make deploy-dev     # Deploy to development
make infra-up       # Deploy infrastructure
```

### Project Structure

```
cnc-calc/
├── frontend/           # Next.js application
│   ├── src/
│   │   ├── app/       # App Router pages
│   │   ├── components/ # React components (ScenarioBuilder, RecommendationDisplay)
│   │   ├── types/     # TypeScript definitions (engine.ts, tool.ts)
│   │   └── lib/       # API client with authentication
├── backend/           # FastAPI application
│   ├── engine/        # Decision engine (NEW)
│   │   ├── schemas/   # Domain models (Material, Machine, Policy, etc.)
│   │   ├── policies/  # Policy implementations
│   │   ├── arbitration/ # Conflict resolution
│   │   ├── constraints/ # Feasible range calculations
│   │   ├── signals/   # Risk assessment
│   │   ├── math/      # Feeds & speeds calculations
│   │   └── explainability/ # Decision trace generation
│   ├── app/
│   │   ├── api/routers/ # API routes (recommend, materials, policies, machines)
│   │   └── core/      # Configuration, auth, rate limiting
│   ├── models/        # SQLAlchemy models (tools, materials, machines, policies)
│   ├── schemas/       # Pydantic schemas (legacy tool schemas)
│   └── services/      # Business logic
├── infra/            # AWS CloudFormation templates
├── .github/workflows/ # CI/CD pipelines
├── monitoring/       # Grafana dashboards
└── docs/            # Documentation
```

## 🔧 Configuration

### Environment Variables

Create `.env` files in the root and backend directories:

```bash
# Root .env
NEXT_PUBLIC_API_URL=http://localhost:8000

# Backend .env
DATABASE_URL=postgresql://cnc_user:cnc_password@localhost:5432/cnc_calc
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-change-in-production
ENVIRONMENT=development
```

### Database Setup

The application uses PostgreSQL with the following tables:
- `tools`: Tool metadata and geometry
- `tool_exports`: Export history and data
- `materials`: Material definitions with properties (JSONB)
- `machines`: Machine definitions with capabilities (JSONB)
- `policies`: Policy definitions with weights and rules (JSONB)
- `recommendations`: Optional storage for recommendation history (JSONB)

**Run migrations and seed data:**
```bash
cd backend
poetry run alembic upgrade head
python scripts/seed_data.py
```

## 📊 API Documentation

### Primary Endpoints (Decision Engine)

- `POST /api/recommend` - Generate feeds & speeds recommendation (requires API key)
- `GET /api/materials` - List available materials
- `GET /api/materials/{id}` - Get specific material
- `GET /api/machines` - List available machines
- `GET /api/machines/{id}` - Get specific machine
- `GET /api/policies` - List available policies
- `POST /api/policies/test` - Test policy combinations

### Tool Management Endpoints

- `GET /api/healthz` - Health check (no auth required)
- `GET /api/tools` - List tools with pagination
- `POST /api/tools` - Create new tool
- `GET /api/tools/{id}` - Get specific tool
- `PUT /api/tools/{id}` - Update tool
- `DELETE /api/tools/{id}` - Delete tool
- `POST /api/tools/{id}/validate` - Validate tool
- `POST /api/tools/{id}/export` - Export tool
- `GET /api/tools/{id}/export/{export_id}/download` - Download export

**Note**: All endpoints except health checks require `X-API-Key` header. See `SECURITY_SETUP.md` for configuration.

### Optimization Policies

1. **Safety Policy**: Conservative parameters prioritizing tool and machine safety
   - Uses lower end of feasible ranges (70% RPM, 60% feedrate)
   - Maximum confidence, minimal risk

2. **Tool Life Policy**: Maximize tool life with lower SFM and feedrates
   - Uses 40% of RPM range, 50% of feedrate range
   - Extends tool longevity

3. **Time Policy**: Maximize material removal rate (MRR) to minimize cycle time
   - Uses 80% of RPM range, 85% of feedrate range
   - Optimizes for speed

4. **Balanced Policy**: Balance tool life, time, and safety
   - Uses middle of feasible ranges
   - Good default for most scenarios

**Note**: Safety is always applied as a base constraint. Multiple policies can be combined with weighted arbitration.

## 🚀 Deployment

### Development
```bash
make deploy-dev
```

### Production
```bash
make deploy-prod
```

### Infrastructure
```bash
make infra-up
```

## 🧪 Testing

### Frontend Tests
```bash
cd frontend
npm run test
npm run test:e2e
```

### Backend Tests
```bash
cd backend
pytest
```

### Integration Tests
```bash
make test
```

## 📈 Monitoring

- **Grafana**: http://localhost:3001 (admin/admin)
- **Health Checks**: `/api/health`, `/api/health/live`, `/api/health/ready`
- **Metrics**: Prometheus-compatible endpoints

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Documentation**: Check the `/docs` directory
- **Issues**: Create a GitHub issue
- **Email**: contact.jameslong@gmail.com

## 🔄 Changelog

### v2.0.0 (Current)
- **Major Pivot**: From tool management SaaS to policy-driven decision engine
- Decision engine with explainability
- Policy system (Safety, Tool Life, Time, Balanced)
- Scenario builder UI
- Materials, machines, and policies management
- Risk assessment and constraint detection
- See `ADAPTATION_SUMMARY.md` for full details

### v1.0.0 (Legacy)
- Tool management system
- Fusion 360 export
- Real-time validation
- Responsive design
