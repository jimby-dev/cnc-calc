"""
Safety-first policy implementation.
Conservative parameters prioritizing tool and machine safety.
"""
from ..policies.base import PolicyBase, PolicyResult
from ..constraints.feasible_ranges import FeasibleRanges


class SafetyPolicy(PolicyBase):
    """Safety-first policy: conservative parameters"""
    
    def apply(
        self,
        feasible_ranges: FeasibleRanges,
        **kwargs
    ) -> PolicyResult:
        """
        Apply safety policy: use conservative parameters (lower end of ranges).
        """
        # Use lower end of RPM range (70% of range)
        rpm_range = feasible_ranges.rpm_max - feasible_ranges.rpm_min
        rpm = feasible_ranges.rpm_min + (rpm_range * 0.3)
        
        # Use lower end of feedrate range (60% of range)
        feedrate_range = feasible_ranges.feedrate_max_mm_per_min - feasible_ranges.feedrate_min_mm_per_min
        feedrate = feasible_ranges.feedrate_min_mm_per_min + (feedrate_range * 0.4)
        
        return PolicyResult(
            rpm=rpm,
            feedrate_mm_per_min=feedrate,
            confidence=0.95,
            reason="Safety-first policy: conservative parameters to maximize tool life and minimize risk",
            constraints_applied=["safety", "conservative_rpm", "conservative_feedrate"]
        )

