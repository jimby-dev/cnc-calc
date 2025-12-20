"""
Coolant schema for machining decision engine.
"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class CoolantType(str, Enum):
    """Coolant type classification"""
    FLOOD = "flood"
    MIST = "mist"
    AIR = "air"
    NONE = "none"
    THROUGH_SPINDLE = "through_spindle"
    EXTERNAL = "external"
    OTHER = "other"


class Coolant(BaseModel):
    """Coolant definition affecting machining parameters"""
    id: str
    name: str = Field(..., min_length=1, description="Coolant name/type")
    type: CoolantType
    
    # Performance factors
    heat_removal_factor: float = Field(
        default=1.0, 
        ge=0, 
        le=2, 
        description="Heat removal effectiveness (0-2, 1.0=standard, >1.0=better cooling)"
    )
    lubrication_factor: float = Field(
        default=1.0,
        ge=0,
        le=2,
        description="Lubrication effectiveness (0-2)"
    )
    chip_evacuation_factor: float = Field(
        default=1.0,
        ge=0,
        le=2,
        description="Chip evacuation effectiveness (0-2)"
    )
    
    # Speed/feed multipliers
    sfm_multiplier: float = Field(
        default=1.0,
        ge=0.5,
        le=2.0,
        description="SFM multiplier (typically 1.0-1.5 for flood, 0.8-1.0 for mist, 0.6-0.8 for air)"
    )
    feedrate_multiplier: float = Field(
        default=1.0,
        ge=0.5,
        le=1.5,
        description="Feedrate multiplier"
    )
    
    # Metadata
    description: Optional[str] = None
    notes: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "flood-coolant",
                "name": "Flood Coolant",
                "type": "flood",
                "heat_removal_factor": 1.5,
                "lubrication_factor": 1.3,
                "chip_evacuation_factor": 1.2,
                "sfm_multiplier": 1.2,
                "feedrate_multiplier": 1.1,
                "description": "Standard flood coolant system"
            }
        }

