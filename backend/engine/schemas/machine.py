"""
Machine schema for machining decision engine.
"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class MachineType(str, Enum):
    """Machine type classification"""
    MILL = "mill"
    LATHE = "lathe"
    ROUTER = "router"
    DRILL = "drill"
    OTHER = "other"


class MachineCapabilities(BaseModel):
    """Machine performance capabilities"""
    # Spindle
    max_rpm: float = Field(..., gt=0, description="Maximum spindle RPM")
    min_rpm: float = Field(..., gt=0, description="Minimum spindle RPM")
    spindle_power_kw: Optional[float] = Field(None, gt=0, description="Spindle power (kW)")
    spindle_torque_nm: Optional[float] = Field(None, gt=0, description="Spindle torque (N·m)")
    
    # Feed rates
    max_feedrate_mm_per_min: float = Field(..., gt=0, description="Maximum feedrate (mm/min)")
    min_feedrate_mm_per_min: float = Field(..., gt=0, description="Minimum feedrate (mm/min)")
    
    # Rigidity and accuracy
    rigidity_factor: float = Field(default=1.0, ge=0, le=10, description="Machine rigidity factor (0-10)")
    accuracy_mm: Optional[float] = Field(None, gt=0, description="Positional accuracy (mm)")
    
    # Work envelope
    max_tool_diameter_mm: Optional[float] = Field(None, gt=0, description="Maximum tool diameter (mm)")
    max_depth_of_cut_mm: Optional[float] = Field(None, gt=0, description="Maximum depth of cut (mm)")


class Machine(BaseModel):
    """Machine definition for machining"""
    id: str
    name: str = Field(..., min_length=1, description="Machine name/model")
    type: MachineType
    capabilities: MachineCapabilities
    
    # Metadata
    manufacturer: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "generic-cnc-mill",
                "name": "Generic CNC Mill",
                "type": "mill",
                "capabilities": {
                    "max_rpm": 24000,
                    "min_rpm": 100,
                    "spindle_power_kw": 3.7,
                    "max_feedrate_mm_per_min": 10000,
                    "min_feedrate_mm_per_min": 1,
                    "rigidity_factor": 7.0,
                    "accuracy_mm": 0.01
                },
                "manufacturer": "Generic",
                "description": "Standard 3-axis CNC mill"
            }
        }

