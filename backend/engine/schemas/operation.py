"""
Operation schema for machining decision engine.
"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class OperationType(str, Enum):
    """Operation type classification"""
    ROUGHING = "roughing"
    FINISHING = "finishing"
    SEMI_FINISH = "semi_finish"
    DRILLING = "drilling"
    TAPPING = "tapping"
    THREAD_MILLING = "thread_milling"
    POCKETING = "pocketing"
    FACING = "facing"
    CONTOURING = "contouring"
    SLOTTING = "sloting"
    OTHER = "other"


class Operation(BaseModel):
    """Operation parameters for machining"""
    id: Optional[str] = None
    type: OperationType
    
    # Cutting parameters (in mm, as per engine requirement)
    depth_of_cut_mm: float = Field(..., gt=0, description="Depth of cut (mm)")
    width_of_cut_mm: float = Field(..., gt=0, description="Width of cut / stepover (mm)")
    
    # Engagement
    radial_engagement_percent: Optional[float] = Field(
        None, 
        ge=0, 
        le=100, 
        description="Radial engagement percentage (0-100)"
    )
    axial_engagement_percent: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        description="Axial engagement percentage (0-100)"
    )
    
    # Surface finish requirements
    surface_finish_ra_um: Optional[float] = Field(
        None,
        gt=0,
        description="Required surface finish Ra (micrometers)"
    )
    
    # Metadata
    description: Optional[str] = None
    notes: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "type": "roughing",
                "depth_of_cut_mm": 2.0,
                "width_of_cut_mm": 5.0,
                "radial_engagement_percent": 50.0,
                "description": "Roughing operation"
            }
        }

