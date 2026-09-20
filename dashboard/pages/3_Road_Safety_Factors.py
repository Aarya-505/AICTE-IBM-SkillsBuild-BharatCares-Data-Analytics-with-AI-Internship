"""
RoadSafe India - Page 3: Road Safety & Infrastructure Contributing Factors
"""

import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configure paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

st.set_page_config(page_title="Contributing Factors | RoadSafe India", page_icon="⚙️", layout="wide")

# Custom CSS
css_path = os.path.join(project_root, "dashboard", "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.html(f"<style>{f.read()}</style>")

st.title("⚙️ Road Infrastructure, Environmental & Behavioral Contributing Factors")
st.caption("Empirical breakdown of accident causation, geometric configurations, and road user vulnerability.")

# Load Datasets
@st.cache_data
def load_factor_data():
    factors_df = pd.read_csv(os.path.join(project_root, "data", "processed", "cleaned_contributing_factors.csv"))
    time_df = pd.read_csv(os.path.join(project_root, "data", "processed", "cleaned_time_slots.csv"))
    return factors_df, time_df

df_factors, df_time = load_factor_data()

# Factor Category Tabs
t1, t2, t3, t4, t5 = st.tabs([
    "🛣️ Road & Junction Geometry",
    "🚶 Vulnerable Road Users (VRUs)",
    "🌧️ Weather & Road Surface",
    "⏰ 24-Hour Diurnal Patterns",
    "🚦 Violations & Human Causes"
])

# -------------------------------------------------------------
# Tab 1: Road & Junction Geometry
# -------------------------------------------------------------
with t1:
    st.subheader("🛣️ Infrastructure & Geometric Configuration Analysis")
    
    col_r1, col_r2 = st.columns(2)
    
    with col_r1:
        st.markdown("#### Road Classification Distribution")
        road_class_df = df_factors[df_factors["Category_Type"] == "Road Classification"]
        fig_rc = px.pie(
            road_class_df, values="Total_Accidents", names="Factor_Name",
            color_discrete_sequence=["#38bdf8", "#818cf8", "#c084fc"],
            hole=0.45,
            title="Crashes by Road Hierarchy"
        )
        fig_rc.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", height=350)
        st.plotly_chart(fig_rc, use_container_width=True)
        
        st.markdown("""
        > **National Highway Impact**: While National Highways account for roughly **2-3%** of India's total road network length, they account for over **30%** of total reported crashes and over **36%** of total fatalities due to high operating speeds and mixed non-motorized traffic.
        """)

    with col_r2:
        st.markdown("#### Junction Type Breakdown")
        junc_df = df_factors[df_factors["Category_Type"] == "Junction Configuration"].sort_values(by="Total_Accidents", ascending=True)
        fig_junc = px.bar(
            junc_df, x="Total_Accidents", y="Factor_Name", orientation="h",
            color="Severity_Index", color_continuous_scale="Reds",
            labels={"Total_Accidents": "Recorded Accidents", "Factor_Name": ""},
            title="Accidents by Junction Configuration"
        )
        fig_junc.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,23,42,0.6)", height=350)
        st.plotly_chart(fig_junc, use_container_width=True)
        
        st.markdown("""
        > **Junction Engineering Finding**: **4-Arm Cross Junctions** and **T-Junctions** represent the highest crash risk among formal intersections due to conflict points and inadequate sight triangles.
        """)

# -------------------------------------------------------------
# Tab 2: Vulnerable Road Users (VRUs) & Vehicle Types
# -------------------------------------------------------------
with t2:
    st.subheader("🚶 Vulnerable Road Users & Modal Split")
    
    user_df = df_factors[df_factors["Category_Type"] == "Road User Type"].sort_values(by="Persons_Killed", ascending=False)
    
    col_u1, col_u2 = st.columns([6, 4])
    
    with col_u1:
        fig_vru = px.bar(
            user_df, x="Factor_Name", y=["Persons_Killed", "Persons_Injured"],
            barmode="group",
            color_discrete_map={"Persons_Killed": "#ef4444", "Persons_Injured": "#38bdf8"},
            labels={"value": "Casualties Count", "Factor_Name": "Road User / Vehicle Category"},
            title="Casualties by Road User Category"
        )
        fig_vru.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,23,42,0.6)", height=400)
        st.plotly_chart(fig_vru, use_container_width=True)

    with col_u2:
        fig_donut = px.pie(
            user_df, values="Persons_Killed", names="Factor_Name",
            color_discrete_sequence=px.colors.qualitative.Prism,
            hole=0.5,
            title="Fatality Share by Mode of Transport"
        )
        fig_donut.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", height=400)
        st.plotly_chart(fig_donut, use_container_width=True)

    st.info("💡 **Urban Planning Imperative**: Two-wheelers and pedestrians constitute over **50%** of all road fatalities in India. Urban design must prioritize segregated pedestrian footpaths, tactile paving, and protected cycle/2-wheeler tracks.")

