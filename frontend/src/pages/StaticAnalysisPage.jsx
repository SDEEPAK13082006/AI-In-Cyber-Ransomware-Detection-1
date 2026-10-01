import React from 'react';
import FileUploader from '../components/analysis/FileUploader';
import { FileSearch, ShieldCheck, Binary, Cpu } from 'lucide-react';

const StaticAnalysisPage = () => {
  return (
    <div className="space-y-6 pb-12">
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl">
        <h1 className="text-xl font-extrabold text-slate-100 flex items-center gap-2">
          <FileSearch className="w-6 h-6 text-cyan-400" />
          Static PE File & Heuristics Analyzer
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Upload Portable Executable (.exe, .dll) binaries for instant PE section entropy analysis, digital signature verification, and SHAP explainability.
        </p>
      </div>

      <FileUploader />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
          <div className="flex items-center gap-2 text-cyan-400 text-xs font-bold">
            <Binary className="w-4 h-4" />
            <span>Entropy Threshold Scan</span>
          </div>
          <p className="text-[11px] text-slate-400">
            Shannon entropy values exceeding 7.2 indicate encrypted payloads or custom malware packers.
          </p>
        </div>

        <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
          <div className="flex items-center gap-2 text-amber-400 text-xs font-bold">
            <Cpu className="w-4 h-4" />
            <span>Import Table Analysis</span>
          </div>
          <p className="text-[11px] text-slate-400">
            Scans for suspicious Win32 APIs (`VirtualAllocEx`, `WriteProcessMemory`, `CreateRemoteThread`).
          </p>
        </div>

        <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
          <div className="flex items-center gap-2 text-emerald-400 text-xs font-bold">
            <ShieldCheck className="w-4 h-4" />
            <span>Digital Certificate Shield</span>
          </div>
          <p className="text-[11px] text-slate-400">
            Verifies Authenticode digital signatures against Microsoft trusted root certificates.
          </p>
        </div>
      </div>
    </div>
  );
};

export default StaticAnalysisPage;
