import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/common/Sidebar';
import Header from './components/common/Header';
import DashboardPage from './pages/DashboardPage';
import StaticAnalysisPage from './pages/StaticAnalysisPage';
import RealtimeMonitorPage from './pages/RealtimeMonitorPage';
import ModelPerformancePage from './pages/ModelPerformancePage';
import LoginPage from './pages/LoginPage';
import AuditLogsPage from './pages/AuditLogsPage';
import SecurityPolicyPage from './pages/SecurityPolicyPage';
import { ThemeProvider } from './context/ThemeContext';
import { AuthProvider, useAuth } from './context/AuthContext';

const Layout = ({ children }) => {
  return (
    <div className="flex min-h-screen bg-slate-950 text-slate-100 font-sans">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Header />
        <main className="flex-1 p-6 overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
};

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  return <Layout>{children}</Layout>;
};

function App() {
  return (
    <AuthProvider>
      <ThemeProvider>
        <Router>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
            <Route path="/static-analysis" element={<ProtectedRoute><StaticAnalysisPage /></ProtectedRoute>} />
            <Route path="/realtime-monitor" element={<ProtectedRoute><RealtimeMonitorPage /></ProtectedRoute>} />
            <Route path="/model-performance" element={<ProtectedRoute><ModelPerformancePage /></ProtectedRoute>} />
            <Route path="/audit-logs" element={<ProtectedRoute><AuditLogsPage /></ProtectedRoute>} />
            <Route path="/settings" element={<ProtectedRoute><SecurityPolicyPage /></ProtectedRoute>} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Router>
      </ThemeProvider>
    </AuthProvider>
  );
}

export default App;
