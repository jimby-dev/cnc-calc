'use client';

import { Tool, ValidationError } from '@/types/tool';
import { validateTool } from '@/utils/validation';
import {
  ArrowDownTrayIcon,
  ExclamationTriangleIcon,
  PencilIcon,
  TrashIcon
} from '@heroicons/react/24/outline';
import { useState } from 'react';
import toast from 'react-hot-toast';

interface ToolCardProps {
  tool: Tool;
  onDelete: (toolId: string) => void;
  onEdit?: (tool: Tool) => void;
}

export default function ToolCard({ tool, onDelete, onEdit }: ToolCardProps) {
  const [isExporting, setIsExporting] = useState(false);
  const [validationErrors, setValidationErrors] = useState<ValidationError[]>([]);

  const handleExport = async (format: 'fusion_json' | 'csv') => {
    setIsExporting(true);
    try {
      // Validate tool before export
      const errors = validateTool(tool);
      setValidationErrors(errors);
      
      const blockingErrors = errors.filter(e => e.severity === 'error');
      if (blockingErrors.length > 0) {
        toast.error('Tool has validation errors. Please fix before exporting.');
        return;
      }

      // TODO: Implement actual export logic
      toast.success(`Exporting ${tool.name} as ${format}...`);
      
      // Simulate export delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      toast.success('Export completed successfully!');
    } catch (error) {
      toast.error('Export failed. Please try again.');
    } finally {
      setIsExporting(false);
    }
  };

  const handleDelete = () => {
    if (window.confirm(`Are you sure you want to delete "${tool.name}"?`)) {
      onDelete(tool.id);
      toast.success('Tool deleted successfully');
    }
  };

  const getToolTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      end_mill: 'End Mill',
      ball_end_mill: 'Ball End Mill',
      chamfer: 'Chamfer',
      drill: 'Drill',
      reamer: 'Reamer',
      thread_mill: 'Thread Mill',
    };
    return labels[type] || type;
  };

  const getToolIcon = (type: string) => {
    // Simple icon representation based on tool type
    return '🔧';
  };

  return (
    <div className="card hover:shadow-md transition-shadow">
      <div className="card-header">
        <div className="flex items-start justify-between">
          <div className="flex items-center space-x-3">
            <span className="text-2xl">{getToolIcon(tool.type)}</span>
            <div>
              <h3 className="font-semibold text-gray-900">{tool.name}</h3>
              <p className="text-sm text-gray-500">{tool.vendor}</p>
            </div>
          </div>
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
            {getToolTypeLabel(tool.type)}
          </span>
        </div>
      </div>

      <div className="card-content">
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-gray-500">Diameter:</span>
            <span className="font-medium">{tool.geometry.diameter}mm</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-gray-500">Flute Length:</span>
            <span className="font-medium">{tool.geometry.fluteLength}mm</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-gray-500">Overall Length:</span>
            <span className="font-medium">{tool.geometry.overallLength}mm</span>
          </div>
          
          {/* Tool-specific geometry */}
          {'fluteCount' in tool.geometry && (
            <div className="flex justify-between text-sm">
              <span className="text-gray-500">Flutes:</span>
              <span className="font-medium">{tool.geometry.fluteCount}</span>
            </div>
          )}
          
          {'helixAngle' in tool.geometry && (
            <div className="flex justify-between text-sm">
              <span className="text-gray-500">Helix Angle:</span>
              <span className="font-medium">{tool.geometry.helixAngle}°</span>
            </div>
          )}
        </div>

        {/* Validation warnings */}
        {validationErrors.length > 0 && (
          <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
            <div className="flex items-start">
              <ExclamationTriangleIcon className="h-5 w-5 text-yellow-400 mt-0.5 mr-2" />
              <div className="text-sm">
                <p className="font-medium text-yellow-800">Validation Issues</p>
                <ul className="mt-1 text-yellow-700">
                  {validationErrors.map((error, index) => (
                    <li key={index} className="text-xs">
                      {error.message}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="card-footer">
        <div className="flex space-x-2 w-full">
          <button
            onClick={() => handleExport('fusion_json')}
            disabled={isExporting}
            className="btn btn-primary btn-sm flex-1"
          >
            <ArrowDownTrayIcon className="h-4 w-4 mr-1" />
            Export
          </button>
          <button
            onClick={() => onEdit?.(tool)}
            className="btn btn-outline btn-sm"
          >
            <PencilIcon className="h-4 w-4" />
          </button>
          <button
            onClick={handleDelete}
            className="btn btn-outline btn-sm text-red-600 hover:text-red-700 hover:bg-red-50"
          >
            <TrashIcon className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
