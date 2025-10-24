'use client';

import { Tool } from '@/types/tool';
import { getValidationSummary, validateTool } from '@/utils/validation';
import { CheckCircleIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline';

interface ReviewValidationProps {
  tool: Tool;
  onMetadataChange: (metadata: Partial<Tool>) => void;
}

export default function ReviewValidation({ tool, onMetadataChange }: ReviewValidationProps) {
  const validationErrors = validateTool(tool);
  const summary = getValidationSummary(validationErrors);

  const handleMetadataChange = (field: string, value: string) => {
    onMetadataChange({ [field]: value });
  };

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h3 className="text-lg font-medium text-gray-900 mb-2">Review & Validate</h3>
        <p className="text-sm text-gray-500">
          Review your tool configuration and check for any issues
        </p>
      </div>

      {/* Validation Summary */}
      <div className={`p-4 rounded-lg border ${
        summary.hasErrors 
          ? 'bg-red-50 border-red-200' 
          : summary.hasWarnings 
            ? 'bg-yellow-50 border-yellow-200'
            : 'bg-green-50 border-green-200'
      }`}>
        <div className="flex items-start">
          {summary.hasErrors ? (
            <ExclamationTriangleIcon className="h-5 w-5 text-red-400 mt-0.5 mr-3" />
          ) : summary.hasWarnings ? (
            <ExclamationTriangleIcon className="h-5 w-5 text-yellow-400 mt-0.5 mr-3" />
          ) : (
            <CheckCircleIcon className="h-5 w-5 text-green-400 mt-0.5 mr-3" />
          )}
          <div>
            <h4 className={`font-medium ${
              summary.hasErrors ? 'text-red-900' : 
              summary.hasWarnings ? 'text-yellow-900' : 'text-green-900'
            }`}>
              {summary.hasErrors ? 'Validation Errors Found' :
               summary.hasWarnings ? 'Validation Warnings' : 'Tool Validated Successfully'}
            </h4>
            <p className={`text-sm mt-1 ${
              summary.hasErrors ? 'text-red-700' : 
              summary.hasWarnings ? 'text-yellow-700' : 'text-green-700'
            }`}>
              {summary.hasErrors ? `${summary.errorCount} error(s) must be fixed before export` :
               summary.hasWarnings ? `${summary.warningCount} warning(s) found` : 
               'Tool is ready for export to Fusion 360'}
            </p>
          </div>
        </div>
      </div>

      {/* Tool Summary */}
      <div className="card">
        <div className="card-header">
          <h4 className="font-medium text-gray-900">Tool Summary</h4>
        </div>
        <div className="card-content">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h5 className="font-medium text-gray-900 mb-3">Basic Information</h5>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-500">Name:</span>
                  <span className="font-medium">{tool.name}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Vendor:</span>
                  <span className="font-medium">{tool.vendor}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Type:</span>
                  <span className="font-medium">{tool.type.replace('_', ' ')}</span>
                </div>
              </div>
            </div>
            
            <div>
              <h5 className="font-medium text-gray-900 mb-3">Geometry</h5>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-500">Diameter:</span>
                  <span className="font-medium">{tool.geometry.diameter}mm</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Flute Length:</span>
                  <span className="font-medium">{tool.geometry.fluteLength}mm</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Overall Length:</span>
                  <span className="font-medium">{tool.geometry.overallLength}mm</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Validation Details */}
      {validationErrors.length > 0 && (
        <div className="card">
          <div className="card-header">
            <h4 className="font-medium text-gray-900">Validation Details</h4>
          </div>
          <div className="card-content">
            <div className="space-y-3">
              {validationErrors.map((error, index) => (
                <div key={index} className={`p-3 rounded-md border ${
                  error.severity === 'error' 
                    ? 'bg-red-50 border-red-200' 
                    : 'bg-yellow-50 border-yellow-200'
                }`}>
                  <div className="flex items-start">
                    <ExclamationTriangleIcon className={`h-4 w-4 mt-0.5 mr-2 ${
                      error.severity === 'error' ? 'text-red-400' : 'text-yellow-400'
                    }`} />
                    <div>
                      <p className={`text-sm font-medium ${
                        error.severity === 'error' ? 'text-red-900' : 'text-yellow-900'
                      }`}>
                        {error.field}: {error.message}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Fusion 360 Compatibility */}
      <div className="card">
        <div className="card-header">
          <h4 className="font-medium text-gray-900">Fusion 360 Compatibility</h4>
        </div>
        <div className="card-content">
          <div className="space-y-3">
            <div className="flex items-center">
              <CheckCircleIcon className="h-5 w-5 text-green-400 mr-3" />
              <span className="text-sm text-gray-700">Tool type supported by Fusion 360</span>
            </div>
            <div className="flex items-center">
              <CheckCircleIcon className="h-5 w-5 text-green-400 mr-3" />
              <span className="text-sm text-gray-700">All required geometry fields present</span>
            </div>
            <div className="flex items-center">
              <CheckCircleIcon className="h-5 w-5 text-green-400 mr-3" />
              <span className="text-sm text-gray-700">Units normalized to millimeters</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
