import React, { useEffect, useState } from 'react';
import { Activity, ShieldAlert, ShieldCheck } from 'lucide-react';
import { fetchLiveActivityLogs } from '../../services/api';

const LiveActivityStream = () => {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const loadLogs = async () => {
      const data = await fetchLiveActivityLogs();
      setLogs(data);
    };
    loadLogs();
  }, []);

  return (
    <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <Activity className="w-5 h-5 text-cyan-400 animate-pulse" />
          <h2 className="text-sm font-bold text-slate-100 uppercase tracking-wider">Live Monitored Telemetry Stream</h2>
        </div>
        <span className="text-[10px] font-mono text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
          Real-time Engine Online
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs text-slate-300">
          <thead className="bg-slate-950/60 text-[10px] uppercase font-bold text-slate-400 tracking-wider">
            <tr>
              <th className="px-3 py-2">Timestamp</th>
              <th className="px-3 py-2">Target File Path</th>
              <th className="px-3 py-2">Behavior Event</th>
              <th className="px-3 py-2">Threat Score</th>
              <th className="px-3 py-2">System Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 font-mono text-[11px]">
            {logs.map((log, idx) => (
              <tr key={idx} className="hover:bg-slate-800/40 transition-colors">
                <td className="px-3 py-2.5 text-slate-400">{log.timestamp}</td>
                <td className="px-3 py-2.5 font-semibold text-slate-200 truncate max-w-xs">{log.file}</td>
                <td className="px-3 py-2.5 text-slate-300">{log.event}</td>
                <td className="px-3 py-2.5">
                  <span className={`px-2 py-0.5 rounded font-bold ${
                    log.risk === 'CRITICAL' ? 'bg-red-500/20 text-red-400 border border-red-500/30' :
                    log.risk === 'HIGH' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' :
                    'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                  }`}>
                    {log.score}%
                  </span>
                </td>
                <td className="px-3 py-2.5 text-slate-300 flex items-center gap-1.5">
                  {log.risk === 'CRITICAL' ? (
                    <ShieldAlert className="w-3.5 h-3.5 text-red-400" />
                  ) : (
                    <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                  )}
                  {log.action}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default LiveActivityStream;
