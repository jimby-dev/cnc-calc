"""
Tests for ValidationService
"""
import pytest
from services.validation_service import ValidationService
from schemas.tool import ToolResponse, ToolType
from datetime import datetime


@pytest.mark.asyncio
async def test_validate_valid_end_mill():
    """Test validation of a valid end mill"""
    service = ValidationService()
    
    tool = ToolResponse(
        id="test-id",
        name="Test Tool",
        vendor="Test Vendor",
        type=ToolType.END_MILL,
        geometry={
            "diameter": 10.0,
            "flute_length": 25.0,
            "overall_length": 50.0,
            "flute_count": 4,
            "helix_angle": 30.0,
            "length_of_cut": 20.0
        },
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    result = await service.validate_tool(tool)
    
    assert result.is_valid is True
    assert len(result.errors) == 0


@pytest.mark.asyncio
async def test_validate_invalid_end_mill():
    """Test validation of an invalid end mill (flute_length >= overall_length)"""
    service = ValidationService()
    
    tool = ToolResponse(
        id="test-id",
        name="Test Tool",
        vendor="Test Vendor",
        type=ToolType.END_MILL,
        geometry={
            "diameter": 10.0,
            "flute_length": 50.0,
            "overall_length": 50.0,  # Same as flute_length - invalid
            "flute_count": 4,
            "helix_angle": 30.0,
            "length_of_cut": 20.0
        },
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    result = await service.validate_tool(tool)
    
    assert result.is_valid is False
    assert len(result.errors) > 0
    assert any("flute length" in error.message.lower() for error in result.errors)

