"""Initial schema

Revision ID: 001_initial
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create tools table
    op.create_table(
        'tools',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('vendor', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('geometry', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('limits', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default='false'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for tools table
    op.create_index(op.f('ix_tools_id'), 'tools', ['id'], unique=False)
    op.create_index(op.f('ix_tools_name'), 'tools', ['name'], unique=False)
    op.create_index(op.f('ix_tools_vendor'), 'tools', ['vendor'], unique=False)
    op.create_index(op.f('ix_tools_type'), 'tools', ['type'], unique=False)
    op.create_index('ix_tools_created_at', 'tools', ['created_at'], unique=False)
    
    # Create tool_exports table
    op.create_table(
        'tool_exports',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('tool_id', sa.String(), nullable=False),
        sa.Column('export_format', sa.String(), nullable=False),
        sa.Column('export_units', sa.String(), nullable=False),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('export_data', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for tool_exports table
    op.create_index(op.f('ix_tool_exports_id'), 'tool_exports', ['id'], unique=False)
    op.create_index(op.f('ix_tool_exports_tool_id'), 'tool_exports', ['tool_id'], unique=False)
    op.create_index('ix_tool_exports_created_at', 'tool_exports', ['created_at'], unique=False)


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_tool_exports_created_at', table_name='tool_exports')
    op.drop_index(op.f('ix_tool_exports_tool_id'), table_name='tool_exports')
    op.drop_index(op.f('ix_tool_exports_id'), table_name='tool_exports')
    op.drop_index('ix_tools_created_at', table_name='tools')
    op.drop_index(op.f('ix_tools_type'), table_name='tools')
    op.drop_index(op.f('ix_tools_vendor'), table_name='tools')
    op.drop_index(op.f('ix_tools_name'), table_name='tools')
    op.drop_index(op.f('ix_tools_id'), table_name='tools')
    
    # Drop tables
    op.drop_table('tool_exports')
    op.drop_table('tools')

