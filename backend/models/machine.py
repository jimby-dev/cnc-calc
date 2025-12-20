"""
Machine database model.
"""
from sqlalchemy import Column, String, JSON, DateTime, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
import uuid

from app.core.database import Base


class Machine(Base):
    """Machine database model"""
    __tablename__ = "machines"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False, index=True)
    capabilities = Column(JSONB, nullable=False)  # MachineCapabilities as JSON
    
    # Metadata
    manufacturer = Column(String, nullable=True)
    description = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)

