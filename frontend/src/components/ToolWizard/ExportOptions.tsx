'use client';

import { Tool } from '@/types/tool';
import { ArrowDownTrayIcon, DocumentArrowDownIcon, LinkIcon } from '@heroicons/react/24/outline';
import { useState } from 'react';
import toast from 'react-hot-toast';

interface ExportOptionsProps {
  tool: Tool;
  onSave: () => void;
}

export default function ExportOptions({ tool, onSave }: ExportOptionsProps) {
  const [exportFormat, setExportFormat] = useState<'fusion_json' | 'csv'>('fusion_json');
  const [exportUnits, setExportUnits] = useState<'metric' | 'imperial'>('metric');
  const [isExporting, setIsExporting] = useState(false);

  const handleExport = async () => {
    setIsExporting(true);
    try {
      // TODO: Implement actual export logic
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      toast.success(`Tool exported as ${exportFormat.toUpperCase()} successfully!`);
    } catch (error) {
      toast.error('Export failed. Please try again.');
    } finally {
      setIsExporting(false);
    }
  };

  const handleSaveAndExport = () => {
    onSave();
    handleExport();
  };

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h3 className="text-lg font-medium text-gray-900 mb-2">Export Options</h3>
        <p className="text-sm text-gray-500">
          Choose your export format and save your tool profile
        </p>
      </div>

      {/* Export Format Selection */}
      <div className="card">
        <div className="card-header">
          <h4 className="font-medium text-gray-900">Export Format</h4>
        </div>
        <div className="card-content">
          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              <input
                type="radio"
                id="fusion_json"
                name="exportFormat"
                value="fusion_json"
                checked={exportFormat === 'fusion_json'}
                onChange={(e) => setExportFormat(e.target.value as 'fusion_json')}
                className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300"
              />
              <label htmlFor="fusion_json" className="flex items-center">
                <DocumentArrowDownIcon className="h-5 w-5 text-gray-400 mr-2" />
                <div>
                  <div className="font-medium text-gray-900">Fusion 360 .tools JSON</div>
                  <div className="text-sm text-gray-500">Direct import into Fusion 360 tool library</div>
                </div>
              </label>
            </div>
            
            <div className="flex items-center space-x-3">
              <input
                type="radio"
                id="csv"
                name="exportFormat"
                value="csv"
                checked={exportFormat === 'csv'}
                onChange={(e) => setExportFormat(e.target.value as 'csv')}
                className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300"
              />
              <label htmlFor="csv" className="flex items-center">
                <DocumentArrowDownIcon className="h-5 w-5 text-gray-400 mr-2" />
                <div>
                  <div className="font-medium text-gray-900">CSV Spreadsheet</div>
                  <div className="text-sm text-gray-500">Compatible with Excel and other tools</div>
                </div>
              </label>
            </div>
          </div>
        </div>
      </div>

      {/* Units Selection */}
      <div className="card">
        <div className="card-header">
          <h4 className="font-medium text-gray-900">Units</h4>
        </div>
        <div className="card-content">
          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              <input
                type="radio"
                id="metric"
                name="exportUnits"
                value="metric"
                checked={exportUnits === 'metric'}
                onChange={(e) => setExportUnits(e.target.value as 'metric')}
                className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300"
              />
              <label htmlFor="metric" className="font-medium text-gray-900">
                Metric (mm)
              </label>
            </div>
            
            <div className="flex items-center space-x-3">
              <input
                type="radio"
                id="imperial"
                name="exportUnits"
                value="imperial"
                checked={exportUnits === 'imperial'}
                onChange={(e) => setExportUnits(e.target.value as 'imperial')}
                className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300"
              />
              <label htmlFor="imperial" className="font-medium text-gray-900">
                Imperial (inches)
              </label>
            </div>
          </div>
        </div>
      </div>

      {/* Export Preview */}
      <div className="card">
        <div className="card-header">
          <h4 className="font-medium text-gray-900">Export Preview</h4>
        </div>
        <div className="card-content">
          <div className="bg-gray-50 rounded-md p-4">
            <pre className="text-xs text-gray-600 overflow-x-auto">
              {exportFormat === 'fusion_json' ? (
                `{
  "toolType": "${tool.type}",
  "diameter": ${tool.geometry.diameter},
  "fluteLength": ${tool.geometry.fluteLength},
  "overallLength": ${tool.geometry.overallLength},
  "vendor": "${tool.vendor}",
  "name": "${tool.name}"
}`
              ) : (
                `Tool Name,Vendor,Type,Diameter,Flute Length,Overall Length
"${tool.name}","${tool.vendor}","${tool.type}",${tool.geometry.diameter},${tool.geometry.fluteLength},${tool.geometry.overallLength}`
              )}
            </pre>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex space-x-4">
        <button
          onClick={handleExport}
          disabled={isExporting}
          className="btn btn-outline btn-md flex-1"
        >
          <ArrowDownTrayIcon className="h-5 w-5 mr-2" />
          {isExporting ? 'Exporting...' : 'Export Only'}
        </button>
        
        <button
          onClick={handleSaveAndExport}
          disabled={isExporting}
          className="btn btn-primary btn-md flex-1"
        >
          <LinkIcon className="h-5 w-5 mr-2" />
          {isExporting ? 'Saving...' : 'Save & Export'}
        </button>
      </div>

      {/* Export Instructions */}
      <div className="card">
        <div className="card-header">
          <h4 className="font-medium text-gray-900">Import Instructions</h4>
        </div>
        <div className="card-content">
          <div className="text-sm text-gray-600 space-y-2">
            {exportFormat === 'fusion_json' ? (
              <>
                <p><strong>For Fusion 360:</strong></p>
                <ol className="list-decimal list-inside space-y-1 ml-4">
                  <li>Open Fusion 360 and go to Manufacture workspace</li>
                  <li>Navigate to Tool Library</li>
                  <li>Click "Import" and select the downloaded .tools file</li>
                  <li>Your tool will be added to the library</li>
                </ol>
              </>
            ) : (
              <>
                <p><strong>For CSV Import:</strong></p>
                <ol className="list-decimal list-inside space-y-1 ml-4">
                  <li>Open the CSV file in Excel or similar application</li>
                  <li>Review and modify data as needed</li>
                  <li>Import into your preferred CAM software</li>
                </ol>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
