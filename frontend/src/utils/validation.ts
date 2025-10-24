import { Tool, ToolGeometry, ValidationError } from '@/types/tool';

export function validateTool(tool: Partial<Tool>): ValidationError[] {
  const errors: ValidationError[] = [];

  // Basic validation
  if (!tool.name || tool.name.trim().length === 0) {
    errors.push({
      field: 'name',
      message: 'Tool name is required',
      severity: 'error'
    });
  }

  if (!tool.vendor || tool.vendor.trim().length === 0) {
    errors.push({
      field: 'vendor',
      message: 'Vendor is required',
      severity: 'error'
    });
  }

  if (!tool.type) {
    errors.push({
      field: 'type',
      message: 'Tool type is required',
      severity: 'error'
    });
  }

  if (!tool.geometry) {
    errors.push({
      field: 'geometry',
      message: 'Tool geometry is required',
      severity: 'error'
    });
    return errors; // Can't validate geometry if it doesn't exist
  }

  // Geometry validation based on tool type
  switch (tool.type) {
    case 'end_mill':
      errors.push(...validateEndMillGeometry(tool.geometry));
      break;
    case 'ball_end_mill':
      errors.push(...validateBallEndMillGeometry(tool.geometry));
      break;
    case 'chamfer':
      errors.push(...validateChamferGeometry(tool.geometry));
      break;
    case 'drill':
      errors.push(...validateDrillGeometry(tool.geometry));
      break;
    case 'reamer':
      errors.push(...validateReamerGeometry(tool.geometry));
      break;
    case 'thread_mill':
      errors.push(...validateThreadMillGeometry(tool.geometry));
      break;
  }

  return errors;
}

function validateEndMillGeometry(geometry: ToolGeometry): ValidationError[] {
  const errors: ValidationError[] = [];
  const geom = geometry as any;

  // Required fields
  if (!geom.diameter || geom.diameter <= 0) {
    errors.push({
      field: 'diameter',
      message: 'Diameter must be greater than 0',
      severity: 'error'
    });
  }

  if (!geom.fluteCount || geom.fluteCount < 1) {
    errors.push({
      field: 'fluteCount',
      message: 'Flute count must be at least 1',
      severity: 'error'
    });
  }

  if (!geom.fluteLength || geom.fluteLength <= 0) {
    errors.push({
      field: 'fluteLength',
      message: 'Flute length must be greater than 0',
      severity: 'error'
    });
  }

  if (!geom.overallLength || geom.overallLength <= 0) {
    errors.push({
      field: 'overallLength',
      message: 'Overall length must be greater than 0',
      severity: 'error'
    });
  }

  if (!geom.lengthOfCut || geom.lengthOfCut <= 0) {
    errors.push({
      field: 'lengthOfCut',
      message: 'Length of cut must be greater than 0',
      severity: 'error'
    });
  }

  // Relationship validation
  if (geom.fluteLength && geom.lengthOfCut && geom.fluteLength < geom.lengthOfCut) {
    errors.push({
      field: 'lengthOfCut',
      message: 'Length of cut cannot exceed flute length',
      severity: 'error'
    });
  }

  if (geom.fluteLength && geom.overallLength && geom.fluteLength >= geom.overallLength) {
    errors.push({
      field: 'fluteLength',
      message: 'Flute length must be less than overall length',
      severity: 'error'
    });
  }

  // Warnings
  if (geom.helixAngle && (geom.helixAngle < 20 || geom.helixAngle > 45)) {
    errors.push({
      field: 'helixAngle',
      message: 'Unusual helix angle - typical range is 20-45 degrees',
      severity: 'warning'
    });
  }

  if (geom.cornerRadius && geom.cornerRadius > geom.diameter / 4) {
    errors.push({
      field: 'cornerRadius',
      message: 'Large corner radius may affect cutting performance',
      severity: 'warning'
    });
  }

  return errors;
}

