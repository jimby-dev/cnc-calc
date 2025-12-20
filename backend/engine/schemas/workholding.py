"""
Workholding schema for machining decision engine.
"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class WorkholdingType(str, Enum):
    """Workholding type classification"""
    VISE = "vise"
    FIXTURE = "fixture"
    CHUCK = "chuck"
    FACE_PLATE = "face_plate"
    MAGNETIC = "magnetic"
    VACUUM = "vacuum"
    CUSTOM = "custom"
    OTHER = "other"


class Workholding(BaseModel):
    """Workholding definition affecting machining parameters"""
    id: str
    name: str = Field(..., min_length=1, description="Workholding name/type")
    type: WorkholdingType
    
    # Rigidity and stability factors
    rigidity_factor: float = Field(default=1.0, ge=0, le=10, description="Workholding rigidity (0-10)")
    stability_factor: float = Field(default=1.0, ge=0, le=10, description="Stability factor (0-10)")
    
    # Constraints on machining
    max_depth_of_cut_reduction: float = Field(
        default=0.0, 
        ge=0, 
        le=1, 
        description="Reduction factor for max DOC (0-1, 0=no reduction, 1=100% reduction)"
    )
    max_feedrate_reduction: float = Field(
        default=0.0,
        ge=0,
        le=1,
        description="Reduction factor for max feedrate (0-1)"
    )
    
    # Metadata
    description: Optional[str] = None
    notes: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "standard-vise",
                "name": "Standard Vise",
                "type": "vise",
                "rigidity_factor": 7.0,
                "stability_factor": 8.0,
                "max_depth_of_cut_reduction": 0.0,
                "max_feedrate_reduction": 0.0,
                "description": "Standard machine vise with good rigidity"
            }
        }

