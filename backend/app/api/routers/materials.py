"""
Materials API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
import structlog

from app.core.database import get_db
from app.core.auth import verify_api_key
from engine.schemas import Material

logger = structlog.get_logger()
router = APIRouter(prefix="/materials", tags=["materials"])


@router.get("/", response_model=List[Material], dependencies=[Depends(verify_api_key)])
async def list_materials(
    category: Optional[str] = Query(None, description="Filter by material category"),
    search: Optional[str] = Query(None, description="Search term"),
    db: AsyncSession = Depends(get_db)
):
    """
    List all available materials.
    """
    try:
        # TODO: Implement database query
        # For now, return empty list
        return []
    except Exception as e:
        error_type = type(e).__name__
        logger.error("Failed to list materials", error_type=error_type, exc_info=False)
        raise HTTPException(status_code=500, detail="Failed to list materials")


@router.get("/{material_id}", response_model=Material, dependencies=[Depends(verify_api_key)])
async def get_material(
    material_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific material by ID.
    """
    try:
        # TODO: Implement database query
        raise HTTPException(status_code=404, detail="Material not found")
    except HTTPException:
        raise
    except Exception as e:
        error_type = type(e).__name__
        logger.error("Failed to get material", material_id=material_id, error_type=error_type, exc_info=False)
        raise HTTPException(status_code=500, detail="Failed to get material")

