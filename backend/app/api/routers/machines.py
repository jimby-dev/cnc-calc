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
from services.machine_service import MachineService

logger = structlog.get_logger()
router = APIRouter(prefix="/machines", tags=["machines"])


@router.get("/", response_model=List[Machine], dependencies=[Depends(verify_api_key)])
async def list_machines(
    type: Optional[str] = Query(None, description="Filter by machine type (mill, lathe, router, ...)"),
    search: Optional[str] = Query(None, description="Search machines by name"),
    db: AsyncSession = Depends(get_db),
):
    """List all available machines, optionally filtered by type or name."""
    try:
        return await MachineService(db).list_machines(machine_type=type, search=search)
    except Exception as e:
        logger.error("Failed to list machines", error_type=type(e).__name__, exc_info=False)
        raise HTTPException(status_code=500, detail="Failed to list machines")


@router.get("/{machine_id}", response_model=Machine, dependencies=[Depends(verify_api_key)])
async def get_machine(
    machine_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific machine by ID."""
    try:
        machine = await MachineService(db).get_machine(machine_id)
        if machine is None:
            raise HTTPException(status_code=404, detail=f"Machine '{machine_id}' not found")
        return machine
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get machine", machine_id=machine_id, error_type=type(e).__name__, exc_info=False)
        raise HTTPException(status_code=500, detail="Failed to get machine")

