'use client';

import { useState, useEffect } from 'react';
import { XMarkIcon, ArrowRightIcon } from '@heroicons/react/24/outline';
import { Scenario, Material, Machine, Policy, Operation, OperationType, PolicyWeights, Recommendation } from '@/types/engine';
import { apiClient } from '@/lib/api-client';

interface ScenarioBuilderProps {
  onClose: () => void;
  onRecommend: (recommendation: any) => void;
}

export default function ScenarioBuilder({ onClose, onRecommend }: ScenarioBuilderProps) {
  const [step, setStep] = useState(1);
  const [materials, setMaterials] = useState<Material[]>([]);
  const [machines, setMachines] = useState<Machine[]>([]);
  const [policies, setPolicies] = useState<Policy[]>([]);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);

  const [scenario, setScenario] = useState<Scenario>({
    tool_id: '',
    material_id: '',
    machine_id: '',
    operation: {
      type: 'roughing',
      depth_of_cut_mm: 2.0,
      width_of_cut_mm: 5.0,
    },
    policy_ids: [],
    weights: {
      tool_life: 0.33,
      time: 0.33,
      safety: 0.34,
    },
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      // Load materials, machines, policies
      // TODO: Implement API calls once backend services are ready
      // const [materialsRes, machinesRes, policiesRes] = await Promise.all([
      //   apiClient.get('/materials'),
      //   apiClient.get('/machines'),
      //   apiClient.get('/policies'),
      // ]);
      // setMaterials(materialsRes.data);
      // setMachines(machinesRes.data);
      // setPolicies(policiesRes.data);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    if (!scenario.tool_id || !scenario.material_id || !scenario.machine_id || scenario.policy_ids.length === 0) {
      alert('Please complete all required fields');
      return;
    }

    setGenerating(true);
    try {
      const response = await apiClient.post<Recommendation>('/recommend', {
        tool_id: scenario.tool_id,
        material_id: scenario.material_id,
        machine_id: scenario.machine_id,
        operation: scenario.operation,
        policy_ids: scenario.policy_ids,
        weights: scenario.weights,
        workholding_id: scenario.workholding_id,
        coolant_id: scenario.coolant_id,
      });
      onRecommend(response);
    } catch (error: any) {
      console.error('Failed to generate recommendation:', error);
      alert(error.response?.data?.detail || 'Failed to generate recommendation');
    } finally {
      setGenerating(false);
    }
  };

  const totalSteps = 5;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900">Build Scenario</h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>

        {/* Progress */}
        <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">
              Step {step} of {totalSteps}
            </span>
            <span className="text-sm text-gray-500">
              {Math.round((step / totalSteps) * 100)}% Complete
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${(step / totalSteps) * 100}%` }}
            />
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6">
          {step === 1 && (
            <ToolSelectionStep
              toolId={scenario.tool_id || ''}
              onSelect={(toolId) => setScenario({ ...scenario, tool_id: toolId })}
            />
          )}
          {step === 2 && (
            <MaterialSelectionStep
              materials={materials}
              selectedId={scenario.material_id || ''}
              onSelect={(materialId) => setScenario({ ...scenario, material_id: materialId })}
              loading={loading}
            />
          )}
          {step === 3 && (
            <MachineSelectionStep
              machines={machines}
              selectedId={scenario.machine_id || ''}
              onSelect={(machineId) => setScenario({ ...scenario, machine_id: machineId })}
              loading={loading}
            />
          )}
          {step === 4 && (
            <OperationStep
              operation={scenario.operation}
              onChange={(operation) => setScenario({ ...scenario, operation })}
            />
          )}
          {step === 5 && (
            <PolicySelectionStep
              policies={policies}
              selectedIds={scenario.policy_ids}
              weights={scenario.weights!}
              onSelectPolicies={(policyIds) => setScenario({ ...scenario, policy_ids: policyIds })}
              onWeightsChange={(weights) => setScenario({ ...scenario, weights })}
              loading={loading}
            />
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between p-6 border-t border-gray-200 bg-gray-50">
          <button
            onClick={() => setStep(Math.max(1, step - 1))}
            disabled={step === 1}
            className="btn btn-outline btn-md disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          {step < totalSteps ? (
            <button
              onClick={() => setStep(step + 1)}
              className="btn btn-primary btn-md"
            >
              Next
              <ArrowRightIcon className="h-5 w-5 ml-2" />
            </button>
          ) : (
            <button
              onClick={handleGenerate}
              disabled={generating}
              className="btn btn-primary btn-md disabled:opacity-50"
            >
              {generating ? 'Generating...' : 'Generate Recommendation'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

// Step components
function ToolSelectionStep({ toolId, onSelect }: { toolId: string; onSelect: (id: string) => void }) {
  return (
    <div>
      <h3 className="text-xl font-semibold mb-4">Select Tool</h3>
      <p className="text-gray-600 mb-6">
        Choose a tool from your library or import a Fusion 360 tool profile.
      </p>
      <div className="space-y-4">
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
          <p className="text-gray-500">Tool selection will be implemented</p>
          <p className="text-sm text-gray-400 mt-2">Import Fusion JSON or select from library</p>
        </div>
      </div>
    </div>
  );
}

function MaterialSelectionStep({ 
  materials, 
  selectedId, 
  onSelect, 
  loading 
}: { 
  materials: Material[]; 
  selectedId: string; 
  onSelect: (id: string) => void;
  loading: boolean;
}) {
  return (
    <div>
      <h3 className="text-xl font-semibold mb-4">Select Material</h3>
      <p className="text-gray-600 mb-6">
        Choose the material you'll be machining.
      </p>
      {loading ? (
        <div className="text-center py-8">Loading materials...</div>
      ) : materials.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          No materials available. Please seed the database.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {materials.map((material) => (
            <button
              key={material.id}
              onClick={() => onSelect(material.id)}
              className={`p-4 border-2 rounded-lg text-left transition-colors ${
                selectedId === material.id
                  ? 'border-blue-600 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
            >
              <div className="font-semibold text-gray-900">{material.name}</div>
              <div className="text-sm text-gray-500 mt-1">{material.category}</div>
              {material.description && (
                <div className="text-sm text-gray-600 mt-2">{material.description}</div>
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

function MachineSelectionStep({ 
  machines, 
  selectedId, 
  onSelect, 
  loading 
}: { 
  machines: Machine[]; 
  selectedId: string; 
  onSelect: (id: string) => void;
  loading: boolean;
}) {
  return (
    <div>
      <h3 className="text-xl font-semibold mb-4">Select Machine</h3>
      <p className="text-gray-600 mb-6">
        Choose the machine you'll be using.
      </p>
      {loading ? (
        <div className="text-center py-8">Loading machines...</div>
      ) : machines.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          No machines available. Please seed the database.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {machines.map((machine) => (
            <button
              key={machine.id}
              onClick={() => onSelect(machine.id)}
              className={`p-4 border-2 rounded-lg text-left transition-colors ${
                selectedId === machine.id
                  ? 'border-blue-600 bg-blue-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
            >
              <div className="font-semibold text-gray-900">{machine.name}</div>
              <div className="text-sm text-gray-500 mt-1">{machine.type}</div>
              <div className="text-sm text-gray-600 mt-2">
                Max RPM: {machine.capabilities.max_rpm.toLocaleString()}
              </div>
              {machine.description && (
                <div className="text-sm text-gray-600 mt-2">{machine.description}</div>
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

function OperationStep({ 
  operation, 
  onChange 
}: { 
  operation: Operation; 
  onChange: (op: Operation) => void;
}) {
  const operationTypes: OperationType[] = [
    'roughing',
    'finishing',
    'semi_finish',
    'drilling',
    'tapping',
    'thread_milling',
    'pocketing',
    'facing',
    'contouring',
    'sloting',
  ];

  return (
    <div>
      <h3 className="text-xl font-semibold mb-4">Operation Parameters</h3>
      <p className="text-gray-600 mb-6">
        Define the cutting operation parameters.
      </p>
      <div className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Operation Type
          </label>
          <select
            value={operation.type}
            onChange={(e) => onChange({ ...operation, type: e.target.value as OperationType })}
            className="input w-full"
          >
            {operationTypes.map((type) => (
              <option key={type} value={type}>
                {type.charAt(0).toUpperCase() + type.slice(1).replace('_', ' ')}
              </option>
            ))}
          </select>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Depth of Cut (mm)
            </label>
            <input
              type="number"
              step="0.1"
              value={operation.depth_of_cut_mm}
              onChange={(e) => onChange({ ...operation, depth_of_cut_mm: parseFloat(e.target.value) || 0 })}
              className="input w-full"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Width of Cut / Stepover (mm)
            </label>
            <input
              type="number"
              step="0.1"
              value={operation.width_of_cut_mm}
              onChange={(e) => onChange({ ...operation, width_of_cut_mm: parseFloat(e.target.value) || 0 })}
              className="input w-full"
            />
          </div>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Radial Engagement (%)
            </label>
            <input
              type="number"
              step="1"
              min="0"
              max="100"
              value={operation.radial_engagement_percent || ''}
              onChange={(e) => onChange({ 
                ...operation, 
                radial_engagement_percent: e.target.value ? parseFloat(e.target.value) : undefined 
              })}
              className="input w-full"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Surface Finish Ra (µm) - Optional
            </label>
            <input
              type="number"
              step="0.1"
              min="0"
              value={operation.surface_finish_ra_um || ''}
              onChange={(e) => onChange({ 
                ...operation, 
                surface_finish_ra_um: e.target.value ? parseFloat(e.target.value) : undefined 
              })}
              className="input w-full"
            />
          </div>
        </div>
      </div>
    </div>
  );
}

function PolicySelectionStep({
  policies,
  selectedIds,
  weights,
  onSelectPolicies,
  onWeightsChange,
  loading,
}: {
  policies: Policy[];
  selectedIds: string[];
  weights: PolicyWeights;
  onSelectPolicies: (ids: string[]) => void;
  onWeightsChange: (weights: PolicyWeights) => void;
  loading: boolean;
}) {
  const handlePolicyToggle = (policyId: string) => {
    if (selectedIds.includes(policyId)) {
      onSelectPolicies(selectedIds.filter(id => id !== policyId));
    } else {
      onSelectPolicies([...selectedIds, policyId]);
    }
  };

  const normalizeWeights = (w: PolicyWeights): PolicyWeights => {
    const total = w.tool_life + w.time + w.safety;
    if (total === 0) return { tool_life: 0.33, time: 0.33, safety: 0.34 };
    return {
      tool_life: w.tool_life / total,
      time: w.time / total,
      safety: w.safety / total,
    };
  };

  return (
    <div>
      <h3 className="text-xl font-semibold mb-4">Select Policies & Weights</h3>
      <p className="text-gray-600 mb-6">
        Choose optimization policies and adjust their weights. Safety is always applied.
      </p>
      
      {loading ? (
        <div className="text-center py-8">Loading policies...</div>
      ) : policies.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          No policies available. Please seed the database.
        </div>
      ) : (
        <>
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Select Policies
            </label>
            <div className="space-y-2">
              {policies.map((policy) => (
                <label key={policy.id} className="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                  <input
                    type="checkbox"
                    checked={selectedIds.includes(policy.id)}
                    onChange={() => handlePolicyToggle(policy.id)}
                    className="mr-3 h-4 w-4 text-blue-600"
                  />
                  <div className="flex-1">
                    <div className="font-medium text-gray-900">{policy.name}</div>
                    {policy.description && (
                      <div className="text-sm text-gray-500">{policy.description}</div>
                    )}
                  </div>
                </label>
              ))}
            </div>
          </div>

          <div className="border-t pt-6">
            <label className="block text-sm font-medium text-gray-700 mb-4">
              Policy Weights (will be normalized)
            </label>
            <div className="space-y-4">
              <div>
                <label className="block text-sm text-gray-600 mb-2">
                  Tool Life: {Math.round(normalizeWeights(weights).tool_life * 100)}%
                </label>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.01"
                  value={weights.tool_life}
                  onChange={(e) => onWeightsChange({ ...weights, tool_life: parseFloat(e.target.value) })}
                  className="w-full"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-600 mb-2">
                  Time: {Math.round(normalizeWeights(weights).time * 100)}%
                </label>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.01"
                  value={weights.time}
                  onChange={(e) => onWeightsChange({ ...weights, time: parseFloat(e.target.value) })}
                  className="w-full"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-600 mb-2">
                  Safety: {Math.round(normalizeWeights(weights).safety * 100)}% (always applied)
                </label>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.01"
                  value={weights.safety}
                  onChange={(e) => onWeightsChange({ ...weights, safety: parseFloat(e.target.value) })}
                  className="w-full"
                />
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

