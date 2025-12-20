"""
Risk assessment and signal computation.
"""
from typing import List, Optional

from ..schemas.signals import Signals, RiskScore, ConstraintType
from ..schemas.tool import EngineTool
from ..schemas.material import Material
from ..schemas.machine import Machine
from ..schemas.operation import Operation
from ..schemas.workholding import Workholding
from ..schemas.coolant import Coolant
from ..constraints.feasible_ranges import FeasibleRanges
from ..math.feeds_speeds import calculate_sfm_from_rpm, calculate_chip_load


def calculate_risk_scores(
    tool: EngineTool,
    material: Material,
    machine: Machine,
    operation: Operation,
    workholding: Optional[Workholding],
    coolant: Optional[Coolant],
    feasible_ranges: FeasibleRanges,
    proposed_rpm: float,
    proposed_feedrate: float
) -> List[RiskScore]:
    """
    Calculate risk scores for various aspects of the machining scenario.
    
    Returns:
        List of risk scores
    """
    risk_scores = []
    
    # Tool wear risk
    tool_wear_risk = _assess_tool_wear_risk(
        material, tool, proposed_rpm, proposed_feedrate
    )
    risk_scores.append(tool_wear_risk)
    
    # Chatter risk
    chatter_risk = _assess_chatter_risk(
        tool, machine, operation, workholding, proposed_rpm, proposed_feedrate
    )
    risk_scores.append(chatter_risk)
    
    # Surface finish risk
    surface_finish_risk = _assess_surface_finish_risk(
        tool, operation, proposed_feedrate, proposed_rpm
    )
    if surface_finish_risk:
        risk_scores.append(surface_finish_risk)
    
    # Power/torque risk
    power_risk = _assess_power_risk(
        tool, material, operation, machine, proposed_rpm, proposed_feedrate
    )
    if power_risk:
        risk_scores.append(power_risk)
    
    return risk_scores


def _assess_tool_wear_risk(
    material: Material,
    tool: EngineTool,
    rpm: float,
    feedrate: float
) -> RiskScore:
    """Assess tool wear risk based on material and parameters"""
    # Base risk from material abrasiveness
    base_risk = material.properties.abrasiveness * 0.5
    
    # Increase risk if SFM is high
    sfm = calculate_sfm_from_rpm(tool.geometry.diameter, rpm)
    if sfm > material.properties.sfm_range_max * 0.9:
        base_risk += 2.0
    
    # Increase risk if chip load is high
    if tool.geometry.flute_count:
        chip_load = calculate_chip_load(feedrate, rpm, tool.geometry.flute_count)
        if chip_load > 0.3:  # High chip load
            base_risk += 1.5
    
    score = min(10.0, base_risk)
    confidence = 0.8
    
    return RiskScore(
        category="tool_wear",
        score=score,
        confidence=confidence,
        reason=f"Tool wear risk based on material abrasiveness ({material.properties.abrasiveness}) and cutting parameters"
    )


def _assess_chatter_risk(
    tool: EngineTool,
    machine: Machine,
    operation: Operation,
    workholding: Optional[Workholding],
    rpm: float,
    feedrate: float
) -> RiskScore:
    """Assess chatter risk based on rigidity and parameters"""
    # Base risk from machine rigidity
    base_risk = (10.0 - machine.capabilities.rigidity_factor) * 0.3
    
    # Increase risk if workholding is less rigid
    if workholding:
        base_risk += (10.0 - workholding.rigidity_factor) * 0.2
    
    # Increase risk with high DOC
    if operation.depth_of_cut_mm > tool.geometry.diameter * 0.5:
        base_risk += 1.0
    
    # Increase risk with high feedrate
    if feedrate > machine.capabilities.max_feedrate_mm_per_min * 0.8:
        base_risk += 1.0
    
    score = min(10.0, base_risk)
    confidence = 0.7
    
    return RiskScore(
        category="chatter",
        score=score,
        confidence=confidence,
        reason=f"Chatter risk based on machine rigidity ({machine.capabilities.rigidity_factor}) and cutting parameters"
    )


