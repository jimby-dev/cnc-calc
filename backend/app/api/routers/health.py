from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db
from app.core.config import settings
from schemas.tool import HealthResponse
from datetime import datetime
import redis.asyncio as redis
import structlog

logger = structlog.get_logger()
router = APIRouter()

async def check_database(db: AsyncSession) -> str:
    """Check database connectivity"""
    try:
        result = await db.execute(text("SELECT 1"))
        return "healthy"
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        return "unhealthy"

async def check_redis() -> str:
    """Check Redis connectivity"""
    try:
        redis_client = redis.from_url(settings.REDIS_URL)
        await redis_client.ping()
        await redis_client.close()
        return "healthy"
    except Exception as e:
        logger.error("Redis health check failed", error=str(e))
        return "unhealthy"

@router.get("/health", response_model=HealthResponse)
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Health check endpoint for monitoring and load balancers
    """
    try:
        # Check database
        db_status = await check_database(db)
        
        # Check Redis
        redis_status = await check_redis()
        
        # Overall status
        overall_status = "healthy" if db_status == "healthy" and redis_status == "healthy" else "unhealthy"
        
        return HealthResponse(
            status=overall_status,
            version=settings.VERSION,
            environment=settings.ENVIRONMENT,
            database=db_status,
            redis=redis_status,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        raise HTTPException(status_code=503, detail="Service unavailable")

@router.get("/health/live")
async def liveness_check():
    """
    Kubernetes liveness probe endpoint
    """
    return {"status": "alive", "timestamp": datetime.utcnow()}

@router.get("/health/ready")
async def readiness_check(db: AsyncSession = Depends(get_db)):
    """
    Kubernetes readiness probe endpoint
    """
    try:
        db_status = await check_database(db)
        redis_status = await check_redis()
        
        if db_status == "healthy" and redis_status == "healthy":
            return {"status": "ready", "timestamp": datetime.utcnow()}
        else:
            raise HTTPException(status_code=503, detail="Service not ready")
            
    except Exception as e:
        logger.error("Readiness check failed", error=str(e))
        raise HTTPException(status_code=503, detail="Service not ready")
