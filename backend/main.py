import sys
from pathlib import Path

# Add backend directory to Python path for engine imports
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import structlog
import uvicorn

from app.core.config import settings
from app.core.redis_client import close_redis_pool
from app.core.auth import verify_api_key
from app.core.rate_limit import RateLimitMiddleware
from app.api.routers import tools, health, recommend, materials, policies, machines

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Create FastAPI app
app = FastAPI(
    title="CNC Calculator API",
    description="API for managing CNC tool profiles and exports",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
)

# Rate limiting middleware (applied first)
app.add_middleware(
    RateLimitMiddleware,
    requests_per_minute=settings.RATE_LIMIT_PER_MINUTE
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Restrict to required methods
    allow_headers=["Content-Type", "X-API-Key"],  # Explicitly allow required headers
)

# Trusted host middleware
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )

# Include routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(tools.router, prefix="/api/tools", tags=["tools"])
app.include_router(recommend.router, prefix="/api", tags=["recommendations"])
app.include_router(materials.router, prefix="/api", tags=["materials"])
app.include_router(policies.router, prefix="/api", tags=["policies"])
app.include_router(machines.router, prefix="/api", tags=["machines"])

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("Starting CNC Calculator API", environment=settings.ENVIRONMENT)
    # Note: Database migrations should be run separately using Alembic
    # Run: alembic upgrade head

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down CNC Calculator API")
    await close_redis_pool()

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    logger.warning(
        "HTTP exception",
        status_code=exc.status_code,
        detail=exc.detail,
        path=request.url.path
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler - sanitizes error information"""
    # Log exception type and path, but not full details
    error_type = type(exc).__name__
    logger.error(
        "Unhandled exception",
        error_type=error_type,
        path=request.url.path,
        exc_info=True  # Full traceback in logs only, not exposed to user
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
        log_config=None  # Use our structured logging
    )
