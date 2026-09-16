import React from 'react';
import {
  Cpu, ShieldCheck, BrainCircuit, Activity, Database, Sliders, GitCompare
} from 'lucide-react';

export default function MethodologyView() {
  return (
    <div className="max-w-5xl mx-auto space-y-10 pb-12">

      {/* Header */}
      <div className="text-center space-y-4 max-w-3xl mx-auto">
        <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-emerald-950/60 border border-emerald-500/30 text-emerald-300 text-xs font-mono">
          <BrainCircuit className="w-3.5 h-3.5 text-emerald-400" />
          <span>Machine Learning Whitepaper & System Architecture</span>
        </div>
        <h2 className="text-3xl sm:text-4xl font-extrabold text-white font-heading tracking-tight">
          Algorithmic Methodology & Explainable AI
        </h2>
        <p className="text-sm sm:text-base text-slate-400 leading-relaxed">
          AutoPricer AI utilizes an ensemble of gradient-boosted tree regressors, conformal prediction intervals, game-theoretic Shapley value attribution, and unsupervised isolation manifolds.
        </p>
      </div>

      {/* 6 Architectural Pillars Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        {/* Pillar 1: Price Regressor */}
        <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-3">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
              <Cpu className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white font-heading">1. Vehicle Price Regressor & Quantiles</h3>
              <span className="text-[11px] font-mono text-emerald-300">XGBoost (R² = 0.9260, MAE = ₹1,13,379)</span>
            </div>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            Trained and benchmarked across Random Forest and XGBoost regressors on 15,411 verified used vehicle transactions.
            XGBoost selected as the champion model. Dual 5th and 95th percentile conformal log-residual distributions calibrate exact 90% confidence prediction intervals.
          </p>
        </div>

        {/* Pillar 2: Selling Time Prediction */}
        <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-3">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 rounded-xl bg-teal-500/10 border border-teal-500/30 text-teal-400">
              <Activity className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white font-heading">2. Selling-Time Velocity Regressor</h3>
              <span className="text-[11px] font-mono text-teal-300">Gradient Boosted Days-on-Market Model</span>
            </div>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            Estimates expected listing turnover duration based on vehicle vintage, odometer wear, brand liquidity elasticity, and pricing deviation relative to segment medians.
          </p>
        </div>

        {/* Pillar 3: Explainable AI */}
        <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-3">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
              <BrainCircuit className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white font-heading">3. Explainable AI: SHAP & LIME</h3>
              <span className="text-[11px] font-mono text-emerald-300">TreeExplainer + Local Surrogates</span>
            </div>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            SHAP (SHapley Additive exPlanations) TreeExplainer attributes exact additive Rupee premiums and discounts to each vehicle attribute, while LIME provides local linear surrogate weights.
          </p>
        </div>

        {/* Pillar 4: Counterfactuals */}
        <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-3">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 rounded-xl bg-teal-500/10 border border-teal-500/30 text-teal-400">
              <Sliders className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white font-heading">4. Counterfactual "What-If" Levers</h3>
              <span className="text-[11px] font-mono text-teal-300">Actionable Value Optimization Engine</span>
            </div>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            Simulates perturbing actionable vehicle features (mileage reduction, model year vintage, regional demand arbitrage, single-ownership certification) to project optimal equity returns.
          </p>
        </div>

        {/* Pillar 5: Recommendations */}
        <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-3">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
              <GitCompare className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white font-heading">5. Recommendation Engine (5 Nearest Neighbors)</h3>
              <span className="text-[11px] font-mono text-emerald-300">K-NN Normalized Cosine Space</span>
            </div>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            Queries a standardized multidimensional feature matrix across the 15,411 vehicle inventory using cosine similarity metric to retrieve the top 5 most comparable active comps.
          </p>
        </div>

        {/* Pillar 6: Fraud & Anomaly Detection */}
        <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-3">
          <div className="flex items-center space-x-3">
            <div className="p-2.5 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white font-heading">6. Isolation Forest Anomaly Detection</h3>
              <span className="text-[11px] font-mono text-rose-300">Continuous Model Decision Function</span>
            </div>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            Unsupervised Isolation Forest evaluates multidimensional feature-to-price residuals. A calibrated logistic risk transfer function maps raw isolation paths to a continuous 0–100 Fraud Risk Score.
          </p>
        </div>

      </div>

      {/* Benchmark Metrics Comparison Table */}
      <div className="glass-panel p-6 sm:p-8 rounded-3xl border border-white/10 space-y-5">
        <h3 className="text-lg font-bold text-white font-heading flex items-center gap-2">
          <Database className="w-5 h-5 text-emerald-400" /> Empirical Regression Benchmark
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-xs font-mono text-left">
            <thead className="border-b border-white/10 text-slate-400 uppercase tracking-wider">
              <tr>
                <th className="py-3 px-4">Model Architecture</th>
                <th className="py-3 px-4">Objective Loss</th>
                <th className="py-3 px-4">Test R²</th>
                <th className="py-3 px-4">Test RMSE</th>
                <th className="py-3 px-4">Test MAE</th>
                <th className="py-3 px-4">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5 text-slate-200">
              <tr className="bg-emerald-500/10 text-emerald-300 font-bold">
                <td className="py-3.5 px-4 font-semibold">XGBoost Regressor (Selected)</td>
                <td className="py-3.5 px-4">Squared Error</td>
                <td className="py-3.5 px-4 text-emerald-400">0.9260</td>
                <td className="py-3.5 px-4">₹2,33,892.60</td>
                <td className="py-3.5 px-4">₹1,13,379.36</td>
                <td className="py-3.5 px-4"><span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 text-[10px]">PRODUCTION</span></td>
              </tr>
              <tr>
                <td className="py-3.5 px-4">Random Forest Regressor</td>
                <td className="py-3.5 px-4">MSE</td>
                <td className="py-3.5 px-4">0.9111</td>
                <td className="py-3.5 px-4">₹2,56,337.80</td>
                <td className="py-3.5 px-4">₹1,20,508.20</td>
                <td className="py-3.5 px-4"><span className="px-2 py-0.5 rounded bg-slate-800 text-slate-400 text-[10px]">BENCHMARK</span></td>
              </tr>
              <tr>
                <td className="py-3.5 px-4">Conformal Log Residuals (90%)</td>
                <td className="py-3.5 px-4">Quantile (q0.05 / q0.95)</td>
                <td className="py-3.5 px-4">89.94% Cov</td>
                <td className="py-3.5 px-4">—</td>
                <td className="py-3.5 px-4">—</td>
                <td className="py-3.5 px-4"><span className="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 text-[10px]">CALIBRATED</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}
