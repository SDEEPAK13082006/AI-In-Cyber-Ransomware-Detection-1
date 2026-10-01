import React from 'react';
import { 
  ResponsiveContainer, 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  Tooltip, 
  CartesianGrid 
} from 'recharts';

const AttackTimelineChart = ({ data }) => {
  const chartData = data || [
    { time: '08:00', benign: 120, ransomware: 0 },
    { time: '10:00', benign: 340, ransomware: 1 },
    { time: '12:00', benign: 510, ransomware: 0 },
    { time: '14:00', benign: 620, ransomware: 4 },
    { time: '16:00', benign: 450, ransomware: 2 },
    { time: '18:00', benign: 780, ransomware: 0 },
    { time: '20:00', benign: 890, ransomware: 5 },
  ];

  return (
    <div className="w-full h-64">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <defs>
            <linearGradient id="colorBenign" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#0284c7" stopOpacity={0.4}/>
              <stop offset="95%" stopColor="#0284c7" stopOpacity={0}/>
            </linearGradient>
            <linearGradient id="colorRansomware" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8}/>
              <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.5} />
          <XAxis dataKey="time" stroke="#94a3b8" fontSize={11} tickLine={false} />
          <YAxis stroke="#94a3b8" fontSize={11} tickLine={false} />
          <Tooltip 
            contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }}
            itemStyle={{ color: '#e2e8f0' }}
          />
          <Area type="monotone" dataKey="benign" name="Benign Scans" stroke="#0284c7" fillOpacity={1} fill="url(#colorBenign)" strokeWidth={2} />
          <Area type="monotone" dataKey="ransomware" name="Ransomware Attempts" stroke="#ef4444" fillOpacity={1} fill="url(#colorRansomware)" strokeWidth={2} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

export default AttackTimelineChart;
