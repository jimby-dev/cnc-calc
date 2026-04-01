"""
Material service: fetches MaterialModel rows and deserializes into engine Material objects.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import Optional, List

from models.material import Material as MaterialModel
from engine.schemas.material import Material, MaterialProperties
import structlog

logger = structlog.get_logger()


class MaterialService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _row_to_schema(self, row: MaterialModel) -> Material:
        return Material(
            id=row.id,
            name=row.name,
            category=row.category,
            properties=MaterialProperties(**row.properties),
            description=row.description,
            common_applications=row.common_applications or [],
            notes=row.notes,
        )

    async def get_material(self, material_id: str) -> Optional[Material]:
        result = await self.db.execute(
            select(MaterialModel).where(
                and_(MaterialModel.id == material_id, MaterialModel.is_deleted == False)
            )
        )
        row = result.scalar_one_or_none()
        return self._row_to_schema(row) if row else None

    async def list_materials(
        self,
        category: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[Material]:
        query = select(MaterialModel).where(MaterialModel.is_deleted == False)
        if category:
            query = query.where(MaterialModel.category == category)
        if search:
            query = query.where(MaterialModel.name.ilike(f"%{search}%"))
        result = await self.db.execute(query.order_by(MaterialModel.name))
        rows = result.scalars().all()
        return [self._row_to_schema(row) for row in rows]
