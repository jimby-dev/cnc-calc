import { Tool } from '@/types/tool';
import { ArrowDownTrayIcon, ClipboardDocumentIcon } from '@heroicons/react/24/outline';
import React from 'react';
import toast from 'react-hot-toast';

interface ExportOptionsProps {
  tool: Tool;
}

const ExportOptions: React.FC<ExportOptionsProps> = ({ tool }) => {
  const handleExportJson = () => {
    // Placeholder for actual API call
    const json = JSON.stringify(tool, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${tool.name.replace(/\s/g, '_')}.tools.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast.success('Fusion .tools JSON exported!');
  };

  const handleExportCsv = () => {
    // Placeholder for actual API call
    const geometryData = tool.geometry || {};
    const headers = ['id', 'name', 'type', 'units', ...Object.keys(geometryData)];
    const values = [
      tool.id,
      tool.name,
      tool.type,
      tool.units,
      ...Object.values(geometryData),
    ];
    const csv = `${headers.join(',')}\n${values.join(',')}`;
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${tool.name.replace(/\s/g, '_')}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast.success('CSV exported!');
  };

  const handleCopyLink = () => {
    // Placeholder for generating a shareable link
    navigator.clipboard.writeText(`http://localhost:3000/tools/${tool.id}`)
      .then(() => toast.success('Tool link copied to clipboard!'))
      .catch(() => toast.error('Failed to copy link.'));
  };

  return (
    <div>
      <h4 className="text-md font-medium text-gray-900 mb-3">Export Options</h4>
      <div className="space-y-4">
        <button
          onClick={handleExportJson}
          className="w-full flex items-center justify-center px-4 py-2 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          <ArrowDownTrayIcon className="h-5 w-5 mr-2" /> Export Fusion .tools JSON
        </button>
        <button
          onClick={handleExportCsv}
          className="w-full flex items-center justify-center px-4 py-2 border border-transparent text-base font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          <ArrowDownTrayIcon className="h-5 w-5 mr-2" /> Export CSV
        </button>
        <button
          onClick={handleCopyLink}
          className="w-full flex items-center justify-center px-4 py-2 border border-transparent text-base font-medium rounded-md text-gray-700 bg-gray-100 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
        >
          <ClipboardDocumentIcon className="h-5 w-5 mr-2" /> Copy Shareable Link
        </button>
      </div>
    </div>
  );
};

export default ExportOptions;