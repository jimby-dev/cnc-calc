"""
Policy schema for machining decision engine.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from enum import Enum


class PolicyType(str, Enum):
    """Policy type classification"""
    SAFETY = "safety"
    TOOL_LIFE = "tool_life"
    TIME = "time"
    SURFACE_FINISH = "surface_finish"
    BALANCED = "balanced"
    CUSTOM = "custom"


class PolicyWeights(BaseModel):
    """Weights for policy arbitration"""
    tool_life: float = Field(default=0.33, ge=0, le=1, description="Tool life optimization weight")
    time: float = Field(default=0.33, ge=0, le=1, description="Time optimization weight")
    safety: float = Field(default=0.34, ge=0, le=1, description="Safety weight (always applied)")
    
    def normalize(self) -> "PolicyWeights":
        """Normalize weights to sum to 1.0"""
        total = self.tool_life + self.time + self.safety
        if total == 0:
            return PolicyWeights(tool_life=0.33, time=0.33, safety=0.34)
        return PolicyWeights(
            tool_life=self.tool_life / total,
            time=self.time / total,
            safety=self.safety / total
        )


class Policy(BaseModel):
    """Policy definition for machining optimization"""
    id: str
    name: str = Field(..., min_length=1, description="Policy name")
    type: PolicyType
    weights: PolicyWeights
    
    # Policy rules (JSON-serializable constraints)
    rules: Dict[str, Any] = Field(default_factory=dict, description="Policy-specific rules")
    
    # Priority (lower = higher priority, safety always first)
    priority: int = Field(default=100, ge=0, description="Policy priority (lower = higher priority)")
    
    # Metadata
    description: Optional[str] = None
    notes: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "safety-first",
                "name": "Safety First",
                "type": "safety",
                "weights": {
                    "tool_life": 0.0,
                    "time": 0.0,
                    "safety": 1.0
                },
                "priority": 1,
                "description": "Maximum safety, conservative parameters"
            }
        }