def _assess_surface_finish_risk(
    tool: EngineTool,
    operation: Operation,
    feedrate: float,
    rpm: float
) -> RiskScore | None:
    """Assess surface finish risk if surface finish requirement exists"""
    if not operation.surface_finish_ra_um:
        return None
    
    # High feedrate relative to RPM reduces surface finish
    if tool.geometry.flute_count:
        chip_load = calculate_chip_load(feedrate, rpm, tool.geometry.flute_count)
        if chip_load > 0.15:  # High chip load for finishing
            return RiskScore(
                category="surface_finish",
                score=5.0,
                confidence=0.8,
                reason=f"High chip load ({chip_load:.3f} mm) may not achieve required surface finish ({operation.surface_finish_ra_um} µm Ra)"
            )
    
    return None


def _assess_power_risk(
    tool: EngineTool,
    material: Material,
    operation: Operation,
    machine: Machine,
    rpm: float,
    feedrate: float
) -> RiskScore | None:
    """Assess power/torque risk if machine power is limited"""
    if not machine.capabilities.spindle_power_kw:
        return None
    
    # Simplified power calculation (rough estimate)
    # Power ≈ (MRR × specific_power) / efficiency
    # For aluminum: ~0.5-1.0 W/(mm³/min)
    # For steel: ~1.5-3.0 W/(mm³/min)
    
    from ..math.feeds_speeds import calculate_mrr
    mrr = calculate_mrr(feedrate, operation.depth_of_cut_mm, operation.width_of_cut_mm)
    
    # Estimate specific power based on material
    if material.category.value == "aluminum":
        specific_power = 0.7  # W/(mm³/min)
    elif material.category.value in ["steel", "stainless_steel"]:
        specific_power = 2.0
    else:
        specific_power = 1.0
    
    estimated_power_kw = (mrr * specific_power) / (1000 * 0.8)  # 80% efficiency
    
    if estimated_power_kw > machine.capabilities.spindle_power_kw * 0.9:
        return RiskScore(
            category="power",
            score=7.0,
            confidence=0.6,
            reason=f"Estimated power ({estimated_power_kw:.2f} kW) approaches machine limit ({machine.capabilities.spindle_power_kw} kW)"
        )
    
    return None


def assess_feasibility(
    feasible_ranges: FeasibleRanges,
    proposed_rpm: float,
    proposed_feedrate: float
) -> tuple[bool, float, list[str]]:
    """
    Assess if proposed parameters are feasible.
    
    Returns:
        (is_feasible, confidence, warnings)
    """
    warnings = []
    is_feasible = True
    
    # Check RPM
    if proposed_rpm < feasible_ranges.rpm_min:
        warnings.append(f"RPM ({proposed_rpm:.0f}) below minimum ({feasible_ranges.rpm_min:.0f})")
        is_feasible = False
    elif proposed_rpm > feasible_ranges.rpm_max:
        warnings.append(f"RPM ({proposed_rpm:.0f}) above maximum ({feasible_ranges.rpm_max:.0f})")
        is_feasible = False
    
    # Check feedrate
    if proposed_feedrate < feasible_ranges.feedrate_min_mm_per_min:
        warnings.append(f"Feedrate ({proposed_feedrate:.1f} mm/min) below minimum ({feasible_ranges.feedrate_min_mm_per_min:.1f} mm/min)")
        is_feasible = False
    elif proposed_feedrate > feasible_ranges.feedrate_max_mm_per_min:
        warnings.append(f"Feedrate ({proposed_feedrate:.1f} mm/min) above maximum ({feasible_ranges.feedrate_max_mm_per_min:.1f} mm/min)")
        is_feasible = False
    
    # Calculate confidence based on how close to limits
    confidence = 1.0
    if feasible_ranges.rpm_max > feasible_ranges.rpm_min:
        rpm_range = feasible_ranges.rpm_max - feasible_ranges.rpm_min
        rpm_distance_from_center = abs(proposed_rpm - (feasible_ranges.rpm_min + feasible_ranges.rpm_max) / 2)
        confidence *= max(0.5, 1.0 - (rpm_distance_from_center / rpm_range))
    
    return is_feasible, confidence, warnings

