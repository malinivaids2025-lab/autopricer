from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class CarInput(BaseModel):
    brand: str = Field(..., json_schema_extra={"example": "Toyota"})
    model: str = Field(..., json_schema_extra={"example": "Camry"})
    year: int = Field(..., ge=1990, le=2026, json_schema_extra={"example": 2020})
    mileage: float = Field(..., ge=0, json_schema_extra={"example": 18000})
    fuel_type: str = Field(..., json_schema_extra={"example": "Petrol"})
    transmission: str = Field(..., json_schema_extra={"example": "Automatic"})
    owner_count: int = Field(1, ge=1, le=5, json_schema_extra={"example": 1})
    region: Optional[str] = Field("Metro", json_schema_extra={"example": "Metro"})
    price: Optional[float] = Field(None, description="Actual listing price if doing a fraud/anomaly check", json_schema_extra={"example": 1850000})


class PricePredictionResponse(BaseModel):
    predicted_price: float
    confidence_interval: List[float] = Field(..., description="[lower_bound, upper_bound] at 90% confidence")
    base_msrp: Optional[float] = Field(None, description="Official original new vehicle base MSRP in INR")
    currency: str = "₹"
    model_used: str
    shap_contributions: List[Dict[str, Any]]
    lime_explanations: Optional[List[Dict[str, Any]]] = None
    counterfactual: Dict[str, Any]
    plain_language_summary: str


class SellingTimePredictionResponse(BaseModel):
    expected_days_to_sale: float
    velocity_category: str = Field(..., description="Fast (0-25d), Average (26-45d), Slow (46+ d)")
    market_factors: List[str]


class SimilarCar(BaseModel):
    brand: str
    model: str
    year: int
    mileage: float
    fuel_type: str
    transmission: str
    price: float
    region: str
    similarity_score: float = Field(..., description="Match percentage 0-100%")


class RecommendationsResponse(BaseModel):
    recommendations: List[SimilarCar]


class FraudCheckResponse(BaseModel):
    fraud_risk_score: float = Field(..., ge=0, le=100, description="Risk score from 0 (Safe) to 100 (High Risk)")
    risk_level: str = Field(..., description="Low Risk, Medium Risk, High Risk")
    is_anomaly: bool
    price_deviation_percentage: float
    reasons: List[str]


class ValuationCompleteResponse(BaseModel):
    predicted_price: float
    confidence_interval: List[float]
    base_msrp: Optional[float] = None
    currency: str = "₹"
    model_used: str
    expected_days_to_sale: float
    velocity_category: str
    fraud_risk: FraudCheckResponse
    shap_contributions: List[Dict[str, Any]]
    lime_explanations: Optional[List[Dict[str, Any]]]
    counterfactual: Dict[str, Any]
    plain_language_summary: str
    similar_cars: List[SimilarCar]


class PhotoConditionEvaluateRequest(BaseModel):
    brand: str
    model: str
    year: int
    mileage: float
    condition_score: float = Field(..., ge=0, le=100, description="Vehicle condition rating from 0 to 100")
    base_price: Optional[float] = None


class PhotoConditionEvaluateResponse(BaseModel):
    brand: str
    model: str
    condition_score: float
    grade: str
    base_fair_price: float
    base_msrp: float
    adjustment_percentage: float
    condition_delta: float
    adjusted_price: float
    capped_at_msrp: bool
    confidence_interval: List[float]


class MarketAnalyticsResponse(BaseModel):
    total_listings: int
    average_price: float
    median_price: float
    average_days_to_sale: float
    brand_summary: List[Dict[str, Any]]
    region_summary: List[Dict[str, Any]]
    year_trend: List[Dict[str, Any]]
    fuel_breakdown: List[Dict[str, Any]]
    transmission_breakdown: List[Dict[str, Any]]
    supply_demand_trend: List[Dict[str, Any]]


class OptionsResponse(BaseModel):
    brands: List[str]
    brand_models: Dict[str, List[str]]
    brand_msrp: Optional[Dict[str, Dict[str, float]]] = None
    fuel_types: List[str]
    transmissions: List[str]
    regions: List[str]
    min_year: int
    max_year: int
