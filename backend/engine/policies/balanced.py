"""
Balanced policy implementation.
Balances tool life, time, and safety.
"""
from ..policies.base import PolicyBase, PolicyResult
from ..constraints.feasible_ranges import FeasibleRanges


class BalancedPolicy(PolicyBase):
    """Balanced policy: balance tool life, time, and safety"""
    
    def apply(
        self,
        feasible_ranges: FeasibleRanges,
        **kwargs
    ) -> PolicyResult:
        """
        Apply balanced policy: use middle of ranges for balanced performance.
        """
        # Use optimal RPM if available, otherwise middle of range
        if feasible_ranges.rpm_optimal:
            rpm = feasible_ranges.rpm_optimal
        else:
            rpm_range = feasible_ranges.rpm_max - feasible_ranges.rpm_min
            rpm = feasible_ranges.rpm_min + (rpm_range * 0.5)
        
        # Use middle of feedrate range
        feedrate_range = feasible_ranges.feedrate_max_mm_per_min - feasible_ranges.feedrate_min_mm_per_min
        feedrate = feasible_ranges.feedrate_min_mm_per_min + (feedrate_range * 0.5)
        
        return PolicyResult(
            rpm=rpm,
            feedrate_mm_per_min=feedrate,
            confidence=0.88,
            reason="Balanced policy: middle-ground parameters balancing tool life, time, and safety",
            constraints_applied=["balanced", "optimal_rpm", "moderate_feedrate"]
        )

