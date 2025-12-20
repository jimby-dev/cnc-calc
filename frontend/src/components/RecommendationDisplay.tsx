'use client';

import { useState } from 'react';
import { 
  CheckCircleIcon, 
  ExclamationTriangleIcon, 
  InformationCircleIcon,
  ChevronDownIcon,
  ChevronRightIcon,
  DocumentArrowDownIcon,
} from '@heroicons/react/24/outline';
import { Recommendation, DecisionNode, RiskScore } from '@/types/engine';

interface RecommendationDisplayProps {
  recommendation: Recommendation;
  onExport?: () => void;
}

export default function RecommendationDisplay({ recommendation, onExport }: RecommendationDisplayProps) {
  const [expandedNodes, setExpandedNodes] = useState<Set<number>>(new Set());
  const [showTrace, setShowTrace] = useState(false);

  const toggleNode = (index: number) => {
    const newExpanded = new Set(expandedNodes);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedNodes(newExpanded);
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return 'text-green-600';
    if (confidence >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getConfidenceBadge = (confidence: number) => {
    if (confidence >= 0.8) return 'bg-green-100 text-green-800';
    if (confidence >= 0.6) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Recommendation</h2>
          <p className="text-sm text-gray-500 mt-1">
            Generated at {recommendation.timestamp ? new Date(recommendation.timestamp).toLocaleString() : 'now'}
          </p>
        </div>
        {onExport && (
          <button
            onClick={onExport}
            className="btn btn-outline btn-md"
          >
            <DocumentArrowDownIcon className="h-5 w-5 mr-2" />
            Export Presets
          </button>
        )}
      </div>

      {/* Core Values */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="text-sm text-gray-500">Spindle RPM</div>
          <div className="text-2xl font-bold text-gray-900">
            {Math.round(recommendation.spindle_rpm).toLocaleString()}
          </div>
        </div>
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="text-sm text-gray-500">Feedrate</div>
          <div className="text-2xl font-bold text-gray-900">
            {Math.round(recommendation.feedrate_mm_per_min).toLocaleString()}
          </div>
          <div className="text-xs text-gray-400 mt-1">mm/min</div>
        </div>
        {recommendation.chip_load_mm && (
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="text-sm text-gray-500">Chip Load</div>
            <div className="text-2xl font-bold text-gray-900">
              {recommendation.chip_load_mm.toFixed(3)}
            </div>
            <div className="text-xs text-gray-400 mt-1">mm</div>
          </div>
        )}
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="text-sm text-gray-500">Confidence</div>
          <div className={`text-2xl font-bold ${getConfidenceColor(recommendation.confidence)}`}>
            {Math.round(recommendation.confidence * 100)}%
          </div>
        </div>
      </div>

      {/* Derived Values */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        <div>
          <div className="text-sm text-gray-500">Surface Speed</div>
          <div className="text-lg font-semibold text-gray-900">
            {recommendation.surface_speed_m_per_min.toFixed(1)} m/min
          </div>
          {recommendation.surface_speed_sfm && (
            <div className="text-sm text-gray-400">
              {recommendation.surface_speed_sfm.toFixed(0)} SFM
            </div>
          )}
        </div>
        {recommendation.material_removal_rate_mm3_per_min && (
          <div>
            <div className="text-sm text-gray-500">Material Removal Rate</div>
            <div className="text-lg font-semibold text-gray-900">
              {recommendation.material_removal_rate_mm3_per_min.toLocaleString()} mm³/min
            </div>
          </div>
        )}
        {recommendation.feedrate_mm_per_rev && (
          <div>
            <div className="text-sm text-gray-500">Feed per Revolution</div>
            <div className="text-lg font-semibold text-gray-900">
              {recommendation.feedrate_mm_per_rev.toFixed(3)} mm/rev
            </div>
          </div>
        )}
      </div>

      {/* Signals and Warnings */}
      <div className="space-y-4">
        {recommendation.signals.dominant_constraint && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <div className="flex items-start">
              <ExclamationTriangleIcon className="h-5 w-5 text-yellow-600 mt-0.5 mr-3" />
              <div className="flex-1">
                <div className="font-medium text-yellow-900">Dominant Constraint</div>
                <div className="text-sm text-yellow-700 mt-1">
                  {recommendation.signals.dominant_constraint.replace('_', ' ').toUpperCase()}
                  {recommendation.signals.constraint_severity > 0 && (
                    <span className="ml-2">
                      (Severity: {recommendation.signals.constraint_severity.toFixed(1)})
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {recommendation.signals.warnings.length > 0 && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <div className="font-medium text-yellow-900 mb-2">Warnings</div>
            <ul className="list-disc list-inside text-sm text-yellow-700 space-y-1">
              {recommendation.signals.warnings.map((warning, idx) => (
                <li key={idx}>{warning}</li>
              ))}
            </ul>
          </div>
        )}

        {recommendation.signals.errors.length > 0 && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="font-medium text-red-900 mb-2">Errors</div>
            <ul className="list-disc list-inside text-sm text-red-700 space-y-1">
              {recommendation.signals.errors.map((error, idx) => (
                <li key={idx}>{error}</li>
              ))}
            </ul>
          </div>
        )}

        {recommendation.signals.risk_scores.length > 0 && (
          <div>
            <div className="font-medium text-gray-900 mb-3">Risk Assessment</div>
            <div className="space-y-2">
              {recommendation.signals.risk_scores.map((risk, idx) => (
                <RiskScoreDisplay key={idx} risk={risk} />
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Explanation Trace */}
      <div className="border-t pt-6">
        <button
          onClick={() => setShowTrace(!showTrace)}
          className="flex items-center justify-between w-full text-left"
        >
          <div className="flex items-center">
            <InformationCircleIcon className="h-5 w-5 text-gray-400 mr-2" />
            <span className="font-medium text-gray-900">
              Decision Trace ({recommendation.trace.total_steps} steps)
            </span>
          </div>
          {showTrace ? (
            <ChevronDownIcon className="h-5 w-5 text-gray-400" />
          ) : (
            <ChevronRightIcon className="h-5 w-5 text-gray-400" />
          )}
        </button>

        {showTrace && (
          <div className="mt-4 space-y-2">
            {recommendation.trace.conflicts_detected.length > 0 && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 mb-4">
                <div className="font-medium text-yellow-900 mb-2">Conflicts Detected</div>
                <ul className="list-disc list-inside text-sm text-yellow-700 space-y-1">
                  {recommendation.trace.conflicts_detected.map((conflict, idx) => (
                    <li key={idx}>{conflict}</li>
                  ))}
                </ul>
              </div>
            )}

            {recommendation.trace.arbitration_strategy && (
              <div className="text-sm text-gray-600 mb-4">
                <span className="font-medium">Arbitration Strategy:</span>{' '}
                {recommendation.trace.arbitration_strategy}
              </div>
            )}

            {recommendation.trace.nodes.map((node, idx) => (
              <DecisionNodeDisplay
                key={idx}
                node={node}
                index={idx}
                isExpanded={expandedNodes.has(idx)}
                onToggle={() => toggleNode(idx)}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function RiskScoreDisplay({ risk }: { risk: RiskScore }) {
  const getScoreColor = (score: number) => {
    if (score <= 3) return 'bg-green-100 text-green-800';
    if (score <= 6) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  return (
    <div className="bg-gray-50 rounded-lg p-3">
      <div className="flex items-center justify-between mb-1">
        <span className="font-medium text-gray-900">{risk.category.replace('_', ' ')}</span>
        <span className={`px-2 py-1 rounded text-xs font-medium ${getScoreColor(risk.score)}`}>
          {risk.score.toFixed(1)}/10
        </span>
      </div>
      <div className="text-sm text-gray-600">{risk.reason}</div>
      <div className="text-xs text-gray-400 mt-1">
        Confidence: {Math.round(risk.confidence * 100)}%
      </div>
    </div>
  );
}

function DecisionNodeDisplay({
  node,
  index,
  isExpanded,
  onToggle,
}: {
  node: DecisionNode;
  index: number;
  isExpanded: boolean;
  onToggle: () => void;
}) {
  return (
    <div className="border border-gray-200 rounded-lg">
      <button
        onClick={onToggle}
        className="w-full flex items-center justify-between p-3 text-left hover:bg-gray-50"
      >
        <div className="flex items-center flex-1">
          {isExpanded ? (
            <ChevronDownIcon className="h-4 w-4 text-gray-400 mr-2" />
          ) : (
            <ChevronRightIcon className="h-4 w-4 text-gray-400 mr-2" />
          )}
          <div>
            <div className="font-medium text-gray-900">{node.step}</div>
            <div className="text-sm text-gray-500">{node.reason}</div>
          </div>
        </div>
        {node.policy_applied && (
          <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded ml-2">
            {node.policy_applied}
          </span>
        )}
      </button>
      {isExpanded && (
        <div className="px-3 pb-3 border-t bg-gray-50">
          <div className="mt-3 space-y-2 text-sm">
            {node.input_value && (
              <div>
                <span className="font-medium text-gray-700">Input:</span>
                <pre className="mt-1 p-2 bg-white rounded text-xs overflow-x-auto">
                  {JSON.stringify(node.input_value, null, 2)}
                </pre>
              </div>
            )}
            <div>
              <span className="font-medium text-gray-700">Output:</span>
              <pre className="mt-1 p-2 bg-white rounded text-xs overflow-x-auto">
                {JSON.stringify(node.output_value, null, 2)}
              </pre>
            </div>
            <div className="text-xs text-gray-500">
              Confidence: {Math.round(node.confidence * 100)}%
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

