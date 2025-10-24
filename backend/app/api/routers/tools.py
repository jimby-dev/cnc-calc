from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import List, Optional
import uuid
from datetime import datetime

from app.core.database import get_db
from models.tool import Tool, ToolExport
from schemas.tool import (
    ToolCreate, ToolUpdate, ToolResponse, ToolListResponse,
    ExportRequest, ExportResponse, ValidationResponse, ValidationError
)
from services.tool_service import ToolService
from services.export_service import ExportService
from services.validation_service import ValidationService
import structlog

logger = structlog.get_logger()
router = APIRouter()

@router.get("/", response_model=ToolListResponse)
async def list_tools(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(20, ge=1, le=100, description="Page size"),
    search: Optional[str] = Query(None, description="Search term"),
    tool_type: Optional[str] = Query(None, description="Filter by tool type"),
    vendor: Optional[str] = Query(None, description="Filter by vendor"),
    db: AsyncSession = Depends(get_db)
):
    """List all tools with pagination and filtering"""
    try:
        tool_service = ToolService(db)
        result = await tool_service.list_tools(
            page=page,
            size=size,
            search=search,
            tool_type=tool_type,
            vendor=vendor
        )
        
        logger.info("Tools listed", count=len(result.tools), page=page, size=size)
        return result
        
    except Exception as e:
        logger.error("Failed to list tools", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to list tools")

@router.post("/", response_model=ToolResponse)
async def create_tool(
    tool_data: ToolCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new tool"""
    try:
        tool_service = ToolService(db)
        tool = await tool_service.create_tool(tool_data)
        
        logger.info("Tool created", tool_id=tool.id, name=tool.name)
        return tool
        
    except Exception as e:
        logger.error("Failed to create tool", error=str(e))
        raise HTTPException(status_code=400, detail="Failed to create tool")

@router.get("/{tool_id}", response_model=ToolResponse)
async def get_tool(
    tool_id: str = Path(..., description="Tool ID"),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific tool by ID"""
    try:
        tool_service = ToolService(db)
        tool = await tool_service.get_tool(tool_id)
        
        if not tool:
            raise HTTPException(status_code=404, detail="Tool not found")
            
        logger.info("Tool retrieved", tool_id=tool_id)
        return tool
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get tool", tool_id=tool_id, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get tool")

@router.put("/{tool_id}", response_model=ToolResponse)
async def update_tool(
    tool_id: str = Path(..., description="Tool ID"),
    tool_data: ToolUpdate = ...,
    db: AsyncSession = Depends(get_db)
):
    """Update a tool"""
    try:
        tool_service = ToolService(db)
        tool = await tool_service.update_tool(tool_id, tool_data)
        
        if not tool:
            raise HTTPException(status_code=404, detail="Tool not found")
            
        logger.info("Tool updated", tool_id=tool_id)
        return tool
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update tool", tool_id=tool_id, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to update tool")

@router.delete("/{tool_id}")
async def delete_tool(
    tool_id: str = Path(..., description="Tool ID"),
    db: AsyncSession = Depends(get_db)
):
    """Delete a tool (soft delete)"""
    try:
        tool_service = ToolService(db)
        success = await tool_service.delete_tool(tool_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Tool not found")
            
        logger.info("Tool deleted", tool_id=tool_id)
        return {"message": "Tool deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to delete tool", tool_id=tool_id, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to delete tool")

@router.post("/{tool_id}/validate", response_model=ValidationResponse)
async def validate_tool(
    tool_id: str = Path(..., description="Tool ID"),
    db: AsyncSession = Depends(get_db)
):
    """Validate a tool for Fusion 360 compatibility"""
    try:
        tool_service = ToolService(db)
        tool = await tool_service.get_tool(tool_id)
        
        if not tool:
            raise HTTPException(status_code=404, detail="Tool not found")
            
        validation_service = ValidationService()
        result = await validation_service.validate_tool(tool)
        
        logger.info("Tool validated", tool_id=tool_id, is_valid=result.is_valid)
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to validate tool", tool_id=tool_id, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to validate tool")

@router.post("/{tool_id}/export", response_model=ExportResponse)
async def export_tool(
    tool_id: str = Path(..., description="Tool ID"),
    export_request: ExportRequest = ...,
    db: AsyncSession = Depends(get_db)
):
    """Export a tool in the specified format"""
    try:
        tool_service = ToolService(db)
        tool = await tool_service.get_tool(tool_id)
        
        if not tool:
            raise HTTPException(status_code=404, detail="Tool not found")
            
        export_service = ExportService(db)
        export_result = await export_service.export_tool(tool, export_request)
        
        logger.info("Tool exported", tool_id=tool_id, format=export_request.format)
        return export_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to export tool", tool_id=tool_id, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to export tool")

@router.get("/{tool_id}/export/{export_id}/download")
async def download_export(
    tool_id: str = Path(..., description="Tool ID"),
    export_id: str = Path(..., description="Export ID"),
    db: AsyncSession = Depends(get_db)
):
    """Download an exported tool file"""
    try:
        export_service = ExportService(db)
        export_data = await export_service.get_export(export_id)
        
        if not export_data:
            raise HTTPException(status_code=404, detail="Export not found")
            
        logger.info("Export downloaded", export_id=export_id)
        return export_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to download export", export_id=export_id, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to download export")
