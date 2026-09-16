import logging
import pickle
from pathlib import Path
from typing import Dict, Any, Tuple, List
import numpy as np
import pandas as pd

from backend.app.config import MODELS_DIR, CURRENT_YEAR
from backend.app.schemas import CarInput
from backend.app.ml.msrp_data import get_base_msrp

logger = logging.getLogger(__name__)

LUXURY_BRANDS = {
    "BMW", "Mercedes-Benz", "Mercedes", "Audi", "Porsche", "Tesla",
    "Jaguar", "Land Rover", "Lexus", "Volvo", "Mini"
}


class PriceModelService:
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.conformal_meta = {"q05_log_err": -0.22, "q95_log_err": 0.24}
        self.metrics = {}
        self.load_models()

    def load_models(self):
        try:
            with open(MODELS_DIR / "price_model.pkl", "rb") as f:
                self.model = pickle.load(f)
            with open(MODELS_DIR / "preprocessor.pkl", "rb") as f:
                self.preprocessor = pickle.load(f)
            if (MODELS_DIR / "conformal_quantiles.json").exists():
                with open(MODELS_DIR / "conformal_quantiles.json", "r") as f:
                    import json
                    self.conformal_meta = json.load(f)
            logger.info("Price models and conformal intervals loaded successfully.")
        except Exception as e:
            logger.warning(f"Price models not loaded yet: {e}")

    def prepare_dataframe(self, car: CarInput) -> pd.DataFrame:
        vehicle_age = max(CURRENT_YEAR - car.year, 0)
        mileage_per_year = car.mileage / max(vehicle_age, 1.0)
        is_luxury = 1 if car.brand in LUXURY_BRANDS else 0

        df = pd.DataFrame([{
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
        return df

    def predict(self, car: CarInput) -> Tuple[float, List[float], str]:
        if self.model is None or self.preprocessor is None:
            self.load_models()

        df = self.prepare_dataframe(car)
        X_trans = self.preprocessor.transform(df)

        pred_price = float(self.model.predict(X_trans)[0])
        pred_price = max(pred_price, 35000.0)

        # Hard validation: A used car valuation must never exceed brand new vehicle MSRP
        base_msrp = get_base_msrp(car.brand, car.model)
        if pred_price > base_msrp:
            logger.warning(
                f"Cap Violation: Raw model prediction ₹{pred_price:,.2f} for used {car.year} {car.brand} {car.model} "
                f"exceeded new vehicle base MSRP ₹{base_msrp:,.2f}. Capping price to 95% of MSRP."
            )
            pred_price = round(base_msrp * 0.95, 2)

        # Calibrated conformal residual quantile bounds (90% coverage)
        q05 = self.conformal_meta.get("q05_log_err", -0.35)
        q95 = self.conformal_meta.get("q95_log_err", 0.26)

        low_bound = float(np.exp(np.log(pred_price) + q05))
        high_bound = float(np.exp(np.log(pred_price) + q95))

        low_bound = round(max(30000.0, low_bound), 2)
        high_bound = round(min(base_msrp, max(pred_price * 1.05, high_bound)), 2)

        model_name = "XGBoost Regressor (Conformal 90% Calibrated Interval)"
        return round(pred_price, 2), [low_bound, high_bound], model_name


price_service = PriceModelService()
