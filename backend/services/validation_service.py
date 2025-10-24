from typing import List, Dict, Any
from schemas.tool import ToolResponse, ValidationResponse, ValidationError, ToolType
import structlog

logger = structlog.get_logger()

class ValidationService:
    def __init__(self):
        pass
    
    async def validate_tool(self, tool: ToolResponse) -> ValidationResponse:
        """Validate a tool for Fusion 360 compatibility"""
        errors: List[ValidationError] = []
        warnings: List[ValidationError] = []
        
        # Basic validation
        self._validate_basic_fields(tool, errors, warnings)
        
        # Geometry validation based on tool type
        if tool.type == ToolType.END_MILL:
            self._validate_end_mill(tool, errors, warnings)
        elif tool.type == ToolType.BALL_END_MILL:
            self._validate_ball_end_mill(tool, errors, warnings)
        elif tool.type == ToolType.CHAMFER:
            self._validate_chamfer(tool, errors, warnings)
        elif tool.type == ToolType.DRILL:
            self._validate_drill(tool, errors, warnings)
        elif tool.type == ToolType.REAMER:
            self._validate_reamer(tool, errors, warnings)
        elif tool.type == ToolType.THREAD_MILL:
            self._validate_thread_mill(tool, errors, warnings)
        
        # Fusion 360 compatibility checks
        self._validate_fusion_compatibility(tool, errors, warnings)
        
        is_valid = len(errors) == 0
        
        return ValidationResponse(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings
        )
    
    def _validate_basic_fields(self, tool: ToolResponse, errors: List[ValidationError], warnings: List[ValidationError]):
        """Validate basic tool fields"""
        geometry = tool.geometry
        
        # Required fields
        if not geometry.get("diameter") or geometry["diameter"] <= 0:
            errors.append(ValidationError(
                field="diameter",
                message="Diameter must be greater than 0",
                severity="error"
            ))
        
        if not geometry.get("flute_length") or geometry["flute_length"] <= 0:
            errors.append(ValidationError(
                field="flute_length",
                message="Flute length must be greater than 0",
                severity="error"
            ))
        
        if not geometry.get("overall_length") or geometry["overall_length"] <= 0:
            errors.append(ValidationError(
                field="overall_length",
                message="Overall length must be greater than 0",
                severity="error"
            ))
        
        # Relationship validation
        if geometry.get("flute_length") and geometry.get("overall_length"):
            if geometry["flute_length"] >= geometry["overall_length"]:
                errors.append(ValidationError(
                    field="flute_length",
                    message="Flute length must be less than overall length",
                    severity="error"
                ))
    
    def _validate_end_mill(self, tool: ToolResponse, errors: List[ValidationError], warnings: List[ValidationError]):
        """Validate end mill specific fields"""
        geometry = tool.geometry
        
        # Required fields
        if not geometry.get("flute_count") or geometry["flute_count"] < 1:
            errors.append(ValidationError(
                field="flute_count",
                message="Flute count must be at least 1",
                severity="error"
            ))
        
        if not geometry.get("helix_angle") or geometry["helix_angle"] < 0:
            errors.append(ValidationError(
                field="helix_angle",
                message="Helix angle must be non-negative",
                severity="error"
            ))
        
        if not geometry.get("length_of_cut") or geometry["length_of_cut"] <= 0:
            errors.append(ValidationError(
                field="length_of_cut",
                message="Length of cut must be greater than 0",
                severity="error"
            ))
        
        # Relationship validation
        if geometry.get("flute_length") and geometry.get("length_of_cut"):
            if geometry["flute_length"] < geometry["length_of_cut"]:
                errors.append(ValidationError(
                    field="length_of_cut",
                    message="Length of cut cannot exceed flute length",
                    severity="error"
                ))
        
        # Warnings
        if geometry.get("helix_angle"):
            if geometry["helix_angle"] < 20 or geometry["helix_angle"] > 45:
                warnings.append(ValidationError(
                    field="helix_angle",
                    message="Unusual helix angle - typical range is 20-45 degrees",
                    severity="warning"
                ))
        
        if geometry.get("corner_radius") and geometry.get("diameter"):
            if geometry["corner_radius"] > geometry["diameter"] / 4:
                warnings.append(ValidationError(
                    field="corner_radius",
                    message="Large corner radius may affect cutting performance",
                    severity="warning"
                ))
    
    def _validate_ball_end_mill(self, tool: ToolResponse, errors: List[ValidationError], warnings: List[ValidationError]):
        """Validate ball end mill specific fields"""
        geometry = tool.geometry
        
        # Required fields
        if not geometry.get("flute_count") or geometry["flute_count"] < 1:
            errors.append(ValidationError(
                field="flute_count",
                message="Flute count must be at least 1",
                severity="error"
            ))
        
        if not geometry.get("tip_radius") or geometry["tip_radius"] <= 0:
            errors.append(ValidationError(
                field="tip_radius",
                message="Tip radius must be greater than 0",
                severity="error"
            ))
        
        # Critical validation for ball end mills
        if geometry.get("diameter") and geometry.get("tip_radius"):
            expected_radius = geometry["diameter"] / 2
            if abs(geometry["tip_radius"] - expected_radius) > 0.01:
                errors.append(ValidationError(
                    field="tip_radius",
                    message="Tip radius must equal half the diameter for ball end mills",
                    severity="error"
                ))
    
    def _validate_chamfer(self, tool: ToolResponse, errors: List[ValidationError], warnings: List[ValidationError]):
        """Validate chamfer mill specific fields"""
        geometry = tool.geometry
        
        # Required fields
        if not geometry.get("included_angle") or geometry["included_angle"] <= 0:
            errors.append(ValidationError(
                field="included_angle",
                message="Included angle is required and must be greater than 0",
                severity="error"
            ))
        
        if geometry.get("tip_flat") is None or geometry["tip_flat"] < 0:
            errors.append(ValidationError(
                field="tip_flat",
                message="Tip flat is required",
                severity="error"
            ))
        
        if not geometry.get("shank_diameter") or geometry["shank_diameter"] <= 0:
            errors.append(ValidationError(
                field="shank_diameter",
                message="Shank diameter must be greater than 0",
                severity="error"
            ))
        
        # Warnings
        if geometry.get("tip_flat") and geometry["tip_flat"] < 0.1:
            warnings.append(ValidationError(
                field="tip_flat",
                message="Very small tip flat may be difficult to manufacture",
                severity="warning"
            ))
    
    def _validate_drill(self, tool: ToolResponse, errors: List[ValidationError], warnings: List[ValidationError]):
        """Validate drill specific fields"""
        geometry = tool.geometry
        
        # Required fields
        if not geometry.get("point_angle") or geometry["point_angle"] <= 0:
            errors.append(ValidationError(
                field="point_angle",
                message="Point angle must be greater than 0",
                severity="error"
            ))
        
        # Warnings
        if geometry.get("point_angle"):
            if geometry["point_angle"] < 90 or geometry["point_angle"] > 150:
                warnings.append(ValidationError(
                    field="point_angle",
                    message="Unusual point angle - typical range is 90-150 degrees",
                    severity="warning"
                ))
    
    def _validate_reamer(self, tool: ToolResponse, errors: List[ValidationError], warnings: List[ValidationError]):
        """Validate reamer specific fields"""
        geometry = tool.geometry
        
        # Optional fields validation
        if geometry.get("lead_angle") is not None:
            if geometry["lead_angle"] < 0 or geometry["lead_angle"] > 90:
                warnings.append(ValidationError(
                    field="lead_angle",
                    message="Lead angle should be between 0 and 90 degrees",
                    severity="warning"
                ))
    
    def _validate_thread_mill(self, tool: ToolResponse, errors: List[ValidationError], warnings: List[ValidationError]):
        """Validate thread mill specific fields"""
        geometry = tool.geometry
        
        # Required fields
        if not geometry.get("pitch") or geometry["pitch"] <= 0:
            errors.append(ValidationError(
                field="pitch",
                message="Pitch must be greater than 0",
                severity="error"
            ))
        
        if not geometry.get("max_thread_length") or geometry["max_thread_length"] <= 0:
            errors.append(ValidationError(
                field="max_thread_length",
                message="Maximum thread length must be greater than 0",
                severity="error"
            ))
        
        # Relationship validation
        if geometry.get("max_thread_length") and geometry.get("flute_length"):
            if geometry["max_thread_length"] > geometry["flute_length"]:
                warnings.append(ValidationError(
                    field="max_thread_length",
                    message="Maximum thread length should not exceed flute length",
                    severity="warning"
                ))
    
    def _validate_fusion_compatibility(self, tool: ToolResponse, errors: List[ValidationError], warnings: List[ValidationError]):
        """Validate Fusion 360 compatibility"""
        # Check if tool type is supported
        supported_types = [
            ToolType.END_MILL,
            ToolType.BALL_END_MILL,
            ToolType.CHAMFER,
            ToolType.DRILL,
            ToolType.REAMER,
            ToolType.THREAD_MILL
        ]
        
        if tool.type not in supported_types:
            errors.append(ValidationError(
                field="type",
                message=f"Tool type '{tool.type}' is not supported by Fusion 360",
                severity="error"
            ))
        
        # Check for reasonable dimension ranges
        geometry = tool.geometry
        
        if geometry.get("diameter"):
            if geometry["diameter"] < 0.1 or geometry["diameter"] > 100:
                warnings.append(ValidationError(
                    field="diameter",
                    message="Diameter outside typical range (0.1-100mm)",
                    severity="warning"
                ))
        
        if geometry.get("overall_length"):
            if geometry["overall_length"] < 1 or geometry["overall_length"] > 500:
                warnings.append(ValidationError(
                    field="overall_length",
                    message="Overall length outside typical range (1-500mm)",
                    severity="warning"
                ))
