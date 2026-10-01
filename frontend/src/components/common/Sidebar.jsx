import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  ShieldAlert, 
  LayoutDashboard, 
  FileSearch, 
  FolderLock, 
  BarChart3, 
  History, 
  Settings, 
  Radio,
  Lock
} from 'lucide-react';

const Sidebar = () => {
  const navItems = [
    { path: '/', label: 'Overview Dashboard', icon: LayoutDashboard },
    { path: '/static-analysis', label: 'Static & PE Analysis', icon: FileSearch },
    { path: '/realtime-monitor', label: 'Live Folder Watcher', icon: FolderLock },
    { path: '/model-performance', label: 'ML Models & SHAP', icon: BarChart3 },
    { path: '/audit-logs', label: 'Threat & Audit Logs', icon: History },
    { path: '/settings', label: 'Security Policy', icon: Settings },
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col min-h-screen select-none">
      {/* Brand Header */}
      <div className="h-16 px-6 flex items-center gap-3 border-b border-slate-800 bg-slate-950/50">
        <div className="p-2 bg-gradient-to-tr from-cyan-600 to-blue-600 rounded-lg shadow-lg shadow-cyan-500/20">
          <ShieldAlert className="w-6 h-6 text-white" />
        </div>
        <div>
          <h1 className="font-bold text-base text-slate-100 tracking-wide">MS Defender</h1>
          <p className="text-[11px] text-cyan-400 font-medium">AI Ransomware Defense</p>
        </div>
      </div>

      {/* Real-time Status Badge */}
      <div className="p-4 mx-3 my-4 rounded-xl bg-slate-800/40 border border-slate-700/50 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="relative flex h-2.5 w-2.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
          </span>
          <span className="text-xs font-semibold text-slate-300">Engine Active</span>
        </div>
        <Radio className="w-4 h-4 text-cyan-400 animate-pulse" />
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 px-3 space-y-1.5">
        <p className="px-3 text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Security Console</p>
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-xs font-medium transition-all duration-200 ${
                  isActive
                    ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 shadow-sm shadow-cyan-500/10 font-semibold'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`
              }
            >
              <Icon className="w-4 h-4 shrink-0" />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      {/* Protection Status Footer */}
      <div className="p-4 border-t border-slate-800 bg-slate-950/40">
        <div className="flex items-center gap-3 text-xs text-slate-400">
          <Lock className="w-4 h-4 text-emerald-400 shrink-0" />
          <div className="truncate">
            <p className="font-semibold text-slate-300">Pre-Encryption Guard</p>
            <p className="text-[10px] text-slate-400">Zero-Day Shield Enabled</p>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
