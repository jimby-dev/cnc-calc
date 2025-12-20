"""
Seed script for initial engine data.
Creates materials, machines, policies, and example tools.
"""
import asyncio
import json
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.core.database import Base
from app.core.config import settings
from models.material import Material as MaterialModel
from models.machine import Machine as MachineModel
from models.policy import Policy as PolicyModel
from models.tool import Tool as ToolModel


async def seed_data():
    """Seed initial data for the decision engine"""
    # Create async engine
    engine = create_async_engine(
        settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
        echo=False
    )
    
    # Create session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        # Seed 6061-T6 Aluminum
        material_6061 = MaterialModel(
            id="6061-t6-aluminum",
            name="6061-T6 Aluminum",
            category="aluminum",
            properties={
                "hardness_hb": 95,
                "machinability_index": 85,
                "base_sfm": 500,
                "sfm_range_min": 300,
                "sfm_range_max": 800,
                "chip_type": "continuous",
                "work_hardening": False,
                "abrasiveness": 0.5,
                "built_up_edge_tendency": 0.3
            },
            description="Common aerospace and general purpose aluminum alloy",
            common_applications=["Aerospace", "Automotive", "General fabrication"]
        )
        session.add(material_6061)
        
        # Seed generic CNC mill
        machine_generic = MachineModel(
            id="generic-cnc-mill",
            name="Generic CNC Mill",
            type="mill",
            capabilities={
                "max_rpm": 24000,
                "min_rpm": 100,
                "spindle_power_kw": 3.7,
                "spindle_torque_nm": 10.0,
                "max_feedrate_mm_per_min": 10000,
                "min_feedrate_mm_per_min": 1,
                "rigidity_factor": 7.0,
                "accuracy_mm": 0.01,
                "max_tool_diameter_mm": 50,
                "max_depth_of_cut_mm": 50
            },
            manufacturer="Generic",
            description="Standard 3-axis CNC mill"
        )
        session.add(machine_generic)
        
        # Seed policies
        safety_policy = PolicyModel(
            id="safety-first",
            name="Safety First",
            type="safety",
            weights={"tool_life": 0.0, "time": 0.0, "safety": 1.0},
            rules={},
            priority=1,
            description="Maximum safety, conservative parameters"
        )
        session.add(safety_policy)
        
        tool_life_policy = PolicyModel(
            id="tool-life-optimization",
            name="Tool Life Optimization",
            type="tool_life",
            weights={"tool_life": 1.0, "time": 0.0, "safety": 0.0},
            rules={},
            priority=50,
            description="Maximize tool life with lower SFM and feedrates"
        )
        session.add(tool_life_policy)
        
        time_policy = PolicyModel(
            id="time-optimization",
            name="Time Optimization",
            type="time",
            weights={"tool_life": 0.0, "time": 1.0, "safety": 0.0},
            rules={},
            priority=50,
            description="Maximize material removal rate to minimize cycle time"
        )
        session.add(time_policy)
        
        balanced_policy = PolicyModel(
            id="balanced",
            name="Balanced",
            type="balanced",
            weights={"tool_life": 0.33, "time": 0.33, "safety": 0.34},
            rules={},
            priority=100,
            description="Balance tool life, time, and safety"
        )
        session.add(balanced_policy)
        
        # Seed example Helical endmill (6mm)
        helical_tool = ToolModel(
            id="helical-endmill-6mm",
            name="6mm End Mill",
            vendor="Helical",
            type="End Mill",
            geometry={
                "diameter": 6.0,
                "flute_length": 12.0,
                "overall_length": 50.0,
                "flute_count": 4,
                "helix_angle": 30.0,
                "corner_radius": 0.5
            },
            limits={
                "max_sfm": 800,
                "max_rpm": 24000,
                "max_feedrate_mm_per_min": 5000,
                "max_chip_load_mm": 0.15,
                "max_depth_of_cut_mm": 12.0
            }
        )
        session.add(helical_tool)
        
        await session.commit()
        print("✓ Seeded materials, machines, policies, and example tool")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_data())

