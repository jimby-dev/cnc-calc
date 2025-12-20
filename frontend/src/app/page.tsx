'use client';

import ScenarioBuilder from '@/components/ScenarioBuilder';
import RecommendationDisplay from '@/components/RecommendationDisplay';
import { Recommendation } from '@/types/engine';
import { SparklesIcon } from '@heroicons/react/24/outline';
import { useState } from 'react';

export default function HomePage() {
  const [showBuilder, setShowBuilder] = useState(false);
  const [recommendation, setRecommendation] = useState<Recommendation | null>(null);

  const handleRecommend = (rec: Recommendation) => {
    setRecommendation(rec);
    setShowBuilder(false);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <SparklesIcon className="h-8 w-8 text-blue-600 mr-3" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Machining Decision Engine</h1>
                <span className="text-sm text-gray-500">Policy-driven feeds & speeds recommendations</span>
              </div>
            </div>
            <button
              onClick={() => setShowBuilder(true)}
              className="btn btn-primary btn-md"
            >
              <SparklesIcon className="h-5 w-5 mr-2" />
              Build Scenario
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {recommendation ? (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-gray-900">Recommendation</h2>
              <button
                onClick={() => {
                  setRecommendation(null);
                  setShowBuilder(true);
                }}
                className="btn btn-outline btn-sm"
              >
                Build New Scenario
              </button>
            </div>
            <RecommendationDisplay 
              recommendation={recommendation}
              onExport={() => {
                // TODO: Implement export functionality
                alert('Export functionality coming soon');
              }}
            />
          </div>
        ) : (
          <div className="text-center py-16">
            <SparklesIcon className="mx-auto h-16 w-16 text-gray-400 mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Get Started with Feeds & Speeds Recommendations
            </h2>
            <p className="text-gray-600 mb-8 max-w-2xl mx-auto">
              Build a machining scenario by selecting your tool, material, machine, and operation parameters.
              Our policy-driven engine will generate explainable recommendations optimized for your goals.
            </p>
            <button
              onClick={() => setShowBuilder(true)}
              className="btn btn-primary btn-lg"
            >
              <SparklesIcon className="h-6 w-6 mr-2" />
              Build Your First Scenario
            </button>
          </div>
        )}
      </main>

      {/* Scenario Builder Modal */}
      {showBuilder && (
        <ScenarioBuilder
          onClose={() => setShowBuilder(false)}
          onRecommend={handleRecommend}
        />
      )}
    </div>
  );
}
