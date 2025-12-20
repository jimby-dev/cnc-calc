"""
Feeds & speeds calculation functions.
All inputs/outputs in metric (mm) as per engine requirement.
"""
import math
from typing import Optional


def calculate_sfm_from_rpm(diameter_mm: float, rpm: float) -> float:
    """
    Calculate surface feet per minute (SFM) from RPM and tool diameter.
    
    Args:
        diameter_mm: Tool diameter in millimeters
        rpm: Spindle RPM
        
    Returns:
        SFM (surface feet per minute)
    """
    # Convert mm to inches
    diameter_inches = diameter_mm / 25.4
    # SFM = (π × diameter_inches × RPM) / 12
    sfm = (math.pi * diameter_inches * rpm) / 12
    return sfm


def calculate_rpm_from_sfm(diameter_mm: float, sfm: float) -> float:
    """
    Calculate RPM from SFM and tool diameter.
    
    Args:
        diameter_mm: Tool diameter in millimeters
        sfm: Desired surface feet per minute
        
    Returns:
        RPM
    """
    # Convert mm to inches
    diameter_inches = diameter_mm / 25.4
    # RPM = (SFM × 12) / (π × diameter_inches)
    if diameter_inches == 0:
        return 0.0
    rpm = (sfm * 12) / (math.pi * diameter_inches)
    return rpm


def calculate_surface_speed(diameter_mm: float, rpm: float) -> float:
    """
    Calculate surface speed in meters per minute.
    
    Args:
        diameter_mm: Tool diameter in millimeters
        rpm: Spindle RPM
        
    Returns:
        Surface speed in m/min
    """
    # Surface speed (m/min) = (π × diameter_mm × RPM) / 1000
    surface_speed = (math.pi * diameter_mm * rpm) / 1000
    return surface_speed


def calculate_feedrate(
    rpm: float,
    chip_load_mm: float,
    flute_count: int
) -> float:
    """
    Calculate feedrate in mm/min from RPM, chip load, and flute count.
    
    Args:
        rpm: Spindle RPM
        chip_load_mm: Chip load per tooth in millimeters
        flute_count: Number of flutes
        
    Returns:
        Feedrate in mm/min
    """
    # Feedrate = RPM × chip_load × flute_count
    feedrate = rpm * chip_load_mm * flute_count
    return feedrate


def calculate_chip_load(
    feedrate_mm_per_min: float,
    rpm: float,
    flute_count: int
) -> float:
    """
    Calculate chip load per tooth from feedrate, RPM, and flute count.
    
    Args:
        feedrate_mm_per_min: Feedrate in mm/min
        rpm: Spindle RPM
        flute_count: Number of flutes
        
    Returns:
        Chip load per tooth in mm
    """
    if rpm == 0 or flute_count == 0:
        return 0.0
    # Chip load = feedrate / (RPM × flute_count)
    chip_load = feedrate_mm_per_min / (rpm * flute_count)
    return chip_load


def calculate_mrr(
    feedrate_mm_per_min: float,
    depth_of_cut_mm: float,
    width_of_cut_mm: float
) -> float:
    """
    Calculate material removal rate (MRR) in mm³/min.
    
    Args:
        feedrate_mm_per_min: Feedrate in mm/min
        depth_of_cut_mm: Depth of cut in mm
        width_of_cut_mm: Width of cut (stepover) in mm
        
    Returns:
        Material removal rate in mm³/min
    """
    mrr = feedrate_mm_per_min * depth_of_cut_mm * width_of_cut_mm
    return mrr


def calculate_feed_per_revolution(
    feedrate_mm_per_min: float,
    rpm: float
) -> float:
    """
    Calculate feed per revolution (mm/rev).
    
    Args:
        feedrate_mm_per_min: Feedrate in mm/min
        rpm: Spindle RPM
        
    Returns:
        Feed per revolution in mm/rev
    """
    if rpm == 0:
        return 0.0
    feed_per_rev = feedrate_mm_per_min / rpm
    return feed_per_rev

