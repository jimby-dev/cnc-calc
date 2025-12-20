"""
Tool schema for engine use (adapted from existing tool schema).
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from enum import Enum


class ToolType(str, Enum):
    """Tool type classification"""
    END_MILL = "End Mill"
    BALL_END_MILL = "Ball End Mill"
    CHAMFER = "Chamfer"
    DRILL = "Drill"
    REAMER = "Reamer"
    THREAD_MILL = "Thread Mill"


class ToolGeometry(BaseModel):
    """Tool geometry parameters (all in mm)"""
    diameter: float = Field(..., gt=0, description="Tool diameter (mm)")
    flute_length: float = Field(..., gt=0, description="Flute length (mm)")
    overall_length: float = Field(..., gt=0, description="Overall length (mm)")
    
    # Tool-specific geometry
    flute_count: Optional[int] = Field(None, gt=0, description="Number of flutes")
    helix_angle: Optional[float] = Field(None, ge=0, le=90, description="Helix angle (degrees)")
    corner_radius: Optional[float] = Field(None, ge=0, description="Corner radius (mm)")
    tip_radius: Optional[float] = Field(None, ge=0, description="Tip radius (mm)")
    
    # Additional geometry (flexible for different tool types)
    extra: Dict[str, Any] = Field(default_factory=dict, description="Additional tool-specific geometry")


class ToolLimits(BaseModel):
    """Tool performance limits"""
    max_sfm: Optional[float] = Field(None, gt=0, description="Maximum SFM")
    max_rpm: Optional[float] = Field(None, gt=0, description="Maximum RPM")
    max_feedrate_mm_per_min: Optional[float] = Field(None, gt=0, description="Maximum feedrate (mm/min)")
    max_chip_load_mm: Optional[float] = Field(None, gt=0, description="Maximum chip load (mm)")
    max_depth_of_cut_mm: Optional[float] = Field(None, gt=0, description="Maximum DOC (mm)")


class EngineTool(BaseModel):
    """Tool definition for engine use"""
    id: str
    name: str
    vendor: Optional[str] = None
    type: ToolType
    geometry: ToolGeometry
    limits: Optional[ToolLimits] = None
    
    # Tool-specific multipliers/factors
    sfm_multiplier: float = Field(default=1.0, ge=0.5, le=2.0, description="SFM adjustment factor")
    feedrate_multiplier: float = Field(default=1.0, ge=0.5, le=2.0, description="Feedrate adjustment factor")
    
    # Metadata
    description: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "helical-endmill-6mm",
                "name": "6mm End Mill",
                "vendor": "Helical",
                "type": "End Mill",
                "geometry": {
                    "diameter": 6.0,
                    "flute_length": 12.0,
                    "overall_length": 50.0,
                    "flute_count": 4,
                    "helix_angle": 30.0,
                    "corner_radius": 0.5
                },
                "limits": {
                    "max_sfm": 800,
                    "max_rpm": 24000
                },
                "sfm_multiplier": 1.0,
                "feedrate_multiplier": 1.0
            }
        }

