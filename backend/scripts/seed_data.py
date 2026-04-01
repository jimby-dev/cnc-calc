"""
Seed script for initial engine data — SQLite edition.
Creates tables if they don't exist, then upserts materials, machines,
policies, and an example tool. Safe to run multiple times.
"""
import asyncio
import sys
from pathlib import Path

# Ensure the backend directory is on sys.path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import select
from app.core.database import engine, AsyncSessionLocal, Base
from models.material import Material as MaterialModel
from models.machine import Machine as MachineModel
from models.policy import Policy as PolicyModel
from models.tool import Tool as ToolModel


# ---------------------------------------------------------------------------
# Data definitions
# ---------------------------------------------------------------------------

MATERIALS = [
    dict(
        id="6061-t6-aluminum",
        name="6061-T6 Aluminum",
        category="aluminum",
        properties=dict(
            hardness_hb=95,
            machinability_index=85,
            thermal_conductivity=167.0,
            base_sfm=500,
            sfm_range_min=300,
            sfm_range_max=800,
            chip_type="continuous",
            work_hardening=False,
            abrasiveness=0.5,
            built_up_edge_tendency=0.3,
        ),
        description="Common aerospace and general-purpose aluminum alloy",
        common_applications=["Aerospace", "Automotive", "General fabrication"],
    ),
    dict(
        id="mild-steel-1018",
        name="Mild Steel 1018",
        category="steel",
        properties=dict(
            hardness_hb=126,
            machinability_index=58,
            thermal_conductivity=51.9,
            base_sfm=200,
            sfm_range_min=100,
            sfm_range_max=350,
            chip_type="continuous",
            work_hardening=False,
            abrasiveness=1.5,
            built_up_edge_tendency=1.0,
        ),
        description="Low-carbon steel, easy to machine and weld",
        common_applications=["Shafts", "Pins", "General structural parts"],
    ),
    dict(
        id="304-stainless-steel",
        name="304 Stainless Steel",
        category="stainless_steel",
        properties=dict(
            hardness_hb=160,
            machinability_index=36,
            thermal_conductivity=16.2,
            base_sfm=120,
            sfm_range_min=60,
            sfm_range_max=200,
            chip_type="stringy",
            work_hardening=True,
            abrasiveness=2.5,
            built_up_edge_tendency=3.0,
        ),
        description="Austenitic stainless steel; work-hardens and runs hot",
        common_applications=["Food equipment", "Medical devices", "Marine hardware"],
    ),
    dict(
        id="titanium-ti6al4v",
        name="Titanium Ti-6Al-4V",
        category="titanium",
        properties=dict(
            hardness_hb=334,
            machinability_index=22,
            thermal_conductivity=6.7,
            melting_point=1660.0,
            base_sfm=80,
            sfm_range_min=40,
            sfm_range_max=150,
            chip_type="segmented",
            work_hardening=True,
            abrasiveness=4.0,
            built_up_edge_tendency=2.0,
        ),
        description="Grade 5 titanium alloy; high strength-to-weight, poor thermal conductivity",
        common_applications=["Aerospace structures", "Medical implants", "High-performance fasteners"],
    ),
    dict(
        id="hdpe-plastic",
        name="HDPE Plastic",
        category="plastic",
        properties=dict(
            machinability_index=95,
            thermal_conductivity=0.45,
            melting_point=130.0,
            base_sfm=800,
            sfm_range_min=500,
            sfm_range_max=1500,
            chip_type="continuous",
            work_hardening=False,
            abrasiveness=0.1,
            built_up_edge_tendency=0.1,
        ),
        description="High-density polyethylene; very easy to machine, low friction",
        common_applications=["Cutting boards", "Bearings", "Wear parts", "Fluid handling"],
    ),
    dict(
        id="carbon-fiber-composite",
        name="Carbon Fiber Composite (CFRP)",
        category="composite",
        properties=dict(
            machinability_index=30,
            thermal_conductivity=5.0,
            base_sfm=400,
            sfm_range_min=200,
            sfm_range_max=700,
            chip_type="segmented",
            work_hardening=False,
            abrasiveness=8.0,
            built_up_edge_tendency=0.1,
        ),
        description="Carbon-fiber-reinforced polymer; highly abrasive, requires sharp tooling",
        common_applications=["Aerospace panels", "Racing components", "Drone frames"],
    ),
]

