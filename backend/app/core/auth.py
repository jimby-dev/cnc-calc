"""
API Key Authentication — passthrough (Tauri local-only build).
The function signature is preserved so all existing Depends(verify_api_key)
call-sites continue to work without modification.
"""
from typing import Optional
from fastapi.security import APIKeyHeader
from fastapi import Security

API_KEY_HEADER = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_HEADER, auto_error=False)


async def verify_api_key(api_key: Optional[str] = Security(api_key_header)) -> bool:
    """Always succeeds — authentication is handled at the Tauri layer."""
    return True
