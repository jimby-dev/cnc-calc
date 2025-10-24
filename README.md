# CNC Calculator

An online tool management system designed specifically for CNC machinists to create, manage, and export tool profiles compatible with Fusion 360.

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

### Tool Management
- **6 Tool Types**: End Mill, Ball End Mill, Chamfer, Drill, Reamer, Thread Mill
- **Dynamic Forms**: Tool-specific geometry forms with real-time validation
- **Visual Preview**: 2D SVG tool cross-section visualization
- **Search & Filter**: Find tools by name, vendor, or type

### Export Capabilities
- **Fusion 360 Integration**: Direct .tools JSON export
- **CSV Export**: Compatible with Excel and other CAM software
- **Unit Conversion**: Metric (mm) and Imperial (inches) support
- **Validation**: Pre-export validation for Fusion 360 compatibility

### User Experience
- **4-Step Wizard**: Guided tool creation process
- **Real-time Validation**: Instant feedback on geometry relationships
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Accessibility**: WCAG compliant with keyboard navigation

## 🏗️ Architecture

### Frontend (Next.js)
- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS with custom components
- **State Management**: React hooks with SWR for data fetching
- **Validation**: Zod schemas with real-time validation
- **3D Visualization**: Three.js for optional 3D tool preview

### Backend (FastAPI)
- **Framework**: FastAPI with async/await support
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Caching**: Redis for session management
- **Validation**: Pydantic models with comprehensive validation
- **Export**: JSON and CSV generation with unit conversion

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
│   │   ├── components/ # React components
│   │   ├── types/     # TypeScript definitions
│   │   └── utils/     # Utility functions
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── api/      # API routes
│   │   ├── core/     # Core configuration
│   │   └── db/       # Database setup
│   ├── models/       # SQLAlchemy models
│   ├── schemas/      # Pydantic schemas
│   └── services/     # Business logic
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

## 📊 API Documentation

### Endpoints

- `GET /api/health` - Health check
- `GET /api/tools` - List tools with pagination
- `POST /api/tools` - Create new tool
- `GET /api/tools/{id}` - Get specific tool
- `PUT /api/tools/{id}` - Update tool
- `DELETE /api/tools/{id}` - Delete tool
- `POST /api/tools/{id}/validate` - Validate tool
- `POST /api/tools/{id}/export` - Export tool
- `GET /api/tools/{id}/export/{export_id}/download` - Download export

### Tool Types

1. **End Mill**: Square end cutting tool
   - Diameter, flute count, helix angle, flute length, length of cut, overall length, corner radius

2. **Ball End Mill**: Spherical end for 3D contouring
   - Diameter, flute count, tip radius, flute length, overall length

3. **Chamfer Mill**: Angled cutting tool
   - Included angle, tip flat, flute length, overall length, shank diameter

4. **Drill**: Pointed tool for holes
   - Diameter, point angle, flute length, overall length

5. **Reamer**: Precision finishing tool
   - Diameter, flute length, overall length, optional lead angle

6. **Thread Mill**: Thread creation tool
   - Diameter, pitch, maximum thread length, flute length, overall length

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

### v1.0.0
- Initial release
- Tool management system
- Fusion 360 export
- Real-time validation
- Responsive design
