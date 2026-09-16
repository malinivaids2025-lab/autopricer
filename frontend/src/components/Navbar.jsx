import React from 'react';
import { Sparkles, BarChart3, BookOpen, Car, Camera, ShieldCheck } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, apiStatus, onNewValuationClick }) {
  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-white/10 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          
          {/* Logo */}
          <div 
            onClick={() => setActiveTab('valuation')}
            className="flex items-center space-x-3 cursor-pointer group"
          >
            <div className="relative">
              <div className="w-11 h-11 rounded-xl bg-gradient-to-tr from-emerald-600 via-emerald-500 to-teal-700 flex items-center justify-center shadow-emerald-glow group-hover:scale-105 transition-transform duration-300">
                <Car className="w-6 h-6 text-slate-950" />
              </div>
              <div className="absolute -bottom-1 -right-1 w-4 h-4 rounded-full bg-slate-950 flex items-center justify-center border border-emerald-500/40">
                <Sparkles className="w-2.5 h-2.5 text-emerald-400 animate-pulse" />
              </div>
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-100 to-slate-300 bg-clip-text text-transparent font-heading">
                  AutoPricer <span className="bg-gradient-to-r from-emerald-400 to-teal-300 bg-clip-text text-transparent">AI</span>
                </span>
                <span className="text-[10px] font-mono uppercase px-1.5 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 font-semibold">
                  ML Engine v2
                </span>
              </div>
              <p className="text-[11px] text-slate-400 hidden sm:block">Intelligent Vehicle Valuation & Market Analytics</p>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="hidden md:flex items-center space-x-1 bg-slate-950/80 p-1.5 rounded-xl border border-white/5">
            <button
              onClick={() => setActiveTab('valuation')}
              className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                activeTab === 'valuation'
                  ? 'bg-gradient-to-r from-emerald-500 to-teal-600 text-slate-950 shadow-emerald-glow font-bold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
              }`}
            >
              <Car className="w-4 h-4" />
              <span>Valuation Studio</span>
            </button>

            <button
              onClick={() => setActiveTab('photo-analysis')}
              className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                activeTab === 'photo-analysis'
                  ? 'bg-gradient-to-r from-emerald-500 to-teal-600 text-slate-950 shadow-emerald-glow font-bold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
              }`}
            >
              <Camera className="w-4 h-4" />
              <span>Photo Analysis</span>
            </button>

            <button
              onClick={() => setActiveTab('analytics')}
              className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                activeTab === 'analytics'
                  ? 'bg-gradient-to-r from-emerald-500 to-teal-600 text-slate-950 shadow-emerald-glow font-bold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
              }`}
            >
              <BarChart3 className="w-4 h-4" />
              <span>Market Analytics</span>
            </button>

            <button
              onClick={() => setActiveTab('methodology')}
              className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                activeTab === 'methodology'
                  ? 'bg-gradient-to-r from-emerald-500 to-teal-600 text-slate-950 shadow-emerald-glow font-bold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'
              }`}
            >
              <BookOpen className="w-4 h-4" />
              <span>ML Architecture</span>
            </button>
          </nav>

          {/* Right Action & API Status */}
          <div className="flex items-center space-x-3">
            {/* API Status Pill */}
            <div className="flex items-center space-x-2 px-3 py-1.5 rounded-full bg-slate-950/80 border border-emerald-500/20 text-xs font-mono">
              <span className={`w-2 h-2 rounded-full ${apiStatus === 'online' ? 'bg-emerald-400 animate-ping' : apiStatus === 'offline' ? 'bg-rose-500' : 'bg-amber-400'}`}></span>
              <span className={apiStatus === 'online' ? 'text-emerald-400' : apiStatus === 'offline' ? 'text-rose-400' : 'text-amber-400'}>
                {apiStatus === 'online' ? 'CONNECTED' : apiStatus === 'offline' ? 'OFFLINE' : 'CONNECTING...'}
              </span>
            </div>

            {/* Quick Valuate CTA */}
            <button
              onClick={() => {
                setActiveTab('valuation');
                if (onNewValuationClick) onNewValuationClick();
              }}
              className="hidden lg:flex items-center space-x-2 px-4 py-2 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 text-slate-950 font-bold text-sm hover:opacity-95 shadow-emerald-glow transition-all"
            >
              <Sparkles className="w-4 h-4" />
              <span>New Valuation</span>
            </button>
          </div>

        </div>

        {/* Mobile Navigation Bar */}
        <div className="grid grid-cols-4 md:hidden py-2 border-t border-white/5 text-center gap-1">
          <button
            onClick={() => setActiveTab('valuation')}
            className={`flex flex-col items-center justify-center py-1.5 px-1 rounded-lg text-[11px] ${
              activeTab === 'valuation' ? 'text-emerald-400 font-bold bg-emerald-500/10' : 'text-slate-400'
            }`}
          >
            <Car className="w-3.5 h-3.5 mb-0.5" />
            <span>Valuation</span>
          </button>
          <button
            onClick={() => setActiveTab('photo-analysis')}
            className={`flex flex-col items-center justify-center py-1.5 px-1 rounded-lg text-[11px] ${
              activeTab === 'photo-analysis' ? 'text-emerald-400 font-bold bg-emerald-500/10' : 'text-slate-400'
            }`}
          >
            <Camera className="w-3.5 h-3.5 mb-0.5" />
            <span>Photo AI</span>
          </button>
          <button
            onClick={() => setActiveTab('analytics')}
            className={`flex flex-col items-center justify-center py-1.5 px-1 rounded-lg text-[11px] ${
              activeTab === 'analytics' ? 'text-emerald-400 font-bold bg-emerald-500/10' : 'text-slate-400'
            }`}
          >
            <BarChart3 className="w-3.5 h-3.5 mb-0.5" />
            <span>Market</span>
          </button>
          <button
            onClick={() => setActiveTab('methodology')}
            className={`flex flex-col items-center justify-center py-1.5 px-1 rounded-lg text-[11px] ${
              activeTab === 'methodology' ? 'text-emerald-400 font-bold bg-emerald-500/10' : 'text-slate-400'
            }`}
          >
            <BookOpen className="w-3.5 h-3.5 mb-0.5" />
            <span>Architecture</span>
          </button>
        </div>

      </div>
    </header>
  );
}
