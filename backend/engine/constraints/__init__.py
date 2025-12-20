"""
Constraint calculation module.
Determines feasible ranges for machining parameters.
"""

from .feasible_ranges import FeasibleRanges, calculate_feasible_ranges

__all__ = [
    "FeasibleRanges",
    "calculate_feasible_ranges",
]

