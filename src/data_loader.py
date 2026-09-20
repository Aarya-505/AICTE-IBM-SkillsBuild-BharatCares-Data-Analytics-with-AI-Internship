"""
RoadSafe India - Data Loader Module
Handles safe ingestion and structural validation of raw MoRTH accident datasets.
"""

import os
import pandas as pd
from typing import Optional, Dict

class DataLoader:
    def __init__(self, raw_dir: str = "data/raw"):
        self.raw_dir = raw_dir

    def _load_csv(self, filename: str) -> pd.DataFrame:
        filepath = os.path.join(self.raw_dir, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Dataset file '{filepath}' not found. Run 'src/data_builder.py' first.")
        df = pd.read_csv(filepath)
        return df

    def load_state_ut_data(self) -> pd.DataFrame:
        """Loads state/UT multi-year accident records (2014-2020)."""
        df = self._load_csv("morth_state_ut_accidents_2014_2020.csv")
        expected_cols = {"State_UT", "Year", "Total_Accidents", "Persons_Killed", "Persons_Injured"}
        if not expected_cols.issubset(df.columns):
            raise ValueError(f"Missing required columns in State/UT dataset. Expected: {expected_cols}")
        return df

    def load_million_plus_cities(self) -> pd.DataFrame:
        """Loads 50 Million-Plus Indian Cities 2020 accident records."""
        df = self._load_csv("morth_million_plus_cities_2020.csv")
        expected_cols = {"City", "State", "Total_Accidents", "Persons_Killed", "Persons_Injured"}
        if not expected_cols.issubset(df.columns):
            raise ValueError(f"Missing required columns in Cities dataset. Expected: {expected_cols}")
        return df

    def load_contributing_factors(self) -> pd.DataFrame:
        """Loads infrastructure, environmental, vehicular, and behavioral contributing factors."""
        df = self._load_csv("morth_contributing_factors_2020.csv")
        expected_cols = {"Category_Type", "Factor_Name", "Total_Accidents", "Persons_Killed", "Persons_Injured"}
        if not expected_cols.issubset(df.columns):
            raise ValueError(f"Missing required columns in Factors dataset. Expected: {expected_cols}")
        return df

    def load_time_slots(self) -> pd.DataFrame:
        """Loads 24-hour diurnal time slot accident distributions."""
        df = self._load_csv("morth_time_slots_2020.csv")
        expected_cols = {"Time_Slot", "Start_Hour", "End_Hour", "Total_Accidents", "Persons_Killed", "Persons_Injured"}
        if not expected_cols.issubset(df.columns):
            raise ValueError(f"Missing required columns in Time Slots dataset. Expected: {expected_cols}")
        return df

    def load_all_raw(self) -> Dict[str, pd.DataFrame]:
        """Loads all raw datasets into a dictionary."""
        return {
            "state_ut": self.load_state_ut_data(),
            "cities": self.load_million_plus_cities(),
            "factors": self.load_contributing_factors(),
            "time_slots": self.load_time_slots()
        }

if __name__ == "__main__":
    loader = DataLoader()
    datasets = loader.load_all_raw()
    for name, df in datasets.items():
        print(f"Dataset '{name}' loaded successfully: {df.shape[0]} rows, {df.shape[1]} columns.")
