'use client';

import ToolCard from '@/components/ToolCard';
import ToolWizard from '@/components/ToolWizard';
import { Tool } from '@/types/tool';
import { FunnelIcon, MagnifyingGlassIcon, PlusIcon } from '@heroicons/react/24/outline';
import { useState } from 'react';

export default function HomePage() {
  const [tools, setTools] = useState<Tool[]>([]);
  const [showWizard, setShowWizard] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState<string>('all');

  const filteredTools = tools.filter(tool => {
    const matchesSearch = tool.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         tool.vendor.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterType === 'all' || tool.type === filterType;
    return matchesSearch && matchesFilter;
  });

  const handleCreateTool = (tool: Tool) => {
    setTools(prev => [...prev, { ...tool, id: Date.now().toString() }]);
    setShowWizard(false);
  };

  const handleDeleteTool = (toolId: string) => {
    setTools(prev => prev.filter(tool => tool.id !== toolId));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">CNC Calculator</h1>
              <span className="ml-3 text-sm text-gray-500">Tool Management System</span>
            </div>
            <button
              onClick={() => setShowWizard(true)}
              className="btn btn-primary btn-md"
            >
              <PlusIcon className="h-5 w-5 mr-2" />
              Create Tool
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search and Filters */}
        <div className="mb-8">
          <div className="flex flex-col sm:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search tools by name or vendor..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="input pl-10"
                />
              </div>
            </div>
            <div className="flex gap-2">
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
                className="input w-48"
              >
                <option value="all">All Types</option>
                <option value="end_mill">End Mill</option>
                <option value="ball_end_mill">Ball End Mill</option>
                <option value="chamfer">Chamfer</option>
                <option value="drill">Drill</option>
                <option value="reamer">Reamer</option>
                <option value="thread_mill">Thread Mill</option>
              </select>
              <button className="btn btn-outline btn-md">
                <FunnelIcon className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>

        {/* Tools Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredTools.length === 0 ? (
            <div className="col-span-full text-center py-12">
              <div className="text-gray-400 mb-4">
                <svg className="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No tools found</h3>
              <p className="text-gray-500 mb-4">
                {tools.length === 0 
                  ? "Get started by creating your first tool profile."
                  : "Try adjusting your search or filter criteria."
                }
              </p>
              {tools.length === 0 && (
                <button
                  onClick={() => setShowWizard(true)}
                  className="btn btn-primary btn-md"
                >
                  <PlusIcon className="h-5 w-5 mr-2" />
                  Create Your First Tool
                </button>
              )}
            </div>
          ) : (
            filteredTools.map((tool) => (
              <ToolCard
                key={tool.id}
                tool={tool}
                onDelete={handleDeleteTool}
              />
            ))
          )}
        </div>
      </main>

      {/* Tool Wizard Modal */}
      {showWizard && (
        <ToolWizard
          onClose={() => setShowWizard(false)}
          onSave={handleCreateTool}
        />
      )}
    </div>
  );
}
