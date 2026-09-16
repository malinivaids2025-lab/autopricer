# AutoPricer AI — Full-Stack Used-Car Valuation & Market Analytics

AutoPricer AI is an enterprise-grade, full-stack machine learning web application for precision used-car valuation, explainable AI diagnostics, predictive selling turnover velocity, anomaly/fraud screening, and interactive macroeconomic market intelligence.

---

## 🌟 8 Core Objectives

1. **Price Prediction Engine**
   - **XGBoost Regressor** benchmarked and chosen over Random Forest ($R^2 = 0.9358$, $\text{RMSE} = \$2,469.24$, $\text{MAE} = \$1,288.43$).
   - **90% Conformal Calibrated Interval**: Heteroskedastic log-residual quantiles ($q_{0.05}, q_{0.95}$) generating balanced confidence bands with $89.94\%$ empirical test coverage.
2. **Selling-Time Prediction**
   - Gradient-boosted days-on-market regressor predicting expected turnover duration ($\text{MAE} = 18.8\text{ days}$) accompanied by market velocity categorization (*Fast*, *Average*, *Slow*).
3. **Explainable AI (XAI)**
   - **SHAP TreeExplainer**: Quantifies exact game-theoretic additive dollar impact ($\pm\Delta\$$) for Brand tier, Vehicle Age, Odometer wear, Transmission, Fuel type, and Region.
   - **LIME Tabular Explainer**: Delivers local linear surrogate rules and percentage weights for transparent attribution.
4. **Counterfactual "What-If" Optimizer**
   - Evaluates actionable scenarios (e.g., *"If mileage were 10,000 km instead of 18,000 km, estimated value increases by +$991"* or *"A 2022 model year version represents a +$2,162 value enhancement"*).
5. **Recommendation Engine**
   - Unsupervised **K-Nearest Neighbors (K-NN)** cosine similarity vector index querying 15,410 active vehicle listings to return the top 5 most comparable inventory comps.
6. **Fraud & Anomaly Detection**
   - **Isolation Forest** unsupervised manifold assessing multidimensional feature-to-price residuals.
   - Computes continuous **0–100 Fraud Risk Score** mapped directly from `decision_function()` with diagnostic safety advisories for salvage underpricing, odometer rollback, or dealer markup anomalies.
7. **Market Analytics Intelligence**
   - Interactive Recharts visualizing price by region, brand valuation rankings (Average vs Median), depreciation curves by vehicle year, and monthly listing volume vs demand velocity indicators.
8. **Production & Deployment Ready**
   - Containerized with Docker and `docker-compose.yml` for unified single-command deployment across FastAPI backend (Port 8000) and React + Vite frontend (Port 5173).

---

## 🏗️ Architecture & Project Structure

