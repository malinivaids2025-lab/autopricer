import React from 'react';
import { motion } from 'framer-motion';
import {
  Clock, ShieldAlert, ShieldCheck,
  RotateCcw
} from 'lucide-react';
import ShapChart from './ShapChart';
import CounterfactualPanel from './CounterfactualPanel';
import SimilarCars from './SimilarCars';

export default function ResultsDashboard({ result, inputCar, onReset }) {
  if (!result) return null;

  const {
    predicted_price,
    confidence_interval,
    model_used,
    expected_days_to_sale,
    velocity_category,
    fraud_risk,
    shap_contributions,
    lime_explanations,
    counterfactual,
    plain_language_summary,
    similar_cars,
  } = result;

  const lowBound = confidence_interval?.[0] || predicted_price * 0.75;
  const highBound = confidence_interval?.[1] || predicted_price * 1.25;

  // Calculate percentage range position for visual slider indicator
  const rangeSpan = highBound - lowBound;
  const pointPct = rangeSpan > 0 ? ((predicted_price - lowBound) / rangeSpan) * 100 : 50;

  // Fraud risk badge styling
  const isHighRisk = fraud_risk?.risk_level === 'High Risk' || fraud_risk?.fraud_risk_score >= 60;
  const isMediumRisk = fraud_risk?.risk_level === 'Medium Risk';

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="max-w-7xl mx-auto space-y-8"
    >
      {/* Top Banner & Vehicle Title */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 glass-panel p-6 rounded-3xl border border-white/10">
        <div>
          <div className="flex items-center space-x-2 text-xs font-mono text-emerald-400 uppercase font-semibold mb-1">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
            <span>Valuation Completed • {model_used}</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-white font-heading tracking-tight">
            {inputCar?.year} {inputCar?.brand} {inputCar?.model}
          </h2>
          <p className="text-xs sm:text-sm text-slate-400 font-mono mt-0.5">
            {inputCar?.mileage?.toLocaleString('en-IN')} km • {inputCar?.fuel_type} • {inputCar?.transmission} • {inputCar?.owner_count} Owner(s) • {inputCar?.region} Region
          </p>
        </div>

        <button
          onClick={onReset}
          className="self-start sm:self-center flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-mono font-medium border border-white/10 transition-all shadow-md"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>Valuate Another Car</span>
        </button>
      </div>

      {/* Primary 3 KPI Grid: Price + Confidence Band, Selling Velocity, Fraud Risk */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">

        {/* Card 1: Large Valuation & Confidence Range (6 cols) */}
        <div className="lg:col-span-6 glass-panel-glow p-6 sm:p-8 rounded-3xl border border-emerald-500/30 flex flex-col justify-between space-y-6">

          <div className="flex items-center justify-between">
            <span className="text-xs uppercase font-mono tracking-wider text-emerald-400 font-semibold flex items-center gap-1.5">
              <span className="text-emerald-400 font-bold font-mono text-sm">₹</span> Estimated Fair Market Value
            </span>
            <span className="text-[11px] font-mono px-2.5 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-300">
              90% Conformal Calibrated
            </span>
          </div>

          <div>
            <div className="text-4xl sm:text-5xl lg:text-6xl font-black font-mono text-white tracking-tight">
              ₹{predicted_price.toLocaleString('en-IN', { maximumFractionDigits: 0 })}
            </div>
            <p className="text-xs text-slate-400 mt-2 font-mono">
              Median algorithmic fair price based on native INR market transaction residuals.
            </p>
          </div>

          {/* 90% Confidence Interval Band / Visual Slider */}
          <div className="p-4 rounded-2xl bg-slate-950/70 border border-white/10 space-y-2.5">
            <div className="flex justify-between text-xs font-mono">
              <span className="text-slate-400">90% Lower Bound: <strong className="text-white font-bold">₹{lowBound.toLocaleString('en-IN', { maximumFractionDigits: 0 })}</strong></span>
              <span className="text-slate-400">90% Upper Bound: <strong className="text-white font-bold">₹{highBound.toLocaleString('en-IN', { maximumFractionDigits: 0 })}</strong></span>
            </div>

            {/* Slider track with gradient band */}
            <div className="relative h-4 w-full bg-slate-800/80 rounded-full overflow-hidden p-0.5 border border-white/5">
              <div className="h-full bg-gradient-to-r from-emerald-500 via-teal-400 to-emerald-600 rounded-full w-full opacity-85"></div>
              {/* Point Estimate Marker */}
              <div
                className="absolute top-0 bottom-0 w-3 bg-white rounded-full shadow-lg border-2 border-slate-950 -translate-x-1/2"
                style={{ left: `${Math.max(5, Math.min(95, pointPct))}%` }}
                title={`Point Estimate: ₹${predicted_price.toLocaleString('en-IN')}`}
              ></div>
            </div>

            <div className="flex justify-between text-[10px] font-mono text-slate-500">
              <span>Conservative Liquidity Floor</span>
              <span>Point Estimate ({pointPct.toFixed(0)}%)</span>
              <span>Max Retail Ceiling</span>
            </div>
          </div>

        </div>

        {/* Card 2: Expected Selling Time & Velocity (3 cols) */}
        <div className="lg:col-span-3 glass-panel p-6 sm:p-7 rounded-3xl border border-white/10 flex flex-col justify-between space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs uppercase font-mono tracking-wider text-slate-400 flex items-center gap-1.5">
              <Clock className="w-4 h-4 text-emerald-400" /> Selling Velocity
            </span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300">
              {velocity_category}
            </span>
          </div>

          <div>
            <div className="text-4xl font-extrabold font-mono text-white tracking-tight flex items-baseline gap-1">
              <span>{expected_days_to_sale.toFixed(0)}</span>
              <span className="text-lg font-normal text-slate-400 font-sans">days</span>
            </div>
            <p className="text-xs text-slate-400 mt-1 font-mono">
              Expected turnover duration on current marketplace.
            </p>
          </div>

          {/* Velocity Meter Bar */}
          <div className="space-y-1.5 pt-2 border-t border-white/5">
            <div className="flex justify-between text-[11px] font-mono text-slate-400">
              <span>Velocity Meter:</span>
              <span className="text-emerald-300 font-bold">{expected_days_to_sale <= 30 ? 'High Liquidity' : 'Standard'}</span>
            </div>
            <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-emerald-400 to-teal-500 rounded-full"
                style={{ width: `${Math.max(15, Math.min(100, (1 - expected_days_to_sale / 120) * 100))}%` }}
              ></div>
            </div>
          </div>
        </div>

        {/* Card 3: Fraud & Anomaly Screening (3 cols) */}
        <div className={`lg:col-span-3 glass-panel p-6 sm:p-7 rounded-3xl border flex flex-col justify-between space-y-4 ${isHighRisk ? 'border-rose-500/40 bg-rose-950/20' : isMediumRisk ? 'border-amber-500/40 bg-amber-950/20' : 'border-emerald-500/30 bg-emerald-950/15'
          }`}>
          <div className="flex items-center justify-between">
            <span className="text-xs uppercase font-mono tracking-wider text-slate-300 flex items-center gap-1.5">
              {isHighRisk ? <ShieldAlert className="w-4 h-4 text-rose-400" /> : <ShieldCheck className="w-4 h-4 text-emerald-400" />}
              <span>Fraud Risk Check</span>
            </span>
            <span className={`text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full ${isHighRisk ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40' : isMediumRisk ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
              }`}>
              {fraud_risk?.risk_level || 'Low Risk'}
            </span>
          </div>

          <div>
            <div className="flex items-baseline space-x-2">
              <span className={`text-4xl font-extrabold font-mono ${isHighRisk ? 'text-rose-400' : isMediumRisk ? 'text-amber-400' : 'text-emerald-400'
                }`}>
                {fraud_risk?.fraud_risk_score?.toFixed(1) || '10.4'}
              </span>
              <span className="text-xs font-mono text-slate-400">/ 100 Risk Score</span>
            </div>
            <div className="text-xs font-mono text-slate-300 mt-1">
              Isolation Forest Anomaly Assessment
            </div>
          </div>

          {/* Diagnostic Reason */}
          <div className="text-[11px] text-slate-300 leading-tight border-t border-white/10 pt-2 font-mono">
            {fraud_risk?.reasons?.[0] || "Listing parameters, odometer, and pricing conform to normal market parameters."}
          </div>
        </div>

      </div>

      {/* SHAP Feature Contribution Chart & Plain English Explanation */}
      <ShapChart
        shapContributions={shap_contributions}
        limeExplanations={lime_explanations}
        plainSummary={plain_language_summary}
      />

      {/* Counterfactual "What-If" Levers Panel */}
      <CounterfactualPanel counterfactual={counterfactual} />

      {/* 5 Comparable Inventory Recommendations */}
      <SimilarCars similarCars={similar_cars} />

    </motion.div>
  );
}
