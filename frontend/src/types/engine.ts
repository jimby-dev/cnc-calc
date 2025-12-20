/**
 * TypeScript types for the machining decision engine.
 * These match the backend engine schemas.
 */

// Material types
export type MaterialCategory = 
  | 'aluminum'
  | 'steel'
  | 'stainless_steel'
  | 'titanium'
  | 'plastic'
  | 'composite'
  | 'other';

export interface MaterialProperties {
  hardness_hb?: number;
  hardness_hrc?: number;
  machinability_index: number;
  thermal_conductivity?: number;
  melting_point?: number;
  base_sfm: number;
  sfm_range_min: number;
  sfm_range_max: number;
  chip_type: string;
  work_hardening: boolean;
  abrasiveness: number;
  built_up_edge_tendency: number;
}

export interface Material {
  id: string;
  name: string;
  category: MaterialCategory;
  properties: MaterialProperties;
  description?: string;
  common_applications?: string[];
  notes?: string;
}

// Machine types
export type MachineType = 'mill' | 'lathe' | 'router' | 'drill' | 'other';

export interface MachineCapabilities {
  max_rpm: number;
  min_rpm: number;
  spindle_power_kw?: number;
  spindle_torque_nm?: number;
  max_feedrate_mm_per_min: number;
  min_feedrate_mm_per_min: number;
  rigidity_factor: number;
  accuracy_mm?: number;
  max_tool_diameter_mm?: number;
  max_depth_of_cut_mm?: number;
}

export interface Machine {
  id: string;
  name: string;
  type: MachineType;
  capabilities: MachineCapabilities;
  manufacturer?: string;
  description?: string;
  notes?: string;
}

// Workholding types
export type WorkholdingType = 
  | 'vise'
  | 'fixture'
  | 'chuck'
  | 'face_plate'
  | 'magnetic'
  | 'vacuum'
  | 'custom'
  | 'other';

export interface Workholding {
  id: string;
  name: string;
  type: WorkholdingType;
  rigidity_factor: number;
  stability_factor: number;
  max_depth_of_cut_reduction: number;
  max_feedrate_reduction: number;
  description?: string;
  notes?: string;
}

// Coolant types
export type CoolantType = 
  | 'flood'
  | 'mist'
  | 'air'
  | 'none'
  | 'through_spindle'
  | 'external'
  | 'other';

export interface Coolant {
  id: string;
  name: string;
  type: CoolantType;
  heat_removal_factor: number;
  lubrication_factor: number;
  chip_evacuation_factor: number;
  sfm_multiplier: number;
  feedrate_multiplier: number;
  description?: string;
  notes?: string;
}

// Operation types
export type OperationType = 
  | 'roughing'
  | 'finishing'
  | 'semi_finish'
  | 'drilling'
  | 'tapping'
  | 'thread_milling'
  | 'pocketing'
  | 'facing'
  | 'contouring'
  | 'sloting'
  | 'other';

export interface Operation {
  id?: string;
  type: OperationType;
  depth_of_cut_mm: number;
  width_of_cut_mm: number;
  radial_engagement_percent?: number;
  axial_engagement_percent?: number;
  surface_finish_ra_um?: number;
  description?: string;
  notes?: string;
}

// Policy types
export type PolicyType = 
  | 'safety'
  | 'tool_life'
  | 'time'
  | 'surface_finish'
  | 'balanced'
  | 'custom';

export interface PolicyWeights {
  tool_life: number;
  time: number;
  safety: number;
}

export interface Policy {
  id: string;
  name: string;
  type: PolicyType;
  weights: PolicyWeights;
  rules: Record<string, any>;
  priority: number;
  description?: string;
  notes?: string;
}

// Signals and constraints
export type ConstraintType = 
  | 'spindle_rpm'
  | 'feedrate'
  | 'depth_of_cut'
  | 'width_of_cut'
  | 'chip_load'
  | 'tool_wear'
  | 'surface_finish'
  | 'chatter'
  | 'power'
  | 'torque'
  | 'rigidity'
  | 'coolant'
  | 'material'
  | 'other';

export interface RiskScore {
  category: string;
  score: number; // 0-10
  confidence: number; // 0-1
  reason: string;
}

export interface Signals {
  risk_scores: RiskScore[];
  dominant_constraint?: ConstraintType;
  constraint_severity: number;
  is_feasible: boolean;
  feasibility_confidence: number;
  warnings: string[];
  errors: string[];
  overall_confidence: number;
}

// Recommendation types
export interface DecisionNode {
  step: string;
  input_value?: any;
  output_value: any;
  reason: string;
  policy_applied?: string;
  confidence: number;
}

export interface RecommendationTrace {
  nodes: DecisionNode[];
  conflicts_detected: string[];
  arbitration_strategy?: string;
  total_steps: number;
}

export interface Recommendation {
  spindle_rpm: number;
  feedrate_mm_per_min: number;
  feedrate_mm_per_rev?: number;
  chip_load_mm?: number;
  surface_speed_m_per_min: number;
  surface_speed_sfm?: number;
  material_removal_rate_mm3_per_min?: number;
  signals: Signals;
  confidence: number;
  trace: RecommendationTrace;
  timestamp?: string;
  scenario_id?: string;
}

// Scenario builder types
export interface Scenario {
  tool_id?: string;
  material_id?: string;
  machine_id?: string;
  operation: Operation;
  policy_ids: string[];
  weights?: PolicyWeights;
  workholding_id?: string;
  coolant_id?: string;
}

