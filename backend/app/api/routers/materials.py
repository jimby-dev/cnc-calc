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
from services.material_service import MaterialService

logger = structlog.get_logger()
router = APIRouter(prefix="/materials", tags=["materials"])


@router.get("/", response_model=List[Material], dependencies=[Depends(verify_api_key)])
async def list_materials(
    category: Optional[str] = Query(None, description="Filter by material category"),
    search: Optional[str] = Query(None, description="Search materials by name"),
    db: AsyncSession = Depends(get_db),
):
    """List all available materials, optionally filtered by category or name."""
    try:
        return await MaterialService(db).list_materials(category=category, search=search)
    except Exception as e:
        logger.error("Failed to list materials", error_type=type(e).__name__, exc_info=False)
        raise HTTPException(status_code=500, detail="Failed to list materials")


@router.get("/{material_id}", response_model=Material, dependencies=[Depends(verify_api_key)])
async def get_material(
    material_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific material by ID."""
    try:
        material = await MaterialService(db).get_material(material_id)
        if material is None:
            raise HTTPException(status_code=404, detail=f"Material '{material_id}' not found")
        return material
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get material", material_id=material_id, error_type=type(e).__name__, exc_info=False)
        raise HTTPException(status_code=500, detail="Failed to get material")

