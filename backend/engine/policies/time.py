"""
Time optimization policy.
Maximizes material removal rate (MRR) to minimize cycle time.
"""
from ..policies.base import PolicyBase, PolicyResult
from ..constraints.feasible_ranges import FeasibleRanges


class TimePolicy(PolicyBase):
    """Time optimization policy: maximize MRR"""
    
    def apply(
        self,
        feasible_ranges: FeasibleRanges,
        **kwargs
    ) -> PolicyResult:
        """
        Apply time policy: use higher RPM and feedrates to maximize MRR.
        """
        # Use higher end of RPM range (80% of range)
        rpm_range = feasible_ranges.rpm_max - feasible_ranges.rpm_min
        rpm = feasible_ranges.rpm_min + (rpm_range * 0.8)
        
        # Use higher end of feedrate range (85% of range)
        feedrate_range = feasible_ranges.feedrate_max_mm_per_min - feasible_ranges.feedrate_min_mm_per_min
        feedrate = feasible_ranges.feedrate_max_mm_per_min - (feedrate_range * 0.15)
        
        return PolicyResult(
            rpm=rpm,
            feedrate_mm_per_min=feedrate,
            confidence=0.85,
            reason="Time optimization: higher parameters to maximize material removal rate",
            constraints_applied=["time", "high_mrr", "high_rpm", "high_feedrate"]
        )

