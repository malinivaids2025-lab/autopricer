import json
import logging
import re
from pathlib import Path
from typing import Dict, Any, Tuple, Optional
import numpy as np
import pandas as pd

from backend.app.config import (
    DATA_DIR,
    RAW_DATA_PATH,
    CLEANED_DATA_PATH,
    EDA_SUMMARY_PATH,
    CURRENT_YEAR,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

LUXURY_BRANDS = {
    "BMW", "Mercedes-Benz", "Mercedes", "Audi", "Porsche", "Tesla",
    "Jaguar", "Land Rover", "Lexus", "Volvo", "Mini", "Bentley", "Ferrari", "Maserati", "Rolls-Royce"
}

REGIONS = ["Metro", "North", "South", "East", "West", "Central"]

COLUMN_MAP_RULES = {
    "brand": ["brand", "make", "manufacturer", "company"],
    "model": ["model", "car_model", "vehicle_model", "trim"],
    "car_name": ["car_name", "name", "vehicle_name"],
    "year": ["year", "model_year", "manufacture_year", "yr"],
    "vehicle_age": ["vehicle_age", "age", "car_age"],
    "mileage": ["km_driven", "kms_driven", "mileage", "odometer", "miles", "distance"],
    "fuel_type": ["fuel_type", "fuel", "engine_fuel"],
    "transmission": ["transmission_type", "transmission", "gearbox", "trans"],
    "owner_count": ["owner", "owner_count", "owners", "previous_owners", "num_owners", "condition"],
    "seller_type": ["seller_type", "seller", "dealer_type"],
    "region": ["region", "location", "city", "state", "zone"],
    "price": ["selling_price", "price", "cost", "target_price", "amount"],
    "listing_date": ["listing_date", "posted_date", "date", "created_at"],
    "days_to_sale": ["days_to_sale", "days_on_market", "selling_days", "time_to_sell"],
    "present_price": ["present_price", "msrp", "new_price", "original_price"],
}


def parse_numeric_str(val: Any) -> Optional[float]:
    """Parse numeric values from formatted strings like '₹15,98,000', '$15,988', '41,406 miles', '19.7 kmpl'."""
    if pd.isna(val):
        return None
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).replace(",", "").replace("$", "").replace("₹", "").replace("Rs.", "").replace("Rs", "").strip()
    match = re.search(r"[-+]?\d*\.?\d+", s)
    if match:
        try:
            return float(match.group(0))
        except ValueError:
            return None
    return None


def parse_owner_count(val: Any, age: float = 3.0) -> int:
    """Parse owner count from various string or numeric formats."""
    if pd.isna(val):
        return 1 if age <= 3 else (2 if age <= 7 else 3)
    if isinstance(val, (int, float)):
        return int(np.clip(val, 1, 4))
    s = str(val).lower()
    if "1" in s or "first" in s or "one" in s:
        return 1
    elif "2" in s or "second" in s or "two" in s:
        return 2
    elif "3" in s or "third" in s or "three" in s:
        return 3
    elif "4" in s or "fourth" in s or "fourth & above" in s or "4+" in s:
        return 4
    return 1 if age <= 3 else (2 if age <= 7 else 3)


