"""
Material schema for machining decision engine.
"""
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class MaterialCategory(str, Enum):
    """Material category classification"""
    ALUMINUM = "aluminum"
    STEEL = "steel"
    STAINLESS_STEEL = "stainless_steel"
    TITANIUM = "titanium"
    PLASTIC = "plastic"
    COMPOSITE = "composite"
    OTHER = "other"


class MaterialProperties(BaseModel):
    """Material physical and machining properties"""
    # Hardness (Brinell or Rockwell)
    hardness_hb: Optional[float] = Field(None, description="Brinell hardness")
    hardness_hrc: Optional[float] = Field(None, description="Rockwell C hardness")
    
    # Machinability (0-100 scale, higher = easier to machine)
    machinability_index: float = Field(..., ge=0, le=100, description="Machinability index (0-100)")
    
    # Thermal properties
    thermal_conductivity: Optional[float] = Field(None, description="Thermal conductivity (W/m·K)")
    melting_point: Optional[float] = Field(None, description="Melting point (°C)")
    
    # Cutting speed factors (SFM multipliers)
    base_sfm: float = Field(..., gt=0, description="Base surface feet per minute")
    sfm_range_min: float = Field(..., gt=0, description="Minimum recommended SFM")
    sfm_range_max: float = Field(..., gt=0, description="Maximum recommended SFM")
    
    # Chip formation
    chip_type: str = Field(default="continuous", description="Chip type (continuous, segmented, stringy)")
    work_hardening: bool = Field(default=False, description="Does material work-harden?")
    
    # Tool wear factors
    abrasiveness: float = Field(default=1.0, ge=0, le=10, description="Abrasiveness factor (0-10)")
    built_up_edge_tendency: float = Field(default=1.0, ge=0, le=10, description="BUE tendency (0-10)")


class Material(BaseModel):
    """Material definition for machining"""
    id: str
    name: str = Field(..., min_length=1, description="Material name (e.g., '6061-T6')")
    category: MaterialCategory
    properties: MaterialProperties
    
    # Metadata
    description: Optional[str] = None
    common_applications: list[str] = Field(default_factory=list)
    notes: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "6061-t6",
                "name": "6061-T6 Aluminum",
                "category": "aluminum",
                "properties": {
                    "hardness_hb": 95,
                    "machinability_index": 85,
                    "base_sfm": 500,
                    "sfm_range_min": 300,
                    "sfm_range_max": 800,
                    "chip_type": "continuous",
                    "work_hardening": False,
                    "abrasiveness": 0.5,
                    "built_up_edge_tendency": 0.3
                },
                "description": "Common aerospace and general purpose aluminum alloy",
                "common_applications": ["Aerospace", "Automotive", "General fabrication"]
            }
        }

