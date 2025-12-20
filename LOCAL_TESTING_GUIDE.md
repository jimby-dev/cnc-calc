# Local Testing Guide

## Can You Test Locally?

**✅ YES** - You can test the webapp locally, but with some limitations.

The application will run, but certain features won't work until the service layer is implemented.

---

## Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# 1. Start all services (database, Redis, backend, frontend)
make docker-up

# 2. Run database migrations
make db-migrate

# 3. Seed initial data (materials, machines, policies)
cd backend
poetry run python scripts/seed_data.py

# 4. Access the app
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup (Without Docker)

```bash
# 1. Install dependencies
make setup

# 2. Start database and Redis
make db-up

# 3. Run migrations
make db-migrate

# 4. Seed data
cd backend
poetry run python scripts/seed_data.py

# 5. Start backend (in one terminal)
cd backend
poetry run uvicorn main:app --reload

# 6. Start frontend (in another terminal)
cd frontend
npm run dev
```

---

## What Works Locally ✅

### Fully Functional

- ✅ **Backend starts** - No import errors (fixed)
- ✅ **Frontend builds and runs** - Next.js dev server works
- ✅ **Health check endpoint** - `/api/healthz` (no auth required)
- ✅ **API documentation** - `/docs` and `/redoc` available in development
- ✅ **Tool CRUD endpoints** - Existing tool management still works
- ✅ **Database migrations** - Can run successfully
- ✅ **Seed data** - Can populate materials, machines, policies

### Partially Functional

- ⚠️ **Scenario Builder UI** - Renders but shows empty states (no data loading)
- ⚠️ **Recommendation Display** - Component works but can't generate recommendations yet
- ⚠️ **API Authentication** - **FIXED**: Now allows development mode without API key

---

## What Doesn't Work Yet ⚠️

### Backend API Endpoints

- ❌ `POST /api/recommend` - Returns 501 (service layer not implemented)
- ❌ `GET /api/materials` - Returns empty array `[]` (no database queries)
- ❌ `GET /api/machines` - Returns empty array `[]` (no database queries)
- ❌ `GET /api/policies` - Returns empty array `[]` (no database queries)

### Frontend Features

- ❌ **Data Loading** - API calls are commented out in `ScenarioBuilder.tsx`
- ❌ **Tool Selection** - Step 1 is placeholder only
- ❌ **Recommendation Generation** - Can't generate recommendations yet
- ❌ **Export Presets** - Button exists but functionality not implemented

---

## Environment Setup

### Backend Environment Variables

Create `backend/.env`:

```env
# Database (docker-compose provides these automatically)
DATABASE_URL=postgresql://cnc_user:cnc_password@localhost:5432/cnc_calc

# Redis (docker-compose provides these automatically)
REDIS_URL=redis://localhost:6379

# Development settings
ENVIRONMENT=development
SECRET_KEY=dev-secret-key-change-in-production

# API Key (OPTIONAL in development - auth allows requests without it)
# API_KEY=dev-api-key-123

# CORS (defaults are fine for localhost)
# ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Frontend Environment Variables

Create `frontend/.env.local`:

```env
# Backend URL
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
# or
NEXT_PUBLIC_API_URL=http://localhost:8000

# API Key (OPTIONAL in development - can be empty)
# NEXT_PUBLIC_API_KEY=dev-api-key-123
```

**Note**: API key is now optional in development mode. The backend will allow requests without it.

---

## Testing Workflow

### 1. Test Backend API

```bash
# Health check (no auth needed)
curl http://localhost:8000/api/healthz

# Tool endpoints (no auth needed in development)
curl http://localhost:8000/api/tools

# Materials endpoint (will return empty array)
curl http://localhost:8000/api/materials

# Recommendation endpoint (will return 501)
curl -X POST http://localhost:8000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"tool_id": "test", "material_id": "test", "machine_id": "test", "operation": {"type": "roughing", "depth_of_cut_mm": 2.0, "width_of_cut_mm": 5.0}, "policy_ids": []}'
```

### 2. Test Frontend

1. Open http://localhost:3000
2. You should see the "Machining Decision Engine" homepage
3. Click "Build Scenario" - modal opens
4. Navigate through steps - UI works but data won't load
5. Step 5 (Policies) will show empty state

### 3. Test Database

```bash
# Connect to database
docker exec -it cnccalc-postgres-1 psql -U cnc_user -d cnc_calc

