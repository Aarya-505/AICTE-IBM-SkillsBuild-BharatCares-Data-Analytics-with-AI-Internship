"""
RoadSafe India - Data Cleaner & Standardization Pipeline
Cleans, standardizes, validates, and computes baseline indicators for road accident data.
Outputs processed datasets and an audit log to 'data/processed/'.
"""

import os
import json
import pandas as pd
import numpy as np
from datetime import datetime
import sys
# Add project root to sys.path if not present
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from src.data_loader import DataLoader
except ImportError:
    from data_loader import DataLoader

class DataCleaner:
    def __init__(self, raw_dir: str = "data/raw", processed_dir: str = "data/processed"):
        self.raw_dir = raw_dir
        self.processed_dir = processed_dir
        self.loader = DataLoader(raw_dir=raw_dir)
        self.audit_log = {
            "pipeline_name": "RoadSafe India Cleaning Pipeline",
            "executed_at": datetime.now().isoformat(),
            "transformations": {}
        }

    def clean_state_ut_data(self) -> pd.DataFrame:
        """Cleans State/UT data, handles types, computes YoY changes and Severity Index."""
        df = self.loader.load_state_ut_data().copy()
        initial_rows = len(df)
        
        # 1. Strip whitespace
        df["State_UT"] = df["State_UT"].astype(str).str.strip()
        
        # 2. Type conversions & sanity validation
        numeric_cols = ["Year", "Total_Accidents", "Persons_Killed", "Persons_Injured"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
        
        # 3. Compute Accident Severity Index (Fatalities per 100 accidents)
        df["Severity_Index"] = np.where(
            df["Total_Accidents"] > 0,
            np.round((df["Persons_Killed"] / df["Total_Accidents"]) * 100, 2),
            0.0
        )
        
        # 4. Sort and calculate Year-over-Year (YoY) Change per State
        df = df.sort_values(by=["State_UT", "Year"]).reset_index(drop=True)
        df["YoY_Accident_Change_%"] = df.groupby("State_UT")["Total_Accidents"].pct_change() * 100
        df["YoY_Fatality_Change_%"] = df.groupby("State_UT")["Persons_Killed"].pct_change() * 100
        df["YoY_Accident_Change_%"] = df["YoY_Accident_Change_%"].round(2).fillna(0.0)
        df["YoY_Fatality_Change_%"] = df["YoY_Fatality_Change_%"].round(2).fillna(0.0)
        
        self.audit_log["transformations"]["state_ut"] = {
            "initial_rows": initial_rows,
            "final_rows": len(df),
            "columns": list(df.columns),
            "years_covered": sorted(df["Year"].unique().tolist()),
            "states_count": df["State_UT"].nunique()
        }
        return df

    def clean_million_plus_cities(self) -> pd.DataFrame:
        """Cleans 50 Million-Plus Cities data, computes Severity Index and Rankings."""
        df = self.loader.load_million_plus_cities().copy()
        initial_rows = len(df)
        
        # 1. Clean strings
        df["City"] = df["City"].astype(str).str.strip()
        df["State"] = df["State"].astype(str).str.strip()
        
        # 2. Numeric casting
        for col in ["Total_Accidents", "Persons_Killed", "Persons_Injured"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
            
        # 3. Severity Index (Fatalities per 100 accidents) & Injury Ratio
        df["Severity_Index"] = np.where(
            df["Total_Accidents"] > 0,
            np.round((df["Persons_Killed"] / df["Total_Accidents"]) * 100, 2),
            0.0
        )
        df["Injury_per_100_Accidents"] = np.where(
            df["Total_Accidents"] > 0,
            np.round((df["Persons_Injured"] / df["Total_Accidents"]) * 100, 2),
            0.0
        )
        
        # 4. National Rankings
        df["Rank_Accidents"] = df["Total_Accidents"].rank(ascending=False, method="min").astype(int)
        df["Rank_Fatalities"] = df["Persons_Killed"].rank(ascending=False, method="min").astype(int)
        df["Rank_Severity"] = df["Severity_Index"].rank(ascending=False, method="min").astype(int)
        
        # 5. Share of 50 Cities Total
        tot_acc = df["Total_Accidents"].sum()
        tot_kill = df["Persons_Killed"].sum()
        df["Accident_Share_%"] = np.round((df["Total_Accidents"] / tot_acc) * 100, 2)
        df["Fatality_Share_%"] = np.round((df["Persons_Killed"] / tot_kill) * 100, 2)
        
        df = df.sort_values(by="Total_Accidents", ascending=False).reset_index(drop=True)
        
        self.audit_log["transformations"]["million_plus_cities"] = {
            "initial_rows": initial_rows,
            "final_rows": len(df),
            "cities_count": df["City"].nunique(),
            "total_recorded_accidents": int(tot_acc),
            "total_recorded_fatalities": int(tot_kill)
        }
        return df

    def clean_contributing_factors(self) -> pd.DataFrame:
        """Cleans contributing factor breakdowns and calculates category severity & shares."""
        df = self.loader.load_contributing_factors().copy()
        initial_rows = len(df)
        
        df["Category_Type"] = df["Category_Type"].astype(str).str.strip()
        df["Factor_Name"] = df["Factor_Name"].astype(str).str.strip()
        
        for col in ["Total_Accidents", "Persons_Killed", "Persons_Injured"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
            
        df["Severity_Index"] = np.where(
            df["Total_Accidents"] > 0,
            np.round((df["Persons_Killed"] / df["Total_Accidents"]) * 100, 2),
            0.0
        )
        
        # Category specific shares
        cat_acc_sums = df.groupby("Category_Type")["Total_Accidents"].transform("sum")
        cat_kill_sums = df.groupby("Category_Type")["Persons_Killed"].transform("sum")
        
        df["Category_Accident_Share_%"] = np.round((df["Total_Accidents"] / cat_acc_sums) * 100, 2)
        df["Category_Fatality_Share_%"] = np.round((df["Persons_Killed"] / cat_kill_sums) * 100, 2)
        
        self.audit_log["transformations"]["contributing_factors"] = {
            "initial_rows": initial_rows,
            "final_rows": len(df),
            "categories": df["Category_Type"].unique().tolist()
        }
        return df

    def clean_time_slots(self) -> pd.DataFrame:
        """Cleans 24-hour diurnal patterns."""
        df = self.loader.load_time_slots().copy()
        initial_rows = len(df)
        
        df["Time_Slot"] = df["Time_Slot"].astype(str).str.strip()
        for col in ["Start_Hour", "End_Hour", "Total_Accidents", "Persons_Killed", "Persons_Injured"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
            
        tot_acc = df["Total_Accidents"].sum()
        tot_kill = df["Persons_Killed"].sum()
        
        df["Accident_Share_%"] = np.round((df["Total_Accidents"] / tot_acc) * 100, 2)
        df["Fatality_Share_%"] = np.round((df["Persons_Killed"] / tot_kill) * 100, 2)
        df["Severity_Index"] = np.where(
            df["Total_Accidents"] > 0,
            np.round((df["Persons_Killed"] / df["Total_Accidents"]) * 100, 2),
            0.0
        )
        
        self.audit_log["transformations"]["time_slots"] = {
            "initial_rows": initial_rows,
            "final_rows": len(df),
            "total_accidents": int(tot_acc),
            "peak_accident_slot": df.loc[df["Total_Accidents"].idxmax()]["Time_Slot"]
        }
        return df

    def run_cleaning_pipeline(self):
        """Executes full cleaning pipeline and writes processed outputs."""
        os.makedirs(self.processed_dir, exist_ok=True)
        
        df_state = self.clean_state_ut_data()
        df_cities = self.clean_million_plus_cities()
        df_factors = self.clean_contributing_factors()
        df_time = self.clean_time_slots()
        
        df_state.to_csv(os.path.join(self.processed_dir, "cleaned_state_ut_trends.csv"), index=False)
        df_cities.to_csv(os.path.join(self.processed_dir, "cleaned_million_plus_cities.csv"), index=False)
        df_factors.to_csv(os.path.join(self.processed_dir, "cleaned_contributing_factors.csv"), index=False)
        df_time.to_csv(os.path.join(self.processed_dir, "cleaned_time_slots.csv"), index=False)
        
        with open(os.path.join(self.processed_dir, "data_cleaning_audit_log.json"), "w", encoding="utf-8") as f:
            json.dump(self.audit_log, f, indent=4)
            
        print("Data cleaning pipeline completed successfully!")
        print(f"Processed files saved to '{self.processed_dir}'.")

if __name__ == "__main__":
    cleaner = DataCleaner()
    cleaner.run_cleaning_pipeline()
