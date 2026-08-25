import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import datetime
import time

# ==========================================
# STREAMLIT PAGE CONFIG & INITIAL SETUP
# ==========================================
st.set_page_config(
    page_title="ICU Sentinel AI | Command Center",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State for Simulated Live Data
if "last_updated" not in st.session_state:
    st.session_state.last_updated = datetime.datetime.now().strftime("%H:%M:%S IST")

if "patient_data" not in st.session_state:
    st.session_state.patient_data = pd.DataFrame([
        {"Bed": 1, "Name": "R. Sharma", "Age": 62, "HR": 118, "BP": "92/58", "SpO2": 91, "RR": 24, "Temp": "38.5 °C", "Risk": "CRITICAL", "Score": 89, "Doctor": "Dr. Mehta"},
        {"Bed": 2, "Name": "A. Patil", "Age": 45, "HR": 92, "BP": "118/72", "SpO2": 96, "RR": 16, "Temp": "36.8 °C", "Risk": "STABLE", "Score": 18, "Doctor": "Dr. Khan"},
        {"Bed": 3, "Name": "M. Joshi", "Age": 58, "HR": 104, "BP": "104/68", "SpO2": 94, "RR": 20, "Temp": "37.4 °C", "Risk": "WARNING", "Score": 54, "Doctor": "Dr. Rao"},
        {"Bed": 4, "Name": "P. Singh", "Age": 71, "HR": 78, "BP": "122/80", "SpO2": 98, "RR": 14, "Temp": "36.6 °C", "Risk": "STABLE", "Score": 12, "Doctor": "Dr. Mehta"},
        {"Bed": 5, "Name": "A. Verma", "Age": 50, "HR": 124, "BP": "88/54", "SpO2": 89, "RR": 28, "Temp": "39.1 °C", "Risk": "CRITICAL", "Score": 92, "Doctor": "Dr. Khan"},
        {"Bed": 6, "Name": "S. Khan", "Age": 66, "HR": 110, "BP": "96/61", "SpO2": 92, "RR": 22, "Temp": "38.2 °C", "Risk": "CRITICAL", "Score": 87, "Doctor": "Dr. Khan"},
        {"Bed": 7, "Name": "N. Rao", "Age": 39, "HR": 74, "BP": "115/75", "SpO2": 99, "RR": 15, "Temp": "36.7 °C", "Risk": "STABLE", "Score": 8, "Doctor": "Dr. Rao"},
        {"Bed": 8, "Name": "K. Gupta", "Age": 53, "HR": 98, "BP": "135/88", "SpO2": 93, "RR": 19, "Temp": "37.9 °C", "Risk": "WARNING", "Score": 62, "Doctor": "Dr. Khan"},
        {"Bed": 9, "Name": "T. Das", "Age": 68, "HR": 80, "BP": "120/78", "SpO2": 97, "RR": 16, "Temp": "36.9 °C", "Risk": "STABLE", "Score": 15, "Doctor": "Dr. Rao"},
        {"Bed": 10, "Name": "J. Pawar", "Age": 61, "HR": 102, "BP": "110/70", "SpO2": 94, "RR": 21, "Temp": "37.6 °C", "Risk": "WARNING", "Score": 58, "Doctor": "Dr. Mehta"},
        {"Bed": 11, "Name": "Unoccupied", "Age": "-", "HR": 0, "BP": "-/-", "SpO2": 0, "RR": 0, "Temp": "-", "Risk": "FREE", "Score": 0, "Doctor": "-"},
        {"Bed": 12, "Name": "Unoccupied", "Age": "-", "HR": 0, "BP": "-/-", "SpO2": 0, "RR": 0, "Temp": "-", "Risk": "FREE", "Score": 0, "Doctor": "-"}
    ])
# ==========================================
# CUSTOM CSS FOR FUTURISTIC UI & ANIMATIONS
# ==========================================
st.markdown("""
<style>
    /* Dark Theme Core Styles */
    .stApp {
        background-color: #050b14;
        color: #e2e8f0;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Neon Glow Text */
    .cyan-glow {
        color: #00f0ff;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.6), 0 0 20px rgba(0, 240, 255, 0.4);
    }
    
    .red-glow {
        color: #ff3366;
        text-shadow: 0 0 10px rgba(255, 51, 102, 0.6);
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(13, 25, 48, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 240, 255, 0.15);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-3px);
        border-color: rgba(0, 240, 255, 0.4);
        box-shadow: 0 10px 30px 0 rgba(0, 240, 255, 0.2);
    }

    /* Bed Status Mini Cards */
    .bed-card-stable {
        background: rgba(16, 185, 129, 0.08);
        border-left: 4px solid #10b981;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }
    
    .bed-card-warning {
        background: rgba(245, 158, 11, 0.08);
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }
    
    .bed-card-critical {
        background: rgba(239, 68, 68, 0.12);
        border-left: 4px solid #ef4444;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        animation: pulse-border 2s infinite;
    }

    .bed-card-free {
        background: rgba(100, 116, 139, 0.08);
        border-left: 4px solid #64748b;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }

    @keyframes pulse-border {
        0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
        70% { box-shadow: 0 0 0 8px rgba(239, 68, 68, 0); }
        100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }

    /* Animated AI Orb */
    .orb-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
    }
    
    .ai-orb {
        width: 130px;
        height: 130px;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, #00f0ff, #7000ff, #050b14);
        box-shadow: 0 0 30px #00f0ff, inset 0 0 15px #ffffff;
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: 900;
        font-size: 24px;
        color: #ffffff;
        text-shadow: 0 0 10px #00f0ff;
        animation: float 4s ease-in-out infinite, glow 2s ease-in-out infinite alternate;
        position: relative;
    }
    
    .ai-orb::before {
        content: '';
        position: absolute;
        width: 155px;
        height: 155px;
        border-radius: 50%;
        border: 2px dashed #00f0ff;
        animation: spin 10s linear infinite;
    }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* Live Pulsing Dot */
    .pulse-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #10b981;
        box-shadow: 0 0 0 rgba(16, 185, 129, 0.4);
        animation: pulse 1.5s infinite;
        margin-right: 8px;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    /* Custom Badges */
    .badge-critical { background-color: #ef4444; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; }
    .badge-warning { background-color: #f59e0b; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; }
    .badge-stable { background-color: #10b981; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; }
    .badge-free { background-color: #64748b; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; }

    /* Hide standard Streamlit header/footer for clean UI */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 10px 0;'>
            <h2 style='color: #00f0ff; margin-bottom: 0px; letter-spacing: 2px;'>ICU SENTINEL</h2>
            <p style='color: #a0aec0; font-size: 11px; font-weight: bold; margin-top: 2px; letter-spacing: 1px;'>AI CRITICAL CARE COMMAND CENTER</p>
        </div>
        <hr style="border: 0.5px solid rgba(0, 240, 255, 0.2); margin-top: 5px; margin-bottom: 20px;">
    """, unsafe_allow_html=True)

    page = st.radio(
        "NAVIGATION",
        [
            "◈ Command Center",
            "❤️ Patient Monitor",
            "🧠 AI Risk Engine",
            "⚠️ Early Warnings",
            "👨‍⚕️ Doctors & Nurses",
            "🛏️ Bed Management",
            "⚙️ Equipment",
            "🩸 Labs & Reports",
            "✚ Clinical Support"
        ],
        label_visibility="collapsed"
    )

    st.markdown("""
        <br><br><br>
        <div style='background: rgba(0, 240, 255, 0.05); border: 1px solid rgba(0, 240, 255, 0.2); border-radius: 8px; padding: 12px; text-align: center;'>
            <p style='color: #10b981; font-weight: bold; margin: 0; font-size: 12px;'>
                <span class="pulse-dot"></span>SYSTEM ONLINE
            </p>
            <p style='color: #a0aec0; font-size: 10px; margin: 4px 0 0 0;'>Fireblaze Tech Event Prototype</p>
            <p style='color: #64748b; font-size: 9px; margin: 2px 0 0 0;'>Simulated Data Stream</p>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# HELPER FUNCTIONS
# ==========================================
def generate_ecg_wave():
    x = np.linspace(0, 4, 400)
    # Simulate standard P-QRS-T complex pattern repeat
    y = np.sin(x * 2 * np.pi * 1.8) * 0.1
    for i in range(len(x)):
        t = x[i] % 0.8
        if 0.2 < t < 0.25:
            y[i] -= 0.15  # Q
        elif 0.25 <= t < 0.32:
            y[i] += 1.8   # R
        elif 0.32 <= t < 0.37:
            y[i] -= 0.4   # S
        elif 0.45 < t < 0.6:
            y[i] += 0.25  # T
    # Add minor baseline noise
    y += np.random.normal(0, 0.02, len(x))
    return x, y

def trigger_vital_simulation():
    df = st.session_state.patient_data.copy()
    for idx, row in df.iterrows():
        if row["Risk"] != "FREE":
            df.at[idx, "HR"] = max(55, min(140, row["HR"] + np.random.randint(-4, 5)))
            df.at[idx, "SpO2"] = max(85, min(100, row["SpO2"] + np.random.randint(-1, 2)))
            df.at[idx, "RR"] = max(12, min(32, row["RR"] + np.random.randint(-1, 2)))
    st.session_state.patient_data = df
    st.session_state.last_updated = datetime.datetime.now().strftime("%H:%M:%S IST")

# ==========================================
# PAGE 1: COMMAND CENTER
# ==========================================
if page == "◈ Command Center":
    # Header Section
    c_title, c_time = st.columns([3, 1])
    with c_title:
        st.markdown("<h1 style='margin:0;'>ICU Intelligence Command Center</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #a0aec0; margin-top: -5px;'>Real-time monitoring · AI prediction · early warning · clinical workflow</p>", unsafe_allow_html=True)
    with c_time:
        st.markdown(f"""
            <div style='text-align: right; background: rgba(0, 240, 255, 0.05); border: 1px solid rgba(0, 240, 255, 0.2); padding: 8px 12px; border-radius: 8px;'>
                <span class="pulse-dot"></span>
                <span style='color:#00f0ff; font-weight:bold;'>LIVE FEED</span><br>
                <span style='color:#e2e8f0; font-size:12px;'>Updated: {st.session_state.last_updated}</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Hero Section with Glowing AI Orb
    hero_left, hero_right = st.columns([2.2, 1])
    with hero_left:
        st.markdown("""
            <div class="glass-card" style="padding: 25px;">
                <h2 style="font-size: 28px; margin-top: 0;">From Raw ICU Signals <span class="cyan-glow">to Intelligent Action.</span></h2>
                <p style="color: #cbd5e1; font-size: 14px; line-height: 1.6;">
                    A unified ICU command center connecting patient vitals, beds, staff, equipment, laboratory information, 
                    and clinical workflow with an AI layer for continuous risk scoring and early warning detection.
                </p>
                <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 15px;">
                    <span style="background: rgba(0, 240, 255, 0.15); border: 1px solid #00f0ff; color: #00f0ff; padding: 4px 12px; border-radius: 15px; font-size: 11px; font-weight: bold;">⚡ Real-Time Vitals</span>
                    <span style="background: rgba(112, 0, 255, 0.15); border: 1px solid #7000ff; color: #b780ff; padding: 4px 12px; border-radius: 15px; font-size: 11px; font-weight: bold;">🧠 AI Risk Scoring</span>
                    <span style="background: rgba(255, 51, 102, 0.15); border: 1px solid #ff3366; color: #ff3366; padding: 4px 12px; border-radius: 15px; font-size: 11px; font-weight: bold;">⚠️ Early Warnings</span>
                    <span style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10b981; color: #10b981; padding: 4px 12px; border-radius: 15px; font-size: 11px; font-weight: bold;">✚ Clinical Decision Support</span>
                    <span style="background: rgba(245, 158, 11, 0.15); border: 1px solid #f59e0b; color: #f59e0b; padding: 4px 12px; border-radius: 15px; font-size: 11px; font-weight: bold;">📊 Hospital Analytics</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    with hero_right:
        st.markdown("""
            <div class="glass-card" style="text-align: center; height: 100%;">
                <p style="color: #a0aec0; font-size: 11px; font-weight: bold; letter-spacing: 1px; margin-bottom: 0;">SENTINEL AI ENGINE ACTIVE</p>
                <div class="orb-container">
                    <div class="ai-orb">AI</div>
                </div>
                <p style="color: #00f0ff; font-size: 12px; margin-top: -10px;">Evaluating 12 Streams / Sec</p>
            </div>
        """, unsafe_allow_html=True)

    # 6 KPI Cards Row
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    kpis = [
        ("ICU BEDS", "12", "9 Occupied · 3 Free", "#00f0ff"),
        ("HIGH-RISK", "3", "AI Prioritized", "#ff3366"),
        ("ACTIVE ALERTS", "7", "2 Critical · 5 Warning", "#f59e0b"),
        ("STAFF ON DUTY", "11", "4 Doctors · 7 Nurses", "#10b981"),
        ("DEVICES ONLINE", "94%", "1 Maint. Alert", "#00f0ff"),
        ("AI EARLY WARN", "87%", "Bed 6 Highest Risk", "#7000ff")
    ]
    
    cols = [k1, k2, k3, k4, k5, k6]
    for i, (title, val, sub, col) in enumerate(kpis):
        with cols[i]:
            st.markdown(f"""
                <div class="glass-card" style="padding: 12px; text-align: center;">
                    <p style="color: #a0aec0; font-size: 10px; font-weight: bold; margin: 0;">{title}</p>
                    <h2 style="color: {col}; margin: 4px 0; font-size: 24px;">{val}</h2>
                    <p style="color: #cbd5e1; font-size: 9px; margin: 0;">{sub}</p>
                </div>
            """, unsafe_allow_html=True)

    # Main Grid: Bed Board (Left 2 cols) & Alerts/ECG (Right 1 col)
    grid_left, grid_right = st.columns([2, 1])

    with grid_left:
        st.markdown("<h3 style='font-size: 16px; color: #00f0ff;'>🛏️ Live ICU Bed Matrix</h3>", unsafe_allow_html=True)
        beds_df = st.session_state.patient_data
        
        # Grid of 12 Bed Mini Cards
        b_cols = st.columns(3)
        for idx, row in beds_df.iterrows():
            col_target = b_cols[idx % 3]
            card_class = f"bed-card-{row['Risk'].lower()}"
            badge_class = f"badge-{row['Risk'].lower()}"
            
            with col_target:
                if row['Risk'] == 'FREE':
                    st.markdown(f"""
                        <div class="{card_class}">
                            <div style="display: flex; justify-content: space-between;">
                                <strong>Bed {row['Bed']}</strong>
                                <span class="{badge_class}">AVAILABLE</span>
                            </div>
                            <p style="font-size: 12px; color: #64748b; margin: 10px 0 0 0;">Ready for admission</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="{card_class}">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <strong>Bed {row['Bed']}</strong>
                                <span class="{badge_class}">{row['Risk']}</span>
                            </div>
                            <div style="font-size: 13px; font-weight: bold; color: #e2e8f0; margin-top: 4px;">{row['Name']} ({row['Age']}y)</div>
                            <div style="font-size: 11px; color: #cbd5e1; margin-top: 6px; display: flex; justify-content: space-between;">
                                <span>HR: <b style="color:#00f0ff">{row['HR']}</b></span>
                                <span>BP: <b>{row['BP']}</b></span>
                                <span>SpO2: <b style="color:#10b981">{row['SpO2']}%</b></span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-size: 16px; color: #00f0ff;'>📊 Resource Utilization & Staffing</h3>", unsafe_allow_html=True)
        
        r1, r2 = st.columns(2)
        with r1:
            st.markdown("""
                <div class="glass-card">
                    <p style="font-size: 12px; font-weight: bold; color: #a0aec0; margin-bottom: 5px;">ICU CAPACITIES</p>
                    <p style="font-size: 11px; margin: 2px 0;">Bed Occupancy (75%)</p>
                    <div style="background:#1e293b; border-radius:5px; height:8px;"><div style="background:#00f0ff; width:75%; height:100%; border-radius:5px;"></div></div>
                    <p style="font-size: 11px; margin: 8px 0 2px 0;">Ventilator Usage (58%)</p>
                    <div style="background:#1e293b; border-radius:5px; height:8px;"><div style="background:#7000ff; width:58%; height:100%; border-radius:5px;"></div></div>
                    <p style="font-size: 11px; margin: 8px 0 2px 0;">Infusion Pumps (67%)</p>
                    <div style="background:#1e293b; border-radius:5px; height:8px;"><div style="background:#f59e0b; width:67%; height:100%; border-radius:5px;"></div></div>
                </div>
            """, unsafe_allow_html=True)
        with r2:
            st.markdown("""
                <div class="glass-card">
                    <p style="font-size: 12px; font-weight: bold; color: #a0aec0; margin-bottom: 8px;">DOCTOR ROUNDS SCHEDULE</p>
                    <div style="font-size: 11px; border-left: 2px solid #00f0ff; padding-left: 8px; margin-bottom: 6px;">
                        <b>08:30</b> - Dr. Mehta (Morning Round · Beds 1–4)
                    </div>
                    <div style="font-size: 11px; border-left: 2px solid #7000ff; padding-left: 8px; margin-bottom: 6px;">
                        <b>11:00</b> - Dr. Khan (Ventilator Review · Beds 5–8)
                    </div>
                    <div style="font-size: 11px; border-left: 2px solid #10b981; padding-left: 8px;">
                        <b>15:30</b> - Dr. Rao (Consultation · Beds 9–12)
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with grid_right:
        st.markdown("<h3 style='font-size: 16px; color: #ff3366;'>⚠️ Critical Early Warning Feed</h3>", unsafe_allow_html=True)
        alerts = [
            ("Bed 6 · CRITICAL", "SpO2 trend below threshold (92%)", "#ef4444"),
            ("Bed 1 · CRITICAL", "Blood pressure drop detected (92/58)", "#ef4444"),
            ("Bed 5 · CRITICAL", "High heart rate (124 bpm) + Fever (39.1°C)", "#ef4444"),
            ("Bed 8 · WARNING", "Body temperature elevated above normal", "#f59e0b"),
            ("Bed 3 · WARNING", "AI Sepsis Risk Score increased +14%", "#f59e0b"),
            ("Bed 10 · WARNING", "Routine Nurse Review overdue", "#f59e0b")
        ]
        
        for title, desc, color in alerts:
            st.markdown(f"""
                <div style="background: rgba(15, 23, 42, 0.8); border-left: 3px solid {color}; padding: 8px 12px; margin-bottom: 8px; border-radius: 4px;">
                    <span style="font-size: 11px; font-weight: bold; color: {color};">{title}</span>
                    <p style="font-size: 11px; color: #cbd5e1; margin: 2px 0 0 0;">{desc}</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<h3 style='font-size: 16px; color: #00f0ff; margin-top: 15px;'>📈 Real-Time ECG Stream</h3>", unsafe_allow_html=True)
        
        # Real-time ECG Plotly Graph
        x_ecg, y_ecg = generate_ecg_wave()
        fig_ecg = go.Figure()
        fig_ecg.add_trace(go.Scatter(x=x_ecg, y=y_ecg, mode='lines', line=dict(color='#00f0ff', width=2)))
        fig_ecg.update_layout(
            title=dict(text="BED 6 - Simulated Lead II", font=dict(size=12, color="#00f0ff")),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(5, 11, 20, 0.9)',
            margin=dict(l=10, r=10, t=30, b=10),
            height=150,
            xaxis=dict(showgrid=True, gridcolor='rgba(0,240,255,0.1)', showticklabels=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(0,240,255,0.1)', showticklabels=False)
        )
        st.plotly_chart(fig_ecg, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("""
            <div style="display: flex; justify-content: space-around; background: rgba(0,240,255,0.05); padding: 8px; border-radius: 6px; border: 1px solid rgba(0,240,255,0.1); text-align: center;">
                <div><span style="font-size: 9px; color: #a0aec0;">HR</span><br><b style="color:#ff3366; font-size:14px;">110 BPM</b></div>
                <div><span style="font-size: 9px; color: #a0aec0;">SpO2</span><br><b style="color:#00f0ff; font-size:14px;">92%</b></div>
                <div><span style="font-size: 9px; color: #a0aec0;">BP</span><br><b style="color:#10b981; font-size:14px;">96/61</b></div>
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# PAGE 2: PATIENT MONITOR
# ==========================================
elif page == "❤️ Patient Monitor":
    st.markdown("<h1>❤️ Patient Vital Signs Monitor</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #a0aec0;'>Real-time multiparameter patient status and live telemetry simulation</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Search & Filter Bar
    c_search, c_risk, c_btn = st.columns([2, 1.5, 1])
    with c_search:
        search_query = st.text_input("🔍 Search by Patient Name or Doctor", "")
    with c_risk:
        risk_filter = st.selectbox("Filter by Risk Level", ["All Levels", "CRITICAL", "WARNING", "STABLE", "FREE"])
    with c_btn:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("⚡ Simulate Live Vitals", use_container_width=True):
            trigger_vital_simulation()
            st.rerun()

    # Filter Data
    df_display = st.session_state.patient_data.copy()
    if search_query:
        df_display = df_display[df_display["Name"].str.contains(search_query, case=False) | df_display["Doctor"].str.contains(search_query, case=False)]
    if risk_filter != "All Levels":
        df_display = df_display[df_display["Risk"] == risk_filter]

    # Styled Table Display
    st.dataframe(
        df_display,
        column_config={
            "Bed": st.column_config.NumberColumn("Bed No", format="%d"),
            "HR": st.column_config.NumberColumn("Heart Rate (BPM)", format="%d"),
            "SpO2": st.column_config.NumberColumn("SpO2 (%)", format="%d%%"),
            "RR": st.column_config.NumberColumn("Resp Rate", format="%d"),
            "Score": st.column_config.ProgressColumn("AI Risk Index", min_value=0, max_value=100, format="%d%%"),
        },
        use_container_width=True,
        hide_index=True
    )

# ==========================================
# PAGE 3: AI RISK ENGINE
# ==========================================
elif page == "🧠 AI Risk Engine":
    st.markdown("<h1>🧠 AI Clinical Risk Prediction Engine</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #a0aec0;'>Machine learning predictive models assessing multi-organ physiological deterioration</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Bed Selection for AI Deep Dive
    selected_bed = st.selectbox("Select ICU Bed for AI Diagnostic Analysis:", [1, 3, 5, 6, 8, 10], index=3)
    p_data = st.session_state.patient_data[st.session_state.patient_data["Bed"] == selected_bed].iloc[0]

    ai_col1, ai_col2 = st.columns([1.2, 2])

    with ai_col1:
        st.markdown(f"""
            <div class="glass-card" style="text-align: center;">
                <h3 style="color: #a0aec0; font-size: 14px;">BED {p_data['Bed']} - {p_data['Name']}</h3>
                <h1 style="color: #ff3366; font-size: 56px; margin: 10px 0;">{p_data['Score']}%</h1>
                <p style="color: #ff3366; font-weight: bold; font-size: 14px;">HIGH DETERIORATION RISK</p>
                <p style="color: #cbd5e1; font-size: 11px;">Score trajectory increased +23% in past 4 hours</p>
                <hr style="border: 0.5px solid rgba(255,255,255,0.1);">
                <div style="text-align: left; font-size: 12px; color: #e2e8f0;">
                    <p><b>Primary Suspected Condition:</b> Severe Sepsis / Septic Shock</p>
                    <p><b>Secondary Risk:</b> Acute Respiratory Distress (ARDS)</p>
                    <p><b>Assigned Clinician:</b> {p_data['Doctor']}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    with ai_col2:
        st.markdown("""
            <div class="glass-card">
                <h3 style="color: #00f0ff; font-size: 16px; margin-top: 0;">AI Feature Attribution (SHAP Contribution Analysis)</h3>
                <p style="color: #a0aec0; font-size: 12px;">Key vital signs and laboratory markers driving the current AI risk prediction:</p>
        """, unsafe_allow_html=True)
        
        # Feature Contribution Chart
        factors = ["SpO2 Desaturation Trend", "Elevated Heart Rate", "Mean Arterial BP Drop", "Lactate Elevation", "WBC Count Marker"]
        weights = [86, 73, 69, 61, 45]
        
        fig_shap = px.bar(
            x=weights, y=factors, orientation='h',
            labels={'x': 'Risk Weight Factor (%)', 'y': 'Clinical Feature'},
            color=weights,
            color_continuous_scale=['#00f0ff', '#ff3366']
        )
        fig_shap.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(5, 11, 20, 0.9)',
            font=dict(color='#e2e8f0'),
            height=200,
            margin=dict(l=10, r=10, t=10, b=10),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_shap, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    # 3 AI Prediction Cards
    st.markdown("<h3 style='font-size: 16px; color: #00f0ff; margin-top: 10px;'>🔮 Specialized Predictive Sub-Models</h3>", unsafe_allow_html=True)
    pm1, pm2, pm3 = st.columns(3)
    with pm1:
        st.markdown("""
            <div class="glass-card">
                <h4 style="color: #ff3366; margin: 0;">Sepsis Early Prediction</h4>
                <h2 style="color: #e2e8f0; margin: 8px 0;">88% Probability</h2>
                <p style="font-size: 11px; color: #a0aec0;">Model detects systemic inflammatory response (SIRS) combined with microvascular hypoperfusion markers.</p>
            </div>
        """, unsafe_allow_html=True)
    with pm2:
        st.markdown("""
            <div class="glass-card">
                <h4 style="color: #f59e0b; margin: 0;">Cardiac Arrest / Shock Risk</h4>
                <h2 style="color: #e2e8f0; margin: 8px 0;">64% Probability</h2>
                <p style="font-size: 11px; color: #a0aec0;">ECG pulse irregularity combined with narrowing pulse pressure indicates impending hemodynamic instability.</p>
            </div>
        """, unsafe_allow_html=True)
    with pm3:
        st.markdown("""
            <div class="glass-card">
                <h4 style="color: #00f0ff; margin: 0;">Respiratory Failure (24h)</h4>
                <h2 style="color: #e2e8f0; margin: 8px 0;">79% Probability</h2>
                <p style="font-size: 11px; color: #a0aec0;">High respiratory rate / SpO2 ratio suggests respiratory muscle fatigue within 12-24 hours.</p>
            </div>
        """, unsafe_allow_html=True)

    # Mandatory Clinical Disclaimer
    st.warning("⚠️ **CLINICAL DISCLAIMER & REGULATORY BOUNDARY:** AI outputs are decision-support signals designed solely for demonstration and clinical prioritization. They do not constitute formal medical diagnoses or treatment orders.")

# ==========================================
# PAGE 4: EARLY WARNINGS
# ==========================================
elif page == "⚠️ Early Warnings":
    st.markdown("<h1>⚠️ ICU Early Warning & Triage System</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #a0aec0;'>Multilevel automated clinical alert protocol and escalation workflow</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # 3 Alert Levels Explanation Cards
    e1, e2, e3 = st.columns(3)
    with e1:
        st.markdown("""
            <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid #ef4444; border-radius: 8px; padding: 15px;">
                <h3 style="color: #ef4444; margin: 0;">LEVEL 3 · CRITICAL</h3>
                <p style="font-size: 12px; color: #cbd5e1; margin-top: 5px;">Immediate bed-side intervention required.</p>
                <b style="font-size: 11px; color: #ef4444;">Action: Auto-notify Bedside Nurse + Duty Intensivist</b>
            </div>
        """, unsafe_allow_html=True)
    with e2:
        st.markdown("""
            <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid #f59e0b; border-radius: 8px; padding: 15px;">
                <h3 style="color: #f59e0b; margin: 0;">LEVEL 2 · WARNING</h3>
                <p style="font-size: 12px; color: #cbd5e1; margin-top: 5px;">Deterioration trend detected over last 2 hours.</p>
                <b style="font-size: 11px; color: #f59e0b;">Action: Flag for Next Doctor Round Review</b>
            </div>
        """, unsafe_allow_html=True)
    with e3:
        st.markdown("""
            <div style="background: rgba(0, 240, 255, 0.15); border: 1px solid #00f0ff; border-radius: 8px; padding: 15px;">
                <h3 style="color: #00f0ff; margin: 0;">LEVEL 1 · WATCH</h3>
                <p style="font-size: 12px; color: #cbd5e1; margin-top: 5px;">Minor physiological variance recorded.</p>
                <b style="font-size: 11px; color: #00f0ff;">Action: Continue Automated Trend Monitoring</b>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><h3 style='font-size: 16px; color: #00f0ff;'>📋 Live Escalation Feed & History</h3>", unsafe_allow_html=True)

    alert_logs = [
        {"Time": "14:22:10", "Bed": "Bed 6", "Level": "LEVEL 3", "Trigger": "SpO2 drop to 91% + Tachypnea (28 bpm)", "Escalated To": "Dr. Khan & Nurse Priya S."},
        {"Time": "14:15:00", "Bed": "Bed 1", "Level": "LEVEL 3", "Trigger": "Hypotension Alert (BP 92/58 mmHg)", "Escalated To": "Dr. Mehta & Nurse Anjali P."},
        {"Time": "13:50:42", "Bed": "Bed 5", "Level": "LEVEL 3", "Trigger": "Hyperthermia (39.1°C) with Tachycardia", "Escalated To": "Dr. Khan"},
        {"Time": "13:30:15", "Bed": "Bed 8", "Level": "LEVEL 2", "Trigger": "Temperature baseline shifted upwards", "Escalated To": "Floor Nurse Duty"},
        {"Time": "12:10:05", "Bed": "Bed 3", "Level": "LEVEL 2", "Trigger": "AI Sepsis Risk score crossed 50% threshold", "Escalated To": "Dr. Rao"},
        {"Time": "11:05:30", "Bed": "Bed 10", "Level": "LEVEL 1", "Trigger": "Mild Heart Rate variation during sleep", "Escalated To": "Automated System Log"}
    ]
    st.table(pd.DataFrame(alert_logs))

# ==========================================
# PAGE 5: DOCTORS & NURSES
# ==========================================
elif page == "👨‍⚕️ Doctors & Nurses":
    st.markdown("<h1>👨‍⚕️ Clinical Roster & Staff Tracking</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #a0aec0;'>Real-time staffing allocations, shift schedules, and security access logs</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    s1, s2 = st.columns(2)

    with s1:
        st.markdown("<h3 style='font-size: 16px; color: #00f0ff;'>👨‍⚕️ Medical Specialists on Duty</h3>", unsafe_allow_html=True)
        doctors = [
            {"Name": "Dr. Mehta", "Role": "Senior Intensivist", "Shift": "08:00 - 16:00", "Next Round": "20:00", "Status": "ON DUTY"},
            {"Name": "Dr. Khan", "Role": "Critical Care Spec.", "Shift": "10:00 - 18:00", "Next Round": "15:00", "Status": "ON DUTY"},
            {"Name": "Dr. Rao", "Role": "Consultant Physician", "Shift": "14:00 - 22:00", "Next Round": "18:30", "Status": "ON DUTY"},
            {"Name": "Dr. Shah", "Role": "Night Intensivist", "Shift": "20:00 - 08:00", "Next Round": "22:00", "Status": "SCHEDULED"}
        ]
        st.dataframe(pd.DataFrame(doctors), use_container_width=True, hide_index=True)

    with s2:
        st.markdown("<h3 style='font-size: 16px; color: #00f0ff;'>👩‍⚕️ Nursing Staff Allocations</h3>", unsafe_allow_html=True)
        nurses = [
            {"Name": "Priya S.", "Role": "Primary ICU Nurse", "Assigned Beds": "Beds 1, 2, 3", "Shift": "08:00 - 20:00", "Status": "ON DUTY"},
            {"Name": "Anjali P.", "Role": "Primary ICU Nurse", "Assigned Beds": "Beds 4, 5, 6", "Shift": "08:00 - 20:00", "Status": "ON DUTY"},
            {"Name": "Rohan M.", "Role": "Senior Staff Nurse", "Assigned Beds": "Beds 7, 8, 9", "Shift": "08:00 - 20:00", "Status": "ON DUTY"},
            {"Name": "Kavita R.", "Role": "Staff Nurse", "Assigned Beds": "Beds 10, 11, 12", "Shift": "08:00 - 20:00", "Status": "ON DUTY"}
        ]
        st.dataframe(pd.DataFrame(nurses), use_container_width=True, hide_index=True)

    st.markdown("<br><h3 style='font-size: 16px; color: #00f0ff;'>🚪 Staff Smart Keycard Access & Entry Logs</h3>", unsafe_allow_html=True)
    access_logs = [
        {"Name": "Priya S.", "Role": "Nurse", "Entry Time": "07:54:12 IST", "Exit Time": "--", "Access Point": "ICU Main Airlock"},
        {"Name": "Dr. Mehta", "Role": "Doctor", "Entry Time": "07:51:00 IST", "Exit Time": "--", "Access Point": "ICU Main Airlock"},
        {"Name": "Anjali P.", "Role": "Nurse", "Entry Time": "08:02:45 IST", "Exit Time": "--", "Access Point": "ICU North Door"},
        {"Name": "Dr. Khan", "Role": "Doctor", "Entry Time": "09:48:30 IST", "Exit Time": "--", "Access Point": "ICU Main Airlock"},
        {"Name": "Dr. Rao", "Role": "Consultant", "Entry Time": "13:42:10 IST", "Exit Time": "--", "Access Point": "ICU Main Airlock"}
    ]
    st.table(pd.DataFrame(access_logs))

# ==========================================
# PAGE 6: BED MANAGEMENT
# ==========================================
elif page == "🛏️ Bed Management":
    st.markdown("<h1>🛏️ ICU Bed Management & Admissions</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #a0aec0;'>Bed occupancy logistics, patient transfers, and discharge workflows</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    bm1, bm2, bm3 = st.columns(3)
    with bm1:
        st.markdown("<div class='glass-card' style='text-align:center;'><h3>Total Beds</h3><h1 style='color:#00f0ff;'>12</h1></div>", unsafe_allow_html=True)
    with bm2:
        st.markdown("<div class='glass-card' style='text-align:center;'><h3>Occupied Beds</h3><h1 style='color:#ff3366;'>9</h1></div>", unsafe_allow_html=True)
    with bm3:
        st.markdown("<div class='glass-card' style='text-align:center;'><h3>Available Beds</h3><h1 style='color:#10b981;'>3</h1></div>", unsafe_allow_html=True)

    st.markdown("<h3 style='font-size: 16px; color: #00f0ff;'>🔄 Bed Movement & Event Log</h3>", unsafe_allow_html=True)
    bed_events = [
        {"Time": "09:35 IST", "Patient": "A. Verma", "Event": "New Emergency Admission", "Bed": "Bed 10", "Handled By": "Nurse Priya S."},
        {"Time": "09:10 IST", "Patient": "M. Joshi", "Event": "Transfer to Step-down Ward", "Bed": "Bed 7", "Handled By": "Dr. Rao"},
        {"Time": "08:45 IST", "Patient": "S. Khan", "Event": "Emergency Admission (Post-Op)", "Bed": "Bed 6", "Handled By": "Nurse Anjali P."},
        {"Time": "07:30 IST", "Patient": "P. Singh", "Event": "Discharged Home", "Bed": "Bed 3", "Handled By": "Dr. Mehta"}
    ]
    st.table(pd.DataFrame(bed_events))

# ==========================================
# PAGE 7: EQUIPMENT
# ==========================================
elif page == "⚙️ Equipment":
    st.markdown("<h1>⚙️ ICU Equipment & IoT Telemetry</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #a0aec0;'>Real-time operational status, battery levels, and maintenance alerts for critical biomedical devices</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    equipment_data = [
        {"Equipment": "Multiparameter Monitor v4", "Location": "Bed 1", "Status": "ONLINE", "Battery": "100%", "Last Calibration": "Today 09:20", "Maintenance": "Optimal"},
        {"Equipment": "Mechanical Ventilator EV-800", "Location": "Bed 2", "Status": "ONLINE", "Battery": "98%", "Last Calibration": "Today 09:15", "Maintenance": "Optimal"},
        {"Equipment": "Smart Infusion Pump", "Location": "Bed 5", "Status": "LOW BATTERY", "Battery": "14%", "Last Calibration": "Today 09:04", "Maintenance": "Service Required"},
        {"Equipment": "Portable ECG Machine", "Location": "Procedure Room", "Status": "READY", "Battery": "85%", "Last Calibration": "Today 08:45", "Maintenance": "Optimal"},
        {"Equipment": "Crash Cart Defibrillator", "Location": "Emergency Bay", "Status": "READY", "Battery": "100%", "Last Calibration": "Today 08:30", "Maintenance": "Optimal"},
        {"Equipment": "Central Telemetry Hub", "Location": "Server Room", "Status": "ONLINE", "Battery": "Mains Power", "Last Calibration": "Yesterday", "Maintenance": "Optimal"}
    ]
    st.dataframe(pd.DataFrame(equipment_data), use_container_width=True, hide_index=True)

# ==========================================
# PAGE 8: LABS & REPORTS
# ==========================================
elif page == "🩸 Labs & Reports":
    st.markdown("<h1>🩸 Laboratory & Hematology Reports</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #a0aec0;'>Automated LIS integration tracking critical arterial blood gas and organ function markers</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    labs_data = [
        {"Patient": "R. Sharma (Bed 1)", "Test": "Hemoglobin (Hb)", "Result": "9.2 g/dL", "Reference": "13.0 - 17.0 g/dL", "Status": "REVIEW REQUIRED"},
        {"Patient": "A. Patil (Bed 2)", "Test": "White Blood Cells (WBC)", "Result": "15.8 K/µL", "Reference": "4.5 - 11.0 K/µL", "Status": "HIGH (INFLAMMATORY)"},
        {"Patient": "S. Khan (Bed 6)", "Test": "Blood Lactate", "Result": "3.8 mmol/L", "Reference": "0.5 - 1.0 mmol/L", "Status": "CRITICAL (HYPOPERFUSION)"},
        {"Patient": "M. Joshi (Bed 3)", "Test": "Serum Creatinine", "Result": "1.4 mg/dL", "Reference": "0.7 - 1.3 mg/dL", "Status": "NORMAL RANGE"},
        {"Patient": "A. Verma (Bed 5)", "Test": "Procalcitonin", "Result": "4.2 ng/mL", "Reference": "< 0.15 ng/mL", "Status": "CRITICAL SEPSIS MARKER"}
    ]
    st.dataframe(pd.DataFrame(labs_data), use_container_width=True, hide_index=True)

    st.markdown("<br><h3 style='font-size: 16px; color: #00f0ff;'>🔗 Connected Data Streams to AI Model</h3>", unsafe_allow_html=True)
    st.info("The Sentinel AI Engine correlates continuous ECG, NIBP, SpO2, and Respiratory streams with discrete LIS outputs (CBC, Arterial Blood Gas, Electrolytes, Renal Panel) to compute dynamic clinical risk scores.")

# ==========================================
# PAGE 9: CLINICAL SUPPORT
# ==========================================
elif page == "✚ Clinical Support":
    st.markdown("<h1>✚ AI Clinical Decision Support System (CDSS)</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #a0aec0;'>Intelligent clinical tools, safety verification systems, and analytical summary engines</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # 6 Premium Cards
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
            <div class="glass-card">
                <span style="color:#00f0ff; font-weight:bold; font-size:18px;">01</span>
                <h4 style="margin: 5px 0;">Clinical Decision Support</h4>
                <p style="font-size:11px; color:#a0aec0;">Surface patient-specific protocol recommendations, care reminders, and diagnostic priorities.</p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="glass-card">
                <span style="color:#00f0ff; font-weight:bold; font-size:18px;">02</span>
                <h4 style="margin: 5px 0;">Drug Interaction Check</h4>
                <p style="font-size:11px; color:#a0aec0;">Automated cross-referencing of active infusions to prevent nephrotoxic or arrhythmogenic polypharmacy.</p>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
            <div class="glass-card">
                <span style="color:#00f0ff; font-weight:bold; font-size:18px;">03</span>
                <h4 style="margin: 5px 0;">ICU Care Guidelines</h4>
                <p style="font-size:11px; color:#a0aec0;">Structured evidentiary checklists for sepsis bundles, ventilator weaning, and central line safety.</p>
            </div>
        """, unsafe_allow_html=True)

    c4, c5, c6 = st.columns(3)
    with c4:
        st.markdown("""
            <div class="glass-card">
                <span style="color:#00f0ff; font-weight:bold; font-size:18px;">04</span>
                <h4 style="margin: 5px 0;">AI Medical Assistant</h4>
                <p style="font-size:11px; color:#a0aec0;">Natural language querying across unstructured clinical notes and longitudinal lab results.</p>
            </div>
        """, unsafe_allow_html=True)
    with c5:
        st.markdown("""
            <div class="glass-card">
                <span style="color:#00f0ff; font-weight:bold; font-size:18px;">05</span>
                <h4 style="margin: 5px 0;">Recovery Analytics</h4>
                <p style="font-size:11px; color:#a0aec0;">Predictive length-of-stay estimation and post-extubation success probability modelling.</p>
            </div>
        """, unsafe_allow_html=True)
    with c6:
        st.markdown("""
            <div class="glass-card">
                <span style="color:#00f0ff; font-weight:bold; font-size:18px;">06</span>
                <h4 style="margin: 5px 0;">Hospital Intelligence Reports</h4>
                <p style="font-size:11px; color:#a0aec0;">Executive telemetry analytics on bed throughput, mortality risk reduction, and device uptime.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="border: 1px dashed rgba(255, 51, 102, 0.4); background: rgba(255, 51, 102, 0.05); border-radius: 8px; padding: 15px; text-align: center;">
            <h4 style="color: #ff3366; margin: 0 0 5px 0;">AI SAFETY & COMPLIANCE BOUNDARY</h4>
            <p style="color: #cbd5e1; font-size: 11px; margin: 0;">
                This competition prototype uses synthetic data. AI outputs are non-binding decision-support signals and must not be used as direct medical orders.
                Production deployment requires clinical validation, HIPAA/GDPR data protection controls, HL7/FHIR EHR integration, and regulatory approval.
            </p>
        </div>
    """, unsafe_allow_html=True)
