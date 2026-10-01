import React, { useEffect, useState } from 'react';
import MetricCards from '../components/dashboard/MetricCards';
import ThreatScoreGauge from '../components/dashboard/ThreatScoreGauge';
import AttackTimelineChart from '../components/dashboard/AttackTimelineChart';
import LiveActivityStream from '../components/dashboard/LiveActivityStream';
import AlertCenter from '../components/alerts/AlertCenter';
import { fetchDashboardMetrics } from '../services/api';
import { ShieldCheck, ShieldAlert, Cpu, Activity } from 'lucide-react';

const DashboardPage = () => {
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    const loadMetrics = async () => {
      const data = await fetchDashboardMetrics();
      setMetrics(data);
    };
    loadMetrics();
  }, []);

  return (
    <div className="space-y-6 pb-12">
      {/* Banner / Header Title */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-gradient-to-r from-slate-900 via-slate-900 to-cyan-950/40 p-6 rounded-2xl border border-slate-800 shadow-xl">
        <div>
          <h1 className="text-xl font-extrabold text-slate-100 flex items-center gap-2">
            <ShieldCheck className="w-6 h-6 text-cyan-400" />
            Security Command Center
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Pre-Encryption Ransomware Defense Platform & Real-Time Behavioral Shield
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="px-3 py-1.5 rounded-xl bg-slate-950/80 border border-slate-800 text-xs font-mono flex items-center gap-2">
            <Activity className="w-4 h-4 text-emerald-400 animate-pulse" />
            <span className="text-slate-300">Telemetry Engine: </span>
            <span className="text-emerald-400 font-bold">ONLINE</span>
          </div>
        </div>
      </div>

      {/* Top Metrics Cards */}
      <MetricCards metrics={metrics} />

      {/* Main Grid Layout: Threat Score & Attack Timeline */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Threat Gauge */}
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl flex flex-col items-center justify-center">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Overall Infrastructure Risk</h3>
          <ThreatScoreGauge score={14.8} riskLevel="SAFE" />
          <p className="text-[11px] text-center text-slate-400 mt-2 px-4">
            Pre-encryption heuristic engine reports zero active ransomware encryption loops.
          </p>
        </div>

        {/* Attack Timeline Chart */}
        <div className="lg:col-span-2 p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wider">Attack Velocity & Threat Trend</h3>
              <p className="text-[11px] text-slate-400">Scanned Benign Operations vs Blocked Ransomware Attempts</p>
            </div>
          </div>
          <AttackTimelineChart data={metrics?.threatTrend} />
        </div>
      </div>

      {/* Live Stream & Alert Center Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <LiveActivityStream />
        </div>
        <div>
          <AlertCenter />
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
