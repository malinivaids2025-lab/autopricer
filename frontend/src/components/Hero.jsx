import React from 'react';
import { motion } from 'framer-motion';
import { Sparkles, ShieldCheck, Cpu, TrendingUp, ChevronRight, CheckCircle2 } from 'lucide-react';

export default function Hero({ onGetStarted, onSelectPreset }) {
  const presets = [
    { label: "Toyota Camry 2020", brand: "Toyota", model: "Camry", year: 2020, mileage: 18000, fuel_type: "Petrol", transmission: "Automatic", owner_count: 1, region: "Metro" },
    { label: "BMW 5 Series 2021", brand: "BMW", model: "5", year: 2021, mileage: 32000, fuel_type: "Diesel", transmission: "Automatic", owner_count: 1, region: "Metro" },
    { label: "Honda City 2019", brand: "Honda", model: "City", year: 2019, mileage: 45000, fuel_type: "Petrol", transmission: "Manual", owner_count: 1, region: "Metro" },
  ];

  return (
    <div className="relative overflow-hidden pt-8 pb-16 lg:py-20">
      {/* Dynamic Background Glow Elements */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-gradient-to-tr from-emerald-600/20 via-teal-600/15 to-emerald-800/20 blur-[120px] pointer-events-none -z-10 rounded-full"></div>
      <div className="absolute top-10 left-10 w-72 h-72 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none -z-10"></div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          
          {/* Left Column: Headline & Value Proposition */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="lg:col-span-7 space-y-6 text-center lg:text-left"
          >
            {/* Top Pill */}
            <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-emerald-950/60 border border-emerald-500/30 text-emerald-300 text-xs font-medium backdrop-blur-md">
              <Sparkles className="w-3.5 h-3.5 text-emerald-400 animate-spin" style={{ animationDuration: '4s' }} />
              <span>Full-Stack Machine Learning Automotive Valuation Engine</span>
            </div>

            {/* Main Headline */}
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white leading-tight font-heading">
              Precision Used-Car <br className="hidden sm:block" />
              <span className="bg-gradient-to-r from-emerald-400 via-teal-300 to-emerald-500 bg-clip-text text-transparent">
                Valuation & AI Insights
              </span>
            </h1>

            {/* Tagline */}
            <p className="text-base sm:text-lg text-slate-300 max-w-2xl mx-auto lg:mx-0 leading-relaxed font-normal">
              Accurately price any vehicle with calibrated <strong className="text-white font-semibold">90% confidence intervals</strong>, 
              explainable <strong className="text-emerald-300 font-semibold">SHAP & LIME</strong> contributions, actionable <strong className="text-teal-300 font-semibold">Counterfactual What-If</strong> optimizations, 
              and unsupervised <strong className="text-emerald-300 font-semibold">Isolation Forest</strong> anomaly screening.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4 pt-2">
              <button
                onClick={onGetStarted}
                className="w-full sm:w-auto flex items-center justify-center space-x-2 px-7 py-4 rounded-xl bg-gradient-to-r from-emerald-500 via-emerald-400 to-teal-600 text-slate-950 font-bold text-base hover:shadow-emerald-glow hover:scale-[1.02] active:scale-[0.98] transition-all duration-200"
              >
                <span>Get Instant Valuation</span>
                <ChevronRight className="w-5 h-5" />
              </button>

              <div className="text-xs text-slate-400 flex items-center space-x-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                <span>No registration required</span>
              </div>
            </div>

            {/* Quick Demo Presets */}
            <div className="pt-4 border-t border-white/5 space-y-2">
              <p className="text-xs uppercase tracking-wider font-mono text-slate-400">Quick Demo Scenarios:</p>
              <div className="flex flex-wrap items-center justify-center lg:justify-start gap-2">
                {presets.map((preset, idx) => (
                  <button
                    key={idx}
                    onClick={() => onSelectPreset(preset)}
                    className="px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700/90 border border-white/10 text-xs text-slate-300 hover:text-emerald-300 transition-colors flex items-center space-x-1.5"
                  >
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                    <span>{preset.label}</span>
                  </button>
                ))}
              </div>
            </div>

          </motion.div>

          {/* Right Column: High-Tech Glass Card Preview */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.7, delay: 0.15 }}
            className="lg:col-span-5 relative"
          >
            <div className="glass-panel-glow rounded-2xl p-6 relative overflow-hidden border border-emerald-500/30">
              
              {/* Header */}
              <div className="flex items-center justify-between pb-4 border-b border-white/10">
                <div className="flex items-center space-x-2">
                  <span className="flex h-2.5 w-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
                  <span className="text-xs font-mono text-emerald-300 uppercase font-semibold">Live Market Valuation Node</span>
                </div>
                <span className="text-xs font-mono text-slate-400">Model: XGBoost v3.4</span>
              </div>

              {/* Sample Output Display */}
              <div className="py-6 space-y-4">
                <div>
                  <span className="text-xs text-slate-400 uppercase font-mono tracking-wider">Benchmark Executive Sedan</span>
                  <h3 className="text-2xl font-bold text-white font-heading">2020 Toyota Camry (18,000 km)</h3>
                </div>

                {/* Simulated Price & Interval */}
                <div className="p-4 rounded-xl bg-slate-950/70 border border-emerald-500/20 space-y-2">
                  <div className="flex items-baseline justify-between">
                    <span className="text-xs text-slate-400 font-mono">Predicted Fair Value</span>
                    <span className="text-xs text-emerald-400 font-mono font-semibold">+31.3% Tier Equity</span>
                  </div>
                  <div className="text-3xl font-extrabold text-white tracking-tight font-mono text-emerald-300">
                    ₹19,04,713
                  </div>
                  <div className="space-y-1">
                    <div className="flex justify-between text-[11px] text-slate-400 font-mono">
                      <span>90% Range: ₹13,33,159</span>
                      <span>Upper: ₹24,75,151</span>
                    </div>
                    <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden p-0.5">
                      <div className="h-full bg-gradient-to-r from-emerald-500 via-teal-400 to-emerald-400 rounded-full w-3/4 ml-[12%]"></div>
                    </div>
                  </div>
                </div>

                {/* 3 Metric Badges */}
                <div className="grid grid-cols-3 gap-2 text-center">
                  <div className="p-2.5 rounded-lg bg-slate-800/50 border border-white/5">
                    <div className="text-[10px] text-slate-400 font-mono">SELLING VELOCITY</div>
                    <div className="text-sm font-bold text-white font-mono">42 Days</div>
                  </div>
                  <div className="p-2.5 rounded-lg bg-slate-800/50 border border-white/5">
                    <div className="text-[10px] text-slate-400 font-mono">FRAUD RISK</div>
                    <div className="text-sm font-bold text-emerald-400 font-mono">Low (10.4)</div>
                  </div>
                  <div className="p-2.5 rounded-lg bg-slate-800/50 border border-white/5">
                    <div className="text-[10px] text-slate-400 font-mono">SIMILAR MATCH</div>
                    <div className="text-sm font-bold text-emerald-300 font-mono">99.8%</div>
                  </div>
                </div>

              </div>

              {/* Bottom Feature Tags */}
              <div className="pt-4 border-t border-white/10 flex items-center justify-between text-xs text-slate-400">
                <span className="flex items-center space-x-1"><Cpu className="w-3.5 h-3.5 text-emerald-400" /><span>SHAP Explainers</span></span>
                <span className="flex items-center space-x-1"><TrendingUp className="w-3.5 h-3.5 text-teal-400" /><span>What-If Levers</span></span>
                <span className="flex items-center space-x-1"><ShieldCheck className="w-3.5 h-3.5 text-emerald-400" /><span>Isolation Forest</span></span>
              </div>

            </div>
          </motion.div>

        </div>
      </div>
    </div>
  );
}
