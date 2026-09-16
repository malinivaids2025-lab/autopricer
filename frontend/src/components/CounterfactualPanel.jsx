import React from 'react';
import { Sparkles, TrendingUp, ArrowRight, CheckCircle2, Sliders, DollarSign } from 'lucide-react';

export default function CounterfactualPanel({ counterfactual }) {
  if (!counterfactual) return null;

  const scenarios = counterfactual.all_scenarios || (counterfactual.primary_counterfactual ? [counterfactual.primary_counterfactual] : []);

  if (scenarios.length === 0) return null;

  return (
    <div className="glass-panel rounded-2xl p-6 border border-white/10 space-y-5">
      
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-white/10">
        <div className="flex items-center space-x-2.5">
          <div className="p-2 rounded-xl bg-teal-500/10 border border-teal-500/30">
            <Sliders className="w-5 h-5 text-teal-400" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white font-heading">
              Counterfactual "What-If" Value Levers
            </h3>
            <p className="text-xs text-slate-400">
              Actionable feature modifications and simulated valuation impact.
            </p>
          </div>
        </div>
        <span className="text-xs font-mono font-semibold px-2.5 py-1 rounded bg-teal-500/10 border border-teal-500/30 text-teal-300">
          {scenarios.length} Scenarios Available
        </span>
      </div>

      {/* Scenarios Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {scenarios.map((s, idx) => {
          const isPositive = s.price_delta >= 0;
          return (
            <div 
              key={idx}
              className="p-4 rounded-xl glass-card border border-white/10 hover:border-teal-500/40 space-y-3 relative group"
            >
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-mono uppercase font-semibold text-teal-400 tracking-wider">
                  {s.type}
                </span>
                <span className={`text-xs font-mono font-bold px-2 py-0.5 rounded-full ${
                  isPositive ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30' : 'bg-slate-800 text-slate-300'
                }`}>
                  {isPositive ? '+' : ''}₹{Math.round(Math.abs(s.price_delta)).toLocaleString('en-IN')}
                </span>
              </div>

              {/* Value Transition Visual */}
              {s.current_value && s.target_value && (
                <div className="flex items-center space-x-2 text-xs font-mono py-1 px-2.5 rounded-lg bg-slate-950/60 border border-white/5">
                  <span className="text-slate-400">{s.current_value}</span>
                  <ArrowRight className="w-3.5 h-3.5 text-teal-400" />
                  <span className="text-white font-bold text-teal-300">{s.target_value}</span>
                  <span className="ml-auto text-slate-400 font-normal">➔ ₹{Math.round(s.new_price)?.toLocaleString('en-IN')}</span>
                </div>
              )}

              {/* Plain Statement */}
              <p className="text-xs text-slate-300 leading-relaxed">
                {s.statement}
              </p>
            </div>
          );
        })}
      </div>

    </div>
  );
}
