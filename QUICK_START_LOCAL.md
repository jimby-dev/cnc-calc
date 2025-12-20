# Quick Start - Local Testing

## ✅ Yes, You Can Test Locally!

The application can run locally, but some features won't work until the service layer is implemented.

---

## Fastest Way to Get Running

### 1. Start Everything with Docker Compose

```bash
# Start all services (database, Redis, backend, frontend)
docker-compose up -d

# Wait a few seconds for services to start, then run migrations
cd backend
poetry run alembic upgrade head

# Seed the database with initial data
poetry run python scripts/seed_data.py
```

### 2. Access the Application

- **Frontend**: http://localhost:3000**
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## What You'll See

### ✅ Works
- Frontend homepage loads
- Scenario builder modal opens
- Step navigation works
- Form inputs work
- Policy weight sliders work
- Health check endpoint works
- Tool management endpoints work

### ⚠️ Limited Functionality
- Materials/machines/policies lists are empty (service layer needed)
- Can't generate recommendations yet (endpoint returns 501)
- Tool selection step is placeholder

---

## Development Mode Features

- **No API Key Required**: Development mode allows requests without API key
- **API Docs Enabled**: `/docs` and `/redoc` available
- **Hot Reload**: Both frontend and backend auto-reload on changes
- **CORS Enabled**: Frontend can call backend from localhost:3000

---

## Troubleshooting

**Backend won't start?**
- Check: `cd backend && poetry install`
- Check: Database is running (`docker ps`)

**Frontend won't start?**
- Check: `cd frontend && npm install`
- Check: Port 3000 is available

**Empty API responses?**
- Expected: Materials/machines/policies return `[]` until service layer is implemented
- This is normal - the endpoints exist but don't query the database yet

**Can't generate recommendations?**
- Expected: Returns 501 until service layer is implemented
- This is normal - the endpoint structure exists but needs database integration

---

## Full Testing Guide

See `LOCAL_TESTING_GUIDE.md` for comprehensive testing instructions, troubleshooting, and details on what works vs. what doesn't.

