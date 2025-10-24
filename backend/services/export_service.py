from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, Any, Optional
import uuid
import json
import csv
import io
from datetime import datetime

from models.tool import Tool, ToolExport
from schemas.tool import ToolResponse, ExportRequest, ExportResponse, ExportFormat, ExportUnits
import structlog

logger = structlog.get_logger()

class ExportService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def export_tool(self, tool: ToolResponse, export_request: ExportRequest) -> ExportResponse:
        """Export a tool in the specified format"""
        export_id = str(uuid.uuid4())
        
        # Generate export data
        export_data = await self._generate_export_data(tool, export_request)
        
        # Create export record
        export_record = ToolExport(
            id=export_id,
            tool_id=tool.id,
            export_format=export_request.format.value,
            export_units=export_request.units.value,
            file_size=len(export_data),
            export_data=export_data,
            created_at=datetime.utcnow()
        )
        
        self.db.add(export_record)
        await self.db.commit()
        
        return ExportResponse(
            export_id=export_id,
            tool_id=tool.id,
            format=export_request.format,
            units=export_request.units,
            file_size=len(export_data),
            download_url=f"/api/tools/{tool.id}/export/{export_id}/download",
            created_at=export_record.created_at
        )
    
    async def _generate_export_data(self, tool: ToolResponse, export_request: ExportRequest) -> str:
        """Generate export data based on format and units"""
        if export_request.format == ExportFormat.FUSION_JSON:
            return await self._generate_fusion_json(tool, export_request.units)
        elif export_request.format == ExportFormat.CSV:
            return await self._generate_csv(tool, export_request.units)
        else:
            raise ValueError(f"Unsupported export format: {export_request.format}")
    
    async def _generate_fusion_json(self, tool: ToolResponse, units: ExportUnits) -> str:
        """Generate Fusion 360 compatible JSON"""
        # Convert units if needed
        geometry = tool.geometry.copy()
        if units == ExportUnits.IMPERIAL:
            geometry = self._convert_to_imperial(geometry)
        
        # Create Fusion 360 compatible structure
        fusion_data = {
            "toolType": self._map_tool_type_to_fusion(tool.type),
            "name": tool.name,
            "vendor": tool.vendor,
            "diameter": geometry.get("diameter", 0),
            "fluteLength": geometry.get("flute_length", 0),
            "overallLength": geometry.get("overall_length", 0),
            "units": "in" if units == ExportUnits.IMPERIAL else "mm"
        }
        
        # Add tool-specific fields
        if tool.type == "end_mill":
            fusion_data.update({
                "fluteCount": geometry.get("flute_count", 2),
                "helixAngle": geometry.get("helix_angle", 30),
                "lengthOfCut": geometry.get("length_of_cut", 0),
                "cornerRadius": geometry.get("corner_radius", 0)
            })
        elif tool.type == "ball_end_mill":
            fusion_data.update({
                "fluteCount": geometry.get("flute_count", 2),
                "tipRadius": geometry.get("tip_radius", 0)
            })
        elif tool.type == "chamfer":
            fusion_data.update({
                "includedAngle": geometry.get("included_angle", 90),
                "tipFlat": geometry.get("tip_flat", 0),
                "shankDiameter": geometry.get("shank_diameter", 0)
            })
        elif tool.type == "drill":
            fusion_data.update({
                "pointAngle": geometry.get("point_angle", 118)
            })
        elif tool.type == "reamer":
            fusion_data.update({
                "leadAngle": geometry.get("lead_angle", 0)
            })
        elif tool.type == "thread_mill":
            fusion_data.update({
                "pitch": geometry.get("pitch", 0),
                "maxThreadLength": geometry.get("max_thread_length", 0)
            })
        
        return json.dumps(fusion_data, indent=2)
    
    async def _generate_csv(self, tool: ToolResponse, units: ExportUnits) -> str:
        """Generate CSV export"""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header row
        headers = [
            "Tool Name", "Vendor", "Type", "Diameter", "Flute Length", 
            "Overall Length", "Units"
        ]
        
        # Add tool-specific headers
        if tool.type == "end_mill":
            headers.extend(["Flute Count", "Helix Angle", "Length of Cut", "Corner Radius"])
        elif tool.type == "ball_end_mill":
            headers.extend(["Flute Count", "Tip Radius"])
        elif tool.type == "chamfer":
            headers.extend(["Included Angle", "Tip Flat", "Shank Diameter"])
        elif tool.type == "drill":
            headers.extend(["Point Angle"])
        elif tool.type == "reamer":
            headers.extend(["Lead Angle"])
        elif tool.type == "thread_mill":
            headers.extend(["Pitch", "Max Thread Length"])
        
        writer.writerow(headers)
        
        # Data row
        geometry = tool.geometry.copy()
        if units == ExportUnits.IMPERIAL:
            geometry = self._convert_to_imperial(geometry)
        
        row = [
            tool.name,
            tool.vendor,
            tool.type,
            geometry.get("diameter", ""),
            geometry.get("flute_length", ""),
            geometry.get("overall_length", ""),
            "in" if units == ExportUnits.IMPERIAL else "mm"
        ]
        
        # Add tool-specific data
        if tool.type == "end_mill":
            row.extend([
                geometry.get("flute_count", ""),
                geometry.get("helix_angle", ""),
                geometry.get("length_of_cut", ""),
                geometry.get("corner_radius", "")
            ])
        elif tool.type == "ball_end_mill":
            row.extend([
                geometry.get("flute_count", ""),
                geometry.get("tip_radius", "")
            ])
        elif tool.type == "chamfer":
            row.extend([
                geometry.get("included_angle", ""),
                geometry.get("tip_flat", ""),
                geometry.get("shank_diameter", "")
            ])
        elif tool.type == "drill":
            row.extend([geometry.get("point_angle", "")])
        elif tool.type == "reamer":
            row.extend([geometry.get("lead_angle", "")])
        elif tool.type == "thread_mill":
            row.extend([
                geometry.get("pitch", ""),
                geometry.get("max_thread_length", "")
            ])
        
        writer.writerow(row)
        
        return output.getvalue()
    
    def _convert_to_imperial(self, geometry: Dict[str, Any]) -> Dict[str, Any]:
        """Convert metric measurements to imperial"""
        converted = geometry.copy()
        
        # Convert mm to inches (1 inch = 25.4 mm)
        mm_fields = ["diameter", "flute_length", "overall_length", "length_of_cut", 
                     "corner_radius", "tip_radius", "tip_flat", "shank_diameter", 
                     "pitch", "max_thread_length"]
        
        for field in mm_fields:
            if field in converted and converted[field] is not None:
                converted[field] = round(converted[field] / 25.4, 4)
        
        return converted
    
    def _map_tool_type_to_fusion(self, tool_type: str) -> str:
        """Map internal tool type to Fusion 360 tool type"""
        mapping = {
            "end_mill": "End Mill",
            "ball_end_mill": "Ball End Mill",
            "chamfer": "Chamfer Mill",
            "drill": "Drill",
            "reamer": "Reamer",
            "thread_mill": "Thread Mill"
        }
        return mapping.get(tool_type, tool_type)
    
    async def get_export(self, export_id: str) -> Optional[str]:
        """Get export data by ID"""
        result = await self.db.execute(
            select(ToolExport).where(ToolExport.id == export_id)
        )
        export = result.scalar_one_or_none()
        
        if export:
            return export.export_data
        return None
