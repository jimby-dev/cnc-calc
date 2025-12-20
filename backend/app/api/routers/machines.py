"""
Machines API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
import structlog

from app.core.database import get_db
from app.core.auth import verify_api_key
from engine.schemas import Machine

logger = structlog.get_logger()
router = APIRouter(prefix="/machines", tags=["machines"])


@router.get("/", response_model=List[Machine], dependencies=[Depends(verify_api_key)])
async def list_machines(
    type: Optional[str] = Query(None, description="Filter by machine type"),
    search: Optional[str] = Query(None, description="Search term"),
    db: AsyncSession = Depends(get_db)
):
    """
    List all available machines.
    """
    try:
        # TODO: Implement database query
        # For now, return empty list
        return []
    except Exception as e:
        error_type = type(e).__name__
        logger.error("Failed to list machines", error_type=error_type, exc_info=False)
        raise HTTPException(status_code=500, detail="Failed to list machines")


@router.get("/{machine_id}", response_model=Machine, dependencies=[Depends(verify_api_key)])
async def get_machine(
    machine_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific machine by ID.
    """
    try:
        # TODO: Implement database query
        raise HTTPException(status_code=404, detail="Machine not found")
    except HTTPException:
        raise
    except Exception as e:
        error_type = type(e).__name__
        logger.error("Failed to get machine", machine_id=machine_id, error_type=error_type, exc_info=False)
        raise HTTPException(status_code=500, detail="Failed to get machine")

