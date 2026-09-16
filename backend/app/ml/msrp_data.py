"""
MSRP (Manufacturer's Suggested Retail Price) reference dictionary and valuation boundary
utilities for all automotive brands and models in the platform.
Used for hard boundary capping and photo-condition valuation calibration.
"""
import logging
from typing import Dict, Any, Tuple

logger = logging.getLogger("autopricer-msrp")

BRAND_MODELS_MSRP: Dict[str, Dict[str, float]] = {
    "Audi": {
        "A4": 4534000.0,
        "A6": 6410000.0,
        "A8": 13400000.0,
        "Q7": 8690000.0,
        "DEFAULT": 5500000.0,
    },
    "BMW": {
        "3": 5500000.0,
        "5": 6800000.0,
        "6": 7500000.0,
        "7": 17000000.0,
        "X1": 4900000.0,
        "X3": 6850000.0,
        "X4": 7400000.0,
        "X5": 10500000.0,
        "Z4": 8900000.0,
        "DEFAULT": 6000000.0,
    },
    "Bentley": {
        "Continental": 38000000.0,
        "DEFAULT": 38000000.0,
    },
    "Datsun": {
        "GO": 450000.0,
        "RediGO": 398000.0,
        "redi-GO": 398000.0,
        "DEFAULT": 420000.0,
    },
    "Ferrari": {
        "GTC4Lusso": 42000000.0,
        "DEFAULT": 42000000.0,
    },
    "Force": {
        "Gurkha": 1550000.0,
        "DEFAULT": 1550000.0,
    },
    "Ford": {
        "Aspire": 800000.0,
        "Ecosport": 1050000.0,
        "Endeavour": 3400000.0,
        "Figo": 720000.0,
        "Freestyle": 750000.0,
        "DEFAULT": 1000000.0,
    },
    "Honda": {
        "Amaze": 850000.0,
        "CR": 3000000.0,
        "CR-V": 3000000.0,
        "City": 1450000.0,
        "Civic": 2050000.0,
        "Jazz": 920000.0,
        "WR-V": 1050000.0,
        "DEFAULT": 1200000.0,
    },
    "Hyundai": {
        "Aura": 780000.0,
        "Creta": 1600000.0,
        "Elantra": 1950000.0,
        "Grand": 720000.0,
        "Santro": 550000.0,
        "Tucson": 3250000.0,
        "Venue": 1050000.0,
        "Verna": 1450000.0,
        "i10": 720000.0,
        "i20": 920000.0,
        "DEFAULT": 1100000.0,
    },
    "ISUZU": {
        "MUX": 3500000.0,
        "DEFAULT": 3500000.0,
    },
    "Isuzu": {
        "D-Max": 2100000.0,
        "MUX": 3500000.0,
        "DEFAULT": 2800000.0,
    },
    "Jaguar": {
        "F-PACE": 7800000.0,
        "XE": 4900000.0,
        "XF": 7400000.0,
        "DEFAULT": 7000000.0,
    },
    "Jeep": {
        "Compass": 2650000.0,
        "Wrangler": 6450000.0,
        "DEFAULT": 2800000.0,
    },
    "Kia": {
        "Carnival": 3350000.0,
        "Seltos": 1600000.0,
        "DEFAULT": 1600000.0,
    },
    "Land Rover": {
        "Rover": 8500000.0,
        "DEFAULT": 8500000.0,
    },
    "Lexus": {
        "ES": 6500000.0,
        "NX": 6750000.0,
        "RX": 9500000.0,
        "DEFAULT": 7500000.0,
    },
    "MG": {
        "Hector": 1900000.0,
        "DEFAULT": 1900000.0,
    },
    "Mahindra": {
        "Alturas": 3100000.0,
        "Bolero": 1020000.0,
        "KUV": 700000.0,
        "KUV100": 700000.0,
        "Marazzo": 1400000.0,
        "Scorpio": 1800000.0,
        "Thar": 1500000.0,
        "XUV300": 1150000.0,
        "XUV500": 2000000.0,
        "DEFAULT": 1400000.0,
    },
    "Maruti Suzuki": {
        "Alto": 480000.0,
        "Baleno": 850000.0,
        "Celerio": 650000.0,
        "Ciaz": 1100000.0,
        "Dzire LXI": 750000.0,
        "Dzire VXI": 820000.0,
        "Dzire ZXI": 920000.0,
        "Eeco": 550000.0,
        "Ertiga": 1100000.0,
        "Ignis": 680000.0,
        "S-Presso": 520000.0,
        "Swift": 800000.0,
        "Swift Dzire": 820000.0,
        "Vitara": 1150000.0,
        "Wagon R": 650000.0,
        "XL6": 1250000.0,
        "DEFAULT": 750000.0,
    },
    "Maserati": {
        "Ghibli": 12000000.0,
        "Quattroporte": 18000000.0,
        "DEFAULT": 15000000.0,
    },
    "Mercedes-AMG": {
        "C": 9000000.0,
        "DEFAULT": 9000000.0,
    },
    "Mercedes-Benz": {
        "C-Class": 6200000.0,
        "CLS": 8600000.0,
        "E-Class": 8000000.0,
        "GL-Class": 7400000.0,
        "GLS": 13500000.0,
        "S-Class": 18000000.0,
        "DEFAULT": 7500000.0,
    },
    "Mini": {
        "Cooper": 4200000.0,
        "DEFAULT": 4200000.0,
    },
    "Nissan": {
        "Kicks": 1150000.0,
        "X-Trail": 3500000.0,
        "DEFAULT": 1400000.0,
    },
    "Porsche": {
        "Cayenne": 16000000.0,
        "Macan": 11000000.0,
        "Panamera": 21000000.0,
        "DEFAULT": 14000000.0,
    },
    "Renault": {
        "Duster": 1200000.0,
        "KWID": 550000.0,
        "Triber": 750000.0,
        "DEFAULT": 750000.0,
    },
    "Rolls-Royce": {
        "Ghost": 75000000.0,
        "DEFAULT": 75000000.0,
    },
    "Skoda": {
        "Octavia": 2900000.0,
        "Rapid": 1100000.0,
        "Superb": 3500000.0,
        "DEFAULT": 1800000.0,
    },
    "Tata": {
        "Altroz": 850000.0,
        "Harrier": 2100000.0,
        "Hexa": 1700000.0,
        "Nexon": 1200000.0,
        "Safari": 2250000.0,
        "Tiago": 720000.0,
        "Tigor": 800000.0,
        "DEFAULT": 1200000.0,
    },
    "Toyota": {
        "Camry": 4617000.0,
        "Fortuner": 4200000.0,
        "Glanza": 850000.0,
        "Innova": 2450000.0,
        "Yaris": 1350000.0,
        "DEFAULT": 2500000.0,
    },
    "Volkswagen": {
        "Polo": 850000.0,
        "Vento": 1250000.0,
        "DEFAULT": 1200000.0,
    },
    "Volvo": {
        "S90": 6850000.0,
        "XC": 6500000.0,
        "XC60": 6900000.0,
        "XC90": 9900000.0,
        "DEFAULT": 6500000.0,
    },
}

