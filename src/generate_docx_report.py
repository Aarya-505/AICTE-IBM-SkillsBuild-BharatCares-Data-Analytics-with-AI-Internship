"""
Word Document (.docx) Generator for AICTE IBM SkillsBuild BharatCares Internship
Generates AaryaMandke_ProjectReport.docx with high-quality styling, tables, formulas, and recommendations.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Set background color of a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set cell internal padding."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_styled_heading(doc, text, level):
    """Add a styled heading with IBM Blue theme."""
    h = doc.add_heading(text, level=level)
    run = h.runs[0] if h.runs else h.add_run(text)
    if level == 1:
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = RGBColor(15, 98, 254)  # IBM Carbon Blue
        h.paragraph_format.space_before = Pt(16)
        h.paragraph_format.space_after = Pt(6)
    elif level == 2:
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 67, 206)
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
    elif level == 3:
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = RGBColor(50, 50, 50)
        h.paragraph_format.space_before = Pt(8)
        h.paragraph_format.space_after = Pt(2)
    return h

def add_callout(doc, text, title="KEY INSIGHT"):
    """Add a shaded callout box."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "EDF5FF")  # Light IBM blue tint
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    # Left border highlight
    tcPr = cell._element.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="0F62FE"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    
    r_title = p.add_run(f"📌 {title}: ")
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(15, 98, 254)
    r_title.font.size = Pt(10)
    
    r_text = p.add_run(text)
    r_text.font.size = Pt(10)
    r_text.font.color.rgb = RGBColor(30, 30, 30)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def generate_report(output_path):
    doc = Document()
    
    # Set standard margins (1 inch)
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
    
    # Title Section
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_p.add_run("RoadSafe India")
    title_run.font.size = Pt(24)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(15, 98, 254)
    
    subtitle_p = doc.add_paragraph()
    subtitle_p.paragraph_format.space_after = Pt(8)
    subtitle_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_run = subtitle_p.add_run("Data-Driven Road Safety Analytics for Safer & Sustainable Urban Planning")
    sub_run.font.size = Pt(14)
    sub_run.font.bold = True
    sub_run.font.color.rgb = RGBColor(80, 80, 80)
    
    # Metadata Badge Box
    meta_table = doc.add_table(rows=1, cols=1)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    m_cell = meta_table.cell(0, 0)
    m_cell.width = Inches(6.5)
    set_cell_background(m_cell, "F4F4F4")
    set_cell_margins(m_cell, top=120, bottom=120, left=150, right=150)
    mp = m_cell.paragraphs[0]
    mp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    mp.paragraph_format.space_after = Pt(0)
    
    m_text = mp.add_run("AICTE | IBM SkillsBuild | BharatCares Internship 2026\n")
    m_text.bold = True
    m_text.font.size = Pt(10.5)
    m_text.font.color.rgb = RGBColor(0, 67, 206)
    
    m_sub = mp.add_run("Author: Aarya Mandke  |  Track: Data Analytics with AI  |  Date: September 2026\nGitHub Repository: https://github.com/Aarya-505/AICTE-IBM-SkillsBuild-BharatCares-Data-Analytics-with-AI-Internship")
    m_sub.font.size = Pt(9.5)
    m_sub.font.color.rgb = RGBColor(100, 100, 100)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    
    # Executive Summary
    add_styled_heading(doc, "Executive Summary", level=1)
    p = doc.add_paragraph()
    p.add_run(
        "India accounts for approximately 1% of the world's vehicular fleet but contributes to nearly 11% of global road traffic fatalities. "
        "Road crashes impose staggering socio-economic losses, estimated between 3% and 5% of India's national Gross Domestic Product (GDP). "
        "Traditional transportation management has remained reactive, addressing accident blackspots only after severe tragedies occur.\n\n"
        "This project, RoadSafe India, establishes an end-to-end data analytics platform, decision-support dashboard, and edge computer-vision proof-of-concept. "
        "Grounded in verified official data from the Ministry of Road Transport and Highways (MoRTH) Transport Research Wing (TRW), "
        "the system analyzes multi-year national trajectories (2014–2020), 50 Million-Plus Urban Agglomerations, infrastructure configurations, and diurnal temporal slots. "
        "By synthesizing mathematical indicators (such as Accident Severity Index, Injury Ratios, and Vulnerable Road User exposure) with Indian Road Congress (IRC) Civil Engineering Codes, "
        "RoadSafe India delivers empirical evidence directly into municipal urban planning workflows."
    )
    
    add_callout(
        doc,
        "National Accident Severity Index (fatalities per 100 crashes) escalated from 28.5 (2014) to 36.0 (2020) despite total crash counts declining during pandemic lockdowns—indicating that higher vehicle speeds on open roads increase trauma lethality.",
        title="CORE RESEARCH FINDING"
    )
    
    # Section 1: Problem Statement & Architecture
    add_styled_heading(doc, "1. Problem Statement & System Architecture", level=1)
    doc.add_paragraph(
        "Modern smart city planning requires evidence-based safety intelligence before civil funds are committed to road construction and signal re-timing. "
        "RoadSafe India establishes a three-tier intelligent transportation architecture:"
    )
    
    # Architecture Table
    arch_table = doc.add_table(rows=4, cols=3)
    arch_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Tier Level", "System Component", "Technical Function & Data Output"]
    for i, h in enumerate(headers):
        cell = arch_table.cell(0, i)
        cell.text = h
        set_cell_background(cell, "0F62FE")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.size = Pt(10)
        
    arch_data = [
        ("Tier 1 (Implemented)", "Empirical Safety Intelligence Layer", "Ingests historical MoRTH accident records; cleans data; computes Accident Severity Index (ASI); classifies urban vulnerability quadrants."),
        ("Tier 2 (Future Scope)", "High-Resolution Spatial Sensing Layer", "Leverages satellite GIS imagery, road network topology, and LiDAR point clouds to detect sight-triangle obstructions and pavement distress."),
        ("Tier 3 (Future Scope)", "Microscopic Traffic Simulation Layer", "Executes SUMO / PTV VISSIM digital twin stress-testing on flagged high-risk corridors to optimize signal phases and roundabout geometry.")
    ]
    
    for row_idx, data in enumerate(arch_data, start=1):
        for col_idx, text in enumerate(data):
            cell = arch_table.cell(row_idx, col_idx)
            cell.text = text
            set_cell_background(cell, "F8F9FA" if row_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.runs[0].font.size = Pt(9.5)
            if col_idx == 0:
                p.runs[0].font.bold = True
                
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    
    # Section 2: Data Grounding & Cleaning Methodology
    add_styled_heading(doc, "2. Data Grounding & Cleaning Pipeline", level=1)
    doc.add_paragraph(
        "To ensure analytical integrity, all datasets were ingested from verified open government sources published by the Transport Research Wing (TRW), "
        "Ministry of Road Transport & Highways (MoRTH), Government of India (data.gov.in)."
    )
    
    doc.add_paragraph("Key Data Sources Processed:")
    sources = [
        "State/UT Longitudinal Records (2014–2020): Multi-year records of total accidents, fatalities, and injuries across 36 Indian States and Union Territories.",
        "50 Million-Plus Urban Agglomerations (2020): High-resolution city-level accident statistics and fatality metrics.",
        "Contributing Factors Dataset (2020): Detailed breakdowns across Road Category (NH/SH/Arterials), Junction Types (4-arm, T-junction, Roundabout), Weather, and Modal Types.",
        "Diurnal Time-Slot Distribution (2020): 3-hour accident intervals mapping peak risk exposure hours."
    ]
    for s in sources:
        doc.add_paragraph(f"• {s}", style='List Bullet')
        
    doc.add_paragraph(
        "A modular, automated data cleaning engine (`src/data_cleaner.py`) was executed. "
        "The pipeline performed string stripping, state name harmonization, missing value imputation, type casting to integer types, "
        "and automated audit logging with rigorous unit test validation (`tests/test_kpis.py`)."
    )
    
    # Section 3: Standardized Mathematical Indicators
    add_styled_heading(doc, "3. Standardized Safety Indicators & Mathematical Formulation", level=1)
    doc.add_paragraph("The platform computes standardized key performance indicators (KPIs) to provide rigorous comparisons:")
    
    kpi_table = doc.add_table(rows=5, cols=3)
    kpi_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    kpi_headers = ["Indicator Name", "Mathematical Formula", "Planning & Safety Interpretation"]
    for i, h in enumerate(kpi_headers):
        cell = kpi_table.cell(0, i)
        cell.text = h
        set_cell_background(cell, "0F62FE")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.size = Pt(10)
        
    kpi_rows = [
        ("Accident Severity Index (ASI)", "ASI = (Persons Killed / Total Accidents) * 100", "Measures fatalities per 100 crashes. Reflects collision trauma severity and speed impact rather than sheer crash frequency."),
        ("Injury Ratio (IR)", "IR = (Persons Injured / Total Accidents) * 100", "Indicates the rate of bodily injury per collision event, crucial for emergency medical capacity planning."),
        ("VRU Fatality Share (%)", "VRU_share = ((Killed_2W + Killed_Ped + Killed_Cycle) / Total Killed) * 100", "Calculates proportion of road trauma borne by non-motorized and two-wheeled vulnerable road users (>53% in India)."),
        ("Year-over-Year Growth (YoY)", "YoY = ((X_t - X_{t-1}) / X_{t-1}) * 100", "Measures annual percentage shift in accident, fatality, or injury metrics.")
    ]
    for row_idx, data in enumerate(kpi_rows, start=1):
        for col_idx, text in enumerate(data):
            cell = kpi_table.cell(row_idx, col_idx)
            cell.text = text
            set_cell_background(cell, "F8F9FA" if row_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.runs[0].font.size = Pt(9.5)
            if col_idx == 0:
                p.runs[0].font.bold = True
                
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    
    # Section 4: Key Insights & Empirical Findings
    add_styled_heading(doc, "4. Empirical Findings & Data Visualizations", level=1)
    
    add_styled_heading(doc, "4.1 Multi-Year National Trajectories (2014–2020)", level=2)
    doc.add_paragraph(
        "Longitudinal analysis of national accident data reveals that while total annual crashes decreased from 489,400 (2014) to 366,138 (2020), "
        "annual fatalities remained disproportionately high (131,714 in 2020). Consequently, National Severity Index grew from 28.5 to 36.0, "
        "signaling an alarming increase in accident lethality."
    )
    
    add_styled_heading(doc, "4.2 50 Million-Plus Cities Vulnerability Matrix", level=2)
    doc.add_paragraph(
        "By plotting Crash Volume vs. Accident Severity Index across India's 50 largest urban agglomerations, the platform segments cities into distinct risk profiles:\n"
        "• High Volume / High Severity (Critical Priority): Metros requiring immediate arterial corridor interventions.\n"
        "• High Severity / Moderate Volume: Cities like Ludhiana, Amritsar, and Patna where high vehicle speeds on un-segregated highways produce fatal trauma despite lower total incident counts.\n"
        "• High Volume / Lower Severity: Highly congested urban centers like Chennai and Delhi where traffic friction reduces average collision velocity."
    )
    
    add_styled_heading(doc, "4.3 Vulnerable Road Users (VRUs) & Infrastructure", level=2)
    doc.add_paragraph(
        "• Two-Wheelers & Pedestrians: Motorized two-wheelers account for 43.5% of total fatalities, and pedestrians account for 15.3%, totaling over 58% of all road deaths.\n"
        "• Junction Risk: 4-arm cross junctions and uncontrolled T-junctions account for over 38% of junction crashes due to conflicting turning movements and inadequate sight distance.\n"
        "• Temporal Peak: 15:00–21:00 represents the peak danger window, driven by evening commute traffic, mixed vehicle speeds, and deteriorating night visibility."
    )
    
    # Section 5: Indian Road Congress (IRC) Engineering Standards
    add_styled_heading(doc, "5. Civil Engineering & IRC Standards Integration", level=1)
    doc.add_paragraph(
        "A core innovation of RoadSafe India is linking safety data directly to codified Indian Road Congress (IRC) civil engineering guidelines:"
    )
    
    irc_table = doc.add_table(rows=5, cols=3)
    irc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    irc_headers = ["Identified Risk Factor", "IRC Standard Code", "Mandated Civil Engineering Intervention"]
    for i, h in enumerate(irc_headers):
        cell = irc_table.cell(0, i)
        cell.text = h
        set_cell_background(cell, "0F62FE")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.size = Pt(10)
        
    irc_data = [
        ("High-Speed Corridor Severe Crashes", "IRC:37 / IRC:58", "Pavement design for high-speed corridors; High-Friction Surface Treatments (HFST) and Stone Matrix Asphalt (SMA) at braking zones."),
        ("4-Arm Intersection Collisions", "IRC:SP:84 / IRC:65", "Conversion of uncontrolled 4-arm junctions into modern roundabouts or channelized islands with protected right-turn bays."),
        ("Vulnerable Road User Casualties", "IRC:103-2012", "Mandatory grade-separated pedestrian crossings, continuous raised footpaths (min 1.8m width), and segregated 2W/cycle tracks."),
        ("Night & Adverse Weather Crashes", "IRC:67 / IRC:35", "Retro-reflective road signage, thermoplastic high-visibility road markings, and solar-powered smart street lighting at blackspots.")
    ]
    for row_idx, data in enumerate(irc_data, start=1):
        for col_idx, text in enumerate(data):
            cell = irc_table.cell(row_idx, col_idx)
            cell.text = text
            set_cell_background(cell, "F8F9FA" if row_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.runs[0].font.size = Pt(9.5)
            if col_idx == 0:
                p.runs[0].font.bold = True
                
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    
    # Section 6: Computer Vision & Edge Traffic Sensing PoC
    add_styled_heading(doc, "6. Edge CCTV Traffic Sensing PoC", level=1)
    doc.add_paragraph(
        "To complement macro statistical data with real-time microscopic traffic counts, RoadSafe India includes a privacy-preserving computer vision module (`src/cctv_tracker.py`).\n\n"
        "• Virtual Tripwire Counting: Uses OpenCV background subtraction and contour detection to count bidirectional vehicle flow across defined entry/exit tripwires.\n"
        "• Privacy Compliance: No facial recognition, license plate extraction, or personal identification is captured, ensuring complete compliance with privacy standards.\n"
        "• Ground Truth Evaluation: Validated against sample traffic footage with precision, recall, and F1-score evaluation metrics."
    )
    
    # Section 7: Strategic Policy & Urban Planning Recommendations
    add_styled_heading(doc, "7. Strategic Policy & Urban Planning Roadmap", level=1)
    doc.add_paragraph(
        "Based on empirical analysis, the project proposes a 4-pillar Safe System strategy for Indian municipalities:\n"
        "1. Safe Speeds: Deploy automated speed enforcement cameras along high-ASI corridors and implement traffic calming in residential zones.\n"
        "2. Safe Infrastructure: Enforce IRC:103 pedestrian standards across all Class-I urban roads and redesign high-risk 4-arm junctions.\n"
        "3. Safe Road Users: Expand helmet and seatbelt compliance campaigns targeting two-wheeler riders and rear-seat passengers.\n"
        "4. Post-Crash Response: Deploy trauma response units strategically along high-fatality National Highways within the 'Golden Hour' window."
    )
    
    # Section 8: Deliverables & Repository Verification
    add_styled_heading(doc, "8. Project Deliverables Checklist", level=1)
    
    deliv_table = doc.add_table(rows=5, cols=3)
    deliv_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    deliv_headers = ["Deliverable Name", "File Path / Name", "Status & Format"]
    for i, h in enumerate(deliv_headers):
        cell = deliv_table.cell(0, i)
        cell.text = h
        set_cell_background(cell, "0F62FE")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
        p.runs[0].font.size = Pt(10)
        
    deliv_data = [
        ("1. Complete Code File", "AaryaMandke_RoadSafeIndia.ipynb", "Complete executed Jupyter Notebook with EDA, KPIs, and Visuals (.ipynb)"),
        ("2. Requirements File", "requirements.txt", "Verified Python package dependencies (.txt)"),
        ("3. Project Report", "AaryaMandke_ProjectReport.docx", "Formatted complete technical project report in Microsoft Word (.docx)"),
        ("4. README File", "README.md", "Complete repository overview, dataset links, setup guide, and tech stack (.md)")
    ]
    for row_idx, data in enumerate(deliv_data, start=1):
        for col_idx, text in enumerate(data):
            cell = deliv_table.cell(row_idx, col_idx)
            cell.text = text
            set_cell_background(cell, "F8F9FA" if row_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.runs[0].font.size = Pt(9.5)
            if col_idx == 0:
                p.runs[0].font.bold = True
                
    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    
    # Save document
    doc.save(output_path)
    print(f"Report successfully saved to: {output_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Save main submission docx in root and reports/
    file_names = [
        os.path.join(base_dir, "AaryaMandke_ProjectReport.docx"),
        os.path.join(base_dir, "Arya_ProjectReport.docx"),
        os.path.join(base_dir, "reports", "AaryaMandke_ProjectReport.docx"),
        os.path.join(base_dir, "reports", "Arya_ProjectReport.docx")
    ]
    
    for fn in file_names:
        generate_report(fn)
