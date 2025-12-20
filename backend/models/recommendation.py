"""
Recommendation database model (optional, for storing recommendation history).
"""
from sqlalchemy import Column, String, JSON, DateTime, Boolean, Float
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
import uuid

from app.core.database import Base


class Recommendation(Base):
    """Recommendation database model (optional storage)"""
    __tablename__ = "recommendations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    scenario_id = Column(String, nullable=True, index=True)
    
    # Core recommendation values
    spindle_rpm = Column(Float, nullable=False)
    feedrate_mm_per_min = Column(Float, nullable=False)
    feedrate_mm_per_rev = Column(Float, nullable=True)
    chip_load_mm = Column(Float, nullable=True)
    surface_speed_m_per_min = Column(Float, nullable=False)
    surface_speed_sfm = Column(Float, nullable=True)
    material_removal_rate_mm3_per_min = Column(Float, nullable=True)
    
    # Signals and confidence
    signals = Column(JSONB, nullable=False)  # Signals as JSON
    confidence = Column(Float, nullable=False)
    
    # Explanation trace
    trace = Column(JSONB, nullable=False)  # RecommendationTrace as JSON
    
    # Input context (for reference)
    input_context = Column(JSONB, nullable=True)  # Tool, material, machine IDs, etc.
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)