# Check if tables exist
\dt

# Check if data is seeded
SELECT * FROM materials;
SELECT * FROM machines;
SELECT * FROM policies;
```

---

## Known Issues & Workarounds

### Issue 1: Empty API Responses

**Problem**: Materials/machines/policies endpoints return `[]`  
**Workaround**: None - service layer needs to be implemented  
**Impact**: Frontend shows empty states

### Issue 2: Recommendation Endpoint Returns 501

**Problem**: Service layer not implemented  
**Workaround**: None - needs implementation  
**Impact**: Can't generate recommendations

### Issue 3: Frontend API Calls Commented Out

**Problem**: API calls are in TODO comments  
**Workaround**: Uncomment lines 47-54 in `ScenarioBuilder.tsx` (but will still get empty arrays)  
**Impact**: Frontend won't attempt to load data

### Issue 4: Database Not Seeded

**Problem**: Need to run seed script  
**Workaround**: Run `python backend/scripts/seed_data.py`  
**Impact**: No materials/machines/policies available

---

## What You Can Test Right Now

### ✅ UI/UX Testing

- Scenario builder modal opens and closes
- Step navigation works
- Form inputs work
- Policy weight sliders work
- Recommendation display component renders (with mock data)

### ✅ Backend Testing

- Backend starts without errors
- Health check works
- Tool CRUD endpoints work (if you have tools)
- API documentation accessible
- Database migrations run
- Seed script runs

### ✅ Integration Testing

- Frontend can connect to backend
- CORS works
- API client includes headers correctly
- Error handling displays properly

---

## Making It More Functional

To make the app semi-functional for testing:

### Step 1: Uncomment Frontend API Calls (5 minutes)

Edit `frontend/src/components/ScenarioBuilder.tsx`:

```typescript
// Uncomment lines 47-54
const [materialsRes, machinesRes, policiesRes] = await Promise.all([
  apiClient.get("/materials"),
  apiClient.get("/machines"),
  apiClient.get("/policies"),
]);
setMaterials(materialsRes);
setMachines(machinesRes);
setPolicies(policiesRes);
```

### Step 2: Implement Basic Service Layer (2-3 hours)

Create service files and implement basic database queries to return seeded data.

### Step 3: Complete Recommendation Endpoint (1-2 hours)

Wire up the decision engine to the API endpoint.

---

## Troubleshooting

### Backend Won't Start

- **Check**: Python path setup in `backend/main.py` (should be there)
- **Check**: Dependencies installed (`poetry install`)
- **Check**: Database running (`docker ps`)

### Frontend Won't Start

- **Check**: Node modules installed (`npm install` in frontend/)
- **Check**: Port 3000 not in use
- **Check**: Backend is running on port 8000

### API Returns 401/403

- **Check**: API key is optional in development (should work without it)
- **Check**: `ENVIRONMENT=development` in backend/.env
- **Check**: CORS settings allow localhost:3000

### Database Connection Errors

- **Check**: PostgreSQL container is running (`docker ps`)
- **Check**: `DATABASE_URL` matches docker-compose settings
- **Check**: Database exists (`docker exec -it <postgres-container> psql -U cnc_user -l`)

### Empty API Responses

- **Expected**: Materials/machines/policies will return `[]` until service layer is implemented
- **Workaround**: None - this is expected behavior

---

## Summary

**Can you test locally?** ✅ **YES**

**What works:**

- Application starts
- UI renders
- Basic navigation works
- Tool management (existing features)
- Health checks

**What doesn't work:**

- Loading materials/machines/policies (empty arrays)
- Generating recommendations (501 error)
- Tool selection in scenario builder

**Status:** Application is **runnable but **partially functional\*\*. You can test the UI and basic functionality, but the decision engine features need service layer implementation to work.

---

## Next Steps to Make It Fully Functional

1. Implement service layer (2-3 hours)
2. Uncomment frontend API calls (5 minutes)
3. Complete recommendation endpoint (1-2 hours)

Total: ~4 hours to make it fully functional for local testing.
