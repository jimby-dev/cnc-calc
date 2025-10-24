import {
  Geometry,
  ToolType
} from '@/types/tool';
import React from 'react';
import { useForm } from 'react-hook-form';

interface GeometryFormProps {
  toolType: ToolType;
  geometry: Partial<Geometry> | undefined;
  onUpdateGeometry: (geometry: Geometry) => void;
  units: 'mm' | 'inch';
  onToggleUnits: (units: 'mm' | 'inch') => void;
}

const GeometryForm: React.FC<GeometryFormProps> = ({
  toolType,
  geometry,
  onUpdateGeometry,
  units,
  onToggleUnits,
}) => {
  const { register, watch, handleSubmit, reset } = useForm<Geometry>({
    defaultValues: geometry,
  });

  // Watch all form fields for real-time updates
  const formValues = watch();

  React.useEffect(() => {
    // Update parent state whenever form values change
    onUpdateGeometry(formValues as Geometry);
  }, [formValues, onUpdateGeometry]);

  React.useEffect(() => {
    // Reset form when toolType changes
    reset(geometry);
  }, [toolType, geometry, reset]);

  const renderFormFields = () => {
    switch (toolType) {
      case 'End Mill':
        return (
          <>
            <InputField label="Diameter" name="diameter" type="number" register={register} units={units} />
            <InputField label="Flute Count" name="fluteCount" type="number" register={register} />
            <InputField label="Helix Angle" name="helixAngle" type="number" register={register} units="°" />
            <InputField label="Flute Length" name="fluteLength" type="number" register={register} units={units} />
            <InputField label="Length of Cut" name="lengthOfCut" type="number" register={register} units={units} />
            <InputField label="Overall Length" name="overallLength" type="number" register={register} units={units} />
            <InputField label="Corner Radius" name="cornerRadius" type="number" register={register} units={units} />
          </>
        );
      case 'Ball End Mill':
        return (
          <>
            <InputField label="Diameter" name="diameter" type="number" register={register} units={units} />
            <InputField label="Flute Count" name="fluteCount" type="number" register={register} />
            <InputField label="Tip Radius" name="tipRadius" type="number" register={register} units={units} />
            <InputField label="Flute Length" name="fluteLength" type="number" register={register} units={units} />
            <InputField label="Overall Length" name="overallLength" type="number" register={register} units={units} />
          </>
        );
      case 'Chamfer':
        return (
          <>
            <InputField label="Included Angle" name="includedAngle" type="number" register={register} units="°" />
            <InputField label="Tip Flat" name="tipFlat" type="number" register={register} units={units} />
            <InputField label="Flute Length" name="fluteLength" type="number" register={register} units={units} />
            <InputField label="Overall Length" name="overallLength" type="number" register={register} units={units} />
            <InputField label="Shank Diameter" name="shankDiameter" type="number" register={register} units={units} />
          </>
        );
      case 'Drill':
        return (
          <>
            <InputField label="Diameter" name="diameter" type="number" register={register} units={units} />
            <InputField label="Point Angle" name="pointAngle" type="number" register={register} units="°" />
            <InputField label="Flute Length" name="fluteLength" type="number" register={register} units={units} />
            <InputField label="Overall Length" name="overallLength" type="number" register={register} units={units} />
          </>
        );
      case 'Reamer':
        return (
          <>
            <InputField label="Diameter" name="diameter" type="number" register={register} units={units} />
            <InputField label="Flute Length" name="fluteLength" type="number" register={register} units={units} />
            <InputField label="Overall Length" name="overallLength" type="number" register={register} units={units} />
            <InputField label="Lead Angle (Optional)" name="leadAngle" type="number" register={register} units="°" />
          </>
        );
      case 'Thread Mill':
        return (
          <>
            <InputField label="Diameter" name="diameter" type="number" register={register} units={units} />
            <InputField label="Pitch" name="pitch" type="number" register={register} units={units} />
            <InputField label="Maximum Thread Length" name="maximumThreadLength" type="number" register={register} units={units} />
            <InputField label="Flute Length" name="fluteLength" type="number" register={register} units={units} />
            <InputField label="Overall Length" name="overallLength" type="number" register={register} units={units} />
          </>
        );
      default:
        return <p className="text-gray-600">Select a tool type to define its geometry.</p>;
    }
  };

  return (
    <div>
      <div className="flex justify-end mb-4">
        <span className="mr-2 text-sm text-gray-700">Units:</span>
        <button
          className={`px-3 py-1 rounded-l-md text-sm ${
            units === 'mm' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'
          }`}
          onClick={() => onToggleUnits('mm')}
        >
          mm
        </button>
        <button
          className={`px-3 py-1 rounded-r-md text-sm ${
            units === 'inch' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'
          }`}
          onClick={() => onToggleUnits('inch')}
        >
          inch
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {renderFormFields()}
      </div>

      {/* Placeholder for SVG Visualization */}
      <div className="mt-6 p-4 border rounded-md bg-gray-50 h-48 flex items-center justify-center">
        <p className="text-gray-500">Dynamic SVG Visualization (Coming Soon)</p>
      </div>
    </div>
  );
};

interface InputFieldProps {
  label: string;
  name: string;
  type: string;
  register: any;
  units?: string;
}

const InputField: React.FC<InputFieldProps> = ({ label, name, type, register, units }) => (
  <div>
    <label htmlFor={name} className="block text-sm font-medium text-gray-700">
      {label}
    </label>
    <div className="mt-1 relative rounded-md shadow-sm">
      <input
        type={type}
        id={name}
        {...register(name, { valueAsNumber: true })}
        className="block w-full rounded-md border-gray-300 pr-10 focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
        step="any"
      />
      {units && (
        <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
          <span className="text-gray-500 sm:text-sm">{units}</span>
        </div>
      )}
    </div>
  </div>
);

export default GeometryForm;