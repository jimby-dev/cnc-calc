"""
Recommendation API endpoints for the decision engine.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import Optional, Dict, Any
import structlog

from app.core.database import get_db
from app.core.auth import verify_api_key
from engine.engine import DecisionEngine
from engine.schemas import Operation, PolicyWeights, Recommendation
from engine.schemas.tool import EngineTool, ToolGeometry, ToolLimits, ToolType
from pydantic import BaseModel
from models.tool import Tool as ToolModel
from services.material_service import MaterialService
from services.machine_service import MachineService
from services.policy_service import PolicyService

logger = structlog.get_logger()
router = APIRouter(prefix="/recommend", tags=["recommendations"])

# Fields that map directly to ToolGeometry named attributes
_GEOMETRY_FIELDS = frozenset(
    {"diameter", "flute_length", "overall_length", "flute_count", "helix_angle", "corner_radius", "tip_radius"}
)


def _row_to_engine_tool(row: ToolModel) -> EngineTool:
    """Convert a Tool ORM row into an EngineTool schema object."""
    geo: Dict[str, Any] = row.geometry or {}
    known = {k: v for k, v in geo.items() if k in _GEOMETRY_FIELDS}
    extra = {k: v for k, v in geo.items() if k not in _GEOMETRY_FIELDS}
    geometry = ToolGeometry(**known, extra=extra)
    limits = ToolLimits(**row.limits) if row.limits else None
    return EngineTool(
        id=row.id,
        name=row.name,
        vendor=row.vendor or "",
        type=ToolType(row.type),
        geometry=geometry,
        limits=limits,
    )


class RecommendRequest(BaseModel):
    """Request schema for recommendation endpoint."""
    tool_id: str
    material_id: str
    machine_id: str
    operation: Operation
    policy_ids: list[str] = []
    weights: Optional[PolicyWeights] = None
    workholding_id: Optional[str] = None
    coolant_id: Optional[str] = None


@router.post("/", response_model=Recommendation, dependencies=[Depends(verify_api_key)])
async def recommend(
    request: RecommendRequest,
    db: AsyncSession = Depends(get_db),
):
    """Generate a feeds & speeds recommendation from the decision engine."""
    try:
        # --- Load tool --------------------------------------------------
        result = await db.execute(
            select(ToolModel).where(
                and_(ToolModel.id == request.tool_id, ToolModel.is_deleted == False)
            )
        )
        tool_row = result.scalar_one_or_none()
        if tool_row is None:
            raise HTTPException(status_code=404, detail=f"Tool '{request.tool_id}' not found")
        engine_tool = _row_to_engine_tool(tool_row)

        # --- Load material ----------------------------------------------
        material = await MaterialService(db).get_material(request.material_id)
        if material is None:
            raise HTTPException(status_code=404, detail=f"Material '{request.material_id}' not found")

        # --- Load machine -----------------------------------------------
        machine = await MachineService(db).get_machine(request.machine_id)
        if machine is None:
            raise HTTPException(status_code=404, detail=f"Machine '{request.machine_id}' not found")

        # --- Load policies (fall back to balanced default if none given) -
        policy_svc = PolicyService(db)
        if request.policy_ids:
            policies = await policy_svc.get_policies_by_ids(request.policy_ids)
            if not policies:
                raise HTTPException(
                    status_code=404,
                    detail=f"None of the requested policies were found: {request.policy_ids}",
                )
        else:
            default = await policy_svc.get_default_policy()
            if default is None:
                raise HTTPException(status_code=503, detail="No policies found in database; run seed script first")
            policies = [default]

        # --- Resolve weights --------------------------------------------
        weights = (request.weights or PolicyWeights()).normalize()

        # --- Run the decision engine ------------------------------------
        engine = DecisionEngine()
        recommendation = engine.recommend(
            tool=engine_tool,
            material=material,
            machine=machine,
            operation=request.operation,
            policies=policies,
            weights=weights,
            workholding=None,
            coolant=None,
        )

        return recommendation

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to generate recommendation", error_type=type(e).__name__, exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate recommendation")

