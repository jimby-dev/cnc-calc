"""
Calculate feasible parameter ranges based on tool, material, and machine constraints.
"""
from pydantic import BaseModel, Field
from typing import Optional

from ..schemas.material import Material
from ..schemas.machine import Machine
from ..schemas.tool import EngineTool
from ..schemas.coolant import Coolant
from ..math.feeds_speeds import calculate_rpm_from_sfm, calculate_sfm_from_rpm


class FeasibleRanges(BaseModel):
    """Feasible parameter ranges for the scenario"""
    # RPM range
    rpm_min: float = Field(..., gt=0, description="Minimum feasible RPM")
    rpm_max: float = Field(..., gt=0, description="Maximum feasible RPM")
    rpm_optimal: Optional[float] = Field(None, gt=0, description="Optimal RPM")
    
    # SFM range
    sfm_min: float = Field(..., gt=0, description="Minimum feasible SFM")
    sfm_max: float = Field(..., gt=0, description="Maximum feasible SFM")
    sfm_optimal: Optional[float] = Field(None, gt=0, description="Optimal SFM")
    
    # Feedrate range
    feedrate_min_mm_per_min: float = Field(..., gt=0, description="Minimum feedrate (mm/min)")
    feedrate_max_mm_per_min: float = Field(..., gt=0, description="Maximum feedrate (mm/min)")
    
    # Chip load range
    chip_load_min_mm: Optional[float] = Field(None, gt=0, description="Minimum chip load (mm)")
    chip_load_max_mm: Optional[float] = Field(None, gt=0, description="Maximum chip load (mm)")
    
    # Constraints limiting the ranges
    limiting_constraints: list[str] = Field(default_factory=list, description="Constraints that limit the ranges")


def calculate_feasible_ranges(
    tool: EngineTool,
    material: Material,
    machine: Machine,
    coolant: Optional[Coolant] = None
) -> FeasibleRanges:
    """
    Calculate feasible parameter ranges based on tool, material, machine, and coolant.
    
    Args:
        tool: Tool definition
        material: Material properties
        machine: Machine capabilities
        coolant: Optional coolant properties
        
    Returns:
        Feasible parameter ranges
    """
    limiting_constraints = []
    
    # Apply coolant multiplier to material SFM
    coolant_multiplier = coolant.sfm_multiplier if coolant else 1.0
    effective_sfm_min = material.properties.sfm_range_min * coolant_multiplier * tool.sfm_multiplier
    effective_sfm_max = material.properties.sfm_range_max * coolant_multiplier * tool.sfm_multiplier
    
    # Calculate RPM range from SFM range
    rpm_from_sfm_min = calculate_rpm_from_sfm(tool.geometry.diameter, effective_sfm_min)
    rpm_from_sfm_max = calculate_rpm_from_sfm(tool.geometry.diameter, effective_sfm_max)
    
    # Apply machine RPM limits
    rpm_min = max(machine.capabilities.min_rpm, rpm_from_sfm_min)
    rpm_max = min(machine.capabilities.max_rpm, rpm_from_sfm_max)
    
    if rpm_min >= rpm_max:
        limiting_constraints.append("Machine RPM limits conflict with material SFM requirements")
        # Use machine limits as fallback
        rpm_min = machine.capabilities.min_rpm
        rpm_max = machine.capabilities.max_rpm
    
    # Check tool RPM limits if specified
    if tool.limits and tool.limits.max_rpm:
        rpm_max = min(rpm_max, tool.limits.max_rpm)
        limiting_constraints.append("Tool maximum RPM")
    
    # Calculate SFM range from final RPM range
    sfm_min = calculate_sfm_from_rpm(tool.geometry.diameter, rpm_min)
    sfm_max = calculate_sfm_from_rpm(tool.geometry.diameter, rpm_max)
    
    # Optimal SFM (middle of material range, adjusted)
    sfm_optimal = (effective_sfm_min + effective_sfm_max) / 2
    rpm_optimal = calculate_rpm_from_sfm(tool.geometry.diameter, sfm_optimal)
    
    # Clamp optimal RPM to feasible range
    rpm_optimal = max(rpm_min, min(rpm_max, rpm_optimal))
    
    # Feedrate range (from machine capabilities)
    feedrate_min = machine.capabilities.min_feedrate_mm_per_min
    feedrate_max = machine.capabilities.max_feedrate_mm_per_min
    
    # Apply coolant multiplier
    if coolant:
        feedrate_max *= coolant.feedrate_multiplier
    
    # Apply tool multiplier
    feedrate_max *= tool.feedrate_multiplier
    
    # Apply tool limits if specified
    if tool.limits and tool.limits.max_feedrate_mm_per_min:
        feedrate_max = min(feedrate_max, tool.limits.max_feedrate_mm_per_min)
        limiting_constraints.append("Tool maximum feedrate")
    
    # Chip load range (typical values, can be refined)
    chip_load_min = 0.01  # Very conservative
    chip_load_max = 0.5   # Aggressive but reasonable
    
    # Apply tool limits if specified
    if tool.limits and tool.limits.max_chip_load_mm:
        chip_load_max = min(chip_load_max, tool.limits.max_chip_load_mm)
    
    return FeasibleRanges(
        rpm_min=rpm_min,
        rpm_max=rpm_max,
        rpm_optimal=rpm_optimal,
        sfm_min=sfm_min,
        sfm_max=sfm_max,
        sfm_optimal=sfm_optimal,
        feedrate_min_mm_per_min=feedrate_min,
        feedrate_max_mm_per_min=feedrate_max,
        chip_load_min_mm=chip_load_min,
        chip_load_max_mm=chip_load_max,
        limiting_constraints=limiting_constraints
    )

