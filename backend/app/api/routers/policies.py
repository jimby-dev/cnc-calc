"""
Policies API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import structlog

from app.core.database import get_db
from app.core.auth import verify_api_key
from engine.schemas import Policy
from services.policy_service import PolicyService

logger = structlog.get_logger()
router = APIRouter(prefix="/policies", tags=["policies"])


@router.get("/", response_model=List[Policy], dependencies=[Depends(verify_api_key)])
async def list_policies(
    db: AsyncSession = Depends(get_db),
):
    """List all available policies, ordered by priority."""
    try:
        return await PolicyService(db).list_policies()
    except Exception as e:
        logger.error("Failed to list policies", error_type=type(e).__name__, exc_info=False)
        raise HTTPException(status_code=500, detail="Failed to list policies")


@router.get("/{policy_id}", response_model=Policy, dependencies=[Depends(verify_api_key)])
async def get_policy(
    policy_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific policy by ID."""
    try:
        policy = await PolicyService(db).get_policy(policy_id)
        if policy is None:
            raise HTTPException(status_code=404, detail=f"Policy '{policy_id}' not found")
        return policy
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get policy", policy_id=policy_id, error_type=type(e).__name__, exc_info=False)
        raise HTTPException(status_code=500, detail="Failed to get policy")