MACHINES = [
    dict(
        id="generic-cnc-mill",
        name="Generic CNC Mill",
        type="mill",
        capabilities=dict(
            max_rpm=24000, min_rpm=100,
            spindle_power_kw=3.7, spindle_torque_nm=10.0,
            max_feedrate_mm_per_min=10000, min_feedrate_mm_per_min=1,
            rigidity_factor=7.0, accuracy_mm=0.01,
            max_tool_diameter_mm=50, max_depth_of_cut_mm=50,
        ),
        manufacturer="Generic",
        description="Standard 3-axis CNC mill — good all-rounder",
    ),
    dict(
        id="hobby-desktop-mill",
        name="Hobby Desktop Mill",
        type="mill",
        capabilities=dict(
            max_rpm=26000, min_rpm=5000,
            spindle_power_kw=0.4,
            max_feedrate_mm_per_min=1800, min_feedrate_mm_per_min=10,
            rigidity_factor=3.5, accuracy_mm=0.05,
            max_tool_diameter_mm=12, max_depth_of_cut_mm=10,
        ),
        manufacturer="Bantam Tools",
        description="Low-rigidity desktop mill suited for aluminium, plastics, and PCBs",
    ),
    dict(
        id="production-vmc",
        name="Production VMC (Haas VF-2 class)",
        type="mill",
        capabilities=dict(
            max_rpm=8100, min_rpm=50,
            spindle_power_kw=22.4, spindle_torque_nm=122.0,
            max_feedrate_mm_per_min=25400, min_feedrate_mm_per_min=1,
            rigidity_factor=9.5, accuracy_mm=0.005,
            max_tool_diameter_mm=100, max_depth_of_cut_mm=100,
        ),
        manufacturer="Haas",
        description="High-rigidity VMC capable of heavy steel and titanium cuts",
    ),
    dict(
        id="cnc-lathe",
        name="CNC Turning Lathe",
        type="lathe",
        capabilities=dict(
            max_rpm=4000, min_rpm=100,
            spindle_power_kw=5.6, spindle_torque_nm=90.0,
            max_feedrate_mm_per_min=5000, min_feedrate_mm_per_min=1,
            rigidity_factor=8.0, accuracy_mm=0.01,
            max_depth_of_cut_mm=5,
        ),
        manufacturer="Generic",
        description="2-axis CNC turning centre for round bar stock",
    ),
    dict(
        id="cnc-router",
        name="CNC Wood/Composite Router",
        type="router",
        capabilities=dict(
            max_rpm=24000, min_rpm=8000,
            spindle_power_kw=2.2,
            max_feedrate_mm_per_min=5000, min_feedrate_mm_per_min=100,
            rigidity_factor=3.0, accuracy_mm=0.1,
            max_tool_diameter_mm=25, max_depth_of_cut_mm=40,
        ),
        manufacturer="Generic",
        description="Low-rigidity gantry router for wood, MDF, HDPE, and composites",
    ),
]

POLICIES = [
    dict(
        id="safety-first",
        name="Safety First",
        type="safety",
        weights=dict(tool_life=0.0, time=0.0, safety=1.0),
        rules={},
        priority=1,
        description="Maximum safety — conservative parameters that prioritise avoiding tool breakage",
    ),
    dict(
        id="tool-life-optimization",
        name="Tool Life Optimization",
        type="tool_life",
        weights=dict(tool_life=1.0, time=0.0, safety=0.0),
        rules={},
        priority=50,
        description="Extend tool life by running lower SFM and lighter chip loads",
    ),
    dict(
        id="time-optimization",
        name="Time Optimization",
        type="time",
        weights=dict(tool_life=0.0, time=1.0, safety=0.0),
        rules={},
        priority=50,
        description="Maximise MRR to minimise cycle time",
    ),
    dict(
        id="balanced",
        name="Balanced",
        type="balanced",
        weights=dict(tool_life=0.33, time=0.33, safety=0.34),
        rules={},
        priority=100,
        description="Balance tool life, cycle time, and safety equally",
    ),
]

TOOLS = [
    dict(
        id="helical-endmill-6mm",
        name="6mm End Mill",
        vendor="Helical",
        type="End Mill",
        geometry=dict(
            diameter=6.0, flute_length=12.0, overall_length=50.0,
            flute_count=4, helix_angle=30.0, corner_radius=0.5,
        ),
        limits=dict(
            max_sfm=800, max_rpm=24000,
            max_feedrate_mm_per_min=5000,
            max_chip_load_mm=0.15,
            max_depth_of_cut_mm=12.0,
        ),
    ),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def _upsert(session, model_cls, records: list[dict]) -> tuple[int, int]:
    """Insert records that don't already exist. Returns (inserted, skipped)."""
    inserted = skipped = 0
    for rec in records:
        existing = await session.get(model_cls, rec["id"])
        if existing is None:
            session.add(model_cls(**rec))
            inserted += 1
        else:
            skipped += 1
    return inserted, skipped


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def seed_data() -> None:
    # Ensure all tables exist (idempotent)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Tables verified / created")

    async with AsyncSessionLocal() as session:
        ins, skip = await _upsert(session, MaterialModel, MATERIALS)
        print(f"  Materials  — inserted {ins}, skipped {skip}")

        ins, skip = await _upsert(session, MachineModel, MACHINES)
        print(f"  Machines   — inserted {ins}, skipped {skip}")

        ins, skip = await _upsert(session, PolicyModel, POLICIES)
        print(f"  Policies   — inserted {ins}, skipped {skip}")

        ins, skip = await _upsert(session, ToolModel, TOOLS)
        print(f"  Tools      — inserted {ins}, skipped {skip}")

        await session.commit()

    print("✓ Seed complete")


if __name__ == "__main__":
    asyncio.run(seed_data())