def auto_detect_and_map_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Intelligently detect and standardize all incoming columns from various dataset formats."""
    lower_col_map = {col.lower().strip().replace(" ", "_"): col for col in df.columns}
    matched_cols: Dict[str, str] = {}

    for standard_name, aliases in COLUMN_MAP_RULES.items():
        for alias in aliases:
            if alias in lower_col_map:
                matched_cols[standard_name] = lower_col_map[alias]
                break

    mapped_df = pd.DataFrame()

    # 1. Car Name, Brand & Model extraction
    if "brand" in matched_cols and "model" in matched_cols:
        mapped_df["brand"] = df[matched_cols["brand"]].astype(str).str.strip()
        mapped_df["model"] = df[matched_cols["model"]].astype(str).str.strip()
    elif "car_name" in matched_cols:
        names = df[matched_cols["car_name"]].astype(str).str.strip()
        split_names = names.str.split(" ", n=1, expand=True)
        mapped_df["brand"] = split_names[0]
        mapped_df["model"] = split_names[1].fillna(split_names[0])
    elif "brand" in matched_cols:
        mapped_df["brand"] = df[matched_cols["brand"]].astype(str).str.strip()
        mapped_df["model"] = mapped_df["brand"]
    else:
        mapped_df["brand"] = "Generic"
        mapped_df["model"] = "Sedan"

    # Clean brand names (capitalize, fix common typos/variations)
    mapped_df["brand"] = mapped_df["brand"].replace({
        "Maruti": "Maruti Suzuki",
        "Mercedes": "Mercedes-Benz",
        "VW": "Volkswagen",
    })

    # 2. Year & Vehicle Age
    if "year" in matched_cols:
        mapped_df["year"] = df[matched_cols["year"]].apply(parse_numeric_str).fillna(CURRENT_YEAR - 5).astype(int)
        mapped_df["vehicle_age"] = np.maximum(CURRENT_YEAR - mapped_df["year"], 0)
    elif "vehicle_age" in matched_cols:
        mapped_df["vehicle_age"] = df[matched_cols["vehicle_age"]].apply(parse_numeric_str).fillna(5).astype(int)
        mapped_df["year"] = CURRENT_YEAR - mapped_df["vehicle_age"]
    else:
        mapped_df["year"] = CURRENT_YEAR - 5
        mapped_df["vehicle_age"] = 5

    # 3. Mileage / Kms Driven
    if "mileage" in matched_cols:
        mapped_df["mileage"] = df[matched_cols["mileage"]].apply(parse_numeric_str)
        # If mileage was km/l, check if km_driven was available or convert
        if mapped_df["mileage"].median() < 50:  # Indicates fuel economy km/l was mapped instead of distance
            if "km_driven" in lower_col_map:
                mapped_df["mileage"] = df[lower_col_map["km_driven"]].apply(parse_numeric_str)
            else:
                mapped_df["mileage"] = mapped_df["vehicle_age"] * 13500.0
    else:
        mapped_df["mileage"] = mapped_df["vehicle_age"] * 13500.0

    mapped_df["mileage"] = mapped_df["mileage"].fillna(mapped_df["vehicle_age"] * 13500.0)

    # 4. Fuel Type
    if "fuel_type" in matched_cols:
        mapped_df["fuel_type"] = df[matched_cols["fuel_type"]].astype(str).str.strip().str.capitalize()
    else:
        mapped_df["fuel_type"] = "Petrol"

    mapped_df["fuel_type"] = mapped_df["fuel_type"].replace({"Cng": "CNG", "Lpg": "LPG"})

    # 5. Transmission
    if "transmission" in matched_cols:
        mapped_df["transmission"] = df[matched_cols["transmission"]].astype(str).str.strip().str.capitalize()
    else:
        mapped_df["transmission"] = "Automatic"

    # 6. Owner Count
    if "owner_count" in matched_cols:
        mapped_df["owner_count"] = [
            parse_owner_count(v, a)
            for v, a in zip(df[matched_cols["owner_count"]], mapped_df["vehicle_age"])
        ]
    else:
        mapped_df["owner_count"] = [
            1 if a <= 3 else (2 if a <= 7 else 3)
            for a in mapped_df["vehicle_age"]
        ]

    # 7. Price & Currency Standardization (Native Indian Rupees INR ₹)
    if "price" in matched_cols:
        mapped_df["price"] = df[matched_cols["price"]].apply(parse_numeric_str)
        median_price = float(mapped_df["price"].median())
        
        # Auto-detect if in Lakhs INR (e.g., 3.5 = 3.5 Lakhs = 350,000 INR)
        if 0 < median_price < 150:
            logger.info(f"Detected Lakhs INR dataset (median: {median_price:.2f} Lakhs); converting to full INR (₹)...")
            mapped_df["price"] = mapped_df["price"] * 100000.0
        # Auto-detect if in USD (e.g. median between 500 and 90,000 USD), convert to INR
        elif 500 <= median_price <= 90000:
            logger.info(f"Detected USD dataset (median: ${median_price:,.0f}); converting to INR (₹)...")
            mapped_df["price"] = mapped_df["price"] * 83.0
        else:
            logger.info(f"Dataset natively in Indian Rupees (INR ₹) (median: ₹{median_price:,.0f}).")
        
        mapped_df["price"] = mapped_df["price"].round(2)
    else:
        mapped_df["price"] = 650000.0

    # 8. Region (if not present, assign realistic deterministic geographic distribution)
    if "region" in matched_cols:
        mapped_df["region"] = df[matched_cols["region"]].astype(str).str.strip()
    else:
        np.random.seed(42)
        mapped_df["region"] = [
            REGIONS[i % len(REGIONS)]
            for i in range(len(mapped_df))
        ]

    # 9. Listing Date & Days to Sale
    if "listing_date" in matched_cols:
        mapped_df["listing_date"] = pd.to_datetime(df[matched_cols["listing_date"]], errors="coerce")
    else:
        np.random.seed(42)
        end_date = pd.Timestamp.now()
        start_date = end_date - pd.Timedelta(days=365)
        sec_range = int((end_date - start_date).total_seconds())
        random_secs = np.random.randint(0, sec_range, size=len(mapped_df))
        mapped_df["listing_date"] = [start_date + pd.Timedelta(seconds=s) for s in random_secs]

    if "days_to_sale" in matched_cols:
        mapped_df["days_to_sale"] = df[matched_cols["days_to_sale"]].apply(parse_numeric_str)
    else:
        # Realistic days to sale calculation based on age, mileage, brand luxury, and price percentile
        np.random.seed(42)
        median_brand_price = mapped_df.groupby("brand")["price"].transform("median").fillna(mapped_df["price"].median())
        price_ratio = (mapped_df["price"] / np.maximum(median_brand_price, 50000.0)).clip(0.5, 2.5)
        base_days = 26.0 * (price_ratio ** 1.8) + (mapped_df["vehicle_age"] * 1.4)
        is_lux = mapped_df["brand"].isin(LUXURY_BRANDS).astype(float)
        base_days = base_days * (1.0 + is_lux * 0.15)
        days = np.random.gamma(shape=3.5, scale=base_days / 3.5)
        mapped_df["days_to_sale"] = np.clip(days, 3, 150).astype(int)

    return mapped_df


def clean_and_preprocess(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Standardize, clean, filter IQR outliers, and engineer features."""
    logger.info(f"Processing raw dataframe with shape: {df.shape}...")
    mapped_df = auto_detect_and_map_columns(df)

    # Filter invalid/null records
    mapped_df = mapped_df.dropna(subset=["price", "brand", "model"])
    mapped_df = mapped_df[mapped_df["price"] > 30000.0]
    mapped_df = mapped_df[mapped_df["mileage"] >= 0.0]

    # Feature Engineering
    mapped_df["year"] = mapped_df["year"].astype(int)
    mapped_df["vehicle_age"] = np.maximum(CURRENT_YEAR - mapped_df["year"], 0)
    mapped_df["owner_count"] = mapped_df["owner_count"].astype(int)
    mapped_df["mileage_per_year"] = mapped_df["mileage"] / np.maximum(mapped_df["vehicle_age"], 1.0)
    mapped_df["is_luxury"] = mapped_df["brand"].isin(LUXURY_BRANDS).astype(int)
    
    # Date features
    mapped_df["listing_date"] = pd.to_datetime(mapped_df["listing_date"])
    mapped_df["listing_month"] = mapped_df["listing_date"].dt.month
    mapped_df["listing_year"] = mapped_df["listing_date"].dt.year
    mapped_df["listing_season"] = mapped_df["listing_month"].map({
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring", 4: "Spring", 5: "Spring",
        6: "Summer", 7: "Summer", 8: "Summer",
        9: "Fall", 10: "Fall", 11: "Fall"
    }).fillna("Spring")
    mapped_df["listing_date_str"] = mapped_df["listing_date"].dt.strftime("%Y-%m-%d")

    # IQR Outlier Capping (Price & Mileage)
    q1_p, q3_p = mapped_df["price"].quantile(0.01), mapped_df["price"].quantile(0.99)
    iqr_p = q3_p - q1_p
    lower_price = max(40000.0, float(q1_p - 1.5 * iqr_p))
    upper_price = float(q3_p + 1.5 * iqr_p)

    q1_m, q3_m = mapped_df["mileage"].quantile(0.01), mapped_df["mileage"].quantile(0.99)
    iqr_m = q3_m - q1_m
    lower_mileage = max(100.0, float(q1_m - 1.5 * iqr_m))
    upper_mileage = float(q3_m + 1.5 * iqr_m)

    outliers_price = int(((mapped_df["price"] < lower_price) | (mapped_df["price"] > upper_price)).sum())
    outliers_mileage = int(((mapped_df["mileage"] < lower_mileage) | (mapped_df["mileage"] > upper_mileage)).sum())

    mapped_df["price"] = mapped_df["price"].clip(lower_price, upper_price)
    mapped_df["mileage"] = mapped_df["mileage"].clip(lower_mileage, upper_mileage)

    cleaning_meta = {
        "initial_rows": int(df.shape[0]),
        "cleaned_rows": int(mapped_df.shape[0]),
        "price_outliers_capped": outliers_price,
        "mileage_outliers_capped": outliers_mileage,
        "price_bounds": [round(lower_price, 2), round(upper_price, 2)],
        "mileage_bounds": [round(lower_mileage, 2), round(upper_mileage, 2)],
    }
    logger.info(f"Cleaning complete. Output shape: {mapped_df.shape}, Meta: {cleaning_meta}")
    return mapped_df, cleaning_meta


