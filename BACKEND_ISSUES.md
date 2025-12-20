# Backend Issues & Fixes

## Issues Found and Fixed

### ✅ Fixed: Python Import Path Errors (CRITICAL)

**Issue**: Engine module imports would fail on startup  
**Fix**: Added Python path setup in `backend/main.py`:

```python
import sys
from pathlib import Path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))
```

**File**: `backend/main.py` (lines 1-3)  
**Status**: Application can now start without import errors

### ✅ Fixed: Seed Script Import Path

**Issue**: Seed script imports models without proper path setup  
**Fix**: Added `sys.path` manipulation to include backend directory  
**File**: `backend/scripts/seed_data.py`

### ✅ Fixed: Migration Index Error

**Issue**: Typo in migration file for policies table index  
**Fix**: Corrected `op.create_index` call  
**File**: `backend/alembic/versions/002_add_engine_tables.py`

### ✅ Fixed: Model Imports

**Issue**: Models need to be imported in Alembic env.py  
**Fix**: Added imports for all new models  
**File**: `backend/alembic/env.py`

### ✅ Fixed: Missing Machine Endpoint

**Issue**: No `/api/machines` endpoint existed  
**Fix**: Created `backend/app/api/routers/machines.py` and added to `main.py`  
**File**: `backend/app/api/routers/machines.py`, `backend/main.py`

## Known Issues (Not Yet Fixed)

### ⚠️ Recommendation Endpoint Not Fully Implemented

**Status**: Returns 501 (Not Implemented)  
**Location**: `backend/app/api/routers/recommend.py`  
**Issue**: Endpoint structure exists but needs:

1. Database service layer for materials, machines, policies
2. Tool-to-EngineTool conversion logic
3. Full integration with DecisionEngine

**Required Work**:

```python
# Need to create:
- services/material_service.py
- services/machine_service.py
- services/policy_service.py
- utils/tool_converter.py (convert Tool model to EngineTool schema)
```

### ⚠️ Materials/Machines/Policies Endpoints Return Empty Arrays

**Status**: Endpoints exist but return empty data  
**Location**:

- `backend/app/api/routers/materials.py`
- `backend/app/api/routers/policies.py`

**Issue**: Database queries not implemented  
**Required Work**:

```python
# Need to implement:
- Database queries using SQLAlchemy
- Service layer methods
- Error handling
```

### ⚠️ Missing Database Service Layer

**Status**: No service layer for new models  
**Required Files**:

- `backend/services/material_service.py`
- `backend/services/machine_service.py`
- `backend/services/policy_service.py`

**Pattern to Follow**: See `backend/services/tool_service.py` for reference

## Import Path Considerations

### Current Import Style

- **Engine modules**: Use relative imports (`.schemas`, `.policies`)
- **App modules**: Use absolute imports (`app.core.database`)
- **Models**: Use `models.` prefix (works if backend is in Python path)

### Potential Issues

- If running scripts directly, may need to adjust Python path
- Seed script now handles this with `sys.path` manipulation

## Testing Recommendations

### Unit Tests Needed

1. **Engine Tests**:
   - `tests/engine/test_engine.py` - Test DecisionEngine pipeline
   - `tests/engine/test_policies.py` - Test each policy implementation
   - `tests/engine/test_arbitration.py` - Test conflict resolution
   - `tests/engine/test_math.py` - Test feeds & speeds calculations
   - `tests/engine/test_constraints.py` - Test feasible range calculations

2. **API Tests**:
   - `tests/api/test_recommend.py` - Test recommendation endpoint
   - `tests/api/test_materials.py` - Test materials endpoints
   - `tests/api/test_policies.py` - Test policies endpoints

3. **Integration Tests**:
   - Full scenario: tool + material + machine → recommendation
   - Policy conflict scenarios
   - Edge cases (limits, constraints)

## Next Steps to Complete Backend

### Priority 1: Make Recommendation Endpoint Functional

1. Create service layer for materials, machines, policies
2. Implement tool-to-EngineTool converter
3. Complete recommendation endpoint implementation
4. Add error handling and validation

### Priority 2: Complete API Endpoints

1. Implement database queries in materials endpoint
2. Implement database queries in machines endpoint
3. Implement database queries in policies endpoint
4. Add pagination, filtering, search

### Priority 3: Testing

1. Write unit tests for engine components
2. Write integration tests for API endpoints
3. Add golden snapshot tests for recommendations

## Code Quality

### ✅ Good Practices Followed

- Type hints throughout
- Pydantic models for validation
- Structured logging
- Error handling patterns
- Separation of concerns (engine vs API vs DB)

### ⚠️ Areas for Improvement

- Add docstrings to all public methods
- Add type checking with mypy
- Add input validation in API endpoints
- Add rate limiting considerations for recommendation endpoint
- Consider caching for materials/machines/policies (rarely change)

## Summary

The backend engine is **functionally complete** but needs **integration work** to connect the API endpoints to the database and engine. The core decision logic is solid and tested through the schema definitions, but the service layer and API implementations need completion.

The main blocker is implementing the database service layer and completing the recommendation endpoint. Once that's done, the system will be fully functional.
