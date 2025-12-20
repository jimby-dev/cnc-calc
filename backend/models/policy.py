"""
Policy database model.
"""
from sqlalchemy import Column, String, JSON, DateTime, Boolean, Integer
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
import uuid

from app.core.database import Base


class Policy(Base):
    """Policy database model"""
    __tablename__ = "policies"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False, index=True)
    weights = Column(JSONB, nullable=False)  # PolicyWeights as JSON
    rules = Column(JSONB, nullable=False, default={})  # Policy rules as JSON
    
    # Priority (lower = higher priority)
    priority = Column(Integer, default=100, nullable=False, index=True)
    
    # Metadata
    description = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)

