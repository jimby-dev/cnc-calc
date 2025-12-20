"""
Tests for ToolService
"""
import pytest
from datetime import datetime
from services.tool_service import ToolService
from schemas.tool import ToolCreate, ToolType, EndMillGeometry


@pytest.mark.asyncio
async def test_create_tool(db_session):
    """Test creating a tool"""
    service = ToolService(db_session)
    
    geometry = EndMillGeometry(
        diameter=10.0,
        flute_length=25.0,
        overall_length=50.0,
        flute_count=4,
        helix_angle=30.0,
        length_of_cut=20.0,
        corner_radius=0.5
    )
    
    tool_data = ToolCreate(
        name="Test End Mill",
        vendor="Test Vendor",
        type=ToolType.END_MILL,
        geometry=geometry.dict()
    )
    
    tool = await service.create_tool(tool_data)
    
    assert tool.id is not None
    assert tool.name == "Test End Mill"
    assert tool.vendor == "Test Vendor"
    assert tool.type == ToolType.END_MILL.value


@pytest.mark.asyncio
async def test_get_tool(db_session):
    """Test getting a tool by ID"""
    service = ToolService(db_session)
    
    geometry = EndMillGeometry(
        diameter=10.0,
        flute_length=25.0,
        overall_length=50.0,
        flute_count=4,
        helix_angle=30.0,
        length_of_cut=20.0
    )
    
    tool_data = ToolCreate(
        name="Test Tool",
        vendor="Test Vendor",
        type=ToolType.END_MILL,
        geometry=geometry.dict()
    )
    
    created = await service.create_tool(tool_data)
    retrieved = await service.get_tool(created.id)
    
    assert retrieved is not None
    assert retrieved.id == created.id
    assert retrieved.name == "Test Tool"


@pytest.mark.asyncio
async def test_list_tools(db_session):
    """Test listing tools with pagination"""
    service = ToolService(db_session)
    
    # Create multiple tools
    for i in range(5):
        geometry = EndMillGeometry(
            diameter=10.0 + i,
            flute_length=25.0,
            overall_length=50.0,
            flute_count=4,
            helix_angle=30.0,
            length_of_cut=20.0
        )
        
        tool_data = ToolCreate(
            name=f"Tool {i}",
            vendor="Test Vendor",
            type=ToolType.END_MILL,
            geometry=geometry.dict()
        )
        
        await service.create_tool(tool_data)
    
    result = await service.list_tools(page=1, size=3)
    
    assert len(result.tools) == 3
    assert result.total == 5
    assert result.page == 1
    assert result.size == 3

