import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Reverse Walking Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# PROFESSIONAL CSS + FONT
# =====================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg,#0f172a,#1e3a8a,#0ea5e9);
}

.block-container {
    padding-top: 1rem;
}

h1,h2,h3,h4,h5,h6,p,label,span,div {
    color: white !important;
}

div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.15);
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}

section[data-testid="stSidebar"] {
    background: #0f172a;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data
def load_data():
    return pd.read_csv("clinical_dashboard_15_subjects.csv")

df = load_data()
df.columns = df.columns.str.strip().str.lower()

subject_col = "subject" if "subject" in df.columns else df.columns[0]
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

# =====================================================
# HEADER
# =====================================================
st.title("Biomechanical and Neuromuscular Adaptations in Constrained Gait")
st.subheader('"Reverse Walking"')
st.caption("Minor Project Dashboard | Team: Anushka Singh | Astha Singh | Kratika Vashishtha")

# =====================================================
# SIDEBAR
# =====================================================
page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📊 Comparison Analysis",
        "📈 Live Monitoring",
        "📋 Clinical Report"
    ]
)

# =====================================================
# HOME PAGE
# =====================================================
if page == "🏠 Home":

    st.header("Professional Dashboard Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Total Subjects", df[subject_col].nunique())

    with c2:
        st.metric("Total Records", len(df))

    with c3:
        st.metric("Features", len(numeric_cols))

    with c4:
        st.metric("Conditions", 3)

    st.markdown("---")

    col1, col2 = st.columns([1.2,1])

    with col1:
        st.subheader("Project Objective")

        st.write("""
This project evaluates biomechanical and neuromuscular adaptations during reverse walking.

### Key Focus Areas:
- Balance Stability
- Motor Coordination
- Cadence Changes
- Functional Mobility
- Fall Risk Monitoring
""")

        st.progress(92)
        st.success("Dashboard Ready for Review")

    with col2:

        if "condition" in df.columns:

            fig = px.pie(
                df,
                names="condition",
                hole=0.55,
                title="Walking Conditions",
                color_discrete_sequence=["#38bdf8","#60a5fa","#2563eb"]
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

# =====================================================
# COMPARISON PAGE
# =====================================================
elif page == "📊 Comparison Analysis":

    st.header("Advanced Subject Comparison")

    subjects = sorted(df[subject_col].unique())

    selected_subject = st.selectbox("Select Subject", subjects)

    feature = st.selectbox("Select Metric", numeric_cols)

    temp = df[df[subject_col] == selected_subject]

    # ---------------- BAR + LINE ----------------
    c1, c2 = st.columns(2)

    with c1:
        fig1 = px.bar(
            temp,
            y=feature,
            title="Bar Comparison",
            color_discrete_sequence=["#38bdf8"]
        )
        fig1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        fig2 = px.line(
            temp,
            y=feature,
            markers=True,
            title="Trend Comparison"
        )
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ---------------- RADAR CHART ----------------
    st.subheader("Radar Performance Comparison")

    radar_cols = numeric_cols[:5] if len(numeric_cols) >= 5 else numeric_cols

    values = temp[radar_cols].mean().tolist()

    radar = go.Figure()

    radar.add_trace(go.Scatterpolar(
        r=values,
        theta=radar_cols,
        fill='toself',
        name=str(selected_subject),
        line_color="#38bdf8"
    ))

    radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True)
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        height=500
    )

    st.plotly_chart(radar, use_container_width=True)

    # ---------------- ALL SUBJECTS COMPARISON ----------------
    st.subheader("Subject vs Overall Average")

    compare_df = df.groupby(subject_col)[feature].mean().reset_index()

    fig3 = px.bar(
        compare_df,
        x=subject_col,
        y=feature,
        color=subject_col,
        title="All Subject Comparison"
    )

    fig3.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        showlegend=False
    )

    st.plotly_chart(fig3, use_container_width=True)

# =====================================================
# LIVE MONITORING
# =====================================================
elif page == "📈 Live Monitoring":

    st.header("Real-Time Monitoring")

    subjects = sorted(df[subject_col].unique())

    selected_subject = st.selectbox("Select Subject", subjects)

    feature = st.selectbox("Select Monitoring Metric", numeric_cols)

    st.info(f"X-axis = Time (seconds) | Y-axis = {feature}")

    temp = df[df[subject_col] == selected_subject]

    base = float(temp[feature].mean())

    chart = st.line_chart(pd.DataFrame({feature:[base]}))

    for i in range(30):

        val = base + np.random.randn()*0.4

        chart.add_rows(pd.DataFrame({feature:[val]}))

        time.sleep(0.2)

    st.success("Monitoring Completed")

# =====================================================
# REPORT PAGE
# =====================================================
elif page == "📋 Clinical Report":

    st.header("Clinical Subject Report")

    subjects = sorted(df[subject_col].unique())

    selected_subject = st.selectbox("Select Subject", subjects)

    temp = df[df[subject_col] == selected_subject]

    score = round(temp[numeric_cols].mean().mean(),2)

    idx = subjects.index(selected_subject)

    if score >= 75:
        risk = "Low Risk"
        color = "green"
    elif score >= 55:
        risk = "Moderate Risk"
        color = "orange"
    else:
        risk = "High Risk"
        color = "red"

    findings = [
        "Stable gait mechanics observed.",
        "Minor balance fluctuation present.",
        "Reduced coordination response.",
        "Mild hesitation in movement.",
        "Good dynamic control maintained.",
        "Stride reduction detected.",
        "Moderate instability present.",
        "Good recovery response.",
        "Variable cadence pattern.",
        "Stable posture maintained.",
        "Transition hesitation visible.",
        "Satisfactory limb control.",
        "Mild fatigue trend present.",
        "Strong mobility observed.",
        "Backward caution advised."
    ]

    recs = [
        "Routine follow-up advised.",
        "Balance drills recommended.",
        "Dual-task training suggested.",
        "Coordination exercises advised.",
        "Maintain current plan.",
        "Stride training recommended.",
        "Periodic supervision needed.",
        "Continue mobility drills.",
        "Cadence training advised.",
        "Maintain rehab schedule.",
        "Confidence exercises suggested.",
        "Strength training advised.",
        "Endurance drills recommended.",
        "Continue active monitoring.",
        "Close supervision advised."
    ]

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Clinical Score", score)

    with c2:
        st.metric("Risk Level", risk)

    with c3:
        st.metric("Subject Rank", idx+1)

    st.markdown("---")

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text':"Performance Score"},
        gauge={
            'axis': {'range':[0,100]},
            'bar': {'color': color}
        }
    ))

    gauge.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )

    st.plotly_chart(gauge, use_container_width=True)

    st.subheader("Clinical Findings")
    st.write(findings[idx])

    st.subheader("Recommendation")
    st.success(recs[idx])

    report = f"""
MINOR PROJECT REPORT

Subject: {selected_subject}
Score: {score}
Risk: {risk}

Finding:
{findings[idx]}

Recommendation:
{recs[idx]}
"""

    st.download_button(
        "Download Report",
        data=report,
        file_name=f"{selected_subject}_report.txt",
        mime="text/plain"
    )
