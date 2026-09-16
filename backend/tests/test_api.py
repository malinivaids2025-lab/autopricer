import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

SAMPLE_CAR = {
    "brand": "Honda",
    "model": "City",
    "year": 2019,
    "mileage": 42000,
    "fuel_type": "Petrol",
    "transmission": "Manual",
    "owner_count": 1,
    "region": "Metro",
    "price": 680000.0,
}

CAMRY_CAR = {
    "brand": "Toyota",
    "model": "Camry",
    "year": 2020,
    "mileage": 18000,
    "fuel_type": "Petrol",
    "transmission": "Automatic",
    "owner_count": 1,
    "region": "Metro",
}


def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["models_ready"]["price_model"] is True
    assert data["models_ready"]["selling_time_model"] is True
    assert data["models_ready"]["recommender"] is True


def test_predict_price():
    response = client.post("/api/predict-price", json=SAMPLE_CAR)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_price" in data
    assert data["predicted_price"] > 0
    assert "base_msrp" in data
    assert data["predicted_price"] <= data["base_msrp"]
    assert len(data["confidence_interval"]) == 2
    assert data["confidence_interval"][0] <= data["predicted_price"] <= data["confidence_interval"][1]
    assert len(data["shap_contributions"]) > 0
    assert "counterfactual" in data
    assert "plain_language_summary" in data


def test_camry_msrp_capping_and_ordering():
    # 2020 Toyota Camry
    val_res = client.post("/api/valuation-complete", json=CAMRY_CAR)
    assert val_res.status_code == 200
    val_data = val_res.json()

    base_price = val_data["predicted_price"]
    conf_interval = val_data["confidence_interval"]
    base_msrp = val_data["base_msrp"]

    assert base_msrp >= 4000000.0  # Camry MSRP is ~46.17 Lakhs
    assert base_price < base_msrp
    assert conf_interval[1] <= base_msrp

    # Test Photo Analysis Evaluation with 95 condition score
    photo_payload = {
        "brand": "Toyota",
        "model": "Camry",
        "year": 2020,
        "mileage": 18000,
        "condition_score": 95.0,
        "base_price": base_price,
    }
    photo_res = client.post("/api/photo-analysis/evaluate", json=photo_payload)
    assert photo_res.status_code == 200
    photo_data = photo_res.json()

    photo_adjusted_price = photo_data["adjusted_price"]

    # Strict ordering requirement:
    # photo_adjusted_price <= upper confidence interval bound <= base_msrp
    assert photo_adjusted_price <= conf_interval[1] <= base_msrp
    assert photo_adjusted_price > base_price  # condition 95 grants positive bonus


def test_predict_selling_time():
    response = client.post("/api/predict-selling-time", json=SAMPLE_CAR)
    assert response.status_code == 200
    data = response.json()
    assert "expected_days_to_sale" in data
    assert 0 < data["expected_days_to_sale"] < 150
    assert "velocity_category" in data
    assert isinstance(data["market_factors"], list)


def test_recommendations():
    response = client.post("/api/recommendations", json=SAMPLE_CAR)
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert len(data["recommendations"]) == 5
    for car in data["recommendations"]:
        assert "brand" in car
        assert "model" in car
        assert "similarity_score" in car
        assert 0 <= car["similarity_score"] <= 100


def test_fraud_check_normal():
    response = client.post("/api/fraud-check", json=SAMPLE_CAR)
    assert response.status_code == 200
    data = response.json()
    assert "fraud_risk_score" in data
    assert "risk_level" in data
    assert "is_anomaly" in data


def test_fraud_check_anomaly():
    scam_car = {
        "brand": "BMW",
        "model": "3 Series",
        "year": 2023,
        "mileage": 5000,
        "fuel_type": "Petrol",
        "transmission": "Automatic",
        "owner_count": 1,
        "region": "Metro",
        "price": 50000.0,
    }
    response = client.post("/api/fraud-check", json=scam_car)
    assert response.status_code == 200
    data = response.json()
    assert data["fraud_risk_score"] >= 35.0
    assert data["risk_level"] in ["Medium Risk", "High Risk"]
    assert len(data["reasons"]) > 0


def test_valuation_complete():
    response = client.post("/api/valuation-complete", json=SAMPLE_CAR)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_price" in data
    assert "confidence_interval" in data
    assert "base_msrp" in data
    assert "expected_days_to_sale" in data
    assert "fraud_risk" in data
    assert "shap_contributions" in data
    assert "similar_cars" in data
    assert len(data["similar_cars"]) == 5


def test_market_analytics():
    response = client.get("/api/market-analytics")
    assert response.status_code == 200
    data = response.json()
    assert data["total_listings"] > 0
    assert len(data["brand_summary"]) > 0
    assert len(data["region_summary"]) > 0
    assert len(data["year_trend"]) > 0
    assert len(data["fuel_breakdown"]) > 0
    assert len(data["supply_demand_trend"]) > 0


def test_options():
    response = client.get("/api/options")
    assert response.status_code == 200
    data = response.json()
    assert len(data["brands"]) > 0
    assert len(data["fuel_types"]) > 0
    assert len(data["transmissions"]) > 0
    assert len(data["regions"]) > 0
    assert "brand_msrp" in data


def test_cors_headers():
    for origin in ["http://localhost:5173", "http://127.0.0.1:5173"]:
        response = client.get("/api/health", headers={"Origin": origin})
        assert response.status_code == 200
        assert response.headers.get("access-control-allow-origin") == origin
        assert response.headers.get("access-control-allow-credentials") == "true"
