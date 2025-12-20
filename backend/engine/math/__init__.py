"""
Mathematical calculations for feeds & speeds.
All calculations use metric units (mm) internally.
"""

from .feeds_speeds import (
    calculate_sfm_from_rpm,
    calculate_rpm_from_sfm,
    calculate_feedrate,
    calculate_chip_load,
    calculate_mrr,
    calculate_surface_speed,
)

__all__ = [
    "calculate_sfm_from_rpm",
    "calculate_rpm_from_sfm",
    "calculate_feedrate",
    "calculate_chip_load",
    "calculate_mrr",
    "calculate_surface_speed",
]

