# How to Start and Stop the Application Locally

## Starting the Application

### Step 1: Start All Services
```bash
docker-compose up -d
```

This starts:
- PostgreSQL database (port 5432)
- Redis (port 6379)
- Backend API (port 8000)
- Frontend (port 3000)
- Optional: Nginx (port 80), Grafana (port 3001)

### Step 2: Run Database Migrations
```bash
cd backend
poetry run alembic upgrade head
```

### Step 3: Seed Initial Data
```bash
# Still in backend directory
poetry run python scripts/seed_data.py
```

### Step 4: Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## Alternative: Using Makefile Commands

```bash
# Start database and Redis only
make db-up

# Run migrations
make db-migrate

# Seed data
make db-seed

# Start frontend and backend manually (in separate terminals)
# Terminal 1:
cd backend && poetry run uvicorn main:app --reload

# Terminal 2:
cd frontend && npm run dev
```

---

## Stopping the Application

### Option 1: Stop All Services (Recommended)
```bash
docker-compose down
```

This stops and removes all containers.

### Option 2: Stop But Keep Data
```bash
docker-compose stop
```

This stops containers but keeps them (data persists). Use `docker-compose start` to restart.

### Option 3: Stop and Remove Volumes (Clean Slate)
```bash
docker-compose down -v
```

**Warning**: This deletes all database data! Use only if you want to start fresh.

---

## Using Makefile

```bash
# Stop all services
make docker-down
```

---

## Quick Reference

### Start Everything
```bash
docker-compose up -d
cd backend && poetry run alembic upgrade head && poetry run python scripts/seed_data.py
```

### Stop Everything
```bash
docker-compose down
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Check Status
```bash
docker-compose ps
```

### Restart a Service
```bash
docker-compose restart backend
docker-compose restart frontend
```

---

## Troubleshooting

### Port Already in Use
If you get "port already in use" errors:
```bash
# Find what's using the port
lsof -i :3000  # Frontend
lsof -i :8000  # Backend
lsof -i :5432  # Database

# Kill the process or change ports in docker-compose.yml
```

### Services Won't Start
```bash
# Check logs
docker-compose logs

# Rebuild containers
docker-compose up -d --build
```

### Database Connection Errors
```bash
# Make sure database is running
docker-compose ps

# Check database logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

---

## One-Liner Commands

### Start Everything (First Time)
```bash
docker-compose up -d && cd backend && poetry run alembic upgrade head && poetry run python scripts/seed_data.py && cd ..
```

### Start Everything (Subsequent Times)
```bash
docker-compose up -d
```

### Stop Everything
```bash
docker-compose down
```

### Full Reset (Delete All Data)
```bash
docker-compose down -v && docker-compose up -d && cd backend && poetry run alembic upgrade head && poetry run python scripts/seed_data.py && cd ..
```

