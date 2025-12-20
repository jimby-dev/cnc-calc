"""
Tool-life optimization policy.
Maximizes tool life by using lower SFM and feedrates.
"""
from ..policies.base import PolicyBase, PolicyResult
from ..constraints.feasible_ranges import FeasibleRanges


class ToolLifePolicy(PolicyBase):
    """Tool-life optimization policy: maximize tool life"""
    
    def apply(
        self,
        feasible_ranges: FeasibleRanges,
        **kwargs
    ) -> PolicyResult:
        """
        Apply tool-life policy: use lower SFM and feedrates to maximize tool life.
        """
        # Use lower end of RPM range (40% of range)
        rpm_range = feasible_ranges.rpm_max - feasible_ranges.rpm_min
        rpm = feasible_ranges.rpm_min + (rpm_range * 0.4)
        
        # Use lower end of feedrate range (50% of range)
        feedrate_range = feasible_ranges.feedrate_max_mm_per_min - feasible_ranges.feedrate_min_mm_per_min
        feedrate = feasible_ranges.feedrate_min_mm_per_min + (feedrate_range * 0.5)
        
        return PolicyResult(
            rpm=rpm,
            feedrate_mm_per_min=feedrate,
            confidence=0.90,
            reason="Tool-life optimization: lower SFM and feedrates to maximize tool life",
            constraints_applied=["tool_life", "low_sfm", "low_feedrate"]
        )

