"""
RoadSafe India - Page 1: India Overview & Multi-Year Trends
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

st.set_page_config(page_title="India Overview | RoadSafe India", page_icon="🇮🇳", layout="wide")

# Custom CSS
css_path = os.path.join(project_root, "dashboard", "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.html(f"<style>{f.read()}</style>")

st.title("🇮🇳 India National Overview & Temporal Trends (2014–2020)")
st.caption("Macro-level longitudinal analysis across Indian States & Union Territories.")

# Load Data
@st.cache_data
def load_trends():
    path = os.path.join(project_root, "data", "processed", "cleaned_state_ut_trends.csv")
    return pd.read_csv(path)

df = load_trends()

# Sidebar Filters
st.sidebar.header("🔍 Trend Filters")
selected_years = st.sidebar.slider(
    "Select Year Range:",
    min_value=int(df["Year"].min()),
    max_value=int(df["Year"].max()),
    value=(int(df["Year"].min()), int(df["Year"].max()))
)

all_states = sorted(df["State_UT"].unique().tolist())
selected_states = st.sidebar.multiselect(
    "Filter by State / UT (Default: All):",
    options=all_states,
    default=[]
)

filtered_df = df[(df["Year"] >= selected_years[0]) & (df["Year"] <= selected_years[1])]
if selected_states:
    filtered_df = filtered_df[filtered_df["State_UT"].isin(selected_states)]

if filtered_df.empty:
    st.warning("No data found matching your selected filters. Please adjust the sidebar selection.")
    st.stop()

# Aggregated Summary
agg_year = filtered_df.groupby("Year").agg({
    "Total_Accidents": "sum",
    "Persons_Killed": "sum",
    "Persons_Injured": "sum"
}).reset_index()

agg_year["Severity_Index"] = (agg_year["Persons_Killed"] / agg_year["Total_Accidents"]) * 100

# Headline KPI Row for filtered selection
tot_acc = int(agg_year["Total_Accidents"].sum())
tot_kill = int(agg_year["Persons_Killed"].sum())
tot_inj = int(agg_year["Persons_Injured"].sum())
avg_asi = KPICalculator.calculate_severity_index(tot_kill, tot_acc)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Total Filtered Accidents", f"{tot_acc:,}")
with c2:
    st.metric("Total Fatalities", f"{tot_kill:,}", delta_color="inverse")
with c3:
    st.metric("Total Injuries", f"{tot_inj:,}")
with c4:
    st.metric("Period Severity Index", f"{avg_asi:.1f}", help="Fatalities per 100 reported crashes")

st.markdown("---")

# Chart Row 1: Dual-Axis Trend & Severity Trajectory
col1, col2 = st.columns([6, 4])

with col1:
    st.subheader("📊 Longitudinal Trajectory: Crashes vs Fatalities")
    fig_line = go.Figure()
    fig_line.add_trace(go.Bar(
        x=agg_year["Year"], y=agg_year["Total_Accidents"],
        name="Total Accidents", marker_color="#38bdf8", opacity=0.8
    ))
    fig_line.add_trace(go.Scatter(
        x=agg_year["Year"], y=agg_year["Persons_Killed"],
        name="Persons Killed", mode="lines+markers",
        line=dict(color="#ef4444", width=3), yaxis="y2"
    ))
    fig_line.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.6)",
        yaxis=dict(title="Total Accidents"),
        yaxis2=dict(title="Fatalities (Persons Killed)", overlaying="y", side="right"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=30, b=20),
        height=380
    )
    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    st.subheader("⚠️ Severity Index Trajectory (Fatalities / 100 Crashes)")
    fig_asi = px.line(
        agg_year, x="Year", y="Severity_Index",
        markers=True, text=agg_year["Severity_Index"].round(1),
        labels={"Severity_Index": "Severity Index", "Year": "Year"}
    )
    fig_asi.update_traces(line_color="#fbbf24", line_width=3, textposition="top center")
    fig_asi.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.6)",
        margin=dict(l=20, r=20, t=30, b=20),
        height=380
    )
    st.plotly_chart(fig_asi, use_container_width=True)

# Chart Row 2: State-wise Comparison for latest year
latest_year = selected_years[1]
st_latest = filtered_df[filtered_df["Year"] == latest_year].sort_values(by="Total_Accidents", ascending=False)

st.subheader(f"🏛️ State / UT Ranking & Distribution ({latest_year})")

col_s1, col_s2 = st.columns([5, 5])

with col_s1:
    fig_state_acc = px.bar(
        st_latest.head(12), x="Total_Accidents", y="State_UT", orientation="h",
        color="Total_Accidents", color_continuous_scale="Blues",
        labels={"Total_Accidents": "Total Accidents", "State_UT": ""},
        title=f"Top States by Reported Crashes ({latest_year})"
    )
    fig_state_acc.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,23,42,0.6)", height=420)
    st.plotly_chart(fig_state_acc, use_container_width=True)

with col_s2:
    st_sev_top = st_latest[st_latest["Total_Accidents"] > 500].sort_values(by="Severity_Index", ascending=False).head(12)
    fig_state_sev = px.bar(
        st_sev_top, x="Severity_Index", y="State_UT", orientation="h",
        color="Severity_Index", color_continuous_scale="Reds",
        labels={"Severity_Index": "Fatalities per 100 Crashes", "State_UT": ""},
        title=f"Top States by Accident Severity ({latest_year}, Min 500 Crashes)"
    )
    fig_state_sev.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,23,42,0.6)", height=420)
    st.plotly_chart(fig_state_sev, use_container_width=True)

# Data Table & Export
with st.expander("📋 View Cleaned Data Table & Export"):
    st.dataframe(filtered_df, use_container_width=True)
    csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Filtered CSV",
        data=csv_bytes,
        file_name=f"roadsafe_india_trends_{selected_years[0]}_{selected_years[1]}.csv",
        mime="text/csv"
    )
