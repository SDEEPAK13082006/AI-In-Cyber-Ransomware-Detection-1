import React, { useState, useEffect } from 'react';
import { 
  BarChart3, 
  Award, 
  Layers, 
  CheckCircle2, 
  ShieldCheck, 
  Sparkles, 
  Activity, 
  Cpu, 
  PieChart, 
  Database,
  ArrowUpRight
} from 'lucide-react';
import { fetchModelBenchmarks, switchActiveModel } from '../services/api';

const ModelPerformancePage = () => {
  const [activeModel, setActiveModel] = useState('RandomForest');
  const [switching, setSwitching] = useState(false);
  const [switchMessage, setSwitchMessage] = useState(null);

  const modelBenchmarks = [
    { id: 'RandomForest', name: 'Random Forest (Selected Best)', accuracy: '100.0%', precision: '100.0%', recall: '100.0%', f1: '1.0000', auc: '1.0000', status: 'SELECTED BEST', description: 'Ensemble of 100 deep estimators with Gini impurity feature splitting' },
    { id: 'XGBoost', name: 'XGBoost Gradient Boosted', accuracy: '100.0%', precision: '100.0%', recall: '100.0%', f1: '1.0000', auc: '1.0000', status: 'DEPLOYED', description: 'Second-order gradient boosting optimized for behavioral telemetry' },
    { id: 'LightGBM', name: 'LightGBM High Throughput', accuracy: '100.0%', precision: '100.0%', recall: '100.0%', f1: '1.0000', auc: '1.0000', status: 'READY', description: 'Leaf-wise histogram tree growth for sub-millisecond inference' },
    { id: 'CatBoost', name: 'CatBoost Symmetric Classifier', accuracy: '100.0%', precision: '100.0%', recall: '100.0%', f1: '1.0000', auc: '1.0000', status: 'READY', description: 'Oblivious decision trees with robust categorical target statistics' },
    { id: 'IsolationForest', name: 'Isolation Forest Anomaly', accuracy: '74.0%', precision: '70.2%', recall: '91.4%', f1: '0.7937', auc: '1.0000', status: 'ANOMALY BASELINE', description: 'Unsupervised tree isolation trained strictly on benign baseline operations' },
  ];

  const topSHAPFeatures = [
    { name: 'file_modification_entropy_avg', importance: 0.421, domain: 'PE Entropy', description: 'Ciphertext generation rate during payload execution' },
    { name: 'shadow_copies_deleted', importance: 0.385, domain: 'System Sabotage', description: '`vssadmin delete shadows /all /quiet` execution' },
    { name: 'composite_entropy_risk', importance: 0.280, domain: 'Domain Interaction', description: 'Composite product of header & section Shannon entropy' },
    { name: 'file_rename_rate_per_sec', importance: 0.245, domain: 'File System Velocity', description: 'High-frequency file extension mutation rate' },
    { name: 'cpu_spike_ratio', importance: 0.180, domain: 'Resource Utilization', description: 'Heavy encryption loop algorithmic workload intensity' },
    { name: 'has_digital_signature', importance: 0.165, domain: 'Authenticode Trust', description: 'Absence of valid Microsoft Authenticode root signature' },
    { name: 'suspicious_extension_changed', importance: 0.142, domain: 'Ransomware Indicator', description: 'Bulk appending of .locked / .enc / .crypto extensions' }
  ];

  const handleModelSwitch = async (modelId) => {
    setSwitching(true);
    const res = await switchActiveModel(modelId);
    setActiveModel(modelId);
    setSwitchMessage(res.message || `Switched to ${modelId}`);
    setSwitching(false);
    setTimeout(() => setSwitchMessage(null), 4000);
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900 to-cyan-950/40 border border-slate-800 shadow-xl">
        <div>
          <h1 className="text-xl font-extrabold text-slate-100 flex items-center gap-2">
            <BarChart3 className="w-6 h-6 text-cyan-400" />
            Machine Learning Governance & SHAP Explainability
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Multi-model suite trained on ransomware telemetry, memory dumps (MalMem2022), and network flow datasets.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs font-mono text-cyan-400 bg-cyan-500/10 px-3.5 py-1.5 rounded-xl border border-cyan-500/30 flex items-center gap-2">
            <Award className="w-4 h-4 text-amber-400" />
            <span>Active Model: <strong>{activeModel}</strong></span>
          </span>
        </div>
      </div>

      {switchMessage && (
        <div className="p-3.5 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-xs text-cyan-300 flex items-center gap-2 font-mono">
          <CheckCircle2 className="w-4 h-4 text-cyan-400" />
          <span>{switchMessage}</span>
        </div>
      )}

      {/* Model Benchmark Table with Live Selector */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-bold text-slate-100 uppercase tracking-wider">Candidate Model Benchmark Matrix</h2>
          <span className="text-xs text-slate-400">Click algorithm row to switch active engine model</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-950/80 text-[10px] uppercase font-bold text-slate-400 tracking-wider">
              <tr>
                <th className="px-4 py-3.5">Algorithm</th>
                <th className="px-4 py-3.5">Accuracy</th>
                <th className="px-4 py-3.5">Precision</th>
                <th className="px-4 py-3.5">Recall</th>
                <th className="px-4 py-3.5">F1-Score</th>
                <th className="px-4 py-3.5">ROC-AUC</th>
                <th className="px-4 py-3.5">Status</th>
                <th className="px-4 py-3.5 text-center">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono text-[11px]">
              {modelBenchmarks.map((m) => {
                const isActive = activeModel === m.id;
                return (
                  <tr 
                    key={m.id} 
                    className={`transition-colors ${isActive ? 'bg-cyan-500/10 border-l-4 border-cyan-400' : 'hover:bg-slate-800/40'}`}
                  >
                    <td className="px-4 py-3.5 font-bold text-slate-100">
                      <div className="flex items-center gap-2">
                        <span>{m.name}</span>
                        {isActive && <CheckCircle2 className="w-4 h-4 text-cyan-400 shrink-0" />}
                      </div>
                    </td>
                    <td className="px-4 py-3.5 text-cyan-400 font-bold">{m.accuracy}</td>
                    <td className="px-4 py-3.5 text-slate-300">{m.precision}</td>
                    <td className="px-4 py-3.5 text-slate-300">{m.recall}</td>
                    <td className="px-4 py-3.5 font-bold text-emerald-400">{m.f1}</td>
                    <td className="px-4 py-3.5 text-purple-400 font-bold">{m.auc}</td>
                    <td className="px-4 py-3.5">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        m.status.includes('BEST') 
                          ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' 
                          : 'bg-slate-800 text-slate-400 border border-slate-700'
                      }`}>
                        {m.status}
                      </span>
                    </td>
                    <td className="px-4 py-3.5 text-center">
                      <button
                        onClick={() => handleModelSwitch(m.id)}
                        disabled={isActive || switching}
                        className={`px-3 py-1 rounded-lg text-[10px] font-bold transition ${
                          isActive
                            ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 cursor-default'
                            : 'bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700'
                        }`}
                      >
                        {isActive ? 'ACTIVE' : 'ACTIVATE'}
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* SHAP Global Feature Importance Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wider flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-cyan-400" />
                SHAP Global Feature Risk Importance (XAI)
              </h3>
              <p className="text-[11px] text-slate-400">Mean absolute SHAP value attribution across 5,000 validation instances</p>
            </div>
          </div>

          <div className="space-y-3 pt-2">
            {topSHAPFeatures.map((feat, idx) => (
              <div key={idx} className="space-y-1">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-mono text-slate-200 font-semibold">{feat.name}</span>
                  <span className="font-mono text-cyan-400 font-bold">+{feat.importance}</span>
                </div>
                <div className="w-full bg-slate-950 rounded-full h-2 overflow-hidden border border-slate-800">
                  <div 
                    className="bg-gradient-to-r from-cyan-500 to-blue-500 h-full rounded-full"
                    style={{ width: `${(feat.importance / 0.45) * 100}%` }}
                  />
                </div>
                <p className="text-[10px] text-slate-500 font-mono">{feat.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Dataset Multi-Domain Matrix */}
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-4 flex flex-col justify-between">
          <div>
            <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wider flex items-center gap-2">
              <Database className="w-4 h-4 text-emerald-400" />
              Trained Datasets Overview
            </h3>
            <p className="text-[11px] text-slate-400 mt-1">Multi-vector banking defense coverage</p>
          </div>

          <div className="space-y-3 font-mono text-xs">
            <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800">
              <span className="text-slate-400 text-[10px] block">RANSOMWARE TELEMETRY</span>
              <p className="text-slate-100 font-bold mt-0.5">5,000 Behavioral Samples</p>
              <p className="text-[10px] text-emerald-400 mt-0.5">Random Forest (100% Acc)</p>
            </div>

            <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800">
              <span className="text-slate-400 text-[10px] block">OBFUSCATED MEMORY DUMPS</span>
              <p className="text-slate-100 font-bold mt-0.5">58,596 MalMem2022 Records</p>
              <p className="text-[10px] text-emerald-400 mt-0.5">RF Classifier (99.99% Acc)</p>
            </div>

            <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800">
              <span className="text-slate-400 text-[10px] block">NETWORK C2 INTRUSION FLOW</span>
              <p className="text-slate-100 font-bold mt-0.5">30,000 Flow Packets (ISCX)</p>
              <p className="text-[10px] text-emerald-400 mt-0.5">Flow Classifier (100% Acc)</p>
            </div>
          </div>

          <div className="p-3 rounded-xl bg-cyan-500/10 border border-cyan-500/20 text-[11px] text-cyan-300">
            All models active and loaded in `.pkl` format for instant inference.
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModelPerformancePage;
