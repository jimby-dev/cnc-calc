from sqlalchemy import Column, String, DateTime, Text, JSON, Float, Integer, Boolean
from sqlalchemy.sql import func
from app.core.database import Base
from datetime import datetime
from typing import Dict, Any, Optional

class Tool(Base):
    __tablename__ = "tools"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    vendor = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False, index=True)  # end_mill, ball_end_mill, etc.
    
    # Geometry stored as JSON
    geometry = Column(JSON, nullable=False)
    
    # Optional limits/performance data
    limits = Column(JSON, nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Soft delete
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "vendor": self.vendor,
            "type": self.type,
            "geometry": self.geometry,
            "limits": self.limits,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Tool":
        """Create model from dictionary"""
        return cls(
            id=data.get("id"),
            name=data["name"],
            vendor=data["vendor"],
            type=data["type"],
            geometry=data["geometry"],
            limits=data.get("limits"),
        )

class ToolExport(Base):
    __tablename__ = "tool_exports"
    
    id = Column(String, primary_key=True, index=True)
    tool_id = Column(String, nullable=False, index=True)
    export_format = Column(String, nullable=False)  # fusion_json, csv
    export_units = Column(String, nullable=False)  # metric, imperial
    
    # Export metadata
    file_size = Column(Integer, nullable=True)
    export_data = Column(Text, nullable=True)  # Store the actual export content
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "tool_id": self.tool_id,
            "export_format": self.export_format,
            "export_units": self.export_units,
            "file_size": self.file_size,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
