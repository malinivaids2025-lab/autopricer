import React from 'react';
import { 
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, 
  Tooltip, Cell, ReferenceLine 
} from 'recharts';
import { Cpu, CheckCircle2, BookOpen } from 'lucide-react';

export default function ShapChart({ shapContributions, limeExplanations, plainSummary }) {
  if (!shapContributions || shapContributions.length === 0) return null;

  // Format data for Recharts horizontal bar chart
  const data = shapContributions.map(item => ({
    name: item.feature,
    impact: item.impact,
    absImpact: Math.abs(item.impact),
    direction: item.impact_direction,
    percentage: item.percentage_contribution,
  }));

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const d = payload[0].payload;
      return (
        <div className="glass-panel p-3 rounded-xl border border-emerald-500/30 text-xs shadow-2xl">
          <div className="font-bold text-white mb-1 font-heading">{d.name}</div>
          <div className="font-mono flex items-center space-x-2">
            <span className="text-slate-400">Impact:</span>
            <span className={`font-bold ${d.impact >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
              {d.impact >= 0 ? '+' : ''}₹{Math.round(d.impact).toLocaleString('en-IN')}
            </span>
          </div>
          <div className="text-[10px] text-slate-400 mt-1 font-mono">
            {d.percentage}% of overall price variance
          </div>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="glass-panel rounded-2xl p-6 border border-white/10 space-y-6">
      
      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-white/10">
        <div className="flex items-center space-x-2.5">
          <div className="p-2 rounded-xl bg-emerald-500/10 border border-emerald-500/30">
            <Cpu className="w-5 h-5 text-emerald-400" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white font-heading">
              Explainable AI: SHAP Feature Contributions
            </h3>
            <p className="text-xs text-slate-400">
              Exact additive price impact in Indian Rupees evaluated via TreeExplainer game-theoretic Shapley values.
            </p>
          </div>
        </div>
        <div className="hidden sm:flex items-center space-x-4 text-xs font-mono">
          <span className="flex items-center gap-1 text-emerald-400"><span className="w-2.5 h-2.5 rounded bg-emerald-500"></span> Value Premium (+)</span>
          <span className="flex items-center gap-1 text-rose-400"><span className="w-2.5 h-2.5 rounded bg-rose-500"></span> Depreciation (-)</span>
        </div>
      </div>

      {/* Horizontal Bar Chart */}
      <div className="h-64 w-full pt-2">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            layout="vertical"
            margin={{ top: 5, right: 20, left: 40, bottom: 5 }}
          >
            <XAxis 
              type="number" 
              tickFormatter={(v) => Math.abs(v) >= 100000 ? '₹' + (v / 100000).toFixed(1) + 'L' : '₹' + (v / 1000).toFixed(0) + 'k'}
              stroke="#64748b"
              fontSize={11}
              fontFamily="monospace"
            />
            <YAxis 
              type="category" 
              dataKey="name" 
              stroke="#94a3b8" 
              fontSize={11}
              width={140}
              tickLine={false}
            />
            <Tooltip content={<CustomTooltip />} />
            <ReferenceLine x={0} stroke="#475569" strokeDasharray="3 3" />
            <Bar dataKey="impact" radius={[4, 4, 4, 4]}>
              {data.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`} 
                  fill={entry.impact >= 0 ? '#10b981' : '#f43f5e'} 
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Plain Language Summary */}
      {plainSummary && (
        <div className="p-4 rounded-xl bg-slate-950/60 border border-white/5 space-y-1.5">
          <span className="text-[10px] uppercase font-mono tracking-wider text-emerald-400 font-semibold flex items-center gap-1">
            <CheckCircle2 className="w-3.5 h-3.5" /> Plain-Language Synthesis
          </span>
          <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
            {plainSummary}
          </p>
        </div>
      )}

      {/* LIME Rules Breakdown */}
      {limeExplanations && limeExplanations.length > 0 && (
        <div className="pt-2">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-mono uppercase text-slate-400 flex items-center gap-1">
              <BookOpen className="w-3.5 h-3.5 text-teal-400" /> Local LIME Surrogate Attribution
            </span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {limeExplanations.map((item, idx) => (
              <div key={idx} className="p-2.5 rounded-lg bg-slate-900/50 border border-white/5 flex items-start justify-between text-xs">
                <div>
                  <div className="font-mono text-slate-200 font-medium">{item.rule}</div>
                  <div className="text-[11px] text-slate-400">{item.description}</div>
                </div>
                <span className={`text-xs font-mono font-bold px-2 py-0.5 rounded ${
                  item.weight >= 0 ? 'bg-emerald-500/10 text-emerald-400' : 'bg-rose-500/10 text-rose-400'
                }`}>
                  {item.weight >= 0 ? '+' : ''}{(item.weight * 100).toFixed(0)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

    </div>
  );
}
