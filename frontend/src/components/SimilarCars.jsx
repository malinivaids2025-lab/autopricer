import React from 'react';
import { Car } from 'lucide-react';

export default function SimilarCars({ similarCars }) {
  if (!similarCars || similarCars.length === 0) return null;

  return (
    <div className="glass-panel rounded-2xl p-6 border border-white/10 space-y-5">

      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-white/10">
        <div className="flex items-center space-x-2.5">
          <div className="p-2 rounded-xl bg-emerald-500/10 border border-emerald-500/30">
            <Car className="w-5 h-5 text-emerald-400" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white font-heading">
              Comparable Inventory Recommendations (5 Nearest Neighbors)
            </h3>
            <p className="text-xs text-slate-400">
              Matched via K-Nearest Neighbors Cosine Vector Space across 15,400+ listings.
            </p>
          </div>
        </div>
        <span className="text-xs font-mono font-semibold px-2.5 py-1 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-300">
          5 Verified Comps
        </span>
      </div>

      {/* Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3.5">
        {similarCars.map((car, idx) => (
          <div
            key={idx}
            className="p-4 rounded-xl glass-card border border-white/10 hover:border-emerald-500/40 flex flex-col justify-between space-y-3 relative group"
          >
            {/* Top Match Badge */}
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-emerald-500/20 border border-emerald-500/40 text-emerald-300">
                {car.similarity_score}% Match
              </span>
              <span className="text-[11px] font-mono text-slate-400">{car.year}</span>
            </div>

            {/* Vehicle Title & Price */}
            <div>
              <h4 className="text-sm font-bold text-white font-heading truncate">
                {car.brand} {car.model}
              </h4>
              <div className="text-lg font-extrabold text-emerald-400 font-mono mt-1">
                ₹{car.price.toLocaleString('en-IN', { maximumFractionDigits: 0 })}
              </div>
            </div>

            {/* Specs Tags */}
            <div className="space-y-1 text-[11px] font-mono text-slate-300 border-t border-white/5 pt-2">
              <div className="flex items-center justify-between">
                <span className="text-slate-500">Odometer:</span>
                <span>{car.mileage.toLocaleString('en-IN')} km</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-slate-500">Powertrain:</span>
                <span>{car.fuel_type} • {car.transmission.slice(0, 4)}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-slate-500">Region:</span>
                <span className="text-slate-300">{car.region}</span>
              </div>
            </div>

          </div>
        ))}
      </div>

    </div>
  );
}
