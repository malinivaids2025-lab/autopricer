import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Car, Calendar, Gauge, Fuel, Cog, Users, MapPin,
  ArrowRight, ArrowLeft, Sparkles, AlertCircle
} from 'lucide-react';

export default function ValuationForm({ options, formData, setFormData, onSubmit, isLoading }) {
  const [currentStep, setCurrentStep] = useState(1);
  const [errors, setErrors] = useState({});

  const availableBrands = options?.brands?.length ? options.brands : [
    "Toyota", "Honda", "Hyundai", "Maruti Suzuki", "BMW", "Mercedes-Benz", "Audi", "Ford", "Mahindra", "Volkswagen", "Tata"
  ];

  const currentModels = options?.brand_models?.[formData.brand] || ["Generic Model", "Sedan", "SUV"];

  // Update model if selected brand changes and current model is not in model list
  useEffect(() => {
    if (options?.brand_models?.[formData.brand]) {
      const models = options.brand_models[formData.brand];
      if (models.length > 0 && !models.includes(formData.model)) {
        setFormData(prev => ({ ...prev, model: models[0] }));
      }
    }
  }, [formData.brand, options]);

  const validateStep = (step) => {
    const newErrors = {};
    if (step === 1) {
      if (!formData.brand) newErrors.brand = "Please select a brand";
      if (!formData.model) newErrors.model = "Please select a model";
      if (!formData.year || formData.year < 1990 || formData.year > 2026) newErrors.year = "Valid year required (1990-2026)";
    } else if (step === 2) {
      if (formData.mileage === "" || formData.mileage < 0) newErrors.mileage = "Valid odometer reading required";
      if (!formData.fuel_type) newErrors.fuel_type = "Please select fuel type";
      if (!formData.transmission) newErrors.transmission = "Please select transmission";
    } else if (step === 3) {
      if (!formData.owner_count || formData.owner_count < 1) newErrors.owner_count = "Owner count required";
      if (!formData.region) newErrors.region = "Please select region";
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleNext = () => {
    if (validateStep(currentStep)) {
      setCurrentStep(prev => Math.min(prev + 1, 3));
    }
  };

  const handlePrev = () => {
    setCurrentStep(prev => Math.max(prev - 1, 1));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateStep(currentStep)) {
      onSubmit(formData);
    }
  };

  const steps = [
    { num: 1, title: "Identity", desc: "Brand, Model & Year" },
    { num: 2, title: "Powertrain", desc: "Odometer & Fuel" },
    { num: 3, title: "Market", desc: "Ownership & Region" },
  ];

  return (
    <div id="valuation-form-section" className="max-w-3xl mx-auto">
      <div className="glass-panel-glow rounded-3xl p-6 sm:p-10 relative overflow-hidden border border-emerald-500/20 shadow-2xl">

        {/* Form Title & Stepper Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-2xl sm:text-3xl font-bold text-white font-heading tracking-tight">
                Vehicle Valuation Studio
              </h2>
              <p className="text-xs sm:text-sm text-slate-400 mt-1">
                Enter vehicle parameters for real-time XGBoost price inference and SHAP explainability.
              </p>
            </div>
            <span className="text-xs font-mono font-semibold px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-300">
              Step {currentStep} of 3
            </span>
          </div>

          {/* Stepper Progress Bar */}
          <div className="grid grid-cols-3 gap-2 sm:gap-3 pt-2">
            {steps.map((step) => {
              const isActive = currentStep === step.num;
              const isDone = currentStep > step.num;
              return (
                <div
                  key={step.num}
                  onClick={() => { if (isDone) setCurrentStep(step.num); }}
                  className={`relative p-3 rounded-xl border transition-all duration-300 ${isDone ? 'cursor-pointer' : ''
                    } ${isActive
                      ? 'bg-slate-800/90 border-emerald-400 shadow-emerald-glow'
                      : isDone
                        ? 'bg-slate-900/60 border-emerald-500/40 text-slate-300'
                        : 'bg-slate-900/30 border-white/5 text-slate-500'
                    }`}
                >
                  <div className="flex items-center space-x-2">
                    <span className={`w-5 h-5 rounded-full text-[11px] font-mono font-bold flex items-center justify-center ${isActive ? 'bg-emerald-500 text-slate-950' : isDone ? 'bg-emerald-600 text-slate-950' : 'bg-slate-800 text-slate-400'
                      }`}>
                      {isDone ? '✓' : step.num}
                    </span>
                    <span className="text-xs font-semibold font-heading truncate">{step.title}</span>
                  </div>
                  <div className="text-[10px] text-slate-400 mt-1 hidden sm:block truncate">{step.desc}</div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Step Forms */}
        <form onSubmit={handleSubmit}>
          <AnimatePresence mode="wait">

            {/* STEP 1: Brand, Model, Year */}
            {currentStep === 1 && (
              <motion.div
                key="step1"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.3 }}
                className="space-y-6"
              >
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">

                  {/* Brand */}
                  <div>
                    <label className="block text-xs font-mono text-slate-300 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
                      <Car className="w-3.5 h-3.5 text-emerald-400" />
                      <span>Manufacturer Brand</span>
                    </label>
                    <select
                      value={formData.brand}
                      onChange={(e) => setFormData({ ...formData, brand: e.target.value })}
                      className="w-full px-4 py-3.5 rounded-xl glass-input text-sm text-white font-medium focus:border-emerald-400"
                    >
                      {availableBrands.map((b) => (
                        <option key={b} value={b} className="bg-slate-900 text-white">{b}</option>
                      ))}
                    </select>
                    {errors.brand && <p className="text-xs text-rose-400 mt-1 flex items-center gap-1"><AlertCircle className="w-3 h-3" />{errors.brand}</p>}
                  </div>

                  {/* Model */}
                  <div>
                    <label className="block text-xs font-mono text-slate-300 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
                      <Cog className="w-3.5 h-3.5 text-emerald-400" />
                      <span>Vehicle Model</span>
                    </label>
                    <select
                      value={formData.model}
                      onChange={(e) => setFormData({ ...formData, model: e.target.value })}
                      className="w-full px-4 py-3.5 rounded-xl glass-input text-sm text-white font-medium focus:border-emerald-400"
                    >
                      {currentModels.map((m) => (
                        <option key={m} value={m} className="bg-slate-900 text-white">{m}</option>
                      ))}
                    </select>
                    {errors.model && <p className="text-xs text-rose-400 mt-1 flex items-center gap-1"><AlertCircle className="w-3 h-3" />{errors.model}</p>}
                  </div>

                </div>

                {/* Model Year Slider / Input */}
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-xs font-mono text-slate-300 uppercase tracking-wider flex items-center space-x-1.5">
                      <Calendar className="w-3.5 h-3.5 text-emerald-400" />
                      <span>Model Year: <strong className="text-emerald-300 text-sm font-bold font-mono ml-1">{formData.year}</strong></span>
                    </label>
                    <span className="text-[11px] font-mono text-slate-400">{2024 - formData.year} Years Old</span>
                  </div>
                  <input
                    type="range"
                    min="2005"
                    max="2024"
                    step="1"
                    value={formData.year}
                    onChange={(e) => setFormData({ ...formData, year: parseInt(e.target.value) })}
                    className="w-full accent-emerald-400 h-2 bg-slate-800 rounded-lg cursor-pointer"
                  />
                  <div className="flex justify-between text-[10px] font-mono text-slate-500 mt-1">
                    <span>2005 (Vintage)</span>
                    <span>2015</span>
                    <span>2020</span>
                    <span>2024 (Brand New)</span>
                  </div>
                </div>
              </motion.div>
            )}

            {/* STEP 2: Powertrain & Mileage */}
            {currentStep === 2 && (
              <motion.div
                key="step2"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.3 }}
                className="space-y-6"
              >
                {/* Odometer (Mileage) */}
                <div>
                  <label className="block text-xs font-mono text-slate-300 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
                    <Gauge className="w-3.5 h-3.5 text-emerald-400" />
                    <span>Odometer Reading (Km Driven)</span>
                  </label>
                  <div className="relative">
                    <input
                      type="number"
                      value={formData.mileage}
                      onChange={(e) => setFormData({ ...formData, mileage: parseFloat(e.target.value) || 0 })}
                      placeholder="e.g. 45000"
                      className="w-full pl-4 pr-16 py-3.5 rounded-xl glass-input text-sm text-white font-mono font-medium focus:border-emerald-400"
                    />
                    <span className="absolute right-4 top-1/2 -translate-y-1/2 text-xs font-mono text-slate-400">km</span>
                  </div>
                  {errors.mileage && <p className="text-xs text-rose-400 mt-1 flex items-center gap-1"><AlertCircle className="w-3 h-3" />{errors.mileage}</p>}
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
                  {/* Fuel Type */}
                  <div>
                    <label className="block text-xs font-mono text-slate-300 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
                      <Fuel className="w-3.5 h-3.5 text-emerald-400" />
                      <span>Fuel Type</span>
                    </label>
                    <select
                      value={formData.fuel_type}
                      onChange={(e) => setFormData({ ...formData, fuel_type: e.target.value })}
                      className="w-full px-4 py-3.5 rounded-xl glass-input text-sm text-white font-medium focus:border-emerald-400"
                    >
                      {["Petrol", "Diesel", "CNG", "Electric", "Hybrid", "LPG"].map((f) => (
                        <option key={f} value={f} className="bg-slate-900 text-white">{f}</option>
                      ))}
                    </select>
                  </div>

                  {/* Transmission */}
                  <div>
                    <label className="block text-xs font-mono text-slate-300 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
                      <Cog className="w-3.5 h-3.5 text-emerald-400" />
                      <span>Transmission</span>
                    </label>
                    <div className="grid grid-cols-2 gap-2">
                      {["Automatic", "Manual"].map((t) => (
                        <button
                          type="button"
                          key={t}
                          onClick={() => setFormData({ ...formData, transmission: t })}
                          className={`py-3 px-3 rounded-xl border text-sm font-medium transition-all ${formData.transmission === t
                              ? 'bg-emerald-500/20 border-emerald-400 text-emerald-300 font-semibold shadow-emerald-glow'
                              : 'bg-slate-900/60 border-white/10 text-slate-400 hover:text-white'
                            }`}
                        >
                          {t}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              </motion.div>
            )}

            {/* STEP 3: Ownership, Region & Optional Target Price */}
            {currentStep === 3 && (
              <motion.div
                key="step3"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.3 }}
                className="space-y-6"
              >
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">

                  {/* Previous Owners */}
                  <div>
                    <label className="block text-xs font-mono text-slate-300 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
                      <Users className="w-3.5 h-3.5 text-emerald-400" />
                      <span>Ownership History</span>
                    </label>
                    <select
                      value={formData.owner_count}
                      onChange={(e) => setFormData({ ...formData, owner_count: parseInt(e.target.value) })}
                      className="w-full px-4 py-3.5 rounded-xl glass-input text-sm text-white font-medium focus:border-emerald-400"
                    >
                      <option value={1} className="bg-slate-900">1st Owner (Single Owner)</option>
                      <option value={2} className="bg-slate-900">2nd Owner</option>
                      <option value={3} className="bg-slate-900">3rd Owner</option>
                      <option value={4} className="bg-slate-900">4+ Owners</option>
                    </select>
                  </div>

                  {/* Region */}
                  <div>
                    <label className="block text-xs font-mono text-slate-300 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
                      <MapPin className="w-3.5 h-3.5 text-emerald-400" />
                      <span>Regional Marketplace</span>
                    </label>
                    <select
                      value={formData.region}
                      onChange={(e) => setFormData({ ...formData, region: e.target.value })}
                      className="w-full px-4 py-3.5 rounded-xl glass-input text-sm text-white font-medium focus:border-emerald-400"
                    >
                      {["Metro", "North", "South", "East", "West", "Central"].map((r) => (
                        <option key={r} value={r} className="bg-slate-900 text-white">{r}</option>
                      ))}
                    </select>
                  </div>

                </div>

                {/* Optional Actual Listed Price for Fraud Screening (in INR) */}
                <div className="p-4 rounded-2xl bg-slate-950/60 border border-white/10 space-y-2">
                  <div className="flex items-center justify-between">
                    <label className="text-xs font-mono text-slate-300 uppercase tracking-wider flex items-center space-x-1.5">
                      <span className="text-emerald-400 font-bold font-mono">₹</span>
                      <span>Target / Asking Price <span className="text-[10px] text-slate-400 font-normal lowercase">(optional fraud check)</span></span>
                    </label>
                    <span className="text-[10px] font-mono text-slate-400">INR (₹)</span>
                  </div>
                  <input
                    type="number"
                    value={formData.price || ''}
                    onChange={(e) => setFormData({ ...formData, price: e.target.value ? parseFloat(e.target.value) : null })}
                    placeholder="e.g. 1850000 (enter asking price to check for underpricing anomalies)..."
                    className="w-full px-4 py-3 rounded-xl glass-input text-sm text-white font-mono font-medium focus:border-emerald-400"
                  />
                  <p className="text-[11px] text-slate-400">
                    If provided, Isolation Forest will evaluate asking price against fair market residuals in ₹ to flag anomalies.
                  </p>
                </div>

              </motion.div>
            )}

          </AnimatePresence>

          {/* Stepper Navigation Buttons */}
          <div className="flex items-center justify-between pt-8 mt-6 border-t border-white/10">
            {currentStep > 1 ? (
              <button
                type="button"
                onClick={handlePrev}
                className="flex items-center space-x-2 px-5 py-3 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-slate-300 text-sm font-medium transition-all"
              >
                <ArrowLeft className="w-4 h-4" />
                <span>Back</span>
              </button>
            ) : <div></div>}

            {currentStep < 3 ? (
              <button
                type="button"
                onClick={handleNext}
                className="flex items-center space-x-2 px-6 py-3 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 text-slate-950 font-bold text-sm hover:shadow-emerald-glow hover:scale-[1.02] active:scale-[0.98] transition-all"
              >
                <span>Continue</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                type="submit"
                disabled={isLoading}
                className={`flex items-center space-x-2 px-8 py-3.5 rounded-xl bg-gradient-to-r from-emerald-400 via-emerald-500 to-teal-600 text-slate-950 font-extrabold text-sm hover:shadow-emerald-glow transition-all ${isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:scale-[1.02] active:scale-[0.98]'
                  }`}
              >
                <Sparkles className="w-4 h-4 text-slate-950" />
                <span>{isLoading ? 'Running ML Models...' : 'Get Valuation & Insights'}</span>
              </button>
            )}
          </div>

        </form>

      </div>
    </div>
  );
}
