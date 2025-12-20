"""
Signals schema for risk assessment and constraint detection.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class ConstraintType(str, Enum):
    """Type of constraint limiting the recommendation"""
    SPINDLE_RPM = "spindle_rpm"
    FEEDRATE = "feedrate"
    DEPTH_OF_CUT = "depth_of_cut"
    WIDTH_OF_CUT = "width_of_cut"
    CHIP_LOAD = "chip_load"
    TOOL_WEAR = "tool_wear"
    SURFACE_FINISH = "surface_finish"
    CHATTER = "chatter"
    POWER = "power"
    TORQUE = "torque"
    RIGIDITY = "rigidity"
    COOLANT = "coolant"
    MATERIAL = "material"
    OTHER = "other"


class RiskScore(BaseModel):
    """Risk assessment for a specific aspect"""
    category: str = Field(..., description="Risk category")
    score: float = Field(..., ge=0, le=10, description="Risk score (0-10, 0=safe, 10=critical)")
    confidence: float = Field(..., ge=0, le=1, description="Confidence in risk assessment (0-1)")
    reason: str = Field(..., description="Explanation of risk")
    
    class Config:
        json_schema_extra = {
            "example": {
                "category": "tool_wear",
                "score": 3.5,
                "confidence": 0.85,
                "reason": "Moderate tool wear expected due to material abrasiveness"
            }
        }


class Signals(BaseModel):
    """Derived signals and risk assessments"""
    # Risk scores
    risk_scores: List[RiskScore] = Field(default_factory=list)
    
    # Dominant constraint (what's limiting the recommendation)
    dominant_constraint: Optional[ConstraintType] = None
    constraint_severity: float = Field(default=0.0, ge=0, le=10, description="Severity of dominant constraint")
    
    # Feasibility indicators
    is_feasible: bool = Field(default=True, description="Is the scenario feasible?")
    feasibility_confidence: float = Field(default=1.0, ge=0, le=1, description="Confidence in feasibility")
    
    # Warning flags
    warnings: List[str] = Field(default_factory=list, description="Warning messages")
    errors: List[str] = Field(default_factory=list, description="Error messages (blocking)")
    
    # Confidence metrics
    overall_confidence: float = Field(default=1.0, ge=0, le=1, description="Overall confidence in recommendation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "risk_scores": [
                    {
                        "category": "tool_wear",
                        "score": 2.0,
                        "confidence": 0.9,
                        "reason": "Low tool wear expected"
                    }
                ],
                "dominant_constraint": "spindle_rpm",
                "constraint_severity": 1.5,
                "is_feasible": True,
                "feasibility_confidence": 0.95,
                "warnings": [],
                "errors": [],
                "overall_confidence": 0.92
            }
        }

