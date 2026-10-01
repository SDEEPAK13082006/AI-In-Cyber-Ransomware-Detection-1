import React from 'react';

const ThreatScoreGauge = ({ score = 15.4, riskLevel = 'LOW' }) => {
  const getScoreColor = (s) => {
    if (s >= 75) return { stroke: '#ef4444', text: 'text-red-500', bg: 'bg-red-500/10', label: 'CRITICAL THREAT' };
    if (s >= 40) return { stroke: '#f59e0b', text: 'text-amber-500', bg: 'bg-amber-500/10', label: 'SUSPICIOUS' };
    return { stroke: '#10b981', text: 'text-emerald-500', bg: 'bg-emerald-500/10', label: 'SYSTEM SAFE' };
  };

  const colorInfo = getScoreColor(score);
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <div className="flex flex-col items-center justify-center p-4">
      <div className="relative w-36 h-36 flex items-center justify-center">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 120 120">
          <circle
            cx="60"
            cy="60"
            r={radius}
            className="stroke-slate-800"
            strokeWidth="10"
            fill="transparent"
          />
          <circle
            cx="60"
            cy="60"
            r={radius}
            stroke={colorInfo.stroke}
            strokeWidth="10"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            className="transition-all duration-1000 ease-out"
          />
        </svg>

        <div className="absolute flex flex-col items-center justify-center">
          <span className="text-2xl font-extrabold text-slate-100 font-mono tracking-tight">
            {score.toFixed(1)}%
          </span>
          <span className="text-[9px] uppercase font-bold tracking-widest text-slate-400">
            Threat Score
          </span>
        </div>
      </div>

      <div className={`mt-3 px-3 py-1 rounded-full border border-current text-xs font-bold font-mono ${colorInfo.text} ${colorInfo.bg}`}>
        {colorInfo.label}
      </div>
    </div>
  );
};

export default ThreatScoreGauge;
