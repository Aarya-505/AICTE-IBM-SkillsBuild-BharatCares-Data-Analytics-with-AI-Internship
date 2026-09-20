"""
RoadSafe India - Key Performance Indicator (KPI) Engine
Provides standardized, mathematically validated road-safety indicators.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional

class KPICalculator:
    """Calculates standardized road safety indicators grounded in transport research."""

    @staticmethod
    def calculate_severity_index(fatalities: float, accidents: float) -> float:
        """
        Accident Severity Index (ASI): Number of persons killed per 100 reported accidents.
        Formula: (Persons Killed / Total Accidents) * 100
        """
        if accidents <= 0:
            return 0.0
        return round(float((fatalities / accidents) * 100), 2)

    @staticmethod
    def calculate_injury_ratio(injuries: float, accidents: float) -> float:
        """
        Injury Rate per 100 Accidents: Number of persons injured per 100 reported accidents.
        Formula: (Persons Injured / Total Accidents) * 100
        """
        if accidents <= 0:
            return 0.0
        return round(float((injuries / accidents) * 100), 2)

    @staticmethod
    def calculate_fatality_to_injury_ratio(fatalities: float, injuries: float) -> float:
        """
        Fatality to Injury Ratio: Indicates the proportion of high-trauma outcomes.
        Formula: Persons Killed / Persons Injured
        """
        if injuries <= 0:
            return 0.0
        return round(float(fatalities / injuries), 3)

    @staticmethod
    def calculate_yoy_growth(current_val: float, previous_val: float) -> float:
        """
        Year-over-Year Percentage Growth.
        Formula: ((Current - Previous) / Previous) * 100
        """
        if previous_val == 0:
            return 0.0
        return round(float(((current_val - previous_val) / previous_val) * 100), 2)

    @classmethod
    def generate_national_kpis(cls, df_state_trends: pd.DataFrame, target_year: int = 2020) -> Dict[str, Any]:
        """Calculates headline national indicators for a given target year."""
        year_df = df_state_trends[df_state_trends["Year"] == target_year]
        if year_df.empty:
            return {}

        tot_acc = int(year_df["Total_Accidents"].sum())
        tot_kill = int(year_df["Persons_Killed"].sum())
        tot_inj = int(year_df["Persons_Injured"].sum())
        severity = cls.calculate_severity_index(tot_kill, tot_acc)
        injury_ratio = cls.calculate_injury_ratio(tot_inj, tot_acc)

        # Compare with previous year if present
        prev_df = df_state_trends[df_state_trends["Year"] == (target_year - 1)]
        prev_acc = int(prev_df["Total_Accidents"].sum()) if not prev_df.empty else 0
        prev_kill = int(prev_df["Persons_Killed"].sum()) if not prev_df.empty else 0

        acc_yoy = cls.calculate_yoy_growth(tot_acc, prev_acc) if prev_acc > 0 else 0.0
        kill_yoy = cls.calculate_yoy_growth(tot_kill, prev_kill) if prev_kill > 0 else 0.0

        return {
            "target_year": target_year,
            "total_accidents": tot_acc,
            "total_fatalities": tot_kill,
            "total_injuries": tot_inj,
            "severity_index": severity,
            "injury_per_100": injury_ratio,
            "accident_yoy_growth_%": acc_yoy,
            "fatality_yoy_growth_%": kill_yoy
        }

    @classmethod
    def generate_city_kpis(cls, df_cities: pd.DataFrame, city_name: Optional[str] = None) -> Dict[str, Any]:
        """Calculates indicators for 50 Million-Plus Cities."""
        if city_name:
            c_row = df_cities[df_cities["City"].str.lower() == city_name.lower()]
            if c_row.empty:
                return {}
            row = c_row.iloc[0]
            return {
                "city": row["City"],
                "state": row["State"],
                "total_accidents": int(row["Total_Accidents"]),
                "fatalities": int(row["Persons_Killed"]),
                "injuries": int(row["Persons_Injured"]),
                "severity_index": float(row["Severity_Index"]),
                "injury_per_100": float(row["Injury_per_100_Accidents"]),
                "rank_accidents": int(row["Rank_Accidents"]),
                "rank_fatalities": int(row["Rank_Fatalities"]),
                "rank_severity": int(row["Rank_Severity"])
            }
        else:
            # 50 Cities aggregate summary
            tot_acc = int(df_cities["Total_Accidents"].sum())
            tot_kill = int(df_cities["Persons_Killed"].sum())
            tot_inj = int(df_cities["Persons_Injured"].sum())
            return {
                "total_cities": len(df_cities),
                "total_accidents": tot_acc,
                "total_fatalities": tot_kill,
                "total_injuries": tot_inj,
                "avg_severity_index": cls.calculate_severity_index(tot_kill, tot_acc),
                "top_accident_city": df_cities.loc[df_cities["Total_Accidents"].idxmax()]["City"],
                "top_fatality_city": df_cities.loc[df_cities["Persons_Killed"].idxmax()]["City"],
                "highest_severity_city": df_cities.loc[df_cities["Severity_Index"].idxmax()]["City"]
            }

    @classmethod
    def generate_vru_kpi(cls, df_factors: pd.DataFrame) -> Dict[str, Any]:
        """Calculates Vulnerable Road User (VRU: Pedestrians, Cyclists, 2-Wheelers) statistics."""
        vru_categories = ["Two-Wheelers (Motorcycles/Scooters)", "Pedestrians (VRU)", "Bicycles (Non-Motorized VRU)"]
        vru_df = df_factors[df_factors["Factor_Name"].isin(vru_categories)]
        all_users = df_factors[df_factors["Category_Type"] == "Road User Type"]
        
        tot_user_acc = all_users["Total_Accidents"].sum()
        tot_user_kill = all_users["Persons_Killed"].sum()
        
        vru_acc = vru_df["Total_Accidents"].sum()
        vru_kill = vru_df["Persons_Killed"].sum()
        
        vru_acc_share = round(float((vru_acc / tot_user_acc) * 100), 2) if tot_user_acc > 0 else 0.0
        vru_kill_share = round(float((vru_kill / tot_user_kill) * 100), 2) if tot_user_kill > 0 else 0.0
        
        return {
            "vru_accidents": int(vru_acc),
            "vru_fatalities": int(vru_kill),
            "vru_accident_share_%": vru_acc_share,
            "vru_fatality_share_%": vru_kill_share,
            "vru_severity_index": cls.calculate_severity_index(vru_kill, vru_acc)
        }

if __name__ == "__main__":
    calc = KPICalculator()
    print("Severity Index (100 killed in 250 crashes):", calc.calculate_severity_index(100, 250))
    print("YoY Growth (120 vs 100):", calc.calculate_yoy_growth(120, 100))
