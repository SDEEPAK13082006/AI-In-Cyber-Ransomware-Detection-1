import React, { useState } from 'react';
import { ShieldAlert, User, KeyRound, ArrowRight, Eye, EyeOff, CheckCircle2, AlertCircle, Loader2, Cpu } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { loginUser } from '../services/api';

const LoginPage = () => {
  const [username, setUsername] = useState('AdminAnalyst');
  const [password, setPassword] = useState('admin123');
  const [role, setRole] = useState('admin');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');
    setSuccessMessage('');
    setLoading(true);

    try {
      const data = await loginUser(username, password);
      setSuccessMessage('Authentication successful! Establishing secure session...');
      setTimeout(() => {
        login(data.username || username, data.role || role, data.access_token);
      }, 800);
    } catch (err) {
      setErrorMessage(err.message || 'Authentication failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleQuickFill = (demoUsername, demoRole) => {
    setUsername(demoUsername);
    setPassword('admin123');
    setRole(demoRole);
    setErrorMessage('');
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4 relative overflow-hidden font-sans">
      {/* Background Ambient Glows & Grid */}
      <div className="absolute inset-0 bg-[radial-gradient(#1e293b_1px,transparent_1px)] [background-size:24px_24px] opacity-30"></div>
      <div className="absolute -top-40 -left-40 w-96 h-96 bg-cyan-600/15 rounded-full blur-3xl pointer-events-none"></div>
      <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-blue-600/15 rounded-full blur-3xl pointer-events-none"></div>

      <div className="w-full max-w-md p-8 rounded-2xl bg-slate-900/90 border border-slate-800 backdrop-blur-2xl shadow-2xl space-y-6 z-10">
        
        {/* Header Branding */}
        <div className="flex flex-col items-center text-center space-y-3">
          <div className="p-3.5 bg-gradient-to-tr from-cyan-600 to-blue-600 rounded-2xl shadow-xl shadow-cyan-500/20 ring-1 ring-cyan-400/30">
            <ShieldAlert className="w-9 h-9 text-white animate-pulse" />
          </div>
          <div>
            <h1 className="text-2xl font-black text-slate-100 tracking-tight flex items-center justify-center gap-2">
              <span>Cyber Shield AI</span>
              <span className="px-2 py-0.5 text-[10px] font-bold bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 rounded-full">v4.2</span>
            </h1>
            <p className="text-xs text-cyan-400/90 font-medium mt-1">Enterprise Ransomware Detection Platform</p>
          </div>
        </div>

        {/* Feedback Alerts */}
        {errorMessage && (
          <div className="p-3 bg-red-950/60 border border-red-800/80 rounded-xl text-red-300 text-xs flex items-start gap-2.5 shadow-sm">
            <AlertCircle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
            <span>{errorMessage}</span>
          </div>
        )}

        {successMessage && (
          <div className="p-3 bg-emerald-950/60 border border-emerald-800/80 rounded-xl text-emerald-300 text-xs flex items-center gap-2.5 shadow-sm">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>{successMessage}</span>
          </div>
        )}

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1.5">Analyst Username</label>
            <div className="relative">
              <User className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter username"
                className="w-full pl-10 pr-4 py-2.5 text-xs bg-slate-950/80 border border-slate-800 rounded-xl text-slate-200 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-all placeholder:text-slate-600"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1.5">Secret Key / Password</label>
            <div className="relative">
              <KeyRound className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500" />
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter password"
                className="w-full pl-10 pr-10 py-2.5 text-xs bg-slate-950/80 border border-slate-800 rounded-xl text-slate-200 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-all placeholder:text-slate-600"
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300 transition-colors"
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1.5">Access Role (RBAC Scope)</label>
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              className="w-full px-3.5 py-2.5 text-xs bg-slate-950/80 border border-slate-800 rounded-xl text-slate-200 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-all cursor-pointer"
            >
              <option value="admin">Administrator / Threat Hunter</option>
              <option value="analyst">SOC Security Analyst</option>
              <option value="auditor">Compliance Auditor</option>
            </select>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white text-xs font-bold rounded-xl shadow-lg shadow-cyan-500/25 flex items-center justify-center gap-2 transition-all mt-3 active:scale-[0.99] disabled:opacity-70 disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin text-white" />
                <span>Authenticating Session...</span>
              </>
            ) : (
              <>
                <span>Authenticate & Access Console</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        {/* Demo Quick Access */}
        <div className="pt-3 border-t border-slate-800/80 space-y-2">
          <p className="text-[11px] font-semibold text-slate-400 text-center">Quick Demo Credentials</p>
          <div className="grid grid-cols-2 gap-2">
            <button
              type="button"
              onClick={() => handleQuickFill('AdminAnalyst', 'admin')}
              className="py-1.5 px-3 text-[11px] font-medium bg-slate-800/60 hover:bg-slate-800 text-cyan-300 rounded-lg border border-slate-700/60 transition-all text-center truncate"
            >
              Admin Analyst
            </button>
            <button
              type="button"
              onClick={() => handleQuickFill('SOCAnalyst', 'analyst')}
              className="py-1.5 px-3 text-[11px] font-medium bg-slate-800/60 hover:bg-slate-800 text-cyan-300 rounded-lg border border-slate-700/60 transition-all text-center truncate"
            >
              SOC Analyst
            </button>
          </div>
        </div>

        {/* Footer info */}
        <div className="text-center text-[10px] text-slate-500 font-mono flex items-center justify-center gap-1.5 pt-1">
          <Cpu className="w-3 h-3 text-cyan-500" />
          <span>OAuth2 • JWT Encryption • Zero-Trust Banking Standard</span>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
