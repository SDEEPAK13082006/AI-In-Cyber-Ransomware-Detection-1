import React, { useState, useEffect } from 'react';
import { 
  History, 
  Search, 
  Filter, 
  Download, 
  RefreshCw, 
  ShieldAlert, 
  ShieldCheck, 
  AlertTriangle, 
  FileText, 
  ExternalLink,
  ChevronLeft,
  ChevronRight,
  Eye,
  X
} from 'lucide-react';
import { fetchAuditLogs, exportAuditLogsCsvUrl } from '../services/api';

const AuditLogsPage = () => {
  const [logs, setLogs] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [riskFilter, setRiskFilter] = useState('ALL');
  const [actionFilter, setActionFilter] = useState('ALL');
  const [selectedRecord, setSelectedRecord] = useState(null);

  const loadLogs = async () => {
    setLoading(true);
    const data = await fetchAuditLogs({
      search: search || undefined,
      risk_level: riskFilter !== 'ALL' ? riskFilter : undefined,
      action: actionFilter !== 'ALL' ? actionFilter : undefined
    });
    setLogs(data.records || []);
    setTotalCount(data.total || 0);
    setLoading(false);
  };

  useEffect(() => {
    loadLogs();
  }, [riskFilter, actionFilter]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    loadLogs();
  };

  const getRiskBadge = (risk) => {
    switch (risk) {
      case 'CRITICAL':
        return 'bg-red-500/20 text-red-400 border border-red-500/40';
      case 'HIGH':
      case 'SUSPICIOUS':
        return 'bg-amber-500/20 text-amber-400 border border-amber-500/40';
      default:
        return 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/40';
    }
  };

  const getActionBadge = (action) => {
    switch (action) {
      case 'QUARANTINED':
      case 'BLOCKED':
        return 'bg-red-950 text-red-400 border border-red-800';
      case 'FLAGGED':
        return 'bg-amber-950 text-amber-400 border border-amber-800';
      default:
        return 'bg-emerald-950 text-emerald-400 border border-emerald-800';
    }
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900 to-indigo-950/40 border border-slate-800 shadow-xl">
        <div>
          <h1 className="text-xl font-extrabold text-slate-100 flex items-center gap-2">
            <History className="w-6 h-6 text-cyan-400" />
            Threat & Incident Audit Logs
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Immutable security event audit trail for forensic compliance and banking ransomware investigation.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={loadLogs}
            className="p-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl transition flex items-center gap-2 text-xs font-semibold"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </button>

          <a
            href={exportAuditLogsCsvUrl()}
            download="ransomware_audit_logs.csv"
            target="_blank"
            rel="noopener noreferrer"
            className="px-4 py-2.5 bg-cyan-600 hover:bg-cyan-500 text-white rounded-xl text-xs font-bold flex items-center gap-2 shadow-lg shadow-cyan-500/20 transition"
          >
            <Download className="w-4 h-4" />
            Export CSV
          </a>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl flex flex-col md:flex-row items-center justify-between gap-4">
        <form onSubmit={handleSearchSubmit} className="flex-1 w-full flex items-center gap-2">
          <div className="relative flex-1">
            <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by file name, process path, or threat indicator..."
              className="w-full pl-10 pr-4 py-2 text-xs bg-slate-950/80 border border-slate-800 rounded-xl text-slate-200 focus:outline-none focus:border-cyan-500 font-mono"
            />
          </div>
          <button
            type="submit"
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-cyan-400 rounded-xl text-xs font-semibold border border-slate-700"
          >
            Search
          </button>
        </form>

        <div className="flex items-center gap-3 w-full md:w-auto">
          <div className="flex items-center gap-2">
            <Filter className="w-4 h-4 text-slate-400" />
            <span className="text-xs text-slate-400 font-semibold">Risk:</span>
            <select
              value={riskFilter}
              onChange={(e) => setRiskFilter(e.target.value)}
              className="bg-slate-950 border border-slate-800 text-xs text-slate-200 rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-cyan-500 font-mono"
            >
              <option value="ALL">All Risk Levels</option>
              <option value="CRITICAL">Critical (Ransomware)</option>
              <option value="SUSPICIOUS">Suspicious</option>
              <option value="SAFE">Safe (Benign)</option>
            </select>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-400 font-semibold">Action:</span>
            <select
              value={actionFilter}
              onChange={(e) => setActionFilter(e.target.value)}
              className="bg-slate-950 border border-slate-800 text-xs text-slate-200 rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-cyan-500 font-mono"
            >
              <option value="ALL">All Actions</option>
              <option value="QUARANTINED">Quarantined</option>
              <option value="BLOCKED">Blocked</option>
              <option value="FLAGGED">Flagged</option>
              <option value="CLEARED">Cleared</option>
            </select>
          </div>
        </div>
      </div>

      {/* Audit Log Table */}
      <div className="rounded-2xl bg-slate-900 border border-slate-800 shadow-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-950/80 text-[10px] uppercase font-bold text-slate-400 tracking-wider border-b border-slate-800">
              <tr>
                <th className="px-4 py-3.5">ID</th>
                <th className="px-4 py-3.5">Timestamp</th>
                <th className="px-4 py-3.5">Analyzed File / Payload</th>
                <th className="px-4 py-3.5">Entropy</th>
                <th className="px-4 py-3.5">Threat Score</th>
                <th className="px-4 py-3.5">Risk Level</th>
                <th className="px-4 py-3.5">Confidence</th>
                <th className="px-4 py-3.5">Action Taken</th>
                <th className="px-4 py-3.5 text-center">Inspect</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono text-[11px]">
              {logs.length === 0 ? (
                <tr>
                  <td colSpan={9} className="px-6 py-8 text-center text-slate-500">
                    No matching audit records found for selected query criteria.
                  </td>
                </tr>
              ) : (
                logs.map((record) => (
                  <tr key={record.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="px-4 py-3 text-slate-500">#{record.id}</td>
                    <td className="px-4 py-3 text-slate-400">{record.timestamp}</td>
                    <td className="px-4 py-3 font-semibold text-slate-100 max-w-xs truncate" title={record.filename}>
                      {record.filename}
                    </td>
                    <td className="px-4 py-3 text-cyan-400">{record.entropy?.toFixed(2) || 'N/A'}</td>
                    <td className="px-4 py-3 font-bold text-slate-200">
                      <span className={record.threat_score >= 75 ? 'text-red-400 font-extrabold' : 'text-emerald-400'}>
                        {record.threat_score?.toFixed(1)}%
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${getRiskBadge(record.risk_level)}`}>
                        {record.risk_level}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-slate-300">{record.prediction_confidence?.toFixed(1)}%</td>
                    <td className="px-4 py-3">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${getActionBadge(record.status)}`}>
                        {record.status}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-center">
                      <button
                        onClick={() => setSelectedRecord(record)}
                        className="p-1.5 rounded-lg bg-slate-800 hover:bg-cyan-500/20 hover:text-cyan-400 text-slate-400 transition"
                        title="View Forensic Details"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Footer info */}
        <div className="px-6 py-3 border-t border-slate-800 bg-slate-950/40 flex items-center justify-between text-xs text-slate-400">
          <span>Showing {logs.length} of {totalCount} total logged events</span>
          <span className="font-mono text-[11px] text-cyan-400">Banking Security Audit Vault v1.0</span>
        </div>
      </div>

      {/* Forensic Detail Modal */}
      {selectedRecord && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden space-y-4">
            <div className="flex items-center justify-between p-5 border-b border-slate-800 bg-slate-950/60">
              <div className="flex items-center gap-2">
                <FileText className="w-5 h-5 text-cyan-400" />
                <h3 className="text-sm font-bold text-slate-100">Forensic Incident Detail #{selectedRecord.id}</h3>
              </div>
              <button
                onClick={() => setSelectedRecord(null)}
                className="p-1 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-slate-200"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-5 space-y-4 text-xs">
              <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1 font-mono">
                <p className="text-slate-400">File Name:</p>
                <p className="text-slate-100 font-bold break-all">{selectedRecord.filename}</p>
              </div>

              <div className="grid grid-cols-2 gap-3 font-mono">
                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                  <span className="text-slate-400">Risk Score:</span>
                  <p className={`text-lg font-bold ${selectedRecord.threat_score >= 75 ? 'text-red-400' : 'text-emerald-400'}`}>
                    {selectedRecord.threat_score}%
                  </p>
                </div>
                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                  <span className="text-slate-400">Shannon Entropy:</span>
                  <p className="text-lg font-bold text-cyan-400">{selectedRecord.entropy}</p>
                </div>
                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                  <span className="text-slate-400">Action:</span>
                  <p className="text-sm font-bold text-amber-400">{selectedRecord.status}</p>
                </div>
                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                  <span className="text-slate-400">Confidence:</span>
                  <p className="text-sm font-bold text-purple-400">{selectedRecord.prediction_confidence}%</p>
                </div>
              </div>

              <div className="p-3 rounded-xl bg-slate-950/80 border border-slate-800">
                <span className="text-slate-400 font-bold uppercase tracking-wider text-[10px]">SHAP Behavioral Assessment</span>
                <p className="text-slate-300 mt-1 leading-relaxed">
                  {selectedRecord.threat_score >= 75
                    ? "High encryption entropy spike combined with process termination and shadow copy deletion indicators confirm active ransomware behavior."
                    : "Low code section entropy, valid Authenticode certificate signature, and zero shadow copy deletion indicators confirm benign system operation."}
                </p>
              </div>
            </div>

            <div className="p-4 border-t border-slate-800 bg-slate-950/40 text-right">
              <button
                onClick={() => setSelectedRecord(null)}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-semibold"
              >
                Close Window
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AuditLogsPage;
