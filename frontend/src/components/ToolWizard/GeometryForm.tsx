'use client';

import { Tool, ToolGeometry, ToolType } from '@/types/tool';
import { useEffect, useState } from 'react';

interface GeometryFormProps {
  toolType: ToolType;
  geometry: ToolGeometry;
  metadata: Partial<Tool>;
  onGeometryChange: (geometry: ToolGeometry) => void;
  onMetadataChange: (metadata: Partial<Tool>) => void;
}

export default function GeometryForm({
  toolType,
  geometry,
  metadata,
  onGeometryChange,
  onMetadataChange
}: GeometryFormProps) {
  const [formData, setFormData] = useState({
    name: metadata.name || '',
    vendor: metadata.vendor || '',
    diameter: (geometry as any)?.diameter || '',
    fluteCount: (geometry as any)?.fluteCount || '',
    helixAngle: (geometry as any)?.helixAngle || '',
    fluteLength: (geometry as any)?.fluteLength || '',
    lengthOfCut: (geometry as any)?.lengthOfCut || '',
    overallLength: (geometry as any)?.overallLength || '',
    cornerRadius: (geometry as any)?.cornerRadius || '',
    tipRadius: (geometry as any)?.tipRadius || '',
    includedAngle: (geometry as any)?.includedAngle || '',
    tipFlat: (geometry as any)?.tipFlat || '',
    shankDiameter: (geometry as any)?.shankDiameter || '',
    pointAngle: (geometry as any)?.pointAngle || '',
    leadAngle: (geometry as any)?.leadAngle || '',
    pitch: (geometry as any)?.pitch || '',
    maxThreadLength: (geometry as any)?.maxThreadLength || '',
  });

  useEffect(() => {
    // Update metadata when form data changes
    onMetadataChange({
      name: formData.name,
      vendor: formData.vendor,
    });

    // Update geometry based on tool type
    const newGeometry = createGeometryFromFormData(toolType, formData);
    onGeometryChange(newGeometry);
  }, [formData, toolType, onGeometryChange, onMetadataChange]);

  const createGeometryFromFormData = (type: ToolType, data: any): ToolGeometry => {
    const baseGeometry = {
      diameter: parseFloat(data.diameter) || 0,
      fluteLength: parseFloat(data.fluteLength) || 0,
      overallLength: parseFloat(data.overallLength) || 0,
    };

    switch (type) {
      case 'end_mill':
        return {
          ...baseGeometry,
          fluteCount: parseInt(data.fluteCount) || 0,
          helixAngle: parseFloat(data.helixAngle) || 0,
          lengthOfCut: parseFloat(data.lengthOfCut) || 0,
          cornerRadius: parseFloat(data.cornerRadius) || 0,
        };
      case 'ball_end_mill':
        return {
          ...baseGeometry,
          fluteCount: parseInt(data.fluteCount) || 0,
          tipRadius: parseFloat(data.tipRadius) || 0,
        };
      case 'chamfer':
        return {
          ...baseGeometry,
          includedAngle: parseFloat(data.includedAngle) || 0,
          tipFlat: parseFloat(data.tipFlat) || 0,
          shankDiameter: parseFloat(data.shankDiameter) || 0,
        };
      case 'drill':
        return {
          ...baseGeometry,
          pointAngle: parseFloat(data.pointAngle) || 0,
        };
      case 'reamer':
        return {
          ...baseGeometry,
          leadAngle: parseFloat(data.leadAngle) || 0,
        };
      case 'thread_mill':
        return {
          ...baseGeometry,
          pitch: parseFloat(data.pitch) || 0,
          maxThreadLength: parseFloat(data.maxThreadLength) || 0,
        };
      default:
        return baseGeometry;
    }
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const renderField = (field: string, label: string, type: string = 'text', placeholder?: string) => (
    <div>
      <label className="label">{label}</label>
      <input
        type={type}
        value={formData[field as keyof typeof formData]}
        onChange={(e) => handleInputChange(field, e.target.value)}
        placeholder={placeholder}
        className="input mt-1"
      />
    </div>
  );

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h3 className="text-lg font-medium text-gray-900 mb-2">Define Tool Geometry</h3>
        <p className="text-sm text-gray-500">
          Enter the specific dimensions for your {toolType.replace('_', ' ')} tool
        </p>
      </div>

      {/* Basic Information */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {renderField('name', 'Tool Name', 'text', 'e.g., 1/4" End Mill')}
        {renderField('vendor', 'Vendor', 'text', 'e.g., Kennametal')}
      </div>

      {/* Common Geometry Fields */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {renderField('diameter', 'Diameter (mm)', 'number', '0.0')}
        {renderField('fluteLength', 'Flute Length (mm)', 'number', '0.0')}
        {renderField('overallLength', 'Overall Length (mm)', 'number', '0.0')}
      </div>

      {/* Tool-specific fields */}
      {toolType === 'end_mill' && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {renderField('fluteCount', 'Flute Count', 'number', '2')}
          {renderField('helixAngle', 'Helix Angle (°)', 'number', '30')}
          {renderField('lengthOfCut', 'Length of Cut (mm)', 'number', '0.0')}
          {renderField('cornerRadius', 'Corner Radius (mm)', 'number', '0.0')}
        </div>
      )}

      {toolType === 'ball_end_mill' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {renderField('fluteCount', 'Flute Count', 'number', '2')}
          {renderField('tipRadius', 'Tip Radius (mm)', 'number', '0.0')}
        </div>
      )}

      {toolType === 'chamfer' && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {renderField('includedAngle', 'Included Angle (°)', 'number', '90')}
          {renderField('tipFlat', 'Tip Flat (mm)', 'number', '0.0')}
          {renderField('shankDiameter', 'Shank Diameter (mm)', 'number', '0.0')}
        </div>
      )}

      {toolType === 'drill' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {renderField('pointAngle', 'Point Angle (°)', 'number', '118')}
        </div>
      )}

      {toolType === 'reamer' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {renderField('leadAngle', 'Lead Angle (°)', 'number', '0')}
        </div>
      )}

      {toolType === 'thread_mill' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {renderField('pitch', 'Pitch (mm)', 'number', '0.0')}
          {renderField('maxThreadLength', 'Max Thread Length (mm)', 'number', '0.0')}
        </div>
      )}

      {/* Visual Preview Placeholder */}
      <div className="mt-8 p-6 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
        <div className="text-center">
          <div className="text-gray-400 mb-2">
            <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h4 className="text-sm font-medium text-gray-900 mb-1">Tool Preview</h4>
          <p className="text-xs text-gray-500">
            Dynamic SVG visualization will appear here as you enter dimensions
          </p>
        </div>
      </div>
    </div>
  );
}
