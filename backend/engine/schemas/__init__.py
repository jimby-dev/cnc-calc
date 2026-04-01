"""
Core domain schemas for the machining decision engine.
"""

from .material import Material, MaterialProperties
from .machine import Machine, MachineCapabilities
from .workholding import Workholding, WorkholdingType
from .coolant import Coolant, CoolantType
from .operation import Operation, OperationType
from .policy import Policy, PolicyType, PolicyWeights
from .signals import Signals, RiskScore, ConstraintType
from .recommendation import Recommendation, RecommendationTrace, DecisionNode
from .tool import EngineTool  # Re-export tool schema for engine use

__all__ = [
    "Material",
    "MaterialProperties",
    "Machine",
    "MachineCapabilities",
    "Workholding",
    "WorkholdingType",
    "Coolant",
    "CoolantType",
    "Operation",
    "OperationType",
    "Policy",
    "PolicyType",
    "PolicyWeights",
    "Signals",
    "RiskScore",
    "ConstraintType",
    "Recommendation",
    "RecommendationTrace",
    "DecisionNode",
    "EngineTool",
]

