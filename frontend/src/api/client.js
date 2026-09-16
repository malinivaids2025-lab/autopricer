import axios from 'axios';

// Read API URL from Vite environment variable (e.g. VITE_API_URL=https://autopricer-backend.onrender.com)
// Defaults to local development endpoint http://127.0.0.1:8000
const rawUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
const API_BASE_URL = rawUrl.replace(/\/+$/, '');

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const checkHealth = async () => {
  const response = await api.get('/api/health');
  return response.data;
};

export const getOptions = async () => {
  const response = await api.get('/api/options');
  return response.data;
};

export const predictPrice = async (carData) => {
  const response = await api.post('/api/predict-price', carData);
  return response.data;
};

export const predictSellingTime = async (carData) => {
  const response = await api.post('/api/predict-selling-time', carData);
  return response.data;
};

export const getRecommendations = async (carData) => {
  const response = await api.post('/api/recommendations', carData);
  return response.data;
};

export const checkFraud = async (carData) => {
  const response = await api.post('/api/fraud-check', carData);
  return response.data;
};

export const getValuationComplete = async (carData) => {
  const response = await api.post('/api/valuation-complete', carData);
  return response.data;
};

export const evaluatePhotoCondition = async (payload) => {
  const response = await api.post('/api/photo-analysis/evaluate', payload);
  return response.data;
};

export const getMarketAnalytics = async () => {
  const response = await api.get('/api/market-analytics');
  return response.data;
};

export default api;
