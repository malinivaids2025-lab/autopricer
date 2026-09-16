import os
import logging
from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import (
    CarInput,
    PricePredictionResponse,
    SellingTimePredictionResponse,
    RecommendationsResponse,
    FraudCheckResponse,
    ValuationCompleteResponse,
    MarketAnalyticsResponse,
    OptionsResponse,
    PhotoConditionEvaluateRequest,
    PhotoConditionEvaluateResponse,
)
from backend.app.config import MODELS_DIR
from backend.app.ml.price_model import price_service
from backend.app.ml.selling_time_model import selling_time_service
from backend.app.ml.explainability import explainability_service
from backend.app.ml.recommender import recommender_service
from backend.app.ml.fraud_detector import fraud_detector_service
from backend.app.ml.market_analytics import market_analytics_service
from backend.app.ml.msrp_data import get_base_msrp, calculate_bounded_condition_adjustment

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("autopricer-api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan event handler.
    Guarantees that on cold boot (such as Render ephemeral instances),
    all ML models exist and are properly trained and loaded.
    """
    required_files = [
        MODELS_DIR / "price_model.pkl",
        MODELS_DIR / "preprocessor.pkl",
        MODELS_DIR / "selling_time_model.pkl",
        MODELS_DIR / "recommender.pkl",
        MODELS_DIR / "fraud_detector.pkl",
    ]
    missing = [f for f in required_files if not f.exists()]
    if missing:
        logger.warning(f"Missing model artifacts on startup ({len(missing)} files). Running automated bootstrap training...")
        try:
            from backend.app.train import run_full_training
            run_full_training()
            logger.info("Automated model training completed on boot.")
        except Exception as e:
            logger.error(f"Error during boot model training: {e}", exc_info=True)

    # Ensure all services have loaded their models
    price_service.load_models()
    selling_time_service.load_models()
    recommender_service.load_models()
    fraud_detector_service.load_models()
    market_analytics_service.load_data()
    logger.info("AutoPricer AI ML services initialized and ready.")
    yield


app = FastAPI(
    title="AutoPricer AI API",
    description="Full-Stack Intelligent Used-Car Valuation & Market Analytics Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Dynamic CORS configuration from environment variable
raw_allowed_origins = os.getenv("ALLOWED_ORIGINS", "")
if raw_allowed_origins.strip():
    allowed_origins = [o.strip() for o in raw_allowed_origins.split(",") if o.strip()]
else:
    allowed_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

# Allow any Vercel preview domain pattern by default or when specified
allow_origin_regex = os.getenv("ALLOWED_ORIGIN_REGEX", r"https://.*\.vercel\.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=allow_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["Health"])
def health_check():
    """System health and model readiness status check."""
    return {
        "status": "online",
        "service": "AutoPricer AI Backend",
        "version": "1.0.0",
        "models_ready": {
            "price_model": price_service.model is not None,
            "quantile_intervals": price_service.conformal_meta is not None,
            "selling_time_model": selling_time_service.model is not None,
            "recommender": recommender_service.knn is not None,
            "fraud_detector": fraud_detector_service.iso_forest is not None,
        }
    }


@app.post("/api/predict-price", response_model=PricePredictionResponse, tags=["Valuation"])
def predict_price(car: CarInput):
    """Predict car price with 90% confidence interval, SHAP feature impact, LIME attribution, and counterfactuals."""
    try:
        pred_price, conf_interval, model_name = price_service.predict(car)
        base_msrp = get_base_msrp(car.brand, car.model)
        shap_contribs = explainability_service.get_shap_contributions(car, pred_price)
        lime_rules = explainability_service.get_lime_explanations(car)
        counterfactual = explainability_service.generate_counterfactual(car, pred_price)
        plain_summary = explainability_service.generate_plain_language_summary(car, pred_price, shap_contribs)

        return PricePredictionResponse(
            predicted_price=pred_price,
            confidence_interval=conf_interval,
            base_msrp=base_msrp,
            currency="₹",
            model_used=model_name,
            shap_contributions=shap_contribs,
            lime_explanations=lime_rules,
            counterfactual=counterfactual,
            plain_language_summary=plain_summary,
        )
    except Exception as e:
        logger.error(f"Error in predict_price: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/predict-selling-time", response_model=SellingTimePredictionResponse, tags=["Valuation"])
def predict_selling_time(car: CarInput):
    """Predict expected days-to-sale and market velocity indicators."""
    try:
        days, category, factors = selling_time_service.predict(car)
        return SellingTimePredictionResponse(
            expected_days_to_sale=days,
            velocity_category=category,
            market_factors=factors,
        )
    except Exception as e:
        logger.error(f"Error in predict_selling_time: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/recommendations", response_model=RecommendationsResponse, tags=["Recommendations"])
def get_recommendations(car: CarInput):
    """Return top 5 most comparable vehicles from inventory using K-Nearest Neighbors similarity."""
    try:
        sim_cars = recommender_service.get_recommendations(car, n_recommendations=5)
        return RecommendationsResponse(recommendations=sim_cars)
    except Exception as e:
        logger.error(f"Error in get_recommendations: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/fraud-check", response_model=FraudCheckResponse, tags=["Risk Analysis"])
def fraud_check(car: CarInput):
    """Evaluate pricing anomaly and fraud risk score using Isolation Forest & domain rules."""
    try:
        pred_price, _, _ = price_service.predict(car)
        result = fraud_detector_service.check_fraud(car, pred_price)
        return result
    except Exception as e:
        logger.error(f"Error in fraud_check: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/valuation-complete", response_model=ValuationCompleteResponse, tags=["Valuation"])
def valuation_complete(car: CarInput):
    """Execute complete full-suite valuation in a single fast call."""
    try:
        pred_price, conf_interval, model_name = price_service.predict(car)
        base_msrp = get_base_msrp(car.brand, car.model)
        days, category, _ = selling_time_service.predict(car)
        shap_contribs = explainability_service.get_shap_contributions(car, pred_price)
        lime_rules = explainability_service.get_lime_explanations(car)
        counterfactual = explainability_service.generate_counterfactual(car, pred_price)
        plain_summary = explainability_service.generate_plain_language_summary(car, pred_price, shap_contribs)
        sim_cars = recommender_service.get_recommendations(car, n_recommendations=5)
        fraud_result = fraud_detector_service.check_fraud(car, pred_price)

        return ValuationCompleteResponse(
            predicted_price=pred_price,
            confidence_interval=conf_interval,
            base_msrp=base_msrp,
            currency="₹",
            model_used=model_name,
            expected_days_to_sale=days,
            velocity_category=category,
            fraud_risk=fraud_result,
            shap_contributions=shap_contribs,
            lime_explanations=lime_rules,
            counterfactual=counterfactual,
            plain_language_summary=plain_summary,
            similar_cars=sim_cars,
        )
    except Exception as e:
        logger.error(f"Error in valuation_complete: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/photo-analysis/evaluate", response_model=PhotoConditionEvaluateResponse, tags=["Photo Analysis"])
def evaluate_photo_condition(req: PhotoConditionEvaluateRequest):
    """
    Evaluate photo condition rating, calculate bounded percentage equity delta,
    and enforce hard MSRP validation boundaries.
    """
    try:
        base_msrp = get_base_msrp(req.brand, req.model)

        # If base price not provided, compute from trained model
        if req.base_price is None or req.base_price <= 0:
            car_input = CarInput(
                brand=req.brand,
                model=req.model,
                year=req.year,
                mileage=req.mileage,
                fuel_type="Petrol",
                transmission="Automatic",
                owner_count=1,
                region="Metro",
            )
            base_price, conf_interval, _ = price_service.predict(car_input)
        else:
            base_price = req.base_price
            q05 = price_service.conformal_meta.get("q05_log_err", -0.35)
            q95 = price_service.conformal_meta.get("q95_log_err", 0.26)
            import numpy as np
            low_bound = round(max(30000.0, float(np.exp(np.log(base_price) + q05))), 2)
            high_bound = round(min(base_msrp, max(base_price * 1.05, float(np.exp(np.log(base_price) + q95)))), 2)
            conf_interval = [low_bound, high_bound]

        adj_pct, delta, final_price = calculate_bounded_condition_adjustment(
            base_price=base_price,
            condition_score=req.condition_score,
            base_msrp=base_msrp,
            max_positive_pct=0.08,
            max_negative_pct=0.15,
        )

        grade = (
            "Grade A+ (Pristine Condition)" if req.condition_score >= 90 else
            "Grade A (Excellent Condition)" if req.condition_score >= 80 else
            "Grade B (Normal Wear & Tear)" if req.condition_score >= 65 else
            "Grade C (Moderate Reconditioning Needed)"
        )

        capped_at_msrp = (base_price + (base_price * (req.condition_score - 80) / 20 * 0.08)) > base_msrp

        return PhotoConditionEvaluateResponse(
            brand=req.brand,
            model=req.model,
            condition_score=req.condition_score,
            grade=grade,
            base_fair_price=base_price,
            base_msrp=base_msrp,
            adjustment_percentage=adj_pct,
            condition_delta=delta,
            adjusted_price=final_price,
            capped_at_msrp=capped_at_msrp,
            confidence_interval=conf_interval,
        )
    except Exception as e:
        logger.error(f"Error in evaluate_photo_condition: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/market-analytics", response_model=MarketAnalyticsResponse, tags=["Market Analytics"])
def get_market_analytics():
    """Return aggregated market trends, regional price charts, brand metrics, and supply-demand indexes."""
    try:
        return market_analytics_service.get_analytics()
    except Exception as e:
        logger.error(f"Error in get_market_analytics: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/options", response_model=OptionsResponse, tags=["Metadata"])
def get_options():
    """Return available brands, models per brand, fuel types, transmissions, and regions for dynamic UI form controls."""
    try:
        return market_analytics_service.get_options()
    except Exception as e:
        logger.error(f"Error in get_options: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
