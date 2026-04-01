"""
Policy service: fetches PolicyModel rows and deserializes into engine Policy objects.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import Optional, List

from models.policy import Policy as PolicyModel
from engine.schemas.policy import Policy, PolicyWeights
import structlog

logger = structlog.get_logger()


class PolicyService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _row_to_schema(self, row: PolicyModel) -> Policy:
        return Policy(
            id=row.id,
            name=row.name,
            type=row.type,
            weights=PolicyWeights(**row.weights),
            rules=row.rules or {},
            priority=row.priority,
            description=row.description,
            notes=row.notes,
        )

    async def get_policy(self, policy_id: str) -> Optional[Policy]:
        result = await self.db.execute(
            select(PolicyModel).where(
                and_(PolicyModel.id == policy_id, PolicyModel.is_deleted == False)
            )
        )
        row = result.scalar_one_or_none()
        return self._row_to_schema(row) if row else None

    async def get_policies_by_ids(self, policy_ids: List[str]) -> List[Policy]:
        """Fetch policies by IDs, preserving priority order."""
        result = await self.db.execute(
            select(PolicyModel).where(
                and_(
                    PolicyModel.id.in_(policy_ids),
                    PolicyModel.is_deleted == False,
                )
            ).order_by(PolicyModel.priority)
        )
        rows = result.scalars().all()
        return [self._row_to_schema(row) for row in rows]

    async def list_policies(self) -> List[Policy]:
        result = await self.db.execute(
            select(PolicyModel)
            .where(PolicyModel.is_deleted == False)
            .order_by(PolicyModel.priority)
        )
        rows = result.scalars().all()
        return [self._row_to_schema(row) for row in rows]

    async def get_default_policy(self) -> Optional[Policy]:
        """Return the balanced policy as a safe default."""
        result = await self.db.execute(
            select(PolicyModel).where(
                and_(PolicyModel.type == "balanced", PolicyModel.is_deleted == False)
            ).limit(1)
        )
        row = result.scalar_one_or_none()
        return self._row_to_schema(row) if row else None
