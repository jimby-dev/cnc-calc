-- Database initialization script for CNC Calculator
-- This script creates the database and initial tables

-- Create database (run as superuser)
-- CREATE DATABASE cnc_calc;

-- Create user (run as superuser)
-- CREATE USER cnc_user WITH PASSWORD 'cnc_password';
-- GRANT ALL PRIVILEGES ON DATABASE cnc_calc TO cnc_user;

-- Connect to cnc_calc database and run the following:

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create tools table
CREATE TABLE IF NOT EXISTS tools (
    id VARCHAR PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    name VARCHAR(100) NOT NULL,
    vendor VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    geometry JSONB NOT NULL,
    limits JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_deleted BOOLEAN DEFAULT FALSE
);

-- Create tool_exports table
CREATE TABLE IF NOT EXISTS tool_exports (
    id VARCHAR PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    tool_id VARCHAR NOT NULL REFERENCES tools(id) ON DELETE CASCADE,
    export_format VARCHAR(20) NOT NULL,
    export_units VARCHAR(10) NOT NULL,
    file_size INTEGER,
    export_data TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_tools_name ON tools(name);
CREATE INDEX IF NOT EXISTS idx_tools_vendor ON tools(vendor);
CREATE INDEX IF NOT EXISTS idx_tools_type ON tools(type);
CREATE INDEX IF NOT EXISTS idx_tools_created_at ON tools(created_at);
CREATE INDEX IF NOT EXISTS idx_tools_is_deleted ON tools(is_deleted);
CREATE INDEX IF NOT EXISTS idx_tool_exports_tool_id ON tool_exports(tool_id);
CREATE INDEX IF NOT EXISTS idx_tool_exports_created_at ON tool_exports(created_at);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
CREATE TRIGGER update_tools_updated_at 
    BEFORE UPDATE ON tools 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data
INSERT INTO tools (id, name, vendor, type, geometry, limits) VALUES
(
    'sample-end-mill-1',
    '1/4" Carbide End Mill',
    'Kennametal',
    'end_mill',
    '{
        "diameter": 6.35,
        "flute_count": 4,
        "helix_angle": 30,
        "flute_length": 12.7,
        "length_of_cut": 10.0,
        "overall_length": 50.8,
        "corner_radius": 0.0
    }',
    '{
        "sfm": 300,
        "stepdown": 1.0,
        "engagement": 50,
        "feed_rate": 500,
        "spindle_speed": 1500
    }'
),
(
    'sample-ball-mill-1',
    '1/8" Ball End Mill',
    'OSG',
    'ball_end_mill',
    '{
        "diameter": 3.175,
        "flute_count": 2,
        "tip_radius": 1.5875,
        "flute_length": 6.35,
        "overall_length": 38.1
    }',
    '{
        "sfm": 250,
        "stepdown": 0.5,
        "engagement": 30,
        "feed_rate": 300,
        "spindle_speed": 2500
    }'
),
(
    'sample-drill-1',
    '1/4" HSS Drill',
    'Cleveland',
    'drill',
    '{
        "diameter": 6.35,
        "point_angle": 118,
        "flute_length": 25.4,
        "overall_length": 76.2
    }',
    '{
        "sfm": 100,
        "feed_rate": 150,
        "spindle_speed": 500
    }'
)
ON CONFLICT (id) DO NOTHING;

-- Grant permissions to cnc_user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO cnc_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO cnc_user;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO cnc_user;
