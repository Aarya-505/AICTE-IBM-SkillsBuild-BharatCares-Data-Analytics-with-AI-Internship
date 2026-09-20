import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest
import pandas as pd
import numpy as np
from src.kpi_calculator import KPICalculator
from src.data_cleaner import DataCleaner

def test_severity_index_normal():
    # 50 fatalities in 200 accidents = 25.0
    asi = KPICalculator.calculate_severity_index(50, 200)
    assert asi == 25.0

def test_severity_index_zero_division():
    asi = KPICalculator.calculate_severity_index(10, 0)
    assert asi == 0.0

def test_injury_ratio():
    ir = KPICalculator.calculate_injury_ratio(150, 200)
    assert ir == 75.0

def test_fatality_to_injury_ratio():
    fir = KPICalculator.calculate_fatality_to_injury_ratio(25, 100)
    assert fir == 0.25

def test_yoy_growth():
    # Growth from 100 to 110 = 10.0%
    g1 = KPICalculator.calculate_yoy_growth(110, 100)
    assert g1 == 10.0
    # Drop from 100 to 80 = -20.0%
    g2 = KPICalculator.calculate_yoy_growth(80, 100)
    assert g2 == -20.0
    # Zero previous value handling
    g3 = KPICalculator.calculate_yoy_growth(100, 0)
    assert g3 == 0.0

def test_data_cleaning_pipeline_integrity():
    cleaner = DataCleaner()
    df_state = cleaner.clean_state_ut_data()
    assert not df_state.empty
    assert "Severity_Index" in df_state.columns
    assert "YoY_Accident_Change_%" in df_state.columns
    
    df_cities = cleaner.clean_million_plus_cities()
    assert len(df_cities) == 50
    assert "Rank_Severity" in df_cities.columns
    
    df_factors = cleaner.clean_contributing_factors()
    assert not df_factors.empty
    assert "Category_Fatality_Share_%" in df_factors.columns
