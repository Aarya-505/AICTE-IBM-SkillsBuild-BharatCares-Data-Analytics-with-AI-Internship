"""
RoadSafe India - Main Streamlit Dashboard Entrypoint
Data-Driven Road Safety Analytics for Safer and More Sustainable Urban Planning
"""

import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configure paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.data_loader import DataLoader
from src.kpi_calculator import KPICalculator

# Set Streamlit Page Config
st.set_page_config(
    page_title="RoadSafe India | Road Safety Analytics",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS Design System
css_path = os.path.join(current_dir, "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.html(f"<style>{f.read()}</style>")

# Data Caching
@st.cache_data
def get_datasets():
    loader = DataLoader(raw_dir=os.path.join(project_root, "data", "raw"))
    return {
        "state_trends": pd.read_csv(os.path.join(project_root, "data", "processed", "cleaned_state_ut_trends.csv")),
        "cities": pd.read_csv(os.path.join(project_root, "data", "processed", "cleaned_million_plus_cities.csv")),
        "factors": pd.read_csv(os.path.join(project_root, "data", "processed", "cleaned_contributing_factors.csv")),
        "time_slots": pd.read_csv(os.path.join(project_root, "data", "processed", "cleaned_time_slots.csv"))
    }

try:
    data = get_datasets()
except Exception as e:
    st.error(f"Error loading datasets: {e}. Please ensure data cleaning pipeline has run.")
    st.stop()

# -------------------------------------------------------------
# Enterprise Header & Project Overview
# -------------------------------------------------------------
st.markdown("""
<div class="hero-banner">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem;">
        <div>
            <h1 class="hero-title">🚦 RoadSafe India</h1>
            <div class="hero-subtitle">
                Data-Driven Road Safety Analytics for Safer & Sustainable Urban Planning
            </div>
        </div>
        <div style="display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap;">
            <span class="pill-tag live">● Live Analytics Platform</span>
            <span class="pill-tag accent">MoRTH TRW Verified</span>
        </div>
    </div>
    <div class="hero-meta">
        <span class="pill-tag"><strong>IBM & AICTE Internship Project</strong></span>
        <span>Developer: <strong style="color: #f8fafc;">Arya</strong> (Computer Engineering)</span>
        <span style="color: #64748b;">•</span>
        <span>Data Grounding: <em>Ministry of Road Transport & Highways (MoRTH) & Open Government Data</em></span>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Headline National KPI Cards (2020 Baseline)
# -------------------------------------------------------------
nat_kpis = KPICalculator.generate_national_kpis(data["state_trends"], target_year=2020)
vru_kpis = KPICalculator.generate_vru_kpi(data["factors"])

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Reported Crashes (2020)</div>
        <div class="metric-value">{nat_kpis.get('total_accidents', 0):,}</div>
        <div class="metric-subtext">📉 YoY Change: <strong style="color: #38bdf8;">{nat_kpis.get('accident_yoy_growth_%', 0):.1f}%</strong> (Lockdown impact)</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card danger">
        <div class="metric-title">Total Fatalities (Killed)</div>
        <div class="metric-value" style="color: #f87171;">{nat_kpis.get('total_fatalities', 0):,}</div>
        <div class="metric-subtext">⚠️ Severe trauma exposure across network</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card warning">
        <div class="metric-title">National Severity Index</div>
        <div class="metric-value" style="color: #fbbf24;">{nat_kpis.get('severity_index', 0):.1f}</div>
        <div class="metric-subtext">Fatalities per 100 reported crashes</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card purple">
        <div class="metric-title">Vulnerable Road Users (VRU)</div>
        <div class="metric-value" style="color: #c084fc;">{vru_kpis.get('vru_fatality_share_%', 0):.1f}%</div>
        <div class="metric-subtext">Pedestrians, 2-Wheelers & Cyclists</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# Executive Analytics Row
# -------------------------------------------------------------
col_left, col_right = st.columns([6, 4])

with col_left:
    st.markdown("### 📈 Multi-Year Crash & Fatality Trajectory (2014–2020)")
    trend_df = data["state_trends"].groupby("Year")[["Total_Accidents", "Persons_Killed"]].sum().reset_index()
    trend_df["Severity_Index"] = (trend_df["Persons_Killed"] / trend_df["Total_Accidents"]) * 100
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=trend_df["Year"], y=trend_df["Total_Accidents"],
        name="Total Crashes", mode="lines+markers",
        line=dict(color="#38bdf8", width=3.5),
        marker=dict(size=8, color="#38bdf8", symbol="circle")
    ))
    fig_trend.add_trace(go.Scatter(
        x=trend_df["Year"], y=trend_df["Persons_Killed"],
        name="Fatalities (Killed)", mode="lines+markers",
        line=dict(color="#f43f5e", width=3, dash="dash"),
        marker=dict(size=8, color="#f43f5e", symbol="square")
    ))
    fig_trend.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.6)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#cbd5e1"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, bgcolor="rgba(15,23,42,0.7)"),
        margin=dict(l=10, r=10, t=30, b=20),
        height=350,
        xaxis=dict(showgrid=True, gridcolor="rgba(148, 163, 184, 0.1)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(148, 163, 184, 0.1)")
    )
    st.plotly_chart(fig_trend, use_container_width=True, config={'displayModeBar': False})

with col_right:
    st.markdown("### 🚨 Top 5 High-Severity Cities (Fatalities / 100 Crashes)")
    top_sev = data["cities"].sort_values(by="Severity_Index", ascending=False).head(5)[["City", "State", "Severity_Index", "Persons_Killed"]]
    
    fig_city = px.bar(
        top_sev, x="Severity_Index", y="City", orientation="h",
        color="Severity_Index",
        color_continuous_scale=["#f59e0b", "#f43f5e", "#991b1b"],
        text="Severity_Index",
        labels={"Severity_Index": "ASI Score", "City": ""}
    )
    fig_city.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.6)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#cbd5e1"),
        coloraxis_showscale=False,
        margin=dict(l=10, r=45, t=30, b=20),
        height=350,
        xaxis=dict(showgrid=True, gridcolor="rgba(148, 163, 184, 0.1)"),
        yaxis=dict(showgrid=False)
    )
    fig_city.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    st.plotly_chart(fig_city, use_container_width=True, config={'displayModeBar': False})

# -------------------------------------------------------------
# Future Scope Section (Dedicated to Road Safety Evolution)
# -------------------------------------------------------------
st.markdown("<div style='margin-top: 1.5rem; margin-bottom: 1rem;'></div>", unsafe_allow_html=True)
st.markdown("### 🔮 Future Scope & Engineering Scalability")

s1, s2, s3 = st.columns(3)

with s1:
    st.markdown("""
    <div class="scope-card">
        <div class="scope-icon">🚦</div>
        <div class="scope-heading">Microscopic Traffic & Signal Simulation</div>
        <div class="scope-desc">
            Integration of historical high-severity corridor coordinates with micro-simulation platforms (SUMO / PTV VISSIM) for virtual stress-testing of traffic signal cycle optimization, lane segregation, and roundabout conversions before physical implementation.
        </div>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown("""
    <div class="scope-card">
        <div class="scope-icon">🛣️</div>
        <div class="scope-heading">Automated Road Safety Auditing (RSA)</div>
        <div class="scope-desc">
            Expanding data feeds with spatial road geometry datasets to automatically evaluate sight-distance clearance, junction turning angles, and pavement surface skid resistance under Indian Road Congress standards (IRC:37, IRC:58, and IRC:SP:84).
        </div>
    </div>
    """, unsafe_allow_html=True)

with s3:
    st.markdown("""
    <div class="scope-card">
        <div class="scope-icon">📹</div>
        <div class="scope-heading">Connected Edge-AI & ITS Infrastructure</div>
        <div class="scope-desc">
            Scaling edge CCTV camera sensors (demonstrated in PoC) into a city-wide Intelligent Transportation System (ITS) network with real-time vehicle classification, speed violation detection, and dynamic Variable Message Signs (VMS) alerting drivers near blackspots.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.82rem; margin-top: 2.5rem; padding-top: 1.5rem; border-top: 1px solid rgba(148, 163, 184, 0.1);">
    <strong>RoadSafe India Decision-Support System</strong> • Grounded in Official MoRTH TRW Reports • Developed for IBM & AICTE Internship
</div>
""", unsafe_allow_html=True)
