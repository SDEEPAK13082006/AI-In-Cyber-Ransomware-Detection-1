import React from 'react';
import { Cpu, ShieldAlert, Layers } from 'lucide-react';

const SHAPExplanationView = ({ drivers }) => {
  if (!drivers || drivers.length === 0) return null;

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2 text-xs font-bold text-slate-300 uppercase tracking-wider">
        <Layers className="w-4 h-4 text-cyan-400" />
        <span>SHAP Feature Risk Attribution (Model Explainability)</span>
      </div>

      <div className="space-y-2">
        {drivers.map((driver, idx) => (
          <div key={idx} className="p-3 rounded-lg bg-slate-950/60 border border-slate-800 flex items-center justify-between text-xs">
            <div className="flex items-center gap-2">
              <ShieldAlert className="w-3.5 h-3.5 text-amber-400 shrink-0" />
              <span className="font-mono text-slate-200 font-medium">{driver.feature}</span>
            </div>
            <span className="font-mono font-bold text-red-400 bg-red-500/10 px-2 py-0.5 rounded border border-red-500/20">
              {driver.impact}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SHAPExplanationView;
