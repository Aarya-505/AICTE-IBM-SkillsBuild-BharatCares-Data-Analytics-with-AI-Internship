# RoadSafe India
### Data-Driven Road Safety Analytics for Safer and Sustainable Urban Planning

[![Python Version](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-1.55-FF4B4B.svg)](https://streamlit.io/)
[![Plotly Charts](https://img.shields.io/badge/Plotly-Interactive-3F88C5.svg)](https://plotly.com/)
[![Tests](https://img.shields.io/badge/pytest-Passing-brightgreen.svg)](https://pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Project Overview
**RoadSafe India** is an end-to-end road safety data analytics pipeline, interactive decision-support dashboard, and computer vision proof-of-concept. Developed as part of the **AICTE IBM SkillsBuild Internship Program** (supported by **BharatCares**), this platform bridges the gap between macro-level Indian road crash records and actionable civil engineering and urban planning interventions.

### Future Scope and System Architecture
In modern smart city engineering, evidence-based safety intelligence provides the empirical foundation for transportation planning. **RoadSafe India** delivers the safety intelligence tier, analyzing historical accident records and edge traffic sensors to identify high-risk corridors, complex junctions, and vulnerable road users. This guides municipal authorities on prioritizing high-resolution spatial audits and microscopic traffic flow simulations.

```
+----------------------------------------------------------------------------------------------------+
|                                  INTELLIGENT TRANSPORTATION ARCHITECTURE                           |
|                                                                                                    |
|   1. EMPIRICAL SAFETY INTELLIGENCE LAYER (RoadSafe India)                                          |
|      - Historical MoRTH Accident Aggregations & Severity Indexes                                   |
|      - High-Risk Corridor & Junction Identification (Spatial Priority Ranking)                     |
|                                         |                                                          |
|                                         v                                                          |
|   2. HIGH-RESOLUTION SPATIAL SENSING & MAPPING LAYER                                              |
|      - High-Resolution Spatial Imagery & GIS Digital Elevation Models                              |
|      - Automated Road Feature Extraction (Road Width, Lane Markings, Encroachments)                |
|      - LiDAR Sight-Triangle Obstruction Detection at Complex 4-Arm Junctions                      |
|                                         |                                                          |
|                                         v                                                          |
|   3. SIMULATION & INTERVENTION LAYER (Digital Twin & Traffic Engine)                               |
|      - Microscopic Traffic Flow Simulation (SUMO / PTV VISSIM) on Flagged Vulnerable Corridors     |
|      - Virtual Stress-Testing of Traffic Signal Retiming, Lane Segregation & Roundabout Conversions|
+----------------------------------------------------------------------------------------------------+
```

---

## Core Features

- **National Longitudinal Trends (2014–2020):** Multi-year accident volume, fatality trajectory, and Year-over-Year (YoY) growth calculations across 36 Indian States and UTs.
- **50 Million-Plus Cities Vulnerability Quadrants:** Interactive scatter matrix mapping Crash Volume against **Accident Severity Index (ASI)** to detect high-lethality corridors.
- **Infrastructure & Contributing Factors Analysis:** Empirical breakdown of road classifications (NH, SH, Arterials), junction configurations (4-arm, T-junction, roundabouts), weather conditions, and 24-hour diurnal patterns.
- **Vulnerable Road User (VRU) Diagnostics:** Quantifying the fatality exposure of pedestrians, motorized two-wheelers, and cyclists (>53% of national casualties).
- **Indian Road Congress (IRC) Engineering Standards Matrix:** Mapping high-risk conditions to **IRC:37** (Flexible Pavements), **IRC:58** (Rigid Concrete Pavements), **IRC:SP:84/87** (Highways), and specialized surface materials (Stone Matrix Asphalt [SMA], High-Friction Surface Treatments [HFST]).
- **Edge-Sensor CCTV Vehicle Counting PoC:** Privacy-compliant computer vision module with virtual tripwire vehicle classification, traffic flow estimation, and ground-truth validation.

---

## Technology Stack

- **Core Language:** Python 3.13
- **Data Engineering & Analytics:** `pandas`, `numpy`
- **Interactive Visualizations:** `plotly`, `seaborn`, `matplotlib`
- **Web Dashboard:** `streamlit`
- **Computer Vision Prototype:** `opencv-python`
- **Testing & Quality Assurance:** `pytest`

---

## Repository Structure

```
AICTE-IBM-SkillsBuild-BharatCares-Data-Analytics-with-AI-Internship/
├── assets/                       # Video feeds, diagrams, sample assets
│   └── sample_traffic_feed.mp4
├── dashboard/                    # Multi-Page Streamlit Dashboard
│   ├── app.py                    # Main dashboard landing page
│   ├── styles.css                # Polished enterprise UI theme
│   └── pages/
│       ├── 1_India_Overview.py
│       ├── 2_Geographical_Analysis.py
│       ├── 3_Road_Safety_Factors.py
│       ├── 4_Urban_Planning_Insights.py
│       └── 5_CCTV_Observation_PoC.py
├── data/
│   ├── raw/                      # Verified MoRTH TRW source datasets
│   └── processed/                # Cleaned, standardized CSV outputs & audit log
├── docs/                         # Technical documentation & engineering guidelines
│   ├── data_dictionary.md
│   └── irc_engineering_guidelines.md
├── notebooks/                    # Jupyter notebooks for interactive analysis
│   └── 01_exploratory_data_analysis.ipynb
├── reports/                      # Full academic & internship project report
│   └── project_summary_report.md
├── src/                          # Core Python processing modules
│   ├── __init__.py
│   ├── data_builder.py           # Raw dataset generator script
│   ├── data_loader.py            # Dataset loader and schema validator
│   ├── data_cleaner.py           # Reproducible data cleaning pipeline
│   ├── kpi_calculator.py         # Standardized KPI engine
│   ├── eda_generator.py          # High-resolution figure exporter
│   └── cctv_tracker.py           # CCTV vehicle counting & evaluation
├── tests/                        # Automated unit tests
│   ├── __init__.py
│   └── test_kpis.py
├── visuals/                      # Exported high-resolution EDA figures
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/Aarya-505/AICTE-IBM-SkillsBuild-BharatCares-Data-Analytics-with-AI-Internship.git
cd AICTE-IBM-SkillsBuild-BharatCares-Data-Analytics-with-AI-Internship
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Data Ingestion & Cleaning Pipeline
```bash
python src/data_builder.py
python src/data_cleaner.py
```

### 4. Run Automated Unit Tests
```bash
python -m pytest tests/
```

### 5. Launch the Interactive Web Dashboard
```bash
streamlit run dashboard/app.py
```
Open your browser and navigate to: `http://localhost:8501`

---

## AICTE | IBM SkillsBuild | BharatCares Submission Deliverables

| Required File | Format | File Name | Description |
| :--- | :--- | :--- | :--- |
| **Code File** | `.ipynb` | `AaryaMandke_RoadSafeIndia.ipynb` | Fully executed, self-contained Jupyter notebook containing data cleaning, KPIs, statistical plots, and CV PoC. |
| **Requirements File** | `.txt` | `requirements.txt` | Complete list of all Python dependencies required to run the project. |
| **Project Report** | `.docx` | `AaryaMandke_ProjectReport.docx` | Comprehensive academic & technical project documentation formatted in Microsoft Word (.docx). |
| **README File** | `.md` | `README.md` | Full repository overview, dataset links, tech stack, setup instructions, and key insights. |

---

## Data Grounding & Dataset Links
Official datasets ingested, standardized, and analyzed in this project:
- **MoRTH Official Publications:** [Transport Research Wing (TRW) - Road Accidents in India](https://morth.nic.in/road-accidents-in-india)
- **Open Government Data (OGD) Portal:** [data.gov.in Road Safety Datasets](https://data.gov.in/)
- **Processed & Raw Repository Data:** Ingested in the [`data/raw/`](data/raw/) and [`data/processed/`](data/processed/) directories.

---

## Author
**Aarya Mandke**  
Computer Engineering Student  
GitHub: [@Aarya-505](https://github.com/Aarya-505)  
*AICTE IBM SkillsBuild BharatCares Data Analytics with AI Internship Project (September 2026)*
