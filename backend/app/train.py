import json
import logging
import pickle
from pathlib import Path
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, IsolationForest
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBRegressor

from backend.app.config import MODELS_DIR, CLEANED_DATA_PATH
from backend.app.data_pipeline import load_or_create_dataset

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

CAT_FEATURES = ["brand", "model", "fuel_type", "transmission", "region"]
NUM_FEATURES = ["year", "vehicle_age", "mileage", "owner_count", "mileage_per_year", "is_luxury"]


def build_preprocessor() -> ColumnTransformer:
    """Build standardized column transformer for categorical and numerical features."""
    return ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CAT_FEATURES),
            ("num", StandardScaler(), NUM_FEATURES),
        ],
        remainder="drop",
    )


def train_price_models(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    preprocessor: ColumnTransformer,
) -> Tuple[Any, str, Dict[str, Any], Any, Any]:
    """Train Random Forest vs XGBoost, evaluate both, and train quantile models for prediction intervals."""
    logger.info("Fitting feature preprocessor...")
    X_train_trans = preprocessor.fit_transform(X_train)
    X_test_trans = preprocessor.transform(X_test)

    # 1. Random Forest
    logger.info("Training Random Forest Regressor...")
    rf = RandomForestRegressor(n_estimators=150, max_depth=18, min_samples_split=4, random_state=42, n_jobs=-1)
    rf.fit(X_train_trans, y_train)
    rf_pred = rf.predict(X_test_trans)
    rf_rmse = float(np.sqrt(mean_squared_error(y_test, rf_pred)))
    rf_mae = float(mean_absolute_error(y_test, rf_pred))
    rf_r2 = float(r2_score(y_test, rf_pred))

    # 2. XGBoost
    logger.info("Training XGBoost Regressor...")
    xgb = XGBRegressor(
        n_estimators=250,
        max_depth=6,
        learning_rate=0.07,
        subsample=0.85,
        colsample_bytree=0.85,
        random_state=42,
        n_jobs=-1,
    )
    xgb.fit(X_train_trans, y_train)
    xgb_pred = xgb.predict(X_test_trans)
    xgb_rmse = float(np.sqrt(mean_squared_error(y_test, xgb_pred)))
    xgb_mae = float(mean_absolute_error(y_test, xgb_pred))
    xgb_r2 = float(r2_score(y_test, xgb_pred))

    metrics = {
        "random_forest": {"rmse": round(rf_rmse, 2), "mae": round(rf_mae, 2), "r2": round(rf_r2, 4)},
        "xgboost": {"rmse": round(xgb_rmse, 2), "mae": round(xgb_mae, 2), "r2": round(xgb_r2, 4)},
    }
    logger.info(f"Price Model Comparison: {metrics}")

    if xgb_r2 >= rf_r2:
        best_model = xgb
        best_name = "XGBoost Regressor"
        logger.info(f"Selected XGBoost as best price model (R²: {xgb_r2:.4f})")
    else:
        best_model = rf
        best_name = "Random Forest Regressor"
        logger.info(f"Selected Random Forest as best price model (R²: {rf_r2:.4f})")

    # 3. Conformal Quantile Calibration for Confidence Intervals (5th and 95th percentiles)
    logger.info("Computing Conformal Residual Quantiles for 90% Confidence Intervals...")
    y_test_pred = best_model.predict(X_test_trans)
    log_residuals = np.log(np.maximum(y_test, 100.0)) - np.log(np.maximum(y_test_pred, 100.0))
    q05_err = float(np.percentile(log_residuals, 5))
    q95_err = float(np.percentile(log_residuals, 95))
    conformal_meta = {
        "q05_log_err": round(q05_err, 5),
        "q95_log_err": round(q95_err, 5),
        "target_coverage": 0.90,
        "empirical_coverage": round(float(((log_residuals >= q05_err) & (log_residuals <= q95_err)).mean()), 4),
    }
    logger.info(f"Conformal Quantiles: {conformal_meta}")

    return best_model, best_name, metrics, conformal_meta


def train_selling_time_model(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    preprocessor: ColumnTransformer,
) -> Tuple[Any, Dict[str, Any]]:
    """Train regression model predicting days to sale."""
    logger.info("Training Selling-Time Prediction Model...")
    X_train_trans = preprocessor.transform(X_train)
    X_test_trans = preprocessor.transform(X_test)

    model = XGBRegressor(
        n_estimators=180,
        max_depth=5,
        learning_rate=0.06,
        subsample=0.85,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train_trans, y_train)
    pred = model.predict(X_test_trans)

    rmse = float(np.sqrt(mean_squared_error(y_test, pred)))
    mae = float(mean_absolute_error(y_test, pred))
    r2 = float(r2_score(y_test, pred))

    metrics = {"rmse": round(rmse, 2), "mae": round(mae, 2), "r2": round(r2, 4)}
    logger.info(f"Selling Time Model Metrics: {metrics}")
    return model, metrics


