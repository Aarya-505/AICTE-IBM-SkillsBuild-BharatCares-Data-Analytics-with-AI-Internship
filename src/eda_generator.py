import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from src.data_cleaner import DataCleaner
except ImportError:
    from data_cleaner import DataCleaner

def generate_eda_figures(output_dir: str = "visuals"):
    os.makedirs(output_dir, exist_ok=True)
    cleaner = DataCleaner()
    
    df_state = cleaner.clean_state_ut_data()
    df_cities = cleaner.clean_million_plus_cities()
    df_factors = cleaner.clean_contributing_factors()
    df_time = cleaner.clean_time_slots()
    
    # Set overall aesthetic style
    sns.set_theme(style="whitegrid", palette="deep")
    plt.rcParams["font.sans-serif"] = "Arial"
    plt.rcParams["axes.edgecolor"] = "#cccccc"
    plt.rcParams["axes.linewidth"] = 0.8
    
    # -------------------------------------------------------------
    # 1. National Trend: Total Accidents vs Fatalities (2014-2020)
    # -------------------------------------------------------------
    nat_trend = df_state.groupby("Year")[["Total_Accidents", "Persons_Killed"]].sum().reset_index()
    nat_trend["Severity_Index"] = (nat_trend["Persons_Killed"] / nat_trend["Total_Accidents"]) * 100
    
    fig, ax1 = plt.subplots(figsize=(10, 5), dpi=300)
    
    color_acc = "#1f77b4"
    color_fat = "#d62728"
    
    ax1.set_title("India Road Safety Trends (2014 - 2020): Accidents vs Fatalities", fontsize=14, fontweight="bold", pad=15)
    ax1.plot(nat_trend["Year"], nat_trend["Total_Accidents"] / 1000, marker="o", color=color_acc, linewidth=2.5, label="Total Accidents (in Thousands)")
    ax1.set_xlabel("Year", fontsize=12, fontweight="semibold")
    ax1.set_ylabel("Total Accidents ('000)", color=color_acc, fontsize=12, fontweight="semibold")
    ax1.tick_params(axis="y", labelcolor=color_acc)
    
    ax2 = ax1.twinx()
    ax2.plot(nat_trend["Year"], nat_trend["Persons_Killed"] / 1000, marker="s", color=color_fat, linewidth=2.5, linestyle="--", label="Persons Killed (in Thousands)")
    ax2.set_ylabel("Fatalities ('000)", color=color_fat, fontsize=12, fontweight="semibold")
    ax2.tick_params(axis="y", labelcolor=color_fat)
    
    fig.tight_layout()
    plt.savefig(os.path.join(output_dir, "01_national_trends_2014_2020.png"))
    plt.close()
    
    # -------------------------------------------------------------
    # 2. Top 10 States by Recorded Accidents vs Fatalities (2020)
    # -------------------------------------------------------------
    st_2020 = df_state[df_state["Year"] == 2020].sort_values(by="Total_Accidents", ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(12, 6), dpi=300)
    bar_width = 0.38
    x_indices = range(len(st_2020))
    
    ax.bar([x - bar_width/2 for x in x_indices], st_2020["Total_Accidents"], width=bar_width, label="Total Accidents", color="#2b5c8f")
    ax.bar([x + bar_width/2 for x in x_indices], st_2020["Persons_Killed"], width=bar_width, label="Persons Killed", color="#e74c3c")
    
    ax.set_xticks(x_indices)
    ax.set_xticklabels(st_2020["State_UT"], rotation=30, ha="right", fontsize=10)
    ax.set_ylabel("Recorded Count", fontsize=12, fontweight="semibold")
    ax.set_title("Top 10 Indian States by Road Accidents & Fatalities (2020)", fontsize=14, fontweight="bold", pad=15)
    ax.legend(frameon=True, facecolor="white", edgecolor="none")
    
    fig.tight_layout()
    plt.savefig(os.path.join(output_dir, "02_top_states_accidents_fatalities_2020.png"))
    plt.close()

    # -------------------------------------------------------------
    # 3. Top 10 Million-Plus Cities by Accident Severity Index (2020)
    # -------------------------------------------------------------
    top_sev_cities = df_cities.sort_values(by="Severity_Index", ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    sns.barplot(data=top_sev_cities, x="Severity_Index", y="City", palette="Reds_r", ax=ax)
    
    ax.set_title("Top 10 Million-Plus Cities by Accident Severity Index (2020)\n(Fatalities per 100 Accidents)", fontsize=13, fontweight="bold", pad=15)
    ax.set_xlabel("Accident Severity Index (Fatalities per 100 Accidents)", fontsize=11, fontweight="semibold")
    ax.set_ylabel("City", fontsize=11, fontweight="semibold")
    
    for p in ax.patches:
        width = p.get_width()
        ax.annotate(f"{width:.1f}", (width + 0.5, p.get_y() + p.get_height() / 2),
                    va="center", fontsize=10, fontweight="bold", color="#333333")
        
    fig.tight_layout()
    plt.savefig(os.path.join(output_dir, "03_city_severity_index_2020.png"))
    plt.close()

    # -------------------------------------------------------------
    # 4. Vulnerable Road Users (VRU) Fatality Distribution
    # -------------------------------------------------------------
    vru_df = df_factors[df_factors["Category_Type"] == "Road User Type"].sort_values(by="Persons_Killed", ascending=False)
    
    fig, ax = plt.subplots(figsize=(8, 8), dpi=300)
    colors = ["#e74c3c", "#e67e22", "#3498db", "#9b59b6", "#1abc9c", "#f1c40f", "#34495e"]
    ax.pie(vru_df["Persons_Killed"], labels=vru_df["Factor_Name"], autopct="%1.1f%%", startangle=140,
           colors=colors, wedgeprops=dict(width=0.4, edgecolor="white"))
    
    ax.set_title("Road User Fatality Breakdown (2020)\nHighlighting Vulnerable Road Users (VRUs)", fontsize=13, fontweight="bold", pad=15)
    
    fig.tight_layout()
    plt.savefig(os.path.join(output_dir, "04_vru_fatality_donut_2020.png"))
    plt.close()

    # -------------------------------------------------------------
    # 5. Diurnal 24-Hour Crash Distribution
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(11, 5), dpi=300)
    sns.lineplot(data=df_time, x="Time_Slot", y="Total_Accidents", marker="o", color="#2980b9", linewidth=2.5, ax=ax, label="Accidents")
    sns.lineplot(data=df_time, x="Time_Slot", y="Persons_Killed", marker="s", color="#c0392b", linewidth=2.5, ax=ax, label="Fatalities")
    
    ax.set_xticklabels(df_time["Time_Slot"], rotation=25, ha="right", fontsize=9)
    ax.set_title("Diurnal Pattern: Road Accidents & Fatalities by 3-Hour Time Slots", fontsize=13, fontweight="bold", pad=15)
    ax.set_xlabel("Time Window", fontsize=11, fontweight="semibold")
    ax.set_ylabel("Recorded Count", fontsize=11, fontweight="semibold")
    ax.legend(frameon=True)
    
    fig.tight_layout()
    plt.savefig(os.path.join(output_dir, "05_diurnal_time_distribution_2020.png"))
    plt.close()

    print(f"Generated 5 publication-ready EDA figures in '{output_dir}'.")

if __name__ == "__main__":
    generate_eda_figures()
