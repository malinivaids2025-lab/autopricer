import logging
import pickle
from typing import List
import numpy as np
import pandas as pd

from app.config import MODELS_DIR, CURRENT_YEAR
from app.schemas import CarInput, SimilarCar

logger = logging.getLogger(__name__)

LUXURY_BRANDS = {
    "BMW", "Mercedes-Benz", "Mercedes", "Audi", "Porsche", "Tesla",
    "Jaguar", "Land Rover", "Lexus", "Volvo", "Mini"
}


class RecommenderService:
    def __init__(self):
        self.knn = None
        self.inventory = None
        self.preprocessor = None
        self.load_models()

    def load_models(self):
        try:
            with open(MODELS_DIR / "recommender.pkl", "rb") as f:
                self.knn = pickle.load(f)
            with open(MODELS_DIR / "inventory_data.pkl", "rb") as f:
                self.inventory = pickle.load(f)
            with open(MODELS_DIR / "preprocessor.pkl", "rb") as f:
                self.preprocessor = pickle.load(f)
            logger.info("Recommendation engine loaded successfully.")
        except Exception as e:
            logger.warning(f"Recommender models not loaded yet: {e}")

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

    def get_recommendations(self, car: CarInput, n_recommendations: int = 5) -> List[SimilarCar]:
        if self.knn is None or self.inventory is None:
            self.load_models()

        df = self.prepare_df(car)
        X_trans = self.preprocessor.transform(df)

        # Query KNN
        distances, indices = self.knn.kneighbors(X_trans, n_neighbors=min(n_recommendations + 5, len(self.inventory)))

        recommended_cars: List[SimilarCar] = []
        seen_combos = set()

        for dist, idx in zip(distances[0], indices[0]):
            row = self.inventory.iloc[idx]
            combo_key = (row["brand"], row["model"], int(row["year"]), int(row["mileage"]))

            # Avoid exact identical duplicate listings if possible
            if combo_key in seen_combos and len(recommended_cars) > 0:
                continue
            seen_combos.add(combo_key)

            # Cosine distance to similarity percentage
            # Cosine distance is 1 - cosine_similarity (range 0 to 2)
            similarity = max(50.0, min(99.4, (1.0 - (dist / 2.0)) * 100.0))

            # Bonus if exact brand matches
            if row["brand"].lower() == car.brand.lower():
                similarity = min(99.8, similarity + 2.5)

            recommended_cars.append(SimilarCar(
                brand=str(row["brand"]),
                model=str(row["model"]),
                year=int(row["year"]),
                mileage=float(row["mileage"]),
                fuel_type=str(row["fuel_type"]),
                transmission=str(row["transmission"]),
                price=float(row["price"]),
                region=str(row.get("region", "Metro")),
                similarity_score=round(float(similarity), 1),
            ))

            if len(recommended_cars) >= n_recommendations:
                break

        return recommended_cars


recommender_service = RecommenderService()
