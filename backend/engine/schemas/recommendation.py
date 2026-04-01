"""
Recommendation schema for decision engine output.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from .signals import Signals


class DecisionNode(BaseModel):
    """A node in the decision trace explaining why a value was chosen"""
    step: str = Field(..., description="Decision step name")
    input_value: Optional[Any] = Field(None, description="Input value considered")
    output_value: Any = Field(..., description="Output value chosen")
    reason: str = Field(..., description="Explanation of decision")
    policy_applied: Optional[str] = Field(None, description="Policy that influenced this decision")
    confidence: float = Field(default=1.0, ge=0, le=1, description="Confidence in this decision")
    
    class Config:
        json_schema_extra = {
            "example": {
                "step": "calculate_sfm",
                "input_value": {"material_base_sfm": 500, "tool_factor": 1.2},
                "output_value": 600,
                "reason": "Applied material base SFM with tool-specific multiplier",
                "policy_applied": "balanced",
                "confidence": 0.95
            }
        }


class RecommendationTrace(BaseModel):
    """Complete trace of decision-making process"""
    nodes: List[DecisionNode] = Field(default_factory=list, description="Decision nodes in order")
    conflicts_detected: List[str] = Field(default_factory=list, description="Policy conflicts detected")
    arbitration_strategy: Optional[str] = Field(None, description="Arbitration strategy used")
    total_steps: int = Field(default=0, description="Total number of decision steps")


class Recommendation(BaseModel):
    """Final recommendation from the decision engine"""
    # Core recommendation values (all in mm or mm/min as per engine requirement)
    spindle_rpm: float = Field(..., gt=0, description="Recommended spindle RPM")
    feedrate_mm_per_min: float = Field(..., gt=0, description="Recommended feedrate (mm/min)")
    feedrate_mm_per_rev: Optional[float] = Field(None, gt=0, description="Feed per revolution (mm/rev)")
    chip_load_mm: Optional[float] = Field(None, gt=0, description="Chip load (mm)")
    
    # Derived values
    surface_speed_m_per_min: float = Field(..., gt=0, description="Surface speed (m/min)")
    surface_speed_sfm: Optional[float] = Field(None, gt=0, description="Surface speed (SFM)")
    material_removal_rate_mm3_per_min: Optional[float] = Field(None, gt=0, description="MRR (mm³/min)")
    
    # Confidence and signals
    signals: Signals = Field(..., description="Risk signals and constraints")
    confidence: float = Field(..., ge=0, le=1, description="Overall confidence (0-1)")
    
    # Explanation
    trace: RecommendationTrace = Field(..., description="Decision trace explaining the recommendation")
    
    # Metadata
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    scenario_id: Optional[str] = Field(None, description="Optional scenario identifier")
    
    class Config:
        json_schema_extra = {
            "example": {
                "spindle_rpm": 12000,
                "feedrate_mm_per_min": 2400,
                "feedrate_mm_per_rev": 0.2,
                "chip_load_mm": 0.1,
                "surface_speed_m_per_min": 150,
                "surface_speed_sfm": 492,
                "material_removal_rate_mm3_per_min": 24000,
                "signals": {
                    "dominant_constraint": "spindle_rpm",
                    "is_feasible": True,
                    "overall_confidence": 0.92
                },
                "confidence": 0.92,
                "trace": {
                    "nodes": [],
                    "total_steps": 0
                }
            }
        }

