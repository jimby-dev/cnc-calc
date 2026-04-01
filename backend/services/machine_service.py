"""
Machine service: fetches MachineModel rows and deserializes into engine Machine objects.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import Optional, List

from models.machine import Machine as MachineModel
from engine.schemas.machine import Machine, MachineCapabilities
import structlog

logger = structlog.get_logger()


class MachineService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _row_to_schema(self, row: MachineModel) -> Machine:
        return Machine(
            id=row.id,
            name=row.name,
            type=row.type,
            capabilities=MachineCapabilities(**row.capabilities),
            manufacturer=row.manufacturer,
            description=row.description,
            notes=row.notes,
        )

    async def get_machine(self, machine_id: str) -> Optional[Machine]:
        result = await self.db.execute(
            select(MachineModel).where(
                and_(MachineModel.id == machine_id, MachineModel.is_deleted == False)
            )
        )
        row = result.scalar_one_or_none()
        return self._row_to_schema(row) if row else None

    async def list_machines(
        self,
        machine_type: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[Machine]:
        query = select(MachineModel).where(MachineModel.is_deleted == False)
        if machine_type:
            query = query.where(MachineModel.type == machine_type)
        if search:
            query = query.where(MachineModel.name.ilike(f"%{search}%"))
        result = await self.db.execute(query.order_by(MachineModel.name))
        rows = result.scalars().all()
        return [self._row_to_schema(row) for row in rows]
