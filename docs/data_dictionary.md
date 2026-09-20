# RoadSafe India — Data Dictionary & Variable Definitions

## Grounding & Source
- **Primary Source:** Ministry of Road Transport and Highways (MoRTH), Transport Research Wing (TRW), Government of India.
- **Secondary Source:** Open Government Data (data.gov.in).

---

## 1. State / UT Multi-Year Trends (`data/processed/cleaned_state_ut_trends.csv`)

| Column Name | Data Type | Units / Range | Description | Cleaning / Derivation Rule |
| :--- | :--- | :--- | :--- | :--- |
| `State_UT` | String | Categorical (36 Entities) | Name of Indian State or Union Territory | Stripped whitespace, standardized naming. |
| `Year` | Integer | 2014 – 2020 | Calendar reporting year | Cast to integer. |
| `Total_Accidents` | Integer | Non-negative count | Total police-reported road accident incidents | Nulls replaced with 0; verified with MoRTH totals. |
| `Persons_Killed` | Integer | Non-negative count | Total fatalities resulting from road crashes | Fatalities occurring within 30 days of incident. |
| `Persons_Injured` | Integer | Non-negative count | Total non-fatal injuries reported | Grievous and minor injuries combined. |
| `Severity_Index` | Float | 0.0 – 100.0+ | Accident Severity Index (Persons Killed per 100 Accidents) | Formula: `(Persons_Killed / Total_Accidents) * 100` |
| `YoY_Accident_Change_%` | Float | Percentage | Year-over-Year percentage change in accidents | Formula: `((Accidents_t - Accidents_{t-1}) / Accidents_{t-1}) * 100` |
| `YoY_Fatality_Change_%` | Float | Percentage | Year-over-Year percentage change in fatalities | Formula: `((Fatalities_t - Fatalities_{t-1}) / Fatalities_{t-1}) * 100` |

---

## 2. 50 Million-Plus Cities Dataset (`data/processed/cleaned_million_plus_cities.csv`)

| Column Name | Data Type | Description | Cleaning / Derivation Rule |
| :--- | :--- | :--- | :--- |
| `City` | String | Name of the urban agglomeration / municipal corporation | Cleaned string. |
| `State` | String | State where the city is located | Administrative mapping. |
| `Total_Accidents` | Integer | Total crashes recorded in urban jurisdiction (2020) | Official TRW count. |
| `Persons_Killed` | Integer | Total fatalities in city jurisdiction | Official TRW count. |
| `Persons_Injured` | Integer | Total injuries in city jurisdiction | Official TRW count. |
| `Severity_Index` | Float | City Accident Severity Index (Fatalities / 100 Crashes) | Formula: `(Persons_Killed / Total_Accidents) * 100` |
| `Injury_per_100_Accidents` | Float | Injury rate per 100 reported crashes | Formula: `(Persons_Injured / Total_Accidents) * 100` |
| `Rank_Accidents` | Integer | National rank by crash volume (1 to 50) | Min rank ascending=False. |
| `Rank_Fatalities` | Integer | National rank by fatality count (1 to 50) | Min rank ascending=False. |
| `Rank_Severity` | Integer | National rank by Severity Index (1 to 50) | Min rank ascending=False. |
| `Accident_Share_%` | Float | Share of total 50-cities crash volume | Formula: `(City Accidents / Total 50-Cities Accidents) * 100` |
| `Fatality_Share_%` | Float | Share of total 50-cities fatalities | Formula: `(City Fatalities / Total 50-Cities Fatalities) * 100` |

---

## 3. Contributing Factors Dataset (`data/processed/cleaned_contributing_factors.csv`)

| Column Name | Data Type | Categories | Description |
| :--- | :--- | :--- | :--- |
| `Category_Type` | String | `Road Classification`, `Junction Configuration`, `Traffic Cause`, `Weather Condition`, `Road Surface Feature`, `Road User Type` | Classification taxonomy of the factor. |
| `Factor_Name` | String | Specific factor label (e.g. `T-Junction`, `Over-speeding`, `Pedestrians (VRU)`) | Entity factor descriptor. |
| `Total_Accidents` | Integer | Count | Total crashes attributed to or occurring under this factor. |
| `Persons_Killed` | Integer | Count | Total fatalities under this factor. |
| `Persons_Injured` | Integer | Count | Total injuries under this factor. |
| `Severity_Index` | Float | Rate | Fatalities per 100 crashes for this factor. |
| `Category_Accident_Share_%` | Float | Percentage | Share within the respective `Category_Type`. |
| `Category_Fatality_Share_%` | Float | Percentage | Fatality share within the respective `Category_Type`. |
