"""
API Key Authentication Middleware
Simple authentication for private API access
"""
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from typing import Optional
import secrets
import structlog

from app.core.config import settings

logger = structlog.get_logger()

# API Key header name
API_KEY_HEADER = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_HEADER, auto_error=False)


async def verify_api_key(api_key: Optional[str] = Security(api_key_header)) -> bool:
    """
    Verify the API key from the request header.
    
    Args:
        api_key: API key from X-API-Key header
        
    Returns:
        True if API key is valid
        
    Raises:
        HTTPException: If API key is missing or invalid
    """
    # Get API key from settings (set via environment variable)
    expected_api_key = settings.API_KEY
    
    # In development, allow requests without API key if none is configured
    # In production, API key is required
    if not expected_api_key:
        if settings.ENVIRONMENT == "development":
            logger.debug("API key not configured in development, allowing request")
            return True
        else:
            logger.warning("API key not configured in production, denying access")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="API authentication not configured"
            )
    
    # If API key is missing or invalid
    # Use constant-time comparison to prevent timing attacks
    if not api_key or not secrets.compare_digest(api_key, expected_api_key):
        logger.warning("Invalid or missing API key", has_key=bool(api_key))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key. Please provide a valid X-API-Key header."
        )
    
    return True

