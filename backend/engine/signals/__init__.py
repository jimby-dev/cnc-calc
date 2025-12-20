"""
Signal computation module.
Calculates risk scores and constraint signals.
"""

from .risk_assessment import calculate_risk_scores, assess_feasibility

__all__ = [
    "calculate_risk_scores",
    "assess_feasibility",
]

