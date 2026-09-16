import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import ValuationForm from './components/ValuationForm';
import ResultsDashboard from './components/ResultsDashboard';
import PhotoAnalysisView from './components/PhotoAnalysisView';
import MarketAnalyticsView from './components/MarketAnalyticsView';
import MethodologyView from './components/MethodologyView';
import {
  checkHealth, getOptions, getValuationComplete, getMarketAnalytics
} from './api/client';
import { AlertTriangle } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('valuation');
  const [apiStatus, setApiStatus] = useState('connecting');
  const [options, setOptions] = useState(null);
  const [analyticsData, setAnalyticsData] = useState(null);
  const [isLoadingAnalytics, setIsLoadingAnalytics] = useState(false);

  // Form & Valuation States
  const [formData, setFormData] = useState({
    brand: 'Toyota',
    model: 'Camry',
    year: 2020,
    mileage: 18000,
    fuel_type: 'Petrol',
    transmission: 'Automatic',
    owner_count: 1,
    region: 'Metro',
    price: null,
  });

  const [submittedCar, setSubmittedCar] = useState(null);
  const [valuationResult, setValuationResult] = useState(null);
  const [isValuationLoading, setIsValuationLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);

  // Initial Data Load & Health Check
  useEffect(() => {
    const initApp = async () => {
      try {
        const health = await checkHealth();
        if (health?.status === 'online') {
          setApiStatus('online');
        }
      } catch (err) {
        console.warn('API health check error:', err);
        setApiStatus('offline');
      }

      try {
        const opts = await getOptions();
        setOptions(opts);
        if (opts.brands?.length && !opts.brands.includes(formData.brand)) {
          setFormData(prev => ({
            ...prev,
            brand: opts.brands[0],
            model: opts.brand_models?.[opts.brands[0]]?.[0] || 'Model'
          }));
        }
      } catch (err) {
        console.warn('Could not load options:', err);
      }
    };

    initApp();
  }, []);

  // Fetch Market Analytics when tab is active
  useEffect(() => {
    if (activeTab === 'analytics' && !analyticsData) {
      setIsLoadingAnalytics(true);
      getMarketAnalytics()
        .then(data => {
          setAnalyticsData(data);
          setIsLoadingAnalytics(false);
        })
        .catch(err => {
          console.error('Market analytics fetch error:', err);
          setIsLoadingAnalytics(false);
        });
    }
  }, [activeTab, analyticsData]);

  const handleValuationSubmit = async (carPayload) => {
    setIsValuationLoading(true);
    setErrorMessage(null);
    try {
      const result = await getValuationComplete(carPayload);
      setValuationResult(result);
      setSubmittedCar(carPayload);
      setIsValuationLoading(false);
      // Smooth scroll to results
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      console.error('Valuation error:', err);
      setErrorMessage(err.response?.data?.detail || 'Failed to compute valuation. Please ensure backend is running.');
      setIsValuationLoading(false);
    }
  };

  const handleSelectPreset = (preset) => {
    setFormData(preset);
    setValuationResult(null);
    const formEl = document.getElementById('valuation-form-section');
    if (formEl) {
      formEl.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleResetValuation = () => {
    setValuationResult(null);
    setSubmittedCar(null);
    const formEl = document.getElementById('valuation-form-section');
    if (formEl) {
      formEl.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const scrollToForm = () => {
    const formEl = document.getElementById('valuation-form-section');
    if (formEl) {
      formEl.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#070c0a] text-slate-100 selection:bg-emerald-500/30 selection:text-emerald-300">

      {/* Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        apiStatus={apiStatus}
        onNewValuationClick={handleResetValuation}
      />

      {/* Main Content Area */}
      <main className="flex-1 px-4 sm:px-6 lg:px-8 py-8">

        {/* Error Toast Notification */}
        {errorMessage && (
          <div className="max-w-3xl mx-auto mb-6 p-4 rounded-2xl bg-rose-950/80 border border-rose-500/40 text-rose-300 text-xs sm:text-sm font-mono flex items-center justify-between shadow-2xl">
            <div className="flex items-center space-x-2">
              <AlertTriangle className="w-5 h-5 text-rose-400 flex-shrink-0" />
              <span>{errorMessage}</span>
            </div>
            <button onClick={() => setErrorMessage(null)} className="text-slate-400 hover:text-white ml-2">✕</button>
          </div>
        )}

        {/* TAB 1: VALUATION STUDIO */}
        {activeTab === 'valuation' && (
          <div className="space-y-12">
            {!valuationResult && (
              <Hero
                onGetStarted={scrollToForm}
                onSelectPreset={handleSelectPreset}
              />
            )}

            {valuationResult ? (
              <ResultsDashboard
                result={valuationResult}
                inputCar={submittedCar}
                onReset={handleResetValuation}
              />
            ) : (
              <ValuationForm
                options={options}
                formData={formData}
                setFormData={setFormData}
                onSubmit={handleValuationSubmit}
                isLoading={isValuationLoading}
              />
            )}
          </div>
        )}

        {/* TAB 2: PHOTO ANALYSIS */}
        {activeTab === 'photo-analysis' && (
          <PhotoAnalysisView
            valuationResult={valuationResult}
            inputCar={submittedCar || formData}
          />
        )}

        {/* TAB 3: MARKET ANALYTICS */}
        {activeTab === 'analytics' && (
          <MarketAnalyticsView
            analyticsData={analyticsData}
            isLoading={isLoadingAnalytics}
          />
        )}

        {/* TAB 4: ML METHODOLOGY */}
        {activeTab === 'methodology' && (
          <MethodologyView />
        )}

      </main>

      {/* Footer */}
      <footer className="glass-panel border-t border-white/5 py-8 mt-16 text-xs text-slate-400">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <span className="font-bold text-white font-heading text-sm">AutoPricer AI</span>
            <span>• Full-Stack Machine Learning Used-Car Valuation Platform</span>
          </div>
          <div className="flex items-center space-x-6 font-mono text-[11px]">
            <span>FastAPI Backend (8000)</span>
            <span>React + Vite Frontend (5173)</span>
            <span>XGBoost + SHAP + Conformal (INR ₹)</span>
          </div>
        </div>
      </footer>

    </div>
  );
}
