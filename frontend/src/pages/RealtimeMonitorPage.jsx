import React, { useState, useEffect } from 'react';
import { 
  FolderLock, 
  FolderPlus, 
  Radio, 
  ShieldAlert, 
  CheckCircle, 
  Flame, 
  AlertOctagon, 
  Zap, 
  RefreshCw,
  FolderMinus
} from 'lucide-react';
import LiveActivityStream from '../components/dashboard/LiveActivityStream';
import { fetchWatchers, addWatchDirectory, simulateAttack } from '../services/api';

const RealtimeMonitorPage = () => {
  const [watchFolders, setWatchFolders] = useState([]);
  const [newFolder, setNewFolder] = useState('');
  const [simulationStatus, setSimulationStatus] = useState(null);
  const [simulating, setSimulating] = useState(false);

  const loadWatchers = async () => {
    const data = await fetchWatchers();
    setWatchFolders(data);
  };

  useEffect(() => {
    loadWatchers();
  }, []);

  const handleAddFolder = async () => {
    if (!newFolder) return;
    await addWatchDirectory(newFolder);
    setWatchFolders([...watchFolders, { path: newFolder, status: 'ACTIVE', events_captured: 0 }]);
    setNewFolder('');
  };

  const handleSimulateAttack = async (type) => {
    setSimulating(true);
    setSimulationStatus({ status: 'TRIGGERING', message: `Injecting synthetic telemetry for ${type}...` });
    
    const result = await simulateAttack(type);
    setSimulationStatus(result);
    setSimulating(false);
    setTimeout(() => setSimulationStatus(null), 5000);
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900 to-cyan-950/40 border border-slate-800 shadow-xl">
        <div>
          <h1 className="text-xl font-extrabold text-slate-100 flex items-center gap-2">
            <FolderLock className="w-6 h-6 text-cyan-400" />
            Real-Time File System & Process Telemetry Watcher
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Kernel and userland directory monitoring engine (`watchdog`). Real-time entropy computation and shadow copy tamper deterrence.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono font-bold">
            <Radio className="w-4 h-4 animate-pulse" />
            <span>3 DIRECTORIES SECURED</span>
          </span>
        </div>
      </div>

      {/* Simulated Ransomware Attack Lab Card */}
      <div className="p-6 rounded-2xl bg-gradient-to-br from-red-950/20 via-slate-900 to-slate-900 border border-red-900/40 shadow-xl space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Flame className="w-5 h-5 text-red-400 animate-pulse" />
            <h2 className="text-sm font-bold text-slate-100 uppercase tracking-wider">
              Simulated Threat Defense Lab
            </h2>
          </div>
          <span className="text-[10px] font-mono text-red-400/80 bg-red-500/10 px-2.5 py-0.5 rounded border border-red-500/20">
            Safety Sandbox Active
          </span>
        </div>

        <p className="text-xs text-slate-400">
          Inject synthetic ransomware behavioral signatures to test real-time watcher detection, pre-encryption process quarantine, and SIEM dispatch.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-1">
          <button
            onClick={() => handleSimulateAttack('WannaCry_Shadow_Delete')}
            disabled={simulating}
            className="p-3 rounded-xl bg-slate-950/80 hover:bg-red-950/50 border border-slate-800 hover:border-red-500/50 text-left transition flex items-start gap-2.5 group"
          >
            <AlertOctagon className="w-4 h-4 text-red-400 shrink-0 mt-0.5 group-hover:scale-110 transition" />
            <div>
              <p className="text-xs font-bold text-slate-200">Shadow Copy Deletion</p>
              <p className="text-[10px] text-slate-400 mt-0.5">`vssadmin delete shadows /all`</p>
            </div>
          </button>

          <button
            onClick={() => handleSimulateAttack('High_Entropy_Mass_Encryption')}
            disabled={simulating}
            className="p-3 rounded-xl bg-slate-950/80 hover:bg-amber-950/50 border border-slate-800 hover:border-amber-500/50 text-left transition flex items-start gap-2.5 group"
          >
            <Zap className="w-4 h-4 text-amber-400 shrink-0 mt-0.5 group-hover:scale-110 transition" />
            <div>
              <p className="text-xs font-bold text-slate-200">Mass Encryption Loop</p>
              <p className="text-[10px] text-slate-400 mt-0.5">Rapid high-entropy ciphertext I/O</p>
            </div>
          </button>

          <button
            onClick={() => handleSimulateAttack('Extension_Rename_Loop')}
            disabled={simulating}
            className="p-3 rounded-xl bg-slate-950/80 hover:bg-purple-950/50 border border-slate-800 hover:border-purple-500/50 text-left transition flex items-start gap-2.5 group"
          >
            <ShieldAlert className="w-4 h-4 text-purple-400 shrink-0 mt-0.5 group-hover:scale-110 transition" />
            <div>
              <p className="text-xs font-bold text-slate-200">Malicious Extension Rename</p>
              <p className="text-[10px] text-slate-400 mt-0.5">Targeting .locked & .crypto extensions</p>
            </div>
          </button>
        </div>

        {simulationStatus && (
          <div className="p-3.5 rounded-xl bg-red-500/10 border border-red-500/30 text-xs text-red-300 flex items-center gap-2">
            <CheckCircle className="w-4 h-4 text-emerald-400" />
            <span>{simulationStatus.message}</span>
          </div>
        )}
      </div>

      {/* Directory Watcher Configuration */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-4">
        <h2 className="text-sm font-bold text-slate-100 uppercase tracking-wider">Configured Protection Directories</h2>
        
        <div className="flex items-center gap-3">
          <input
            type="text"
            value={newFolder}
            onChange={(e) => setNewFolder(e.target.value)}
            placeholder="Enter absolute folder path to monitor (e.g. C:\Users\Finance\Data)..."
            className="flex-1 px-4 py-2.5 text-xs bg-slate-950/70 border border-slate-800 rounded-xl text-slate-200 focus:outline-none focus:border-cyan-500 font-mono"
          />
          <button
            onClick={handleAddFolder}
            className="px-4 py-2.5 bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold rounded-xl flex items-center gap-2 shadow-lg shadow-cyan-500/20 transition"
          >
            <FolderPlus className="w-4 h-4" />
            Add Watch Directory
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-2">
          {watchFolders.map((folder, idx) => (
            <div key={idx} className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 flex items-center justify-between">
              <div className="truncate mr-2">
                <p className="text-xs font-mono font-bold text-slate-200 truncate" title={folder.path}>{folder.path}</p>
                <p className="text-[10px] text-slate-400 mt-0.5">{folder.events_captured || 850} scan events captured</p>
              </div>
              <span className="flex items-center gap-1 text-[10px] font-mono font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20 shrink-0">
                <Radio className="w-3 h-3 animate-pulse" />
                ACTIVE
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Monitored Event Log Stream */}
      <LiveActivityStream />
    </div>
  );
};

export default RealtimeMonitorPage;
