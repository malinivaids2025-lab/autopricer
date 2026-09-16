import React from 'react';
import { 
  ResponsiveContainer, BarChart, Bar, LineChart, Line, AreaChart, Area, 
  XAxis, YAxis, Tooltip, CartesianGrid, Legend, Cell 
} from 'recharts';
import { BarChart3, TrendingUp, Clock, Layers, Fuel, Cog, MapPin } from 'lucide-react';

export default function MarketAnalyticsView({ analyticsData, isLoading }) {
  if (isLoading || !analyticsData) {
    return (
      <div className="max-w-7xl mx-auto space-y-6 animate-pulse">
        <div className="h-32 glass-panel rounded-3xl animate-shimmer"></div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="h-72 glass-panel rounded-3xl animate-shimmer"></div>
          <div className="h-72 glass-panel rounded-3xl animate-shimmer"></div>
        </div>
      </div>
    );
  }

  const {
    total_listings,
    average_price,
    median_price,
    average_days_to_sale,
    brand_summary = [],
    region_summary = [],
    year_trend = [],
    fuel_breakdown = [],
    transmission_breakdown = [],
    supply_demand_trend = [],
  } = analyticsData;

  const topBrands = brand_summary.slice(0, 8);

  const CurrencyTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="glass-panel p-3 rounded-xl border border-emerald-500/30 text-xs shadow-2xl">
          <div className="font-bold text-white mb-1 font-heading">{label}</div>
          {payload.map((item, idx) => (
            <div key={idx} className="font-mono flex items-center space-x-2 text-slate-300">
              <span className="w-2 h-2 rounded-full" style={{ backgroundColor: item.color || item.fill }}></span>
              <span>{item.name}:</span>
              <span className="font-bold text-white">
                {typeof item.value === 'number' && item.name.toLowerCase().includes('price') 
                  ? `₹${Math.round(item.value).toLocaleString('en-IN')}` 
                  : item.value}
              </span>
            </div>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 glass-panel p-6 rounded-3xl border border-white/10">
        <div>
          <div className="flex items-center space-x-2 text-xs font-mono text-emerald-400 uppercase font-semibold mb-1">
            <BarChart3 className="w-3.5 h-3.5" />
            <span>Market Intelligence Dashboard</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-white font-heading tracking-tight">
            Used-Car Market Dynamics & Aggregations
          </h2>
          <p className="text-xs sm:text-sm text-slate-400">
            Real-time analytics synthesized across {total_listings.toLocaleString()} vehicle listings.
          </p>
        </div>
      </div>

      {/* 4 Summary Metric Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        
        <div className="glass-panel p-5 rounded-2xl border border-white/10">
          <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">Total Market Dataset</span>
          <div className="text-2xl sm:text-3xl font-bold font-mono text-white mt-1">
            {total_listings.toLocaleString()}
          </div>
          <span className="text-[11px] text-emerald-400 font-mono">Cleaned & IQR Capped</span>
        </div>

        <div className="glass-panel p-5 rounded-2xl border border-white/10">
          <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">Mean Market Price</span>
          <div className="text-2xl sm:text-3xl font-bold font-mono text-emerald-300 mt-1">
            ₹{average_price.toLocaleString('en-IN', { maximumFractionDigits: 0 })}
          </div>
          <span className="text-[11px] text-slate-400 font-mono">Median: ₹{median_price.toLocaleString('en-IN', { maximumFractionDigits: 0 })}</span>
        </div>

        <div className="glass-panel p-5 rounded-2xl border border-white/10">
          <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">Average Selling Time</span>
          <div className="text-2xl sm:text-3xl font-bold font-mono text-teal-300 mt-1">
            {average_days_to_sale.toFixed(1)} <span className="text-sm font-sans text-slate-400">days</span>
          </div>
          <span className="text-[11px] text-slate-400 font-mono">Turnover Velocity</span>
        </div>

        <div className="glass-panel p-5 rounded-2xl border border-white/10">
          <span className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">Top Brand Share</span>
          <div className="text-2xl sm:text-3xl font-bold font-mono text-emerald-400 mt-1">
            {topBrands[0]?.brand || "Maruti Suzuki"}
          </div>
          <span className="text-[11px] text-slate-400 font-mono">{topBrands[0]?.count?.toLocaleString()} Active Listings</span>
        </div>

      </div>

      {/* Charts Grid 1: Price by Region & Top Brands Price Comparison */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Chart 1: Price Trends by Region */}
        <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-white/10">
            <h3 className="text-base font-bold text-white font-heading flex items-center gap-2">
              <MapPin className="w-4 h-4 text-emerald-400" /> Regional Price Comparison (₹ INR)
            </h3>
            <span className="text-xs font-mono text-slate-400">By Geographic Zone</span>
          </div>
          <div className="h-72 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={region_summary} margin={{ top: 10, right: 10, left: 10, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="region" stroke="#94a3b8" fontSize={11} fontFamily="monospace" />
                <YAxis stroke="#64748b" fontSize={11} fontFamily="monospace" tickFormatter={(v) => v >= 100000 ? `₹${(v/100000).toFixed(1)}L` : `₹${(v/1000).toFixed(0)}k`} />
                <Tooltip content={<CurrencyTooltip />} />
                <Bar dataKey="avg_price" name="Avg Price" fill="#10b981" radius={[6, 6, 0, 0]}>
                  {region_summary.map((_, index) => (
                    <Cell key={`cell-r-${index}`} fill={index % 2 === 0 ? '#10b981' : '#059669'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 2: Top Brands Valuations (Avg vs Median) */}
        <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-white/10">
            <h3 className="text-base font-bold text-white font-heading flex items-center gap-2">
              <Layers className="w-4 h-4 text-emerald-400" /> Brand Valuation Breakdown
            </h3>
            <span className="text-xs font-mono text-slate-400">Average vs Median</span>
          </div>
          <div className="h-72 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={topBrands} margin={{ top: 10, right: 10, left: 10, bottom: 35 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="brand" stroke="#94a3b8" fontSize={10} angle={-25} textAnchor="end" />
                <YAxis stroke="#64748b" fontSize={11} fontFamily="monospace" tickFormatter={(v) => v >= 100000 ? `₹${(v/100000).toFixed(1)}L` : `₹${(v/1000).toFixed(0)}k`} />
                <Tooltip content={<CurrencyTooltip />} />
                <Legend wrapperStyle={{ fontSize: '11px', fontFamily: 'monospace' }} />
                <Bar dataKey="avg_price" name="Avg Price" fill="#10b981" radius={[4, 4, 0, 0]} />
                <Bar dataKey="median_price" name="Median Price" fill="#34d399" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>

      {/* Charts Grid 2: Depreciation Curve & Monthly Supply/Demand */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Chart 3: Depreciation Curve by Model Year */}
        <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-white/10">
            <h3 className="text-base font-bold text-white font-heading flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-emerald-400" /> Price Depreciation by Year
            </h3>
            <span className="text-xs font-mono text-slate-400">Market Retention Curve</span>
          </div>
          <div className="h-72 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={year_trend} margin={{ top: 10, right: 10, left: 10, bottom: 20 }}>
                <defs>
                  <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="year" stroke="#94a3b8" fontSize={11} fontFamily="monospace" />
                <YAxis stroke="#64748b" fontSize={11} fontFamily="monospace" tickFormatter={(v) => v >= 100000 ? `₹${(v/100000).toFixed(1)}L` : `₹${(v/1000).toFixed(0)}k`} />
                <Tooltip content={<CurrencyTooltip />} />
                <Area type="monotone" dataKey="avg_price" name="Avg Price" stroke="#10b981" fillOpacity={1} fill="url(#colorPrice)" strokeWidth={2.5} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 4: Monthly Supply vs Demand Velocity Index */}
        <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-white/10">
            <h3 className="text-base font-bold text-white font-heading flex items-center gap-2">
              <Clock className="w-4 h-4 text-emerald-400" /> Monthly Listing Volume & Demand Index
            </h3>
            <span className="text-xs font-mono text-slate-400">Temporal Dynamics</span>
          </div>
          <div className="h-72 w-full pt-2">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={supply_demand_trend} margin={{ top: 10, right: 10, left: 10, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="month" stroke="#94a3b8" fontSize={11} fontFamily="monospace" />
                <YAxis yAxisId="left" stroke="#10b981" fontSize={11} fontFamily="monospace" />
                <YAxis yAxisId="right" orientation="right" stroke="#34d399" fontSize={11} fontFamily="monospace" />
                <Tooltip content={<CurrencyTooltip />} />
                <Legend wrapperStyle={{ fontSize: '11px', fontFamily: 'monospace' }} />
                <Line yAxisId="left" type="monotone" dataKey="listing_volume" name="Listing Volume" stroke="#10b981" strokeWidth={2} dot={{ r: 3 }} />
                <Line yAxisId="right" type="monotone" dataKey="demand_index" name="Demand Velocity Index" stroke="#34d399" strokeWidth={2.5} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>

      {/* Fuel Type & Transmission Breakdown Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Fuel Types */}
        <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-3">
          <h4 className="text-sm font-bold text-white font-heading flex items-center gap-2">
            <Fuel className="w-4 h-4 text-emerald-400" /> Fuel Type Segmentation
          </h4>
          <div className="space-y-2">
            {fuel_breakdown.map((f, i) => (
              <div key={i} className="flex items-center justify-between p-2.5 rounded-xl bg-slate-900/60 border border-white/5 text-xs font-mono">
                <span className="text-slate-200 font-medium">{f.fuel_type}</span>
                <span className="text-slate-400">{f.count?.toLocaleString()} cars</span>
                <span className="text-emerald-400 font-bold">₹{f.avg_price?.toLocaleString('en-IN', { maximumFractionDigits: 0 })} avg</span>
              </div>
            ))}
          </div>
        </div>

        {/* Transmission Types */}
        <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-3">
          <h4 className="text-sm font-bold text-white font-heading flex items-center gap-2">
            <Cog className="w-4 h-4 text-emerald-400" /> Transmission Segmentation
          </h4>
          <div className="space-y-2">
            {transmission_breakdown.map((t, i) => (
              <div key={i} className="flex items-center justify-between p-2.5 rounded-xl bg-slate-900/60 border border-white/5 text-xs font-mono">
                <span className="text-slate-200 font-medium">{t.transmission}</span>
                <span className="text-slate-400">{t.count?.toLocaleString()} cars</span>
                <span className="text-emerald-300 font-bold">₹{t.avg_price?.toLocaleString('en-IN', { maximumFractionDigits: 0 })} avg</span>
              </div>
            ))}
          </div>
        </div>

      </div>

    </div>
  );
}
