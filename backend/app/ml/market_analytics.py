import json
import logging
from typing import Dict, Any, List
import pandas as pd

from app.config import EDA_SUMMARY_PATH, CLEANED_DATA_PATH
from app.schemas import MarketAnalyticsResponse, OptionsResponse
from app.ml.msrp_data import BRAND_MODELS_MSRP

logger = logging.getLogger(__name__)


class MarketAnalyticsService:
    def __init__(self):
        self.eda_data = None
        self.cleaned_df = None
        self.load_data()

    def load_data(self):
        try:
            if EDA_SUMMARY_PATH.exists():
                with open(EDA_SUMMARY_PATH, "r") as f:
                    self.eda_data = json.load(f)
            if CLEANED_DATA_PATH.exists():
                self.cleaned_df = pd.read_csv(CLEANED_DATA_PATH)
            logger.info("Market analytics data loaded.")
        except Exception as e:
            logger.warning(f"Market analytics data load error: {e}")

    def get_analytics(self) -> MarketAnalyticsResponse:
        if self.eda_data is None or self.cleaned_df is None:
            self.load_data()

        # Supply / Demand trend aggregation over months
        supply_demand = []
        if self.cleaned_df is not None and "listing_month" in self.cleaned_df.columns:
            month_names = {
                1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
                7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
            }
            monthly_grp = self.cleaned_df.groupby("listing_month").agg(
                listing_volume=("price", "count"),
                avg_price=("price", "mean"),
                avg_days_to_sale=("days_to_sale", "mean")
            ).reset_index().sort_values(by="listing_month")

            for _, r in monthly_grp.iterrows():
                m_int = int(r["listing_month"])
                vol = int(r["listing_volume"])
                days = float(r["avg_days_to_sale"])
                # Demand score: inverse of days to sale scaled with volume
                demand_score = round(max(30.0, min(95.0, 100.0 - (days * 1.1) + (vol / 50.0))), 1)
                supply_demand.append({
                    "month": month_names.get(m_int, f"M{m_int}"),
                    "month_number": m_int,
                    "listing_volume": vol,
                    "avg_price": round(float(r["avg_price"]), 2),
                    "avg_days_to_sale": round(days, 1),
                    "demand_index": demand_score,
                })
        else:
            supply_demand = [
                {"month": "Jan", "listing_volume": 1240, "avg_price": 720000, "avg_days_to_sale": 42.1, "demand_index": 68.0},
                {"month": "Feb", "listing_volume": 1310, "avg_price": 745000, "avg_days_to_sale": 39.5, "demand_index": 72.0},
                {"month": "Mar", "listing_volume": 1450, "avg_price": 760000, "avg_days_to_sale": 36.2, "demand_index": 78.5},
                {"month": "Apr", "listing_volume": 1520, "avg_price": 780000, "avg_days_to_sale": 34.0, "demand_index": 82.0},
                {"month": "May", "listing_volume": 1490, "avg_price": 775000, "avg_days_to_sale": 35.8, "demand_index": 80.0},
                {"month": "Jun", "listing_volume": 1380, "avg_price": 750000, "avg_days_to_sale": 38.4, "demand_index": 74.0},
            ]

        meta = self.eda_data.get("metadata", {}) if self.eda_data else {}
        p_stats = self.eda_data.get("price_stats", {}) if self.eda_data else {}
        d_stats = self.eda_data.get("days_to_sale_stats", {}) if self.eda_data else {}

        return MarketAnalyticsResponse(
            total_listings=int(meta.get("cleaned_rows", len(self.cleaned_df) if self.cleaned_df is not None else 15000)),
            average_price=float(p_stats.get("mean", 750000.0)),
            median_price=float(p_stats.get("median", 550000.0)),
            average_days_to_sale=float(d_stats.get("mean", 41.5)),
            brand_summary=self.eda_data.get("brand_summary", []) if self.eda_data else [],
            region_summary=self.eda_data.get("region_summary", []) if self.eda_data else [],
            year_trend=self.eda_data.get("year_trend", []) if self.eda_data else [],
            fuel_breakdown=self.eda_data.get("fuel_breakdown", []) if self.eda_data else [],
            transmission_breakdown=self.eda_data.get("transmission_breakdown", []) if self.eda_data else [],
            supply_demand_trend=supply_demand,
        )

    def get_options(self) -> OptionsResponse:
        if self.cleaned_df is None:
            self.load_data()

        if self.cleaned_df is not None:
            brands = sorted(self.cleaned_df["brand"].unique().tolist())
            brand_models = {}
            for brand in brands:
                models = sorted(self.cleaned_df[self.cleaned_df["brand"] == brand]["model"].unique().tolist())
                brand_models[brand] = models

            fuel_types = sorted(self.cleaned_df["fuel_type"].unique().tolist())
            transmissions = sorted(self.cleaned_df["transmission"].unique().tolist())
            regions = sorted(self.cleaned_df["region"].unique().tolist())
            min_year = int(self.cleaned_df["year"].min())
            max_year = int(self.cleaned_df["year"].max())
        else:
            brands = ["Honda", "Toyota", "Ford", "BMW", "Mercedes-Benz", "Hyundai", "Maruti Suzuki"]
            brand_models = {b: ["Model A", "Model B"] for b in brands}
            fuel_types = ["Petrol", "Diesel", "Hybrid", "CNG", "Electric"]
            transmissions = ["Automatic", "Manual"]
            regions = ["Metro", "North", "South", "East", "West", "Central"]
            min_year = 2010
            max_year = 2024

        return OptionsResponse(
            brands=brands,
            brand_models=brand_models,
            brand_msrp=BRAND_MODELS_MSRP,
            fuel_types=fuel_types,
            transmissions=transmissions,
            regions=regions,
            min_year=min_year,
            max_year=max_year,
        )


market_analytics_service = MarketAnalyticsService()