def generate_eda_summary(df: pd.DataFrame, cleaning_meta: Dict[str, Any]) -> Dict[str, Any]:
    """Generate comprehensive EDA metrics, correlations, and aggregated market breakdowns."""
    logger.info("Computing EDA summary statistics...")

    price_stats = {
        "mean": round(float(df["price"].mean()), 2),
        "median": round(float(df["price"].median()), 2),
        "std": round(float(df["price"].std()), 2),
        "min": round(float(df["price"].min()), 2),
        "q25": round(float(df["price"].quantile(0.25)), 2),
        "q75": round(float(df["price"].quantile(0.75)), 2),
        "max": round(float(df["price"].max()), 2),
    }

    mileage_stats = {
        "mean": round(float(df["mileage"].mean()), 2),
        "median": round(float(df["mileage"].median()), 2),
        "std": round(float(df["mileage"].std()), 2),
        "min": round(float(df["mileage"].min()), 2),
        "max": round(float(df["mileage"].max()), 2),
    }

    days_stats = {
        "mean": round(float(df["days_to_sale"].mean()), 2),
        "median": round(float(df["days_to_sale"].median()), 2),
        "min": int(df["days_to_sale"].min()),
        "max": int(df["days_to_sale"].max()),
    }

    # Brand Breakdown
    brand_summary = (
        df.groupby("brand")
        .agg(
            count=("price", "count"),
            avg_price=("price", "mean"),
            median_price=("price", "median"),
            avg_days_to_sale=("days_to_sale", "mean")
        )
        .reset_index()
        .sort_values(by="count", ascending=False)
    )
    brand_list = [
        {
            "brand": str(row["brand"]),
            "count": int(row["count"]),
            "avg_price": round(float(row["avg_price"]), 2),
            "median_price": round(float(row["median_price"]), 2),
            "avg_days_to_sale": round(float(row["avg_days_to_sale"]), 1),
        }
        for _, row in brand_summary.iterrows()
    ]

    # Regional Aggregations
    region_summary = (
        df.groupby("region")
        .agg(
            count=("price", "count"),
            avg_price=("price", "mean"),
            avg_mileage=("mileage", "mean"),
            avg_days_to_sale=("days_to_sale", "mean")
        )
        .reset_index()
    )
    region_list = [
        {
            "region": str(row["region"]),
            "count": int(row["count"]),
            "avg_price": round(float(row["avg_price"]), 2),
            "avg_mileage": round(float(row["avg_mileage"]), 1),
            "avg_days_to_sale": round(float(row["avg_days_to_sale"]), 1),
        }
        for _, row in region_summary.iterrows()
    ]

    # Year Depreciation Trend
    year_summary = (
        df.groupby("year")
        .agg(
            count=("price", "count"),
            avg_price=("price", "mean"),
            avg_mileage=("mileage", "mean")
        )
        .reset_index()
        .sort_values(by="year")
    )
    year_list = [
        {
            "year": int(row["year"]),
            "count": int(row["count"]),
            "avg_price": round(float(row["avg_price"]), 2),
            "avg_mileage": round(float(row["avg_mileage"]), 1),
        }
        for _, row in year_summary.iterrows()
    ]

    # Fuel Type Breakdown
    fuel_summary = (
        df.groupby("fuel_type")
        .agg(count=("price", "count"), avg_price=("price", "mean"))
        .reset_index()
    )
    fuel_list = [
        {"fuel_type": str(row["fuel_type"]), "count": int(row["count"]), "avg_price": round(float(row["avg_price"]), 2)}
        for _, row in fuel_summary.iterrows()
    ]

    # Transmission Breakdown
    trans_summary = (
        df.groupby("transmission")
        .agg(count=("price", "count"), avg_price=("price", "mean"))
        .reset_index()
    )
    trans_list = [
        {"transmission": str(row["transmission"]), "count": int(row["count"]), "avg_price": round(float(row["avg_price"]), 2)}
        for _, row in trans_summary.iterrows()
    ]

    # Correlation Matrix
    numeric_df = df[["year", "mileage", "owner_count", "vehicle_age", "price", "days_to_sale", "is_luxury"]]
    corr_matrix = numeric_df.corr().round(4).to_dict()

    eda_data = {
        "metadata": cleaning_meta,
        "price_stats": price_stats,
        "mileage_stats": mileage_stats,
        "days_to_sale_stats": days_stats,
        "brand_summary": brand_list,
        "region_summary": region_list,
        "year_trend": year_list,
        "fuel_breakdown": fuel_list,
        "transmission_breakdown": trans_list,
        "correlation_matrix": corr_matrix,
    }

    with open(EDA_SUMMARY_PATH, "w") as f:
        json.dump(eda_data, f, indent=2)
    logger.info(f"EDA Summary saved to {EDA_SUMMARY_PATH}")

    return eda_data