GLOBAL_FALLBACK_MSRP = 1200000.0


def get_base_msrp(brand: str, model: str) -> float:
    """
    Retrieve authentic Indian market MSRP (New Vehicle Ex-Showroom Price) in INR for brand & model.
    """
    brand_dict = BRAND_MODELS_MSRP.get(brand)
    if not brand_dict:
        # Case-insensitive search
        for b, models in BRAND_MODELS_MSRP.items():
            if b.lower() == str(brand).lower():
                brand_dict = models
                break

    if not brand_dict:
        return GLOBAL_FALLBACK_MSRP

    if model in brand_dict:
        return brand_dict[model]

    # Partial model search
    for m, msrp in brand_dict.items():
        if m.lower() in str(model).lower() or str(model).lower() in m.lower():
            return msrp

    return brand_dict.get("DEFAULT", GLOBAL_FALLBACK_MSRP)


def calculate_bounded_condition_adjustment(
    base_price: float,
    condition_score: float,
    base_msrp: float,
    max_positive_pct: float = 0.08,
    max_negative_pct: float = 0.15,
) -> Tuple[float, float, float]:
    """
    Calculate bounded percentage adjustment from vehicle photo condition score.
    Baseline score = 80 (Standard good used condition).
    A score of 95 (Pristine A+) grants up to ~+4.5% to +6%.
    A score of 60 (Wear C) adjusts down by ~-6.7%.
    
    Returns:
        (adjustment_percentage, delta_in_inr, final_capped_price)
    """
    baseline_score = 80.0
    score_diff = condition_score - baseline_score

    if score_diff >= 0:
        # Scale smoothly between 0 and max_positive_pct
        pct = (score_diff / (100.0 - baseline_score)) * max_positive_pct
        pct = min(pct, max_positive_pct)
    else:
        # Scale smoothly between 0 and -max_negative_pct
        pct = (score_diff / baseline_score) * max_negative_pct
        pct = max(pct, -max_negative_pct)

    raw_delta = round(base_price * pct, 2)
    tentative_price = round(base_price + raw_delta, 2)

    # Hard Validation: Used car valuation MUST NEVER exceed base MSRP
    if tentative_price > base_msrp:
        logger.warning(
            f"Cap Violation Detected: Tentative photo-adjusted price ₹{tentative_price:,.2f} "
            f"exceeded new vehicle base MSRP ₹{base_msrp:,.2f}. Capping price to 95% of MSRP."
        )
        final_price = round(base_msrp * 0.95, 2)
        adjusted_delta = round(final_price - base_price, 2)
        adjusted_pct = (adjusted_delta / base_price) if base_price > 0 else 0.0
        return round(adjusted_pct * 100, 2), adjusted_delta, final_price

    return round(pct * 100, 2), raw_delta, tentative_price
