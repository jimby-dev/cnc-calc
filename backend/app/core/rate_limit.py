"""
Redis-based Rate Limiting Middleware
Prevents API abuse and works with multiple instances
"""
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from datetime import datetime, timedelta
import structlog

from app.core.config import settings
from app.core.redis_client import get_redis_client

logger = structlog.get_logger()


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Redis-based rate limiter for production use with multiple instances.
    Uses sliding window algorithm with Redis.
    """
    
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.window_seconds = 60
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks
        if request.url.path in ["/api/health", "/api/health/live", "/api/health/ready"]:
            return await call_next(request)
        
        # Get client identifier (IP address)
        client_ip = request.client.host if request.client else "unknown"
        redis_key = f"rate_limit:{client_ip}"
        
        try:
            redis_client = await get_redis_client()
            current_time = datetime.utcnow()
            window_start = current_time - timedelta(seconds=self.window_seconds)
            
            # Use Redis pipeline for atomic operations
            pipe = redis_client.pipeline()
            
            # Remove old entries (outside window)
            pipe.zremrangebyscore(redis_key, 0, window_start.timestamp())
            
            # Count requests in current window
            pipe.zcard(redis_key)
            
            # Add current request
            pipe.zadd(redis_key, {str(current_time.timestamp()): current_time.timestamp()})
            
            # Set expiration
            pipe.expire(redis_key, self.window_seconds)
            
            # Execute pipeline
            results = await pipe.execute()
            request_count = results[1]  # Count from zcard
            
            # Check if limit exceeded
            if request_count >= self.requests_per_minute:
                logger.warning(
                    "Rate limit exceeded",
                    client_ip=client_ip,
                    count=request_count,
                    limit=self.requests_per_minute,
                    path=request.url.path
                )
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded: {self.requests_per_minute} requests per minute. Please try again later."
                )
            
            # Process request
            response = await call_next(request)
            
            # Add rate limit headers
            remaining = max(0, self.requests_per_minute - request_count - 1)
            reset_time = int((current_time + timedelta(seconds=self.window_seconds)).timestamp())
            
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(remaining)
            response.headers["X-RateLimit-Reset"] = str(reset_time)
            
            return response
            
        except HTTPException:
            raise
        except Exception as e:
            # If Redis fails, log and allow request (fail open)
            logger.error("Rate limit check failed", error=str(e), client_ip=client_ip)
            return await call_next(request)

