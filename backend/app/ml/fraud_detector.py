import logging
import pickle
from typing import Tuple, List, Optional
import numpy as np
import pandas as pd

from backend.app.config import MODELS_DIR, CURRENT_YEAR
from backend.app.schemas import CarInput, FraudCheckResponse

logger = logging.getLogger(__name__)

LUXURY_BRANDS = {
    "BMW", "Mercedes-Benz", "Mercedes", "Audi", "Porsche", "Tesla",
    "Jaguar", "Land Rover", "Lexus", "Volvo", "Mini"
}


class FraudDetectorService:
    def __init__(self):
        self.iso_forest = None
        self.preprocessor = None
        self.price_model = None
        self.load_models()

    def load_models(self):
        try:
            with open(MODELS_DIR / "fraud_detector.pkl", "rb") as f:
                self.iso_forest = pickle.load(f)
            with open(MODELS_DIR / "preprocessor.pkl", "rb") as f:
                self.preprocessor = pickle.load(f)
            with open(MODELS_DIR / "price_model.pkl", "rb") as f:
                self.price_model = pickle.load(f)
            logger.info("Fraud detection model loaded successfully.")
        except Exception as e:
            logger.warning(f"Fraud detector model not loaded yet: {e}")

    def prepare_df(self, car: CarInput) -> pd.DataFrame:
        vehicle_age = max(CURRENT_YEAR - car.year, 0)
        mileage_per_year = car.mileage / max(vehicle_age, 1.0)
        is_luxury = 1 if car.brand in LUXURY_BRANDS else 0

        return pd.DataFrame([{
            "brand": car.brand,
            "model": car.model,
            "year": car.year,
            "vehicle_age": vehicle_age,
            "mileage": car.mileage,
            "fuel_type": car.fuel_type,
            "transmission": car.transmission,
            "owner_count": car.owner_count,
            "region": car.region or "Metro",
            "mileage_per_year": mileage_per_year,
            "is_luxury": is_luxury,
        }])

    def check_fraud(self, car: CarInput, pred_price: Optional[float] = None) -> FraudCheckResponse:
        if self.iso_forest is None or self.price_model is None:
            self.load_models()

        df = self.prepare_df(car)
        X_trans = self.preprocessor.transform(df)

        if pred_price is None:
            pred_price = float(self.price_model.predict(X_trans)[0])

        actual_price = car.price if (car.price is not None and car.price > 0) else pred_price
        diff_pct = ((actual_price - pred_price) / max(pred_price, 1000.0)) * 100.0
        abs_diff_pct = abs(diff_pct)

        reasons: List[str] = []
        risk_score = 10.0  # Baseline low risk

        # 1. Compute Raw Machine Learning Isolation Forest Score
        iso_score = 0.0
        is_anomaly = False
        try:
            price_ratio = np.clip(actual_price / max(pred_price, 100.0), 0.1, 5.0)
            abs_diff = abs(actual_price - pred_price)
            anomaly_feat = np.array([[
                price_ratio,
                abs_diff,
                float(df["vehicle_age"].values[0]),
                float(df["mileage"].values[0]),
                float(df["is_luxury"].values[0]),
            ]])
            if hasattr(self.iso_forest, "anomaly_scaler_"):
                anomaly_feat = self.iso_forest.anomaly_scaler_.transform(anomaly_feat)

            # decision_function: positive = inlier, negative = anomaly/outlier
            raw_decision = float(self.iso_forest.decision_function(anomaly_feat)[0])
            iso_pred = int(self.iso_forest.predict(anomaly_feat)[0])
            is_anomaly = (iso_pred == -1)

            # Continuous model score using logistic transformation of decision_function
            model_risk_prob = 1.0 / (1.0 + np.exp(10.0 * raw_decision))
            risk_score = model_risk_prob * 100.0
        except Exception as e:
            logger.warning(f"Isolation Forest inference fallback: {e}")
            risk_score = 15.0

        # 2. Diagnostic reason formulation (domain context for user explainability)
        if diff_pct < -45.0:
            reasons.append(
                f"Listing is priced {abs(diff_pct):.1f}% below fair market valuation (₹{pred_price:,.0f}). "
                "Severe warning for salvage title, flood damage, or fraudulent escrow deposit listing."
            )
        elif diff_pct < -20.0:
            reasons.append(
                f"Listing is priced {abs(diff_pct):.1f}% below estimated market average. "
                "Verify vehicle service history and registration documents."
            )
        elif diff_pct > 50.0:
            reasons.append(
                f"Listing price is {diff_pct:.1f}% above segment benchmarks. "
                "Significant risk of inflated dealership markups or erroneous listing metadata."
            )
        elif diff_pct > 25.0:
            reasons.append(f"Priced {diff_pct:.1f}% above fair value; buyer negotiation strongly advised.")

        age = CURRENT_YEAR - car.year
        if age >= 8 and car.mileage < 10000:
            reasons.append(
                f"Unusually low odometer ({car.mileage:,.0f} km) for a {age}-year-old vehicle. Potential odometer rollback risk."
            )
        elif age <= 2 and car.mileage > 120000:
            reasons.append("Extremely high commercial / fleet mileage for vehicle age.")

        if age <= 1 and car.owner_count >= 3:
            reasons.append(f"Multiple owners ({car.owner_count}) within first year of registration indicates potential lemon or recurring mechanical defect.")

        # Final calibrated score bounds and classification
        risk_score = float(np.clip(risk_score, 5.0, 99.0))

        if risk_score >= 60.0 or is_anomaly:
            risk_level = "High Risk" if risk_score >= 70.0 else "Medium Risk"
            is_anomaly = True
        elif risk_score >= 35.0:
            risk_level = "Medium Risk"
        else:
            risk_level = "Low Risk"
            is_anomaly = False
            if not reasons:
                reasons.append("Listing parameters, odometer, and pricing conform to normal market parameters.")

        return FraudCheckResponse(
            fraud_risk_score=round(risk_score, 1),
            risk_level=risk_level,
            is_anomaly=is_anomaly,
            price_deviation_percentage=round(diff_pct, 1),
            reasons=reasons,
        )


fraud_detector_service = FraudDetectorService()
