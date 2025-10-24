from pydantic import BaseModel, Field, validator
from typing import Dict, Any, Optional, Union, List
from datetime import datetime
from enum import Enum

class ToolType(str, Enum):
    END_MILL = "end_mill"
    BALL_END_MILL = "ball_end_mill"
    CHAMFER = "chamfer"
    DRILL = "drill"
    REAMER = "reamer"
    THREAD_MILL = "thread_mill"

class ExportFormat(str, Enum):
    FUSION_JSON = "fusion_json"
    CSV = "csv"

class ExportUnits(str, Enum):
    METRIC = "metric"
    IMPERIAL = "imperial"

# Base geometry schemas
class BaseGeometry(BaseModel):
    diameter: float = Field(..., gt=0, description="Tool diameter in mm")
    flute_length: float = Field(..., gt=0, description="Flute length in mm")
    overall_length: float = Field(..., gt=0, description="Overall length in mm")

class EndMillGeometry(BaseGeometry):
    flute_count: int = Field(..., ge=1, description="Number of flutes")
    helix_angle: float = Field(..., ge=0, le=90, description="Helix angle in degrees")
    length_of_cut: float = Field(..., gt=0, description="Length of cut in mm")
    corner_radius: Optional[float] = Field(None, ge=0, description="Corner radius in mm")

class BallEndMillGeometry(BaseGeometry):
    flute_count: int = Field(..., ge=1, description="Number of flutes")
    tip_radius: float = Field(..., gt=0, description="Tip radius in mm")

class ChamferGeometry(BaseGeometry):
    included_angle: float = Field(..., gt=0, le=180, description="Included angle in degrees")
    tip_flat: float = Field(..., ge=0, description="Tip flat in mm")
    shank_diameter: float = Field(..., gt=0, description="Shank diameter in mm")

class DrillGeometry(BaseGeometry):
    point_angle: float = Field(..., gt=0, le=180, description="Point angle in degrees")

class ReamerGeometry(BaseGeometry):
    lead_angle: Optional[float] = Field(None, ge=0, le=90, description="Lead angle in degrees")

class ThreadMillGeometry(BaseGeometry):
    pitch: float = Field(..., gt=0, description="Thread pitch in mm")
    max_thread_length: float = Field(..., gt=0, description="Maximum thread length in mm")

# Union type for all geometry types
GeometryType = Union[
    EndMillGeometry,
    BallEndMillGeometry,
    ChamferGeometry,
    DrillGeometry,
    ReamerGeometry,
    ThreadMillGeometry,
]

class ToolLimits(BaseModel):
    sfm: Optional[float] = Field(None, gt=0, description="Surface feet per minute")
    stepdown: Optional[float] = Field(None, gt=0, description="Stepdown in mm")
    engagement: Optional[float] = Field(None, gt=0, le=100, description="Engagement percentage")
    feed_rate: Optional[float] = Field(None, gt=0, description="Feed rate in mm/min")
    spindle_speed: Optional[float] = Field(None, gt=0, description="Spindle speed in RPM")

# Tool schemas
class ToolBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Tool name")
    vendor: str = Field(..., min_length=1, max_length=100, description="Tool vendor")
    type: ToolType = Field(..., description="Tool type")
    geometry: Dict[str, Any] = Field(..., description="Tool geometry data")
    limits: Optional[ToolLimits] = Field(None, description="Tool performance limits")

class ToolCreate(ToolBase):
    pass

class ToolUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    vendor: Optional[str] = Field(None, min_length=1, max_length=100)
    geometry: Optional[Dict[str, Any]] = None
    limits: Optional[ToolLimits] = None

class ToolResponse(ToolBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ToolListResponse(BaseModel):
    tools: List[ToolResponse]
    total: int
    page: int
    size: int

# Export schemas
class ExportRequest(BaseModel):
    format: ExportFormat = Field(..., description="Export format")
    units: ExportUnits = Field(..., description="Export units")
    
class ExportResponse(BaseModel):
    export_id: str
    tool_id: str
    format: ExportFormat
    units: ExportUnits
    file_size: Optional[int] = None
    download_url: Optional[str] = None
    created_at: datetime

# Validation schemas
class ValidationError(BaseModel):
    field: str
    message: str
    severity: str  # "error" or "warning"

class ValidationResponse(BaseModel):
    is_valid: bool
    errors: List[ValidationError]
    warnings: List[ValidationError]

# Health check schema
class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
    database: str
    redis: str
    timestamp: datetime
