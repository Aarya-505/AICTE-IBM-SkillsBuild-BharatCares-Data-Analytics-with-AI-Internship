"""
RoadSafe India - Page 4: Urban Planning & Civil Engineering Decision Support
"""

import os
import sys
import streamlit as st
import pandas as pd

# Configure paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

st.set_page_config(page_title="Urban Planning & Engineering | RoadSafe India", page_icon="🏗️", layout="wide")

# Custom CSS
css_path = os.path.join(project_root, "dashboard", "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.html(f"<style>{f.read()}</style>")

st.title("🏗️ Urban Planning, Pavement Materials & Digital Twin Integration")
st.caption("Translating empirical road-safety intelligence into civil engineering standards and urban planning interventions.")

# -------------------------------------------------------------
# 1. Urban Planning Decision Support Matrix
# -------------------------------------------------------------
st.subheader("📋 1. Evidence-Based Urban Planning Action Matrix")
st.markdown("Connecting empirical findings to target stakeholders, geometric redesign, and policy interventions:")

planning_data = [
    {
        "Observed Evidence": "Pedestrians & 2-Wheelers constitute >50% of total fatalities (VRU vulnerability).",
        "Planning Interpretation": "Lack of segregated right-of-way (ROW) and inadequate non-motorized transport (NMT) infrastructure.",
        "Primary Stakeholder": "Urban Local Bodies (ULBs) & Smart City SPVs",
        "Recommended Intervention": "Construct continuous, barrier-segregated footpaths (min 1.8m width), grade-separated mid-block pedestrian crossings, and dedicated two-wheeler/cycle lanes.",
        "Target Monitoring KPI": "VRU Fatality Share Reduction (%)"
    },
    {
        "Observed Evidence": "4-Arm Cross Junctions and T-Junctions account for over 1 lakh reported crashes.",
        "Planning Interpretation": "Conflicting traffic streams, excessive curb return radii encouraging high turn speeds, and absence of channelizing islands.",
        "Primary Stakeholder": "Municipal Traffic Police & Public Works Dept (PWD)",
        "Recommended Intervention": "Convert high-speed uncontrolled 4-arm junctions into modern roundabouts or compact signalized intersections with pedestrian refuge islands.",
        "Target Monitoring KPI": "Junction Crash Frequency Reduction (%)"
    },
    {
        "Observed Evidence": "Accident volume peaks between 18:00–21:00, while severity peaks between 00:00–06:00.",
        "Planning Interpretation": "Evening congestion friction vs late-night high-speed freight movement with reduced visibility.",
        "Primary Stakeholder": "City Development Authorities & Power DISCOMs",
        "Recommended Intervention": "Upgrade corridor illumination to LED smart lighting (>30 Lux on arterials), implement dynamic variable speed limits (VSL) during night hours, and deploy automated speed cameras.",
        "Target Monitoring KPI": "Night Severity Index Reduction"
    },
    {
        "Observed Evidence": "National & State Highways contribute >60% of all fatalities despite lower length share.",
        "Planning Interpretation": "High speed differentials between long-haul freight and local rural/peri-urban non-motorized traffic.",
        "Primary Stakeholder": "NHAI, MoRTH & State PWD Highways",
        "Recommended Intervention": "Construct grade-separated service roads in built-up bypass areas, provide crash barriers (W-beam/thrie-beam) on curves, and implement access control.",
        "Target Monitoring KPI": "Highway Fatality per 100km Rate"
    }
]

df_plan = pd.DataFrame(planning_data)
st.dataframe(df_plan, use_container_width=True)

st.markdown("---")

# -------------------------------------------------------------
# 2. Road Design & Pavement Material Assessment (IRC Guidelines)
# -------------------------------------------------------------
st.subheader("🛣️ 2. Indian Road Congress (IRC) Materials & Design Support")
st.markdown("""
> [!IMPORTANT]
> **Engineering Decision Support Boundary:** Accident records identify *where* distress or safety vulnerabilities occur. Actual pavement thickness, subgrade design, and material specification require on-site engineering tests (CBR, MSA, BPN) in accordance with the Indian Road Congress standards below:
""")

col_m1, col_m2 = st.columns(2)

with col_m1:
    st.markdown("""
    #### 📐 Applicable Indian Standards (IRC Framework)
    * **IRC:37-2018:** *Guidelines for the Design of Flexible Pavements* (Defines sub-base, Dense Bituminous Macadam [DBM], and Bituminous Concrete [BC] wearing courses based on Million Standard Axles [MSA] and California Bearing Ratio [CBR]).
    * **IRC:58-2015:** *Guidelines for the Design of Plain Jointed Rigid Pavements for Highways* (Concrete pavements for heavy commercial loading zones and toll plazas).
    * **IRC:SP:84 / IRC:SP:87:** *Manual of Specifications & Standards for 4/6-laning of Highways*.
    * **IRC:67-2012 & IRC:35-2015:** *Code of Practice for Road Signs and Thermoplastic Road Markings*.
    * **IRC:SP:88-2019:** *Manual on Road Safety Audit (RSA)*.
    """)

with col_m2:
    st.markdown("""
    #### 🧪 Recommended Surface Materials for High-Risk Zones
    * **High-Friction Surface Treatment (HFST):** Epoxy-bonded calcined bauxite aggregate on sharp curves, bridge approaches, and signalized junction approaches (increases Skid Resistance Index).
    * **Stone Matrix Asphalt (SMA) (IRC:SP:79):** Gap-graded bituminous mix with cellulose fibers for heavy-load rutting resistance on expressways and urban bus lanes.
    * **Micro-surfacing / Slurry Seal (IRC:SP:81):** Cold-mix polymer-modified bitumen emulsion for rejuvenating aged asphalt and restoring skid texture without structural rebuilding.
    * **Porous Friction Courses (PFC):** Open-graded friction course to evacuate rainwater rapidly, eliminating hydroplaning in high-rainfall monsoon corridors.
    """)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 3. Mandatory Engineering Site Survey Checklist
# -------------------------------------------------------------
st.subheader("📝 3. Mandatory Pre-Engineering Survey Checklist")
st.markdown("Before implementing physical civil redesign on high-risk corridors identified by RoadSafe India, the following engineering tests must be conducted:")

c_chk1, c_chk2 = st.columns(2)

with c_chk1:
    st.checkbox("✅ **Geotechnical Subgrade Soil Testing:** Measure California Bearing Ratio (CBR) and Liquid Limit/Plasticity Index.", value=True)
    st.checkbox("✅ **Traffic Exposure & Axle Load Survey:** Conduct 7-day classified volume count (AADT) and Weigh-in-Motion (WIM) for Vehicle Damage Factor (VDF).", value=True)
    st.checkbox("✅ **Pavement Condition Survey (PCI):** Falling Weight Deflectometer (FWD) for structural strength & Network Survey Vehicle (NSV) for roughness (IRI).", value=True)

with c_chk2:
    st.checkbox("✅ **Surface Skid Resistance Testing:** British Pendulum Number (BPN) test on wet pavement sections.", value=True)
    st.checkbox("✅ **Hydrological & Drainage Audit:** Stormwater runoff modeling and culvert capacity check for monsoon flood mitigation.", value=True)
    st.checkbox("✅ **Sightline & Geometric Audit:** 3D sight distance verification (Stopping Sight Distance [SSD] and Intersection Sight Distance [ISD]).", value=True)

st.markdown("---")

# -------------------------------------------------------------
# 4. Future Scope: Advanced Digital Infrastructure & Traffic Simulation
# -------------------------------------------------------------
st.subheader("🌐 4. Future Scope: Advanced Digital Infrastructure & Traffic Simulation")
st.markdown("""
How **RoadSafe India** scales into a future-ready multi-tiered intelligent transportation and planning architecture:
""")

st.markdown("""
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
|   3. SIMULATION & INTERVENTION LAYER (Digital Twin Engine)                                         |
|      - Microscopic Traffic Flow Simulation (SUMO / PTV VISSIM) on Flagged Vulnerable Corridors     |
|      - Virtual Stress-Testing of Traffic Signal Retiming, Lane Segregation & Roundabout Conversions|
+----------------------------------------------------------------------------------------------------+
```
""")