def train_recommender(df: pd.DataFrame, preprocessor: ColumnTransformer) -> Tuple[NearestNeighbors, pd.DataFrame]:
    """Train Nearest-Neighbours recommender on the entire vehicle inventory."""
    logger.info("Fitting Nearest Neighbors Recommendation Engine...")
    X_all_trans = preprocessor.transform(df)
    knn = NearestNeighbors(n_neighbors=15, metric="cosine", algorithm="auto")
    knn.fit(X_all_trans)

    # Save a lean copy of inventory for recommendation retrieval
    inventory_lean = df[
        ["brand", "model", "year", "mileage", "fuel_type", "transmission", "owner_count", "region", "price"]
    ].copy().reset_index(drop=True)

    return knn, inventory_lean


def train_fraud_detector(df: pd.DataFrame, preprocessor: ColumnTransformer, price_model: Any) -> IsolationForest:
    """Train Isolation Forest anomaly detector on feature residuals and pricing characteristics."""
    logger.info("Training Isolation Forest Fraud & Anomaly Detector...")
    X_trans = preprocessor.transform(df)
    predicted_prices = price_model.predict(X_trans)
    actual_prices = df["price"].values

    price_ratio = np.clip(actual_prices / np.maximum(predicted_prices, 50000.0), 0.1, 5.0)
    abs_diff = np.abs(actual_prices - predicted_prices)

    # Feature space for anomaly detection: price ratio, absolute diff, vehicle age, mileage
    anomaly_features = np.column_stack([
        price_ratio,
        abs_diff,
        df["vehicle_age"].values,
        df["mileage"].values,
        df["is_luxury"].values,
    ])
    scaler = StandardScaler()
    anomaly_features_scaled = scaler.fit_transform(anomaly_features)

    iso_forest = IsolationForest(
        n_estimators=120,
        contamination=0.03,
        random_state=42,
        n_jobs=-1,
    )
    iso_forest.fit(anomaly_features_scaled)
    iso_forest.anomaly_scaler_ = scaler
    return iso_forest


def run_full_training():
    """Execute end-to-end model training pipeline and serialize all artifacts."""
    logger.info("Starting AutoPricer AI model training suite...")
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    df, eda = load_or_create_dataset()

    feature_cols = ["brand", "model", "year", "vehicle_age", "mileage", "fuel_type", "transmission", "owner_count", "region", "mileage_per_year", "is_luxury"]
    X = df[feature_cols].copy()
    y_price = df["price"].copy()
    y_days = df["days_to_sale"].copy()

    X_train, X_test, y_p_train, y_p_test, y_d_train, y_d_test = train_test_split(
        X, y_price, y_days, test_size=0.20, random_state=42
    )

    # 1. Price Model & Quantiles
    preprocessor = build_preprocessor()
    best_price_model, best_price_name, price_metrics, conformal_meta = train_price_models(
        X_train, X_test, y_p_train, y_p_test, preprocessor
    )

    # 2. Selling Time Model
    selling_model, selling_metrics = train_selling_time_model(
        X_train, X_test, y_d_train, y_d_test, preprocessor
    )

    # 3. Recommendation Engine
    knn_recommender, inventory_lean = train_recommender(df, preprocessor)

    # 4. Fraud Detector
    fraud_detector = train_fraud_detector(df, preprocessor, best_price_model)

    # Save artifacts
    logger.info(f"Persisting model artifacts to {MODELS_DIR}...")
    with open(MODELS_DIR / "price_model.pkl", "wb") as f:
        pickle.dump(best_price_model, f)

    with open(MODELS_DIR / "preprocessor.pkl", "wb") as f:
        pickle.dump(preprocessor, f)

    with open(MODELS_DIR / "conformal_quantiles.json", "w") as f:
        json.dump(conformal_meta, f, indent=2)

    with open(MODELS_DIR / "selling_time_model.pkl", "wb") as f:
        pickle.dump(selling_model, f)

    with open(MODELS_DIR / "recommender.pkl", "wb") as f:
        pickle.dump(knn_recommender, f)

    with open(MODELS_DIR / "inventory_data.pkl", "wb") as f:
        pickle.dump(inventory_lean, f)

    with open(MODELS_DIR / "fraud_detector.pkl", "wb") as f:
        pickle.dump(fraud_detector, f)

    all_metrics = {
        "best_price_model": best_price_name,
        "price_metrics": price_metrics,
        "selling_time_metrics": selling_metrics,
        "dataset_size": int(len(df)),
        "inventory_count": int(len(inventory_lean)),
    }

    with open(MODELS_DIR / "model_metrics.json", "w") as f:
        json.dump(all_metrics, f, indent=2)

    logger.info(f"Model training complete! Summary: {all_metrics}")
    return all_metrics


if __name__ == "__main__":
    metrics = run_full_training()
    print("\n================ TRAINING FINISHED SUCCESSFULLY ================")
    print(f"Best Price Model: {metrics['best_price_model']}")
    print(f"Price Metrics: {metrics['price_metrics']}")
    print(f"Selling Time Metrics: {metrics['selling_time_metrics']}")
    print("===============================================================\n")
