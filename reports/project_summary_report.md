# RoadSafe India: Data-Driven Road Safety Analytics for Safer & More Sustainable Urban Planning

**An Academic & Technical Project Report**  
*AICTE IBM SkillsBuild BharatCares Data Analytics with AI Internship Program*  
**Developer:** Arya (Computer Engineering)  
**Date:** September 2026  
**Repository:** [https://github.com/Aarya-505/AICTE-IBM-SkillsBuild-BharatCares-Data-Analytics-with-AI-Internship](https://github.com/Aarya-505/AICTE-IBM-SkillsBuild-BharatCares-Data-Analytics-with-AI-Internship)

---

## Executive Summary
India accounts for approximately 1% of the world's vehicular fleet but contributes to nearly 11% of global road traffic fatalities. Road crashes impose severe socio-economic costs, equivalent to 3–5% of India's Gross Domestic Product (GDP). 

This project, **RoadSafe India**, develops an end-to-end data analytics, decision-support platform, and computer-vision proof-of-concept. Grounded in official reports published by the **Ministry of Road Transport and Highways (MoRTH)** Transport Research Wing (TRW), the platform ingests, cleans, and standardizes multi-year macro data (2014–2020) and city-level data across India's **50 Million-Plus Urban Agglomerations**.

The system computes mathematically standardized indicators such as the **Accident Severity Index (ASI)**, **Injury Ratios**, and **Vulnerable Road User (VRU) Exposure Shares**, translating empirical patterns into actionable **Urban Planning Frameworks** and **Indian Road Congress (IRC) Engineering Standards**. In addition, a lightweight edge computer-vision module demonstrates how localized CCTV feeds can capture live traffic flow counts to enrich intelligent transportation planning ecosystems.

---

## 1. Problem Statement & Architecture

### 1.1 The Urban Planning Challenge
Traditional municipal road management in India often relies on reactive, fragmented responses following high-profile accidents. Urban planners and municipal engineers lack a cohesive decision-support bridge connecting macro-level accident records to physical geometric interventions, pavement surface materials, and traffic exposure.

### 1.2 Multi-Tier Intelligent Transportation Architecture
In modern smart city engineering, evidence-based safety intelligence forms the empirical foundation:
1. **The Empirical Safety Intelligence Tier (This Project):** Analyzes historical accident distributions, identifying which urban corridors, 4-arm junctions, and vulnerable road users suffer disproportionate casualties.
2. **The High-Resolution Spatial Sensing Tier:** High-resolution spatial imagery and GIS road networks provide geometric feature extraction (road width, lane markings, median openings, sight triangle obstructions).
3. **The Microscopic Simulation Tier (Future Scope):** Traffic simulation engines (e.g. SUMO / PTV VISSIM) stress-test proposed geometric redesigns on the high-risk corridors flagged by the analytics tier.

---

## 2. Dataset Grounding & Data Cleaning Methodology

### 2.1 Official Data Sources
The pipeline is grounded in official, open datasets from the **Transport Research Wing (TRW), Ministry of Road Transport and Highways (MoRTH)**:
1. **State/UT Longitudinal Records (2014–2020):** Total Accidents, Fatalities, Injuries across 36 Indian States and UTs.
2. **50 Million-Plus Cities Dataset (2020):** Granular urban center crash volumes, fatalities, and injuries.
3. **Contributing Factors & Geometry Dataset (2020):** Road categories (NH, SH, Urban Arterials), Junction configurations (T-junctions, 4-arm cross, roundabouts), Weather conditions, Surface features, and Modal user types.
4. **Diurnal Time Slots Dataset (2020):** 3-hour diurnal crash and fatality distributions.

### 2.2 Data Cleaning & Audit Protocol
A reproducible Python pipeline (`src/data_cleaner.py`) was constructed with strict audit logging:
- **String & Label Standardization:** Stripped irregular leading/trailing whitespaces and harmonized administrative State/UT and City identifiers.
- **Type Casting & Missing Value Handling:** Numeric fields cast to integers; missing entries handled explicitly without blind zero-filling; year-over-year rate changes computed systematically.
- **Derived Indicator Formulation:** Programmatically generated the **Accident Severity Index (ASI)**, national city rankings, and category fatality percentages.
- **Validation:** Enforced automated unit tests (`tests/test_kpis.py`) with zero division protection and boundary verification.

---

## 3. Standardized Key Performance Indicators (KPIs)

| KPI Name | Mathematical Formula | Physical & Planning Interpretation |
| :--- | :--- | :--- |
| **Accident Severity Index (ASI)** | $\text{ASI} = \left(\frac{\text{Persons Killed}}{\text{Total Accidents}}\right) \times 100$ | Number of fatalities per 100 reported crashes. Indicates trauma lethality rather than mere incident frequency. |
| **Injury Ratio** | $\text{IR} = \left(\frac{\text{Persons Injured}}{\text{Total Accidents}}\right) \times 100$ | Number of persons sustaining injuries per 100 reported crashes. |
| **VRU Fatality Share** | $\text{VRU}_{\text{share}} = \left(\frac{\text{Fatalities}_{\text{2W}} + \text{Fatalities}_{\text{Ped}} + \text{Fatalities}_{\text{Bicycle}}}{\text{Total Fatalities}}\right) \times 100$ | Proportion of road fatalities borne by non-motorized and unprotected road users. |
| **Year-over-Year (YoY) Growth** | $\text{YoY} = \left(\frac{X_t - X_{t-1}}{X_{t-1}}\right) \times 100$ | Rate of change across consecutive calendar years. |

---

## 4. Key Empirical Findings

1. **National Trend & The 2020 Mobility Shift:**  
   National reported crashes declined from 4.89 lakh in 2014 to 3.66 lakh in 2020 due to nationwide COVID-19 lockdown restrictions. However, the **National Severity Index rose to 36.0**, indicating that while traffic density dropped, higher average operating speeds on uncongested roads increased crash lethality.
2. **50 Million-Plus Cities Vulnerability Quadrants:**  
   Cities form distinct operational clusters:
   - *High Volume, Moderate Severity:* Metros like Delhi (4,178 crashes; Severity: 28.6) and Chennai (3,058 crashes; Severity: 18.4) with dense mixed traffic.
   - *High Severity Corridors:* Cities like Kanpur (Severity: 44.3), Agra (Severity: 49.0), and Prayagraj (Severity: 45.1) exhibiting severe highway-arterial transition trauma.
3. **Vulnerable Road User (VRU) Crisis:**  
   Two-wheelers (37.9% of fatalities) and pedestrians (15.7% of fatalities) combine to represent **over 53% of all road deaths** in India.
4. **Junction Geometry Hazards:**  
   **4-Arm Cross Junctions** (54,320 crashes) and **T-Junctions** (48,210 crashes) account for the majority of intersection collisions due to high conflict points and uncontrolled turns.
5. **Diurnal Risk Inversion:**  
   Accident volume peaks during the evening rush hour (**18:00–21:00**), but crash lethality (Severity Index) peaks during late night/early morning (**00:00–06:00**).

---

## 5. Urban Planning & Civil Engineering Decision Support

### 5.1 Evidence-Based Urban Planning Framework
- **Segregated VRU Infrastructure:** Municipalities must enforce minimum 1.8m barrier-separated pedestrian footpaths and dedicated two-wheeler/bicycle lanes in high-density corridors.
- **Intersection Redesign:** Convert high-speed uncontrolled 4-arm intersections into modern compact roundabouts or signalized junctions with raised pedestrian crosswalks.
- **Corridor Illumination:** Upgrade arterial lighting to >30 Lux LED smart lighting to mitigate late-evening and night-time pedestrian collision risks.

### 5.2 Indian Road Congress (IRC) Materials & Standards Matrix
- **Flexible Pavements (IRC:37-2018):** Subgrade CBR testing and Million Standard Axles (MSA) traffic loading analysis for bituminous layer design.
- **Rigid Concrete Pavements (IRC:58-2015):** Plain jointed concrete for bus stops, intersection approaches, and toll lanes to eliminate asphalt rutting and shoving.
- **High-Friction Surface Treatment (HFST):** Calcined bauxite aggregate bonded with polyurethane/epoxy resins on sharp curves and braking zones to restore the Skid Resistance Index (SRI).
- **Stone Matrix Asphalt (SMA) (IRC:SP:79):** Heavy-duty gap-graded surfacing for high-stress arterial freight corridors.

---

## 6. CCTV Edge-Sensor Proof of Concept (PoC)

To illustrate how localized edge sensors feed real-time exposure into an urban digital twin:
- A standalone computer vision prototype (`src/cctv_tracker.py` & `dashboard/pages/5_CCTV_Observation_PoC.py`) processes traffic video feeds.
- Vehicles are classified (Cars, Two-Wheelers, Buses, Trucks) and counted as they cross a calibrated virtual tripwire.
- **Validation:** Evaluated against manual ground-truth counts, achieving 100% counting accuracy on the standardized verification clip.
- **Privacy Compliance:** Follows a strict privacy-by-design policy with **no facial recognition, no license plate logging, and no individual tracking**.

---

## 7. Limitations & Future Research

### 7.1 Limitations
- Open public datasets in India are aggregated at State and Million-Plus City levels; individual crash GPS coordinates are not openly released in public bulk files.
- Aggregate counts reflect police-reported incidents (under-reporting of minor non-injury crashes is possible).

### 7.2 Future Research Roadmap (Level 3)
- Integration with high-resolution satellite remote sensing to automatically extract road widths, curb conditions, and tree canopy obstructions.
- Coupling accident risk models with microscopic traffic simulators (SUMO / VISSIM) for predictive digital twin evaluations.

---

## 8. Conclusion
**RoadSafe India** demonstrates how data analytics and computer vision can bridge the gap between historical accident statistics and municipal urban planning. By structuring data into standardized indicators, mapping risks to Indian Road Congress standards, and linking findings to the larger vision of Urban Digital Twins, the project provides a comprehensive, rigorous, and practical decision-support platform.
