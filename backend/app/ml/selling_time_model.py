import logging
import pickle
from pathlib import Path
from typing import Dict, Any, Tuple, List
import numpy as np
import pandas as pd

from app.config import MODELS_DIR, CURRENT_YEAR
from app.schemas import CarInput

logger = logging.getLogger(__name__)

LUXURY_BRANDS = {
    "BMW", "Mercedes-Benz", "Mercedes", "Audi", "Porsche", "Tesla",
    "Jaguar", "Land Rover", "Lexus", "Volvo", "Mini"
}


class SellingTimeService:
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.load_models()

    def load_models(self):
        try:
            with open(MODELS_DIR / "selling_time_model.pkl", "rb") as f:
                self.model = pickle.load(f)
            with open(MODELS_DIR / "preprocessor.pkl", "rb") as f:
                self.preprocessor = pickle.load(f)
            logger.info("Selling time model loaded successfully.")
        except Exception as e:
            logger.warning(f"Selling time model not loaded yet: {e}")

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

    def predict(self, car: CarInput) -> Tuple[float, str, List[str]]:
        if self.model is None or self.preprocessor is None:
            self.load_models()

        df = self.prepare_dataframe(car)
        X_trans = self.preprocessor.transform(df)

        days = float(self.model.predict(X_trans)[0])
        days = max(5.0, min(days, 120.0))

        # Categorize velocity
        if days <= 25.0:
            category = "Fast Velocity"
        elif days <= 45.0:
            category = "Average Velocity"
        else:
            category = "Slow / Niche Velocity"

        factors = []
        age = CURRENT_YEAR - car.year
        if age <= 3:
            factors.append("Low vehicle age accelerates buyer interest.")
        elif age >= 8:
            factors.append("Older vehicle vintage slightly dampens daily inquiry volume.")

        if car.mileage < 40000:
            factors.append("Below-average mileage creates high buyer demand.")
        elif car.mileage > 90000:
            factors.append("High odometer reading requires competitive pricing for faster turnover.")

        if car.brand in ["Maruti Suzuki", "Hyundai", "Honda", "Toyota"]:
            factors.append("High-volume mass-market brand with broad buyer pool.")
        elif car.brand in LUXURY_BRANDS:
            factors.append("Luxury segment typically experiences longer negotiation and financing cycles.")

        if car.transmission == "Automatic":
            factors.append("Automatic transmission aligns with growing urban preference.")

        return round(days, 1), category, factors


selling_time_service = SellingTimeService()
