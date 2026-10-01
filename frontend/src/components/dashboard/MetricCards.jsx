import React from 'react';
import { Files, AlertTriangle, ShieldCheck, FolderGit2, Cpu, Activity } from 'lucide-react';

const MetricCards = ({ metrics }) => {
  const cards = [
    {
      title: 'Total Files Analyzed',
      value: metrics?.totalFilesAnalyzed?.toLocaleString() || '14,285',
      subtext: '+1,240 scan events today',
      icon: Files,
      color: 'text-cyan-400',
      bg: 'bg-cyan-500/10',
      border: 'border-cyan-500/20'
    },
    {
      title: 'Suspicious Heuristics',
      value: metrics?.suspiciousFiles || '34',
      subtext: 'Requires Analyst Review',
      icon: AlertTriangle,
      color: 'text-amber-400',
      bg: 'bg-amber-500/10',
      border: 'border-amber-500/20'
    },
    {
      title: 'Ransomware Payloads Blocked',
      value: metrics?.ransomwareBlocked || '12',
      subtext: 'Zero Encryption Incidents',
      icon: ShieldCheck,
      color: 'text-emerald-400',
      bg: 'bg-emerald-500/10',
      border: 'border-emerald-500/20'
    },
    {
      title: 'Monitored Folders',
      value: metrics?.activeWatchers || '4',
      subtext: 'Real-time System Watchers',
      icon: FolderGit2,
      color: 'text-purple-400',
      bg: 'bg-purple-500/10',
      border: 'border-purple-500/20'
    }
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card, idx) => {
        const Icon = card.icon;
        return (
          <div
            key={idx}
            className={`p-4 rounded-xl bg-slate-900/70 border ${card.border} backdrop-blur-md shadow-lg flex flex-col justify-between hover:border-slate-700 transition-all duration-200`}
          >
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-semibold text-slate-400">{card.title}</span>
              <div className={`p-2 rounded-lg ${card.bg}`}>
                <Icon className={`w-4 h-4 ${card.color}`} />
              </div>
            </div>
            <div>
              <h3 className="text-2xl font-extrabold text-slate-100 font-mono tracking-tight">{card.value}</h3>
              <p className="text-[11px] text-slate-400 font-medium mt-1">{card.subtext}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default MetricCards;
