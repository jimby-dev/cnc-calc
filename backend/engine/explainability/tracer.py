"""
Decision trace generation for explainability.
"""
from typing import List, Optional
from datetime import datetime

from ..schemas.recommendation import RecommendationTrace, DecisionNode
from ..schemas.policy import Policy
from ..policies.base import PolicyResult
from ..arbitration.arbitrator import ConflictResolution


class DecisionTracer:
    """Traces decision-making process for explainability"""
    
    def __init__(self):
        self.nodes: List[DecisionNode] = []
        self.conflicts: List[str] = []
        self.arbitration_strategy: Optional[str] = None
    
    def add_node(
        self,
        step: str,
        input_value: any,
        output_value: any,
        reason: str,
        policy_applied: Optional[str] = None,
        confidence: float = 1.0
    ):
        """Add a decision node to the trace"""
        self.nodes.append(DecisionNode(
            step=step,
            input_value=input_value,
            output_value=output_value,
            reason=reason,
            policy_applied=policy_applied,
            confidence=confidence
        ))
    
    def add_conflict(self, conflict: str):
        """Add a detected conflict"""
        self.conflicts.append(conflict)
    
    def set_arbitration_strategy(self, strategy: str):
        """Set the arbitration strategy used"""
        self.arbitration_strategy = strategy
    
    def build_trace(self) -> RecommendationTrace:
        """Build the final trace"""
        return RecommendationTrace(
            nodes=self.nodes,
            conflicts_detected=self.conflicts,
            arbitration_strategy=self.arbitration_strategy,
            total_steps=len(self.nodes)
        )


class Tracer:
    """Static tracer utilities"""
    
    @staticmethod
    def trace_feasible_ranges(
        tracer: DecisionTracer,
        feasible_ranges,
        tool_diameter: float
    ):
        """Trace feasible range calculation"""
        tracer.add_node(
            step="calculate_feasible_ranges",
            input_value={
                "tool_diameter_mm": tool_diameter,
                "rpm_range": (feasible_ranges.rpm_min, feasible_ranges.rpm_max),
                "sfm_range": (feasible_ranges.sfm_min, feasible_ranges.sfm_max)
            },
            output_value={
                "rpm_min": feasible_ranges.rpm_min,
                "rpm_max": feasible_ranges.rpm_max,
                "feedrate_min": feasible_ranges.feedrate_min_mm_per_min,
                "feedrate_max": feasible_ranges.feedrate_max_mm_per_min
            },
            reason=f"Calculated feasible ranges from tool, material, and machine constraints. Limiting constraints: {', '.join(feasible_ranges.limiting_constraints)}",
            confidence=0.95
        )
    
    @staticmethod
    def trace_policy_application(
        tracer: DecisionTracer,
        policy: Policy,
        policy_result: PolicyResult
    ):
        """Trace policy application"""
        tracer.add_node(
            step=f"apply_policy_{policy.type.value}",
            input_value={
                "policy_type": policy.type.value,
                "policy_name": policy.name,
                "feasible_ranges": "available"
            },
            output_value={
                "rpm": policy_result.rpm,
                "feedrate_mm_per_min": policy_result.feedrate_mm_per_min
            },
            reason=policy_result.reason,
            policy_applied=policy.type.value,
            confidence=policy_result.confidence
        )
    
    @staticmethod
    def trace_arbitration(
        tracer: DecisionTracer,
        resolution: ConflictResolution,
        policy_results: List[PolicyResult]
    ):
        """Trace arbitration process"""
        if resolution.conflicts_detected:
            for conflict in resolution.conflicts_detected:
                tracer.add_conflict(conflict)
        
        tracer.set_arbitration_strategy(resolution.arbitration_strategy)
        
        tracer.add_node(
            step="arbitrate_policies",
            input_value={
                "policy_results": [
                    {"rpm": r.rpm, "feedrate": r.feedrate_mm_per_min}
                    for r in policy_results
                ],
                "conflicts": resolution.conflicts_detected
            },
            output_value={
                "final_rpm": resolution.final_rpm,
                "final_feedrate_mm_per_min": resolution.final_feedrate_mm_per_min
            },
            reason=f"Arbitrated between {len(policy_results)} policies using {resolution.arbitration_strategy}",
            confidence=resolution.confidence
        )