function validateBallEndMillGeometry(geometry: ToolGeometry): ValidationError[] {
  const errors: ValidationError[] = [];
  const geom = geometry as any;

  // Required fields
  if (!geom.diameter || geom.diameter <= 0) {
    errors.push({
      field: 'diameter',
      message: 'Diameter must be greater than 0',
      severity: 'error'
    });
  }

  if (!geom.tipRadius || geom.tipRadius <= 0) {
    errors.push({
      field: 'tipRadius',
      message: 'Tip radius must be greater than 0',
      severity: 'error'
    });
  }

  // Critical validation for ball end mills
  if (geom.diameter && geom.tipRadius && Math.abs(geom.tipRadius - geom.diameter / 2) > 0.01) {
    errors.push({
      field: 'tipRadius',
      message: 'Tip radius must equal half the diameter for ball end mills',
      severity: 'error'
    });
  }

  return errors;
}

function validateChamferGeometry(geometry: ToolGeometry): ValidationError[] {
  const errors: ValidationError[] = [];
  const geom = geometry as any;

  // Required fields
  if (!geom.includedAngle || geom.includedAngle <= 0) {
    errors.push({
      field: 'includedAngle',
      message: 'Included angle is required and must be greater than 0',
      severity: 'error'
    });
  }

  if (!geom.tipFlat || geom.tipFlat < 0) {
    errors.push({
      field: 'tipFlat',
      message: 'Tip flat is required',
      severity: 'error'
    });
  }

  // Warnings
  if (geom.tipFlat && geom.tipFlat < 0.1) {
    errors.push({
      field: 'tipFlat',
      message: 'Very small tip flat may be difficult to manufacture',
      severity: 'warning'
    });
  }

  return errors;
}

function validateDrillGeometry(geometry: ToolGeometry): ValidationError[] {
  const errors: ValidationError[] = [];
  const geom = geometry as any;

  // Required fields
  if (!geom.diameter || geom.diameter <= 0) {
    errors.push({
      field: 'diameter',
      message: 'Diameter must be greater than 0',
      severity: 'error'
    });
  }

  if (!geom.pointAngle || geom.pointAngle <= 0) {
    errors.push({
      field: 'pointAngle',
      message: 'Point angle must be greater than 0',
      severity: 'error'
    });
  }

  return errors;
}

function validateReamerGeometry(geometry: ToolGeometry): ValidationError[] {
  const errors: ValidationError[] = [];
  const geom = geometry as any;

  // Required fields
  if (!geom.diameter || geom.diameter <= 0) {
    errors.push({
      field: 'diameter',
      message: 'Diameter must be greater than 0',
      severity: 'error'
    });
  }

  return errors;
}

function validateThreadMillGeometry(geometry: ToolGeometry): ValidationError[] {
  const errors: ValidationError[] = [];
  const geom = geometry as any;

  // Required fields
  if (!geom.diameter || geom.diameter <= 0) {
    errors.push({
      field: 'diameter',
      message: 'Diameter must be greater than 0',
      severity: 'error'
    });
  }

  if (!geom.pitch || geom.pitch <= 0) {
    errors.push({
      field: 'pitch',
      message: 'Pitch must be greater than 0',
      severity: 'error'
    });
  }

  if (!geom.maxThreadLength || geom.maxThreadLength <= 0) {
    errors.push({
      field: 'maxThreadLength',
      message: 'Maximum thread length must be greater than 0',
      severity: 'error'
    });
  }

  return errors;
}

export function isToolValid(tool: Partial<Tool>): boolean {
  const errors = validateTool(tool);
  return errors.filter(e => e.severity === 'error').length === 0;
}

export function getValidationSummary(errors: ValidationError[]): {
  errorCount: number;
  warningCount: number;
  hasErrors: boolean;
  hasWarnings: boolean;
} {
  const errorCount = errors.filter(e => e.severity === 'error').length;
  const warningCount = errors.filter(e => e.severity === 'warning').length;
  
  return {
    errorCount,
    warningCount,
    hasErrors: errorCount > 0,
    hasWarnings: warningCount > 0
  };
}
