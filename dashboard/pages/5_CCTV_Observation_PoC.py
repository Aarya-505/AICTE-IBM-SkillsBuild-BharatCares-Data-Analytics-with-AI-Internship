"""
RoadSafe India - Page 5: CCTV Edge-Sensor Traffic Observation Proof of Concept (PoC)
"""

import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px

# Configure paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.cctv_tracker import CCTVTrafficTracker

st.set_page_config(page_title="CCTV Observation PoC | RoadSafe India", page_icon="📹", layout="wide")

# Custom CSS
css_path = os.path.join(project_root, "dashboard", "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.html(f"<style>{f.read()}</style>")

st.title("📹 CCTV Edge-Sensor Traffic Observation Prototype (PoC)")
st.caption("Demonstrating localized edge computer vision for traffic exposure estimation and digital twin sensor feeds.")

# Ethical & Privacy Notice Callout
st.markdown("""
<div style="background-color: #064e3b; border-left: 5px solid #10b981; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem; color: #ecfdf5;">
    <strong>🔒 Privacy-First & Ethical Architecture:</strong>
    <p style="margin-top: 0.25rem; margin-bottom: 0; font-size: 0.9rem;">
        This prototype is strictly designed for <em>traffic volume estimation and vehicle class modal distribution</em>. 
        It <strong>does not</strong> perform facial recognition, license plate recognition (ANPR), or individual citizen tracking.
    </p>
</div>
""", unsafe_allow_html=True)

# Instantiate Tracker
tracker = CCTVTrafficTracker()

# Interactive Run Controls
col_ctrl1, col_ctrl2 = st.columns([7, 3])

with col_ctrl1:
    st.markdown("### 🎥 Camera Feed & Tripwire Inference")
    
    # Process or load clip
    sample_vid = os.path.join(project_root, "assets", "sample_traffic_feed.mp4")
    if not os.path.exists(sample_vid):
        sample_vid = tracker.generate_synthetic_traffic_clip(output_path=sample_vid)

    results = tracker.process_and_evaluate(sample_vid)

    # Video display
    if os.path.exists(sample_vid):
        st.video(sample_vid)
    else:
        st.info("Sample video is ready for processing.")

with col_ctrl2:
    st.markdown("### 📊 Edge Sensor Metrics")
    
    st.markdown(f"""
    <div class="metric-card" style="margin-bottom: 1rem;">
        <div class="metric-title">Observed Vehicle Count</div>
        <div class="metric-value">{results['model_detected_total']}</div>
        <div class="metric-subtext">Ground Truth: <strong>{results['ground_truth_total']}</strong></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-card" style="margin-bottom: 1rem;">
        <div class="metric-title">Model Counting Accuracy</div>
        <div class="metric-value" style="color: #34d399;">{results['accuracy_percentage']}%</div>
        <div class="metric-subtext">Evaluated vs Manual Benchmark</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Estimated Flow Rate</div>
        <div class="metric-value" style="color: #38bdf8;">{results['estimated_flow_rate_vpm']}</div>
        <div class="metric-subtext">Vehicles per Minute (vpm)</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Section 2: Modal Split Breakdown & Error Analysis
col_m1, col_m2 = st.columns(2)

with col_m1:
    st.subheader("🚗 Vehicle Modal Distribution (Detected)")
    counts_data = [
        {"Vehicle Class": k, "Detected Count": v}
        for k, v in results["counts_by_class"].items() if k != "Total"
    ]
    df_counts = pd.DataFrame(counts_data)
    
    fig_modal = px.bar(
        df_counts, x="Vehicle Class", y="Detected Count",
        color="Vehicle Class", color_discrete_sequence=px.colors.qualitative.Safe,
        title="Classified Vehicle Count across Tripwire"
    )
    fig_modal.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15,23,42,0.6)", height=340)
    st.plotly_chart(fig_modal, use_container_width=True)

with col_m2:
    st.subheader("⚠️ Known Edge Limitations & Validation Constraints")
    st.markdown("""
    In real-world urban deployments, computer-vision edge sensors face known challenges that must be documented:
    """)
    for lim in results["known_edge_limitations"]:
        st.markdown(f"- 🔴 **{lim}**")
    
    st.markdown("""
    > **Data Fusion Principle:** CCTV traffic flow counts provide the **denominator** (exposure rate) that transforms raw historical accident counts into true **crash risk per million vehicle-kilometers traveled (VKT)**.
    """)
