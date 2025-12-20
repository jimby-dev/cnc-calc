"""
Base policy interface.
"""
from abc import ABC, abstractmethod
from pydantic import BaseModel

from ..schemas.policy import Policy
from ..schemas.recommendation import Recommendation
from ..constraints.feasible_ranges import FeasibleRanges


class PolicyResult(BaseModel):
    """Result from applying a policy"""
    rpm: float
    feedrate_mm_per_min: float
    confidence: float = 1.0
    reason: str = ""
    constraints_applied: list[str] = []


class PolicyBase(ABC):
    """Base class for policy implementations"""
    
    def __init__(self, policy: Policy):
        self.policy = policy
    
    @abstractmethod
    def apply(
        self,
        feasible_ranges: FeasibleRanges,
        **kwargs
    ) -> PolicyResult:
        """
        Apply the policy to generate a recommendation.
        
        Args:
            feasible_ranges: Feasible parameter ranges
            **kwargs: Additional context (tool, material, operation, etc.)
            
        Returns:
            Policy result with recommended parameters
        """
        pass
    
    def get_priority(self) -> int:
        """Get policy priority (lower = higher priority)"""
        return self.policy.priority

