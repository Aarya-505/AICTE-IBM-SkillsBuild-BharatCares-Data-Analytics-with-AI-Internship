"""
RoadSafe India - Page 2: Geographical & 50 Million-Plus Cities Analysis
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

from src.kpi_calculator import KPICalculator

st.set_page_config(page_title="Geographical & City Analysis | RoadSafe India", page_icon="🏙️", layout="wide")

# Custom CSS
css_path = os.path.join(project_root, "dashboard", "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.html(f"<style>{f.read()}</style>")

st.title("🏙️ Geographical & 50 Million-Plus Cities Road Safety Analysis")
st.caption("Urban-level comparative diagnostics across India's largest metropolitan centers (2020).")

# Load Cities Data
@st.cache_data
def load_cities():
    path = os.path.join(project_root, "data", "processed", "cleaned_million_plus_cities.csv")
    return pd.read_csv(path)

df_cities = load_cities()

# Summary Metrics
city_summary = KPICalculator.generate_city_kpis(df_cities)

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Total Million-Plus Cities", f"{city_summary['total_cities']}")
with m2:
    st.metric("Total Recorded Urban Crashes", f"{city_summary['total_accidents']:,}")
with m3:
    st.metric("Total Urban Fatalities", f"{city_summary['total_fatalities']:,}")
with m4:
    st.metric("Average Urban Severity Index", f"{city_summary['avg_severity_index']:.1f}")

st.markdown("---")

# Section 1: Single City Deep-Dive Profile
st.subheader("🔍 Individual City Road Safety Card")
selected_city = st.selectbox(
    "Select a City to Inspect:",
    options=df_cities["City"].tolist(),
    index=0
)

city_kpi = KPICalculator.generate_city_kpis(df_cities, city_name=selected_city)

if city_kpi:
    c_col1, c_col2, c_col3, c_col4 = st.columns(4)
    with c_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Reported Crashes</div>
            <div class="metric-value">{city_kpi['total_accidents']:,}</div>
            <div class="metric-subtext">National Rank: <strong>#{city_kpi['rank_accidents']}</strong> / 50</div>
        </div>
        """, unsafe_allow_html=True)
    with c_col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Persons Killed (Fatalities)</div>
            <div class="metric-value" style="color: #ef4444;">{city_kpi['fatalities']:,}</div>
            <div class="metric-subtext">National Rank: <strong>#{city_kpi['rank_fatalities']}</strong> / 50</div>
        </div>
        """, unsafe_allow_html=True)
    with c_col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Severity Index</div>
            <div class="metric-value" style="color: #fbbf24;">{city_kpi['severity_index']:.1f}</div>
            <div class="metric-subtext">Rank by Severity: <strong>#{city_kpi['rank_severity']}</strong></div>
        </div>
        """, unsafe_allow_html=True)
    with c_col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Injury Rate / 100 Crashes</div>
            <div class="metric-value" style="color: #38bdf8;">{city_kpi['injury_per_100']:.1f}</div>
            <div class="metric-subtext">State: <strong>{city_kpi['state']}</strong></div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Section 2: Crash Volume vs Severity Quadrant Matrix
st.subheader("🎯 Urban Crash Vulnerability Matrix (Crash Volume vs Severity Index)")
st.markdown("""
* **Top-Right Quadrant (Critical Zone):** High Crash Volume & High Severity Index (Urgent multi-modal & engineering interventions).
* **Bottom-Right Quadrant (High Exposure Zone):** High Crash Volume with Lower Severity (Dense urban traffic, high property damage/minor injury).
* **Top-Left Quadrant (High Lethality Corridor):** Lower Crash Volume but High Fatality Rate (High-speed ring roads, poor night lighting).
""")

fig_scatter = px.scatter(
    df_cities,
    x="Total_Accidents",
    y="Severity_Index",
    size="Persons_Killed",
    color="Severity_Index",
    hover_name="City",
    hover_data=["State", "Persons_Killed", "Persons_Injured", "Rank_Accidents"],
    color_continuous_scale="Turbo",
    labels={
        "Total_Accidents": "Total Recorded Accidents (Crash Volume)",
        "Severity_Index": "Accident Severity Index (Fatalities per 100 Crashes)"
    },
    text="City"
)
fig_scatter.update_traces(textposition='top right', textfont_size=9)
fig_scatter.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15,23,42,0.6)",
    height=550,
    margin=dict(l=20, r=20, t=30, b=20)
)
st.plotly_chart(fig_scatter, use_container_width=True)

# Section 3: Top & Bottom 10 Comparison
col_c1, col_c2 = st.columns(2)

with col_c1:
    st.subheader("🚨 Top 10 Cities by Crash Volume")
    top_acc = df_cities.sort_values(by="Total_Accidents", ascending=False).head(10)
    fig_top_acc = px.bar(
        top_acc, x="Total_Accidents", y="City", orientation="h",
        color="Total_Accidents", color_continuous_scale="Blues",
        labels={"Total_Accidents": "Crashes", "City": ""}
    )
    fig_top_acc.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,23,42,0.6)", height=400)
    st.plotly_chart(fig_top_acc, use_container_width=True)

with col_c2:
    st.subheader("⚠️ Top 10 Cities by Severity Index")
    top_sev = df_cities.sort_values(by="Severity_Index", ascending=False).head(10)
    fig_top_sev = px.bar(
        top_sev, x="Severity_Index", y="City", orientation="h",
        color="Severity_Index", color_continuous_scale="Reds",
        labels={"Severity_Index": "Fatalities / 100 Crashes", "City": ""}
    )
    fig_top_sev.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,23,42,0.6)", height=400)
    st.plotly_chart(fig_top_sev, use_container_width=True)

# Data Table & Export
with st.expander("📋 View Complete 50 Million-Plus Cities Dataset"):
    st.dataframe(df_cities, use_container_width=True)
    csv_bytes = df_cities.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download 50 Cities Processed CSV",
        data=csv_bytes,
        file_name="roadsafe_india_50_cities_2020.csv",
        mime="text/csv"
    )
