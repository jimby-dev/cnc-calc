from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload
from typing import List, Optional
import uuid
from datetime import datetime

from models.tool import Tool
from schemas.tool import ToolCreate, ToolUpdate, ToolResponse, ToolListResponse
import structlog

logger = structlog.get_logger()

class ToolService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_tool(self, tool_data: ToolCreate) -> ToolResponse:
        """Create a new tool"""
        tool_id = str(uuid.uuid4())
        
        tool = Tool(
            id=tool_id,
            name=tool_data.name,
            vendor=tool_data.vendor,
            type=tool_data.type.value,
            geometry=tool_data.geometry,
            limits=tool_data.limits.dict() if tool_data.limits else None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        self.db.add(tool)
        await self.db.commit()
        await self.db.refresh(tool)
        
        return ToolResponse.from_orm(tool)
    
    async def get_tool(self, tool_id: str) -> Optional[ToolResponse]:
        """Get a tool by ID"""
        result = await self.db.execute(
            select(Tool).where(
                and_(Tool.id == tool_id, Tool.is_deleted == False)
            )
        )
        tool = result.scalar_one_or_none()
        
        if tool:
            return ToolResponse.from_orm(tool)
        return None
    
    async def list_tools(
        self,
        page: int = 1,
        size: int = 20,
        search: Optional[str] = None,
        tool_type: Optional[str] = None,
        vendor: Optional[str] = None
    ) -> ToolListResponse:
        """List tools with pagination and filtering"""
        
        # Build query
        query = select(Tool).where(Tool.is_deleted == False)
        
        # Apply filters
        if search:
            search_filter = or_(
                Tool.name.ilike(f"%{search}%"),
                Tool.vendor.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
        
        if tool_type:
            query = query.where(Tool.type == tool_type)
            
        if vendor:
            query = query.where(Tool.vendor.ilike(f"%{vendor}%"))
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        offset = (page - 1) * size
        query = query.offset(offset).limit(size).order_by(Tool.created_at.desc())
        
        # Execute query
        result = await self.db.execute(query)
        tools = result.scalars().all()
        
        # Convert to response models
        tool_responses = [ToolResponse.from_orm(tool) for tool in tools]
        
        return ToolListResponse(
            tools=tool_responses,
            total=total,
            page=page,
            size=size
        )
    
    async def update_tool(self, tool_id: str, tool_data: ToolUpdate) -> Optional[ToolResponse]:
        """Update a tool"""
        result = await self.db.execute(
            select(Tool).where(
                and_(Tool.id == tool_id, Tool.is_deleted == False)
            )
        )
        tool = result.scalar_one_or_none()
        
        if not tool:
            return None
        
        # Update fields
        update_data = tool_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == "limits" and value is not None:
                setattr(tool, field, value.dict())
            else:
                setattr(tool, field, value)
        
        tool.updated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(tool)
        
        return ToolResponse.from_orm(tool)
    
    async def delete_tool(self, tool_id: str) -> bool:
        """Soft delete a tool"""
        result = await self.db.execute(
            select(Tool).where(
                and_(Tool.id == tool_id, Tool.is_deleted == False)
            )
        )
        tool = result.scalar_one_or_none()
        
        if not tool:
            return False
        
        tool.is_deleted = True
        tool.updated_at = datetime.utcnow()
        
        await self.db.commit()
        return True
    
    async def get_tool_by_name_and_vendor(self, name: str, vendor: str) -> Optional[ToolResponse]:
        """Get a tool by name and vendor (for duplicate checking)"""
        result = await self.db.execute(
            select(Tool).where(
                and_(
                    Tool.name == name,
                    Tool.vendor == vendor,
                    Tool.is_deleted == False
                )
            )
        )
        tool = result.scalar_one_or_none()
        
        if tool:
            return ToolResponse.from_orm(tool)
        return None
