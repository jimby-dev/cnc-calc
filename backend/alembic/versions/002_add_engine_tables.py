"""Add engine tables

Revision ID: 002_add_engine_tables
Revises: 001_initial
Create Date: 2024-01-15 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '002_add_engine_tables'
down_revision: Union[str, None] = '001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create materials table
    op.create_table(
        'materials',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('properties', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('common_applications', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_index('ix_materials_id', 'materials', ['id'], unique=False)
    op.create_index('ix_materials_name', 'materials', ['name'], unique=False)
    op.create_index('ix_materials_category', 'materials', ['category'], unique=False)
    op.create_index('ix_materials_is_deleted', 'materials', ['is_deleted'], unique=False)
    
    # Create machines table
    op.create_table(
        'machines',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('capabilities', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('manufacturer', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_index('ix_machines_id', 'machines', ['id'], unique=False)
    op.create_index('ix_machines_name', 'machines', ['name'], unique=False)
    op.create_index('ix_machines_type', 'machines', ['type'], unique=False)
    op.create_index('ix_machines_is_deleted', 'machines', ['is_deleted'], unique=False)
    
    # Create policies table
    op.create_table(
        'policies',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('weights', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('rules', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.Column('priority', sa.Integer(), nullable=False, server_default='100'),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_index('ix_policies_id', 'policies', ['id'], unique=False)
    op.create_index('ix_policies_name', 'policies', ['name'], unique=False)
    op.create_index('ix_policies_type', 'policies', ['type'], unique=False)
    op.create_index('ix_policies_priority', 'policies', ['priority'], unique=False)
    op.create_index('ix_policies_is_deleted', 'policies', ['is_deleted'], unique=False)
    
    # Create recommendations table (optional, for storing recommendation history)
    op.create_table(
        'recommendations',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('scenario_id', sa.String(), nullable=True),
        sa.Column('spindle_rpm', sa.Float(), nullable=False),
        sa.Column('feedrate_mm_per_min', sa.Float(), nullable=False),
        sa.Column('feedrate_mm_per_rev', sa.Float(), nullable=True),
        sa.Column('chip_load_mm', sa.Float(), nullable=True),
        sa.Column('surface_speed_m_per_min', sa.Float(), nullable=False),
        sa.Column('surface_speed_sfm', sa.Float(), nullable=True),
        sa.Column('material_removal_rate_mm3_per_min', sa.Float(), nullable=True),
        sa.Column('signals', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False),
        sa.Column('trace', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('input_context', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_index('ix_recommendations_id', 'recommendations', ['id'], unique=False)
    op.create_index('ix_recommendations_scenario_id', 'recommendations', ['scenario_id'], unique=False)
    op.create_index('ix_recommendations_created_at', 'recommendations', ['created_at'], unique=False)
    op.create_index('ix_recommendations_is_deleted', 'recommendations', ['is_deleted'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_recommendations_is_deleted', table_name='recommendations')
    op.drop_index('ix_recommendations_created_at', table_name='recommendations')
    op.drop_index('ix_recommendations_scenario_id', table_name='recommendations')
    op.drop_index('ix_recommendations_id', table_name='recommendations')
    op.drop_table('recommendations')
    
    op.drop_index('ix_policies_is_deleted', table_name='policies')
    op.drop_index('ix_policies_priority', table_name='policies')
    op.drop_index('ix_policies_type', table_name='policies')
    op.drop_index('ix_policies_name', table_name='policies')
    op.drop_index('ix_policies_id', table_name='policies')
    op.drop_table('policies')
    
    op.drop_index('ix_machines_is_deleted', table_name='machines')
    op.drop_index('ix_machines_type', table_name='machines')
    op.drop_index('ix_machines_name', table_name='machines')
    op.drop_index('ix_machines_id', table_name='machines')
    op.drop_table('machines')
    
    op.drop_index('ix_materials_is_deleted', table_name='materials')
    op.drop_index('ix_materials_category', table_name='materials')
    op.drop_index('ix_materials_name', table_name='materials')
    op.drop_index('ix_materials_id', table_name='materials')
    op.drop_table('materials')