# -------------------------------------------------------------
# Tab 3: Weather & Road Surface
# -------------------------------------------------------------
with t3:
    st.subheader("🌧️ Environmental Conditions & Surface Deterioration")
    
    col_w1, col_w2 = st.columns(2)
    
    with col_w1:
        st.markdown("#### Atmospheric / Weather Conditions")
        weather_df = df_factors[df_factors["Category_Type"] == "Weather Condition"].sort_values(by="Total_Accidents", ascending=False)
        fig_weather = px.bar(
            weather_df, x="Factor_Name", y="Total_Accidents",
            color="Severity_Index", color_continuous_scale="Viridis",
            labels={"Total_Accidents": "Accidents", "Factor_Name": "Weather"},
            title="Crashes by Weather Condition"
        )
        fig_weather.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,23,42,0.6)", height=360)
        st.plotly_chart(fig_weather, use_container_width=True)

    with col_w2:
        st.markdown("#### Road Features & Surface Quality")
        surf_df = df_factors[df_factors["Category_Type"] == "Road Surface Feature"].sort_values(by="Total_Accidents", ascending=False)
        fig_surf = px.bar(
            surf_df, x="Factor_Name", y="Total_Accidents",
            color="Severity_Index", color_continuous_scale="Plasma",
            labels={"Total_Accidents": "Accidents", "Factor_Name": "Road Feature"},
            title="Crashes by Road Surface Feature"
        )
        fig_surf.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,23,42,0.6)", height=360)
        st.plotly_chart(fig_surf, use_container_width=True)

# -------------------------------------------------------------
# Tab 4: 24-Hour Diurnal Patterns
# -------------------------------------------------------------
with t4:
    st.subheader("⏰ Diurnal (24-Hour) Crash & Lethality Rhythm")
    
    fig_diurnal = go.Figure()
    fig_diurnal.add_trace(go.Bar(
        x=df_time["Time_Slot"], y=df_time["Total_Accidents"],
        name="Total Reported Crashes", marker_color="#38bdf8", opacity=0.8
    ))
    fig_diurnal.add_trace(go.Scatter(
        x=df_time["Time_Slot"], y=df_time["Severity_Index"],
        name="Severity Index (Fatalities/100 Crashes)", mode="lines+markers",
        line=dict(color="#f59e0b", width=3.5), yaxis="y2"
    ))
    fig_diurnal.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.6)",
        yaxis=dict(title="Accident Volume"),
        yaxis2=dict(title="Severity Index (Lethality)", overlaying="y", side="right"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=30, b=20),
        height=420
    )
    st.plotly_chart(fig_diurnal, use_container_width=True)

    st.markdown("""
    * **Crash Volume Peak:** Occurs during the **18:00 - 21:00 (Evening Rush / Night Window)** due to high mixed vehicular congestion, fading ambient daylight, and fatigue.
    * **Lethality Peak:** Late-night and early-morning slots (**00:00 - 06:00**) exhibit higher **Severity Index** due to higher uninhibited travel speeds and delayed emergency response (Golden Hour delays).
    """)

# -------------------------------------------------------------
# Tab 5: Violations & Human Causes
# -------------------------------------------------------------
with t5:
    st.subheader("🚦 Human Contributing Factors & Rule Violations")
    
    causes_df = df_factors[df_factors["Category_Type"] == "Traffic Cause"].sort_values(by="Total_Accidents", ascending=False)
    
    col_h1, col_h2 = st.columns([6, 4])
    
    with col_h1:
        fig_cause = px.bar(
            causes_df, x="Total_Accidents", y="Factor_Name", orientation="h",
            color="Category_Accident_Share_%", color_continuous_scale="OrRd",
            labels={"Total_Accidents": "Recorded Violations / Crashes", "Factor_Name": ""},
            title="Reported Contributing Violations"
        )
        fig_cause.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,23,42,0.6)", height=380)
        st.plotly_chart(fig_cause, use_container_width=True)

    with col_h2:
        st.markdown("""
        ### Key Behavioral Observations:
        * **Over-speeding:** Accounts for over **70%** of all recorded human-related crash causes in MoRTH records.
        * **Wrong-Side Driving & Lane Indiscipline:** Major source of head-on collisions at medians and uncontrolled openings.
        * **Mobile Phone Distraction:** Rapidly emerging risk factor across urban multi-lane corridors.
        """)

# Export Button
with st.expander("📋 Download Factors Dataset"):
    csv_bytes = df_factors.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Contributing Factors CSV",
        data=csv_bytes,
        file_name="roadsafe_india_contributing_factors_2020.csv",
        mime="text/csv"
    )
