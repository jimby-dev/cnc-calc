"""
Main decision engine pipeline.
Orchestrates the complete recommendation generation process.
"""
from typing import List, Optional

from .schemas import (
    EngineTool, Material, Machine, Operation, Workholding, Coolant,
    Policy, PolicyWeights, Recommendation, Signals
)
from .constraints.feasible_ranges import calculate_feasible_ranges, FeasibleRanges
from .signals.risk_assessment import calculate_risk_scores, assess_feasibility
from .policies import SafetyPolicy, ToolLifePolicy, TimePolicy, BalancedPolicy
from .arbitration.arbitrator import Arbitrator
from .explainability.tracer import DecisionTracer, Tracer
from .math.feeds_speeds import (
    calculate_surface_speed, calculate_chip_load, calculate_mrr,
    calculate_feed_per_revolution, calculate_sfm_from_rpm
)


class DecisionEngine:
    """Main decision engine for feeds & speeds recommendations"""
    
    def __init__(self):
        self.policy_factories = {
            "safety": SafetyPolicy,
            "tool_life": ToolLifePolicy,
            "time": TimePolicy,
            "balanced": BalancedPolicy,
        }
    
    def recommend(
        self,
        tool: EngineTool,
        material: Material,
        machine: Machine,
        operation: Operation,
        policies: List[Policy],
        weights: PolicyWeights,
        workholding: Optional[Workholding] = None,
        coolant: Optional[Coolant] = None
    ) -> Recommendation:
        """
        Generate a feeds & speeds recommendation.
        
        Pipeline:
        1) Normalize inputs
        2) Compute baseline feasible ranges
        3) Compute derived signals (risk scores)
        4) Apply policies (safety first, then optimization)
        5) Detect conflicts
        6) Arbitrate deterministically via weighted strategy
        7) Emit recommendation + explanation trace
        """
        tracer = DecisionTracer()
        
        # Step 1: Normalize inputs (already in correct format)
        # Step 2: Compute baseline feasible ranges
        feasible_ranges = calculate_feasible_ranges(
            tool, material, machine, coolant
        )
        Tracer.trace_feasible_ranges(tracer, feasible_ranges, tool.geometry.diameter)
        
        # Step 3: Apply policies (safety first, then optimization)
        policy_results = []
        policy_types = []
        
        # Sort policies by priority (lower = higher priority)
        sorted_policies = sorted(policies, key=lambda p: p.priority)
        
        for policy in sorted_policies:
            policy_class = self.policy_factories.get(policy.type.value)
            if not policy_class:
                continue
            
            policy_instance = policy_class(policy)
            result = policy_instance.apply(
                feasible_ranges=feasible_ranges,
                tool=tool,
                material=material,
                machine=machine,
                operation=operation,
                workholding=workholding,
                coolant=coolant
            )
            
            policy_results.append(result)
            policy_types.append(policy.type.value)
            
            Tracer.trace_policy_application(tracer, policy, result)
        
        # Step 4: Detect conflicts and arbitrate
        arbitrator = Arbitrator(weights)
        resolution = arbitrator.arbitrate(policy_results, policy_types)
        Tracer.trace_arbitration(tracer, resolution, policy_results)
        
        # Step 5: Compute derived signals (risk scores)
        risk_scores = calculate_risk_scores(
            tool, material, machine, operation,
            workholding, coolant, feasible_ranges,
            resolution.final_rpm, resolution.final_feedrate_mm_per_min
        )
        
        # Assess feasibility
        is_feasible, feasibility_confidence, warnings = assess_feasibility(
            feasible_ranges, resolution.final_rpm, resolution.final_feedrate_mm_per_min
        )
        
        # Determine dominant constraint
        dominant_constraint = None
        constraint_severity = 0.0
        if feasible_ranges.limiting_constraints:
            dominant_constraint = feasible_ranges.limiting_constraints[0]
            constraint_severity = 2.0  # Moderate severity
        
        # Build signals
        signals = Signals(
            risk_scores=risk_scores,
            dominant_constraint=dominant_constraint,
            constraint_severity=constraint_severity,
            is_feasible=is_feasible,
            feasibility_confidence=feasibility_confidence,
            warnings=warnings,
            errors=[] if is_feasible else ["Parameters outside feasible range"],
            overall_confidence=resolution.confidence * feasibility_confidence
        )
        
        # Step 6: Calculate derived values
        surface_speed_m_per_min = calculate_surface_speed(
            tool.geometry.diameter, resolution.final_rpm
        )
        surface_speed_sfm = calculate_sfm_from_rpm(
            tool.geometry.diameter, resolution.final_rpm
        )
        
        chip_load = None
        if tool.geometry.flute_count:
            chip_load = calculate_chip_load(
                resolution.final_feedrate_mm_per_min,
                resolution.final_rpm,
                tool.geometry.flute_count
            )
        
        feed_per_rev = calculate_feed_per_revolution(
            resolution.final_feedrate_mm_per_min,
            resolution.final_rpm
        )
        
        mrr = calculate_mrr(
            resolution.final_feedrate_mm_per_min,
            operation.depth_of_cut_mm,
            operation.width_of_cut_mm
        )
        
        # Step 7: Build recommendation
        recommendation = Recommendation(
            spindle_rpm=resolution.final_rpm,
            feedrate_mm_per_min=resolution.final_feedrate_mm_per_min,
            feedrate_mm_per_rev=feed_per_rev,
            chip_load_mm=chip_load,
            surface_speed_m_per_min=surface_speed_m_per_min,
            surface_speed_sfm=surface_speed_sfm,
            material_removal_rate_mm3_per_min=mrr,
            signals=signals,
            confidence=signals.overall_confidence,
            trace=tracer.build_trace()
        )
        
        return recommendation

