"""
Material database model.
"""
from sqlalchemy import Column, String, JSON, DateTime, Boolean
from datetime import datetime
import uuid

from app.core.database import Base


class Material(Base):
    """Material database model"""
    __tablename__ = "materials"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False, index=True)
    properties = Column(JSON, nullable=False)  # MaterialProperties as JSON
    
    # Metadata
    description = Column(String, nullable=True)
    common_applications = Column(JSON, nullable=True)  # Array of strings
    notes = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)

