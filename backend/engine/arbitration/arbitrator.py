"""
Arbitration system for resolving conflicts between multiple policies.
"""
from typing import List
from pydantic import BaseModel

from ..schemas.policy import Policy, PolicyWeights
from ..policies.base import PolicyResult


class ConflictResolution(BaseModel):
    """Result of conflict resolution"""
    final_rpm: float
    final_feedrate_mm_per_min: float
    conflicts_detected: List[str] = []
    arbitration_strategy: str = ""
    confidence: float = 1.0


class Arbitrator:
    """Arbitrates between multiple policy results"""
    
    def __init__(self, weights: PolicyWeights):
        self.weights = weights.normalize()
    
    def arbitrate(
        self,
        policy_results: List[PolicyResult],
        policy_types: List[str]
    ) -> ConflictResolution:
        """
        Arbitrate between multiple policy results using weighted strategy.
        
        Args:
            policy_results: List of policy results to arbitrate
            policy_types: List of policy type names (e.g., ["safety", "tool_life", "time"])
            
        Returns:
            Final arbitrated recommendation
        """
        if not policy_results:
            raise ValueError("No policy results to arbitrate")
        
        if len(policy_results) == 1:
            # Single policy, no arbitration needed
            result = policy_results[0]
            return ConflictResolution(
                final_rpm=result.rpm,
                final_feedrate_mm_per_min=result.feedrate_mm_per_min,
                conflicts_detected=[],
                arbitration_strategy="single_policy",
                confidence=result.confidence
            )
        
        # Detect conflicts
        conflicts = self._detect_conflicts(policy_results)
        
        # Weighted average arbitration
        final_rpm, final_feedrate = self._weighted_average(
            policy_results, policy_types
        )
        
        # Calculate overall confidence (weighted average)
        confidence = sum(r.confidence for r in policy_results) / len(policy_results)
        
        return ConflictResolution(
            final_rpm=final_rpm,
            final_feedrate_mm_per_min=final_feedrate,
            conflicts_detected=conflicts,
            arbitration_strategy="weighted_average",
            confidence=confidence
        )
    
    def _detect_conflicts(self, results: List[PolicyResult]) -> List[str]:
        """Detect conflicts between policy results"""
        conflicts = []
        
        # Check RPM conflicts (if spread is large)
        rpms = [r.rpm for r in results]
        rpm_spread = max(rpms) - min(rpms)
        rpm_range = max(rpms) - min(rpms)
        if rpm_range > 0 and rpm_spread / max(rpms) > 0.3:  # >30% spread
            conflicts.append("RPM conflict: policies recommend significantly different RPM values")
        
        # Check feedrate conflicts
        feedrates = [r.feedrate_mm_per_min for r in results]
        feedrate_spread = max(feedrates) - min(feedrates)
        if max(feedrates) > 0 and feedrate_spread / max(feedrates) > 0.4:  # >40% spread
            conflicts.append("Feedrate conflict: policies recommend significantly different feedrates")
        
        return conflicts
    
    def _weighted_average(
        self,
        results: List[PolicyResult],
        policy_types: List[str]
    ) -> tuple[float, float]:
        """Calculate weighted average of policy results"""
        # Map policy types to weights
        weight_map = {
            "safety": self.weights.safety,
            "tool_life": self.weights.tool_life,
            "time": self.weights.time,
            "balanced": (self.weights.tool_life + self.weights.time) / 2,  # Average of tool_life and time
        }
        
        total_weight = 0.0
        weighted_rpm = 0.0
        weighted_feedrate = 0.0
        
        for result, policy_type in zip(results, policy_types):
            weight = weight_map.get(policy_type, 0.33)  # Default weight
            total_weight += weight
            weighted_rpm += result.rpm * weight
            weighted_feedrate += result.feedrate_mm_per_min * weight
        
        if total_weight == 0:
            # Fallback: simple average
            return (
                sum(r.rpm for r in results) / len(results),
                sum(r.feedrate_mm_per_min for r in results) / len(results)
            )
        
        return (
            weighted_rpm / total_weight,
            weighted_feedrate / total_weight
        )