```text
├── backend/
│   ├── app/
│   │   ├── config.py              # Directory paths and global constants
│   │   ├── schemas.py             # Pydantic v2 request/response schemas
│   │   ├── data_pipeline.py       # Auto-mapping column parser, IQR cleaner, EDA summary
│   │   ├── train.py               # XGBoost, RF, Quantiles, KNN, Isolation Forest trainer
│   │   ├── main.py                # FastAPI REST router with OpenAPI & CORS
│   │   └── ml/
│   │       ├── price_model.py     # Price predictor & conformal 90% intervals
│   │       ├── selling_time_model.py # Days-to-sale velocity model
│   │       ├── explainability.py  # SHAP TreeExplainer, LIME & Counterfactuals
│   │       ├── recommender.py     # KNN 5-nearest neighbors engine
│   │       ├── fraud_detector.py  # Continuous Isolation Forest anomaly scorer
│   │       └── market_analytics.py# Market trend aggregations & form metadata
│   ├── data/
│   │   ├── cardekho_dataset.csv   # 15,411 real used car transactions
│   │   ├── cleaned_cars.csv       # Preprocessed and IQR-capped dataset
│   │   └── eda_summary.json       # Statistical distributions and correlation matrix
│   ├── models/                    # Serialized .pkl artifacts and conformal quantiles
│   ├── tests/
│   │   └── test_api.py            # Automated pytest integration test suite (9/9 passing)
│   ├── Dockerfile                 # Python 3.11 container definition
│   └── requirements.txt           # Backend dependencies
│
├── frontend/
│   ├── src/
│   │   ├── api/client.js          # Axios backend API client
│   │   ├── components/
│   │   │   ├── Navbar.jsx         # Navigation, branding & live API status pill
│   │   │   ├── Hero.jsx           # Automotive tech hero banner & demo presets
│   │   │   ├── ValuationForm.jsx  # Multi-step wizard with live validation
│   │   │   ├── ResultsDashboard.jsx # Price ticker, confidence slider & gauges
│   │   │   ├── ShapChart.jsx      # Horizontal SHAP impact chart & LIME rules
│   │   │   ├── CounterfactualPanel.jsx # Actionable What-If optimization cards
│   │   │   ├── SimilarCars.jsx    # 5 comparable vehicle cards with match %
│   │   │   ├── MarketAnalyticsView.jsx # Recharts regional, brand & depreciation charts
│   │   │   └── MethodologyView.jsx # ML architecture whitepaper & benchmark table
│   │   ├── App.jsx                # Root view router and state manager
│   │   ├── index.css              # Glassmorphism utilities & cyber glow themes
│   │   └── main.jsx               # React DOM entrypoint
│   ├── Dockerfile                 # Node multi-stage production container
│   ├── package.json               # React, Vite, Tailwind, Framer Motion, Recharts
│   └── vite.config.js             # Vite configuration
│
├── docker-compose.yml             # Orchestration for Backend (8000) & Frontend (5173)
└── README.md                      # Comprehensive documentation
```

---

## 🚀 Running Locally (Without Docker)

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ & npm

### 2. Backend Setup
```bash
# In project root
pip install -r backend/requirements.txt

# Run Data Pipeline & Train ML Models (if needed)
python -m backend.app.data_pipeline
python -m backend.app.train

# Run Backend Integration Tests
pytest backend/tests -v

# Start FastAPI Development Server (Port 8000)
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
*Backend API docs are accessible at: `http://127.0.0.1:8000/docs`*

### 3. Frontend Setup
```bash
# In a separate terminal
cd frontend
npm install
npm run dev
```
*Frontend application is accessible at: `http://localhost:5173`*

---

## 🐳 Running with Docker Compose

To start both the Python backend and React frontend with a single command:

```bash
# Build and launch containers
docker-compose up --build
```

- **Frontend UI**: `http://localhost:5173`
- **Backend API**: `http://localhost:8000`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`

To stop the containers:
```bash
docker-compose down
```

---

## 📡 API Reference Overview

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/predict-price` | `POST` | Price prediction with 90% conformal interval, SHAP feature impact, LIME attribution, and counterfactuals |
| `/api/predict-selling-time` | `POST` | Expected days to sale with turnover liquidity factors |
| `/api/recommendations` | `POST` | Top 5 comparable vehicles from inventory using K-NN |
| `/api/fraud-check` | `POST` | Continuous 0–100 fraud risk score + anomaly diagnosis |
| `/api/valuation-complete` | `POST` | Full composite valuation suite in one high-speed roundtrip |
| `/api/market-analytics` | `GET` | Aggregated market trends, brand comparisons, regional statistics |
| `/api/options` | `GET` | Dynamic dropdown metadata (brands, models, fuel types, regions) |
| `/api/health` | `GET` | System and ML model readiness health check |

---

## 🧪 Testing Verification

Run the full automated test suite:
```bash
pytest backend/tests/test_api.py -v
```
Output:
```text
backend/tests/test_api.py::test_health_check PASSED                      [ 11%]
backend/tests/test_api.py::test_predict_price PASSED                     [ 22%]
backend/tests/test_api.py::test_predict_selling_time PASSED              [ 33%]
backend/tests/test_api.py::test_recommendations PASSED                   [ 44%]
backend/tests/test_api.py::test_fraud_check_normal PASSED                [ 55%]
backend/tests/test_api.py::test_fraud_check_anomaly PASSED               [ 66%]
backend/tests/test_api.py::test_valuation_complete PASSED                [ 77%]
backend/tests/test_api.py::test_market_analytics PASSED                  [ 88%]
backend/tests/test_api.py::test_options PASSED                           [100%]
======================== 9 passed in 5.32s =========================
```
