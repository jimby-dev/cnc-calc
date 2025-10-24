'use client';

import { ToolType } from '@/types/tool';
import {
  ArrowDownIcon,
  ArrowRightIcon,
  ArrowUpIcon,
  BoltIcon,
  CircleStackIcon,
  WrenchScrewdriverIcon
} from '@heroicons/react/24/outline';

interface ToolTypeSelectionProps {
  selectedType: ToolType | undefined;
  onTypeChange: (type: ToolType) => void;
}

const toolTypes = [
  {
    id: 'end_mill' as ToolType,
    name: 'End Mill',
    description: 'Square end cutting tool for milling operations',
    icon: WrenchScrewdriverIcon,
    features: ['Square end', 'Multiple flutes', 'Helix angle', 'Corner radius']
  },
  {
    id: 'ball_end_mill' as ToolType,
    name: 'Ball End Mill',
    description: 'Spherical end for 3D contouring and finishing',
    icon: CircleStackIcon,
    features: ['Spherical end', '3D contouring', 'Finishing operations']
  },
  {
    id: 'chamfer' as ToolType,
    name: 'Chamfer Mill',
    description: 'Angled cutting tool for chamfering edges',
    icon: ArrowDownIcon,
    features: ['Angled cutting', 'Edge chamfering', 'V-shaped profile']
  },
  {
    id: 'drill' as ToolType,
    name: 'Drill',
    description: 'Pointed tool for creating holes',
    icon: ArrowUpIcon,
    features: ['Pointed tip', 'Hole drilling', 'Point angle']
  },
  {
    id: 'reamer' as ToolType,
    name: 'Reamer',
    description: 'Precision tool for finishing holes',
    icon: BoltIcon,
    features: ['Precision finishing', 'Tight tolerances', 'Lead angle']
  },
  {
    id: 'thread_mill' as ToolType,
    name: 'Thread Mill',
    description: 'Tool for creating internal or external threads',
    icon: ArrowRightIcon,
    features: ['Thread creation', 'Pitch control', 'Thread length']
  }
];

export default function ToolTypeSelection({ selectedType, onTypeChange }: ToolTypeSelectionProps) {
  return (
    <div className="space-y-6">
      <div className="text-center">
        <h3 className="text-lg font-medium text-gray-900 mb-2">Select Tool Type</h3>
        <p className="text-sm text-gray-500">
          Choose the type of cutting tool you want to create
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {toolTypes.map((toolType) => {
          const Icon = toolType.icon;
          const isSelected = selectedType === toolType.id;
          
          return (
            <button
              key={toolType.id}
              onClick={() => onTypeChange(toolType.id)}
              className={`p-6 rounded-lg border-2 text-left transition-all hover:shadow-md ${
                isSelected
                  ? 'border-primary-500 bg-primary-50 ring-2 ring-primary-200'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
            >
              <div className="flex items-start space-x-4">
                <div className={`p-3 rounded-lg ${
                  isSelected ? 'bg-primary-100 text-primary-600' : 'bg-gray-100 text-gray-600'
                }`}>
                  <Icon className="h-6 w-6" />
                </div>
                <div className="flex-1 min-w-0">
                  <h4 className={`font-medium ${
                    isSelected ? 'text-primary-900' : 'text-gray-900'
                  }`}>
                    {toolType.name}
                  </h4>
                  <p className={`text-sm mt-1 ${
                    isSelected ? 'text-primary-700' : 'text-gray-500'
                  }`}>
                    {toolType.description}
                  </p>
                  <div className="mt-3">
                    <ul className="text-xs space-y-1">
                      {toolType.features.map((feature, index) => (
                        <li key={index} className={`${
                          isSelected ? 'text-primary-600' : 'text-gray-500'
                        }`}>
                          • {feature}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </button>
          );
        })}
      </div>

      {selectedType && (
        <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <div className="w-2 h-2 bg-blue-400 rounded-full mt-2"></div>
            </div>
            <div className="ml-3">
              <h4 className="text-sm font-medium text-blue-900">
                {toolTypes.find(t => t.id === selectedType)?.name} Selected
              </h4>
              <p className="text-sm text-blue-700 mt-1">
                Next, you'll define the specific geometry and dimensions for this tool type.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
