'use client';

import { Tool, ToolGeometry, ToolType } from '@/types/tool';
import { ChevronLeftIcon, ChevronRightIcon, XMarkIcon } from '@heroicons/react/24/outline';
import { useState } from 'react';
import ExportOptions from './ToolWizard/ExportOptions';
import GeometryForm from './ToolWizard/GeometryForm';
import ReviewValidation from './ToolWizard/ReviewValidation';
import ToolTypeSelection from './ToolWizard/ToolTypeSelection';

interface ToolWizardProps {
  onClose: () => void;
  onSave: (tool: Tool) => void;
  initialTool?: Partial<Tool>;
}

export default function ToolWizard({ onClose, onSave, initialTool }: ToolWizardProps) {
  const [currentStep, setCurrentStep] = useState(1);
  const [toolData, setToolData] = useState<Partial<Tool>>({
    name: '',
    vendor: '',
    type: 'End Mill',
    geometry: {} as ToolGeometry,
    limits: {},
    units: 'mm',
    ...initialTool,
  });

  const steps = [
    { id: 1, name: 'Tool Type', description: 'Select the type of tool' },
    { id: 2, name: 'Geometry', description: 'Define tool dimensions' },
    { id: 3, name: 'Review', description: 'Validate and preview' },
    { id: 4, name: 'Export', description: 'Save and export' },
  ];

  const handleNext = () => {
    if (currentStep < steps.length) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrevious = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleToolTypeChange = (type: ToolType) => {
    setToolData(prev => ({ ...prev, type }));
  };

  const handleGeometryChange = (geometry: ToolGeometry) => {
    setToolData(prev => ({ ...prev, geometry }));
  };

  const handleMetadataChange = (updates: Partial<Tool>) => {
    setToolData(prev => ({ ...prev, ...updates }));
  };

  const handleSave = () => {
    if (!toolData.name || !toolData.vendor || !toolData.geometry) {
      return;
    }

    const tool: Tool = {
      id: toolData.id || Date.now().toString(),
      name: toolData.name,
      vendor: toolData.vendor,
      type: toolData.type!,
      geometry: toolData.geometry,
      limits: toolData.limits,
      units: toolData.units || 'mm',
      createdAt: toolData.createdAt || new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    onSave(tool);
  };

  const canProceed = () => {
    switch (currentStep) {
      case 1:
        return toolData.type !== undefined;
      case 2:
        return toolData.name && toolData.vendor && toolData.geometry;
      case 3:
        return true; // Review step is always available
      case 4:
        return true; // Export step is always available
      default:
        return false;
    }
  };

  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <ToolTypeSelection
            selectedType={toolData.type}
            onTypeChange={handleToolTypeChange}
          />
        );
      case 2:
        return (
          <GeometryForm
            toolType={toolData.type!}
            geometry={toolData.geometry}
            onUpdateGeometry={handleGeometryChange}
            units={toolData.units || 'mm'}
            onToggleUnits={(units) => setToolData(prev => ({ ...prev, units }))}
          />
        );
      case 3:
        return (
          <ReviewValidation
            tool={toolData as Tool}
            onMetadataChange={handleMetadataChange}
          />
        );
      case 4:
        return (
          <ExportOptions
            tool={toolData as Tool}
          />
        );
      default:
        return null;
    }
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex min-h-screen items-center justify-center p-4">
        <div className="fixed inset-0 bg-black bg-opacity-50" onClick={onClose} />
        
        <div className="relative bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
          {/* Header */}
          <div className="px-6 py-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-semibold text-gray-900">Create New Tool</h2>
                <p className="text-sm text-gray-500 mt-1">
                  Step {currentStep} of {steps.length}: {steps[currentStep - 1].description}
                </p>
              </div>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600"
              >
                <XMarkIcon className="h-6 w-6" />
              </button>
            </div>
            
            {/* Progress Steps */}
            <div className="mt-4">
              <nav className="flex space-x-8">
                {steps.map((step) => (
                  <div key={step.id} className="flex items-center">
                    <div
                      className={`flex items-center justify-center w-8 h-8 rounded-full text-sm font-medium ${
                        step.id <= currentStep
                          ? 'bg-primary-600 text-white'
                          : 'bg-gray-200 text-gray-600'
                      }`}
                    >
                      {step.id}
                    </div>
                    <div className="ml-3">
                      <p className={`text-sm font-medium ${
                        step.id <= currentStep ? 'text-primary-600' : 'text-gray-500'
                      }`}>
                        {step.name}
                      </p>
                    </div>
                    {step.id < steps.length && (
                      <div className={`ml-8 h-0.5 w-8 ${
                        step.id < currentStep ? 'bg-primary-600' : 'bg-gray-200'
                      }`} />
                    )}
                  </div>
                ))}
              </nav>
            </div>
          </div>

          {/* Content */}
          <div className="px-6 py-6 overflow-y-auto max-h-[60vh]">
            {renderStep()}
          </div>

          {/* Footer */}
          <div className="px-6 py-4 border-t border-gray-200 bg-gray-50">
            <div className="flex justify-between">
              <button
                onClick={handlePrevious}
                disabled={currentStep === 1}
                className="btn btn-outline btn-md disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <ChevronLeftIcon className="h-5 w-5 mr-2" />
                Previous
              </button>
              
              <div className="flex space-x-3">
                <button
                  onClick={onClose}
                  className="btn btn-ghost btn-md"
                >
                  Cancel
                </button>
                {currentStep < steps.length ? (
                  <button
                    onClick={handleNext}
                    disabled={!canProceed()}
                    className="btn btn-primary btn-md disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Next
                    <ChevronRightIcon className="h-5 w-5 ml-2" />
                  </button>
                ) : (
                  <button
                    onClick={handleSave}
                    className="btn btn-primary btn-md"
                  >
                    Save Tool
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