def load_or_create_dataset(force_synthetic: bool = False) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Load real dataset from /backend/data (prioritizing cardekho_dataset.csv or used_cars.csv)."""
    target_csv = None

    # Priority 1: cardekho_dataset.csv
    cardekho_csv = DATA_DIR / "cardekho_dataset.csv"
    used_cars_csv = DATA_DIR / "used_cars.csv"
    web_scraped_csv = DATA_DIR / "car_web_scraped_dataset.csv"

    if cardekho_csv.exists() and not force_synthetic:
        target_csv = cardekho_csv
    elif used_cars_csv.exists() and not force_synthetic:
        target_csv = used_cars_csv
    elif web_scraped_csv.exists() and not force_synthetic:
        target_csv = web_scraped_csv
    else:
        # Fallback to any other CSV in DATA_DIR
        csv_files = [f for f in DATA_DIR.glob("*.csv") if f.name not in ["cleaned_cars.csv"]]
        if csv_files and not force_synthetic:
            target_csv = csv_files[0]

    if target_csv is not None:
        logger.info(f"Loading real dataset from: {target_csv.name}")
        df_raw = pd.read_csv(target_csv)
    else:
        logger.info("No CSV found. Creating synthetic dataset...")
        from backend.app.data_pipeline import generate_synthetic_data
        df_raw = generate_synthetic_data(num_samples=5000)
        df_raw.to_csv(RAW_DATA_PATH, index=False)

    df_cleaned, meta = clean_and_preprocess(df_raw)
    df_cleaned.to_csv(CLEANED_DATA_PATH, index=False)
    logger.info(f"Cleaned dataset saved to {CLEANED_DATA_PATH} with {len(df_cleaned)} rows.")

    eda = generate_eda_summary(df_cleaned, meta)
    return df_cleaned, eda


if __name__ == "__main__":
    df, eda = load_or_create_dataset()
    print("\n================ UPDATED DATA PIPELINE & EDA SUMMARY ================")
    print(f"Dataset Loaded: {eda['metadata']['cleaned_rows']} records")
    print(f"Price Stats: Mean = ₹{eda['price_stats']['mean']:,.2f}, Median = ₹{eda['price_stats']['median']:,.2f}")
    print(f"Price Range: ₹{eda['price_stats']['min']:,.2f} - ₹{eda['price_stats']['max']:,.2f}")
    print(f"Mileage Stats: Mean = {eda['mileage_stats']['mean']:,.1f} km, Median = {eda['mileage_stats']['median']:,.1f} km")
    print(f"Average Days to Sale: {eda['days_to_sale_stats']['mean']:.1f} days")
    print("Top 5 Brands by Volume:")
    for b in eda['brand_summary'][:5]:
        print(f"  - {b['brand']}: {b['count']} listings | Avg Price: ₹{b['avg_price']:,.2f} | Avg Days to Sale: {b['avg_days_to_sale']}")
    print("Fuel Breakdown:")
    for f in eda['fuel_breakdown']:
        print(f"  - {f['fuel_type']}: {f['count']} listings | Avg Price: ₹{f['avg_price']:,.2f}")
    print("Transmission Breakdown:")
    for t in eda['transmission_breakdown']:
        print(f"  - {t['transmission']}: {t['count']} listings | Avg Price: ₹{t['avg_price']:,.2f}")
    print("====================================================================\n")
