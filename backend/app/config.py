import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
RAW_DATA_PATH = DATA_DIR / "used_cars.csv"
CLEANED_DATA_PATH = DATA_DIR / "cleaned_cars.csv"
EDA_SUMMARY_PATH = DATA_DIR / "eda_summary.json"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Reference Year for feature engineering
CURRENT_YEAR = 2024
