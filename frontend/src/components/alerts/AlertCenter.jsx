import React, { useState } from 'react';
import { Bell, ShieldAlert, Volume2, VolumeX, CheckCircle, Trash2 } from 'lucide-react';

const AlertCenter = () => {
  const [soundEnabled, setSoundEnabled] = useState(true);
  const [alerts, setAlerts] = useState([
    { id: 1, type: 'CRITICAL', title: 'Ransomware Blocked (LockBit 3.0 Variant)', message: 'High velocity file rename & shadow copy deletion detected on C:\\Users\\Desktop\\Vault. Execution killed.', time: '2 mins ago' },
    { id: 2, type: 'HIGH', title: 'Unsigned Executable Scanned', message: 'PE entropy = 7.84. High probability of packed/encrypted payload.', time: '14 mins ago' },
    { id: 3, type: 'MEDIUM', title: 'Registry Run Key Modification', message: 'Process vssadmin.exe attempted privilege escalation.', time: '1 hour ago' },
  ]);

  const clearAlerts = () => setAlerts([]);

  return (
    <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2">
          <Bell className="w-5 h-5 text-cyan-400" />
          <h2 className="text-sm font-bold text-slate-100 uppercase tracking-wider">Live Security Alert Center</h2>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => setSoundEnabled(!soundEnabled)}
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors"
            title={soundEnabled ? "Mute Alert Audio" : "Enable Alert Audio"}
          >
            {soundEnabled ? <Volume2 className="w-4 h-4 text-emerald-400" /> : <VolumeX className="w-4 h-4 text-slate-500" />}
          </button>
          <button
            onClick={clearAlerts}
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-red-400 transition-colors"
            title="Clear All Alerts"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      {alerts.length === 0 ? (
        <div className="py-8 text-center text-slate-500 text-xs flex flex-col items-center gap-2">
          <CheckCircle className="w-8 h-8 text-emerald-500/40" />
          <p>No active security alerts. All systems protected.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {alerts.map((alert) => (
            <div 
              key={alert.id} 
              className={`p-3.5 rounded-xl border flex items-start gap-3 text-xs transition-all ${
                alert.type === 'CRITICAL'
                  ? 'bg-red-500/10 border-red-500/30 text-red-200'
                  : alert.type === 'HIGH'
                  ? 'bg-amber-500/10 border-amber-500/30 text-amber-200'
                  : 'bg-slate-800/60 border-slate-700/50 text-slate-300'
              }`}
            >
              <ShieldAlert className={`w-5 h-5 shrink-0 mt-0.5 ${
                alert.type === 'CRITICAL' ? 'text-red-400 animate-pulse' : 'text-amber-400'
              }`} />
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-slate-100">{alert.title}</span>
                  <span className="text-[10px] text-slate-400 font-mono">{alert.time}</span>
                </div>
                <p className="mt-1 text-slate-300 leading-relaxed text-[11px]">{alert.message}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AlertCenter;
