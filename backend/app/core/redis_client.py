"""
Redis client connection pool for reuse across the application
"""
import redis.asyncio as redis
from app.core.config import settings
import structlog

logger = structlog.get_logger()

# Global Redis connection pool
_redis_pool: redis.Redis | None = None


async def get_redis_client() -> redis.Redis:
    """
    Get Redis client from connection pool.
    Creates pool on first call if it doesn't exist.
    """
    global _redis_pool
    
    if _redis_pool is None:
        _redis_pool = redis.from_url(
            settings.REDIS_URL,
            password=settings.REDIS_PASSWORD,
            encoding="utf-8",
            decode_responses=True,
            max_connections=10,
        )
        logger.info("Redis connection pool created", url=settings.REDIS_URL)
    
    return _redis_pool


async def close_redis_pool() -> None:
    """Close Redis connection pool"""
    global _redis_pool
    
    if _redis_pool:
        await _redis_pool.aclose()
        _redis_pool = None
        logger.info("Redis connection pool closed")

