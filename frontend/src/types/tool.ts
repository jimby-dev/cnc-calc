export type ToolType = 
  | 'end_mill'
  | 'ball_end_mill'
  | 'chamfer'
  | 'drill'
  | 'reamer'
  | 'thread_mill';

export interface ToolMeta {
  id: string;
  name: string;
  vendor: string;
  type: ToolType;
  createdAt: string;
  updatedAt: string;
}

export interface EndMillGeometry {
  diameter: number; // mm
  fluteCount: number;
  helixAngle: number; // degrees
  fluteLength: number; // mm
  lengthOfCut: number; // mm
  overallLength: number; // mm
  cornerRadius?: number; // mm
}

export interface BallEndMillGeometry {
  diameter: number; // mm
  fluteCount: number;
  tipRadius: number; // mm (should equal diameter / 2)
  fluteLength: number; // mm
  overallLength: number; // mm
}

export interface ChamferGeometry {
  includedAngle: number; // degrees
  tipFlat: number; // mm
  fluteLength: number; // mm
  overallLength: number; // mm
  shankDiameter: number; // mm
}

export interface DrillGeometry {
  diameter: number; // mm
  pointAngle: number; // degrees
  fluteLength: number; // mm
  overallLength: number; // mm
}

export interface ReamerGeometry {
  diameter: number; // mm
  fluteLength: number; // mm
  overallLength: number; // mm
  leadAngle?: number; // degrees
}

export interface ThreadMillGeometry {
  diameter: number; // mm
  pitch: number; // mm
  maxThreadLength: number; // mm
  fluteLength: number; // mm
  overallLength: number; // mm
}

export type ToolGeometry = 
  | EndMillGeometry
  | BallEndMillGeometry
  | ChamferGeometry
  | DrillGeometry
  | ReamerGeometry
  | ThreadMillGeometry;

export interface ToolLimits {
  sfm?: number; // Surface feet per minute
  stepdown?: number; // mm
  engagement?: number; // percentage
  feedRate?: number; // mm/min
  spindleSpeed?: number; // RPM
}

export interface Tool extends ToolMeta {
  geometry: ToolGeometry;
  limits?: ToolLimits;
}

export interface ValidationError {
  field: string;
  message: string;
  severity: 'error' | 'warning';
}

export interface FusionExportData {
  toolType: string;
  diameter: number;
  fluteCount?: number;
  helixAngle?: number;
  fluteLength: number;
  overallLength: number;
  cornerRadius?: number;
  tipRadius?: number;
  includedAngle?: number;
  tipFlat?: number;
  shankDiameter?: number;
  pointAngle?: number;
  leadAngle?: number;
  pitch?: number;
  maxThreadLength?: number;
}

export interface ExportOptions {
  format: 'fusion_json' | 'csv';
  units: 'metric' | 'imperial';
}
