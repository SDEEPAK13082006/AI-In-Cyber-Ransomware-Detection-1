import React, { useState, useEffect } from 'react';
import { 
  Settings, 
  ShieldAlert, 
  ShieldCheck, 
  Sliders, 
  Save, 
  Bell, 
  Lock, 
  AlertOctagon, 
  Cpu, 
  CheckCircle2, 
  Volume2, 
  Webhook
} from 'lucide-react';
import { fetchSecurityPolicy, updateSecurityPolicy } from '../services/api';

const SecurityPolicyPage = () => {
  const [policy, setPolicy] = useState({
    sensitivity_threshold: 75.0,
    auto_quarantine: true,
    shadow_copy_protection: true,
    entropy_threshold: 7.2,
    alert_sound: true,
    webhook_url: 'https://hooks.slack.com/services/BANK/CYBER/ALERTS'
  });
  const [savedStatus, setSavedStatus] = useState(false);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    const load = async () => {
      const data = await fetchSecurityPolicy();
      setPolicy(data);
    };
    load();
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    await updateSecurityPolicy(policy);
    setSaving(false);
    setSavedStatus(true);
    setTimeout(() => setSavedStatus(false), 3000);
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900 to-cyan-950/40 border border-slate-800 shadow-xl">
        <div>
          <h1 className="text-xl font-extrabold text-slate-100 flex items-center gap-2">
            <Settings className="w-6 h-6 text-cyan-400" />
            Security & Ransomware Defense Policy
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Configure automated response triggers, pre-encryption detection thresholds, and incident notification dispatchers.
          </p>
        </div>

        {savedStatus && (
          <div className="flex items-center gap-2 px-4 py-2 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 rounded-xl text-xs font-semibold">
            <CheckCircle2 className="w-4 h-4" />
            <span>Policy Enforced Successfully</span>
          </div>
        )}
      </div>

      <form onSubmit={handleSave} className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Detection Engine Sensitivity Card */}
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-6">
          <div className="flex items-center gap-3 border-b border-slate-800 pb-4">
            <div className="p-2 rounded-xl bg-cyan-500/10 text-cyan-400">
              <Sliders className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-sm font-bold text-slate-100">Machine Learning Sensitivity Threshold</h2>
              <p className="text-[11px] text-slate-400">Risk cutoff for automatic process kill and file quarantine</p>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-xs font-semibold mb-2">
                <span className="text-slate-300">Quarantine Threat Score Threshold:</span>
                <span className="text-cyan-400 font-mono font-bold text-sm">{policy.sensitivity_threshold}%</span>
              </div>
              <input
                type="range"
                min="50"
                max="95"
                step="1"
                value={policy.sensitivity_threshold}
                onChange={(e) => setPolicy({ ...policy, sensitivity_threshold: parseFloat(e.target.value) })}
                className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-500"
              />
              <div className="flex justify-between text-[10px] text-slate-500 font-mono mt-1">
                <span>50% (High Sensitivity)</span>
                <span>75% (Recommended)</span>
                <span>95% (Conservative)</span>
              </div>
            </div>

            <div className="pt-2">
              <div className="flex justify-between text-xs font-semibold mb-2">
                <span className="text-slate-300">Shannon Entropy Limit:</span>
                <span className="text-amber-400 font-mono font-bold text-sm">{policy.entropy_threshold}</span>
              </div>
              <input
                type="range"
                min="6.0"
                max="7.99"
                step="0.05"
                value={policy.entropy_threshold}
                onChange={(e) => setPolicy({ ...policy, entropy_threshold: parseFloat(e.target.value) })}
                className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-amber-500"
              />
              <p className="text-[11px] text-slate-400 mt-1">
                Files exceeding this Shannon entropy level are flagged for cipher-text payload scanning.
              </p>
            </div>
          </div>
        </div>

        {/* Automated Defense Enforcement */}
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-6">
          <div className="flex items-center gap-3 border-b border-slate-800 pb-4">
            <div className="p-2 rounded-xl bg-red-500/10 text-red-400">
              <Lock className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-sm font-bold text-slate-100">Automated Quarantine & Mitigation</h2>
              <p className="text-[11px] text-slate-400">Active behavioral defense shields</p>
            </div>
          </div>

          <div className="space-y-4">
            <label className="flex items-center justify-between p-3.5 rounded-xl bg-slate-950/70 border border-slate-800 cursor-pointer hover:border-slate-700 transition">
              <div>
                <p className="text-xs font-bold text-slate-200">Automatic Process Termination & Quarantine</p>
                <p className="text-[11px] text-slate-400">Immediately kill PID and isolate payload when risk exceeds threshold</p>
              </div>
              <input
                type="checkbox"
                checked={policy.auto_quarantine}
                onChange={(e) => setPolicy({ ...policy, auto_quarantine: e.target.checked })}
                className="w-4 h-4 text-cyan-600 bg-slate-900 border-slate-700 rounded focus:ring-cyan-500"
              />
            </label>

            <label className="flex items-center justify-between p-3.5 rounded-xl bg-slate-950/70 border border-slate-800 cursor-pointer hover:border-slate-700 transition">
              <div>
                <p className="text-xs font-bold text-slate-200">Shadow Copy (`vssadmin`) Block Shield</p>
                <p className="text-[11px] text-slate-400">Intercept and deny any unprivileged shadow copy delete calls</p>
              </div>
              <input
                type="checkbox"
                checked={policy.shadow_copy_protection}
                onChange={(e) => setPolicy({ ...policy, shadow_copy_protection: e.target.checked })}
                className="w-4 h-4 text-cyan-600 bg-slate-900 border-slate-700 rounded focus:ring-cyan-500"
              />
            </label>

            <label className="flex items-center justify-between p-3.5 rounded-xl bg-slate-950/70 border border-slate-800 cursor-pointer hover:border-slate-700 transition">
              <div>
                <p className="text-xs font-bold text-slate-200">Audible Incident Alert Sound</p>
                <p className="text-[11px] text-slate-400">Play synthesized warning chime when ransomware is detected</p>
              </div>
              <input
                type="checkbox"
                checked={policy.alert_sound}
                onChange={(e) => setPolicy({ ...policy, alert_sound: e.target.checked })}
                className="w-4 h-4 text-cyan-600 bg-slate-900 border-slate-700 rounded focus:ring-cyan-500"
              />
            </label>
          </div>
        </div>

        {/* SIEM & Webhook Integrations */}
        <div className="lg:col-span-2 p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-6">
          <div className="flex items-center gap-3 border-b border-slate-800 pb-4">
            <div className="p-2 rounded-xl bg-purple-500/10 text-purple-400">
              <Webhook className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-sm font-bold text-slate-100">SIEM & Incident Webhook Integration</h2>
              <p className="text-[11px] text-slate-400">Push high-priority ransomware incident alerts to Slack, Microsoft Teams, or Splunk</p>
            </div>
          </div>

          <div className="space-y-3">
            <label className="text-xs font-semibold text-slate-300">Webhook Receiver URL:</label>
            <div className="flex items-center gap-3">
              <input
                type="text"
                value={policy.webhook_url}
                onChange={(e) => setPolicy({ ...policy, webhook_url: e.target.value })}
                placeholder="https://hooks.slack.com/services/..."
                className="flex-1 px-4 py-2.5 text-xs bg-slate-950 border border-slate-800 rounded-xl text-slate-200 focus:outline-none focus:border-cyan-500 font-mono"
              />
            </div>
          </div>

          <div className="flex justify-end pt-4 border-t border-slate-800">
            <button
              type="submit"
              disabled={saving}
              className="px-6 py-2.5 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white text-xs font-bold rounded-xl shadow-lg shadow-cyan-500/20 flex items-center gap-2 transition"
            >
              <Save className="w-4 h-4" />
              {saving ? 'Applying Policy Changes...' : 'Save & Enforce Security Policy'}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
};

export default SecurityPolicyPage;
