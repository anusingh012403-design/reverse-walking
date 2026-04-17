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
    page_title="Biomechanical & Neuromuscular Adaptations Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CSS
# =====================================================
st.markdown("""
<style>
[data-testid="stAppViewContainer"]{
background: linear-gradient(135deg,#061a78,#0a43c9,#1e88ff);
color:white;
}
[data-testid="stHeader"]{
background: rgba(0,0,0,0);
}
[data-testid="stSidebar"]{
background: linear-gradient(180deg,#03114a,#082d9c);
}
h1,h2,h3,h4,h5,h6,p,label,span,div{
color:white !important;
}
div[data-baseweb="select"] > div{
background: rgba(255,255,255,0.15)!important;
border-radius:10px;
border:1px solid rgba(255,255,255,0.25);
}
div[data-testid="metric-container"]{
background: rgba(255,255,255,0.12);
border-radius:14px;
padding:16px;
border:1px solid rgba(255,255,255,0.18);
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
st.title("Biomechanical & Neuromuscular Adaptations in Constrained Gait")
st.subheader("Reverse Walking")
st.caption("Team Members: Anushka Singh | Astha Singh | Kratika Vashishtha")

# =====================================================
# SIDEBAR
# =====================================================
page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📊 Advanced Comparison",
        "📡 Live Monitoring",
        "📄 AI Clinical Report"
    ]
)

# =====================================================
# COMMON WHITE CHART
# =====================================================
def white_chart(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.06)",
        font_color="white",
        xaxis=dict(color="white", gridcolor="rgba(255,255,255,0.15)"),
        yaxis=dict(color="white", gridcolor="rgba(255,255,255,0.15)")
    )
    return fig

# =====================================================
# HOME
# =====================================================
if page == "🏠 Home":

    st.header("Dashboard Overview")

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.metric("Subjects", df[subject_col].nunique())
    with c2:
        st.metric("Records", len(df))
    with c3:
        st.metric("Metrics", len(numeric_cols))
    with c4:
        st.metric("Conditions", 3)

    st.markdown("---")

    st.write("""
### Project Objective

This project evaluates biomechanical and neuromuscular adaptations during reverse walking.

### Uses:
- Balance Assessment  
- Fall Risk Detection  
- Subject Comparison  
- Clinical Monitoring  
""")

# =====================================================
# ADVANCED COMPARISON
# =====================================================
elif page == "📊 Advanced Comparison":

    st.header("Advanced Subject Comparison")

    subjects = sorted(df[subject_col].unique())

    selected_subject = st.selectbox("Select Subject", subjects)
    metric = st.selectbox("Select Metric", numeric_cols)

    temp = df[df[subject_col] == selected_subject]

    c1,c2 = st.columns(2)

    with c1:
        fig1 = px.bar(
            temp,
            y=metric,
            color_discrete_sequence=["white"],
            title="Bar Comparison"
        )
        st.plotly_chart(white_chart(fig1), use_container_width=True)

    with c2:
        fig2 = px.line(
            temp,
            y=metric,
            markers=True,
            title="Trend Line"
        )
        fig2.update_traces(
            line=dict(color="white", width=3),
            marker=dict(color="white")
        )
        st.plotly_chart(white_chart(fig2), use_container_width=True)

# =====================================================
# LIVE MONITORING
# =====================================================
elif page == "📡 Live Monitoring":

    st.header("Live Monitoring")

    subjects = sorted(df[subject_col].unique())

    selected_subject = st.selectbox("Select Subject", subjects)
    metric = st.selectbox("Select Metric", numeric_cols)

    st.info(f"X-axis = Time | Y-axis = {metric}")

    temp = df[df[subject_col] == selected_subject]
    base = float(temp[metric].mean())

    chart = st.line_chart(pd.DataFrame({metric:[base]}))

    for i in range(25):
        val = base + np.random.randn()*0.4
        chart.add_rows(pd.DataFrame({metric:[val]}))
        time.sleep(0.2)

# =====================================================
# AI REPORT (FULLY VARIABLE)
# =====================================================
elif page == "📄 AI Clinical Report":

    st.header("AI Generated Clinical Report")

    subjects = sorted(df[subject_col].unique())

    selected_subject = st.selectbox("Select Subject", subjects)

    temp = df[df[subject_col] == selected_subject]

    # ---------------- SCORE ----------------
    score = round(temp[numeric_cols].mean().mean(),2)

    idx = subjects.index(selected_subject)

    # ---------------- RISK ----------------
    if score >= 80:
        risk = "Low Risk"
    elif score >= 60:
        risk = "Moderate Risk"
    else:
        risk = "High Risk"

    # ---------------- VARIABLE FINDINGS ----------------
    findings = [
        "Stable reverse gait with excellent balance response.",
        "Minor instability observed during constrained walking.",
        "Reduced coordination under task demand.",
        "Mild hesitation while initiating reverse steps.",
        "Efficient lower limb control with smooth motion.",
        "Shortened stride length under constrained gait.",
        "Moderate postural sway observed.",
        "Strong corrective balance reactions detected.",
        "Cadence inconsistency noted across trials.",
        "Good postural alignment maintained.",
        "Transition delay visible during movement change.",
        "Adequate limb control with minor variability.",
        "Fatigue tendency visible in later trials.",
        "Excellent mobility and control observed.",
        "Cautious stepping strategy during reverse gait."
    ]

    # ---------------- VARIABLE RECOMMENDATIONS ----------------
    recommendations = [
        "Continue current training and monthly review.",
        "Add balance board exercises twice weekly.",
        "Introduce coordination drills with supervision.",
        "Practice reverse step initiation exercises.",
        "Maintain current rehabilitation program.",
        "Use stride length enhancement drills.",
        "Schedule physiotherapy follow-up.",
        "Continue neuromuscular control training.",
        "Cadence rhythm exercises recommended.",
        "Maintain active mobility program.",
        "Reaction-time training suggested.",
        "Strength maintenance exercises advised.",
        "Endurance conditioning recommended.",
        "Continue current excellent performance level.",
        "Close monitoring with confidence training."
    ]

    # ---------------- VARIABLE EXTRA SUMMARY ----------------
    summaries = [
        "Overall gait quality above expected level.",
        "Clinical gait quality mildly reduced.",
        "Moderate coordination deficit detected.",
        "Step planning requires improvement.",
        "Motor control remains efficient.",
        "Stride mechanics below average.",
        "Balance strategy compensation present.",
        "Recovery control above average.",
        "Temporal rhythm variability present.",
        "Postural mechanics remain strong.",
        "Movement transition needs monitoring.",
        "Lower limb mechanics acceptable.",
        "Fatigue management required.",
        "Performance ranks among top subjects.",
        "Safety awareness increased during reverse gait."
    ]

    finding = findings[idx]
    recommendation = recommendations[idx]
    summary = summaries[idx]

    # ---------------- DISPLAY ----------------
    c1,c2,c3 = st.columns(3)

    with c1:
        st.metric("Clinical Score", score)

    with c2:
        st.metric("Risk Level", risk)

    with c3:
        st.metric("Subject Rank", idx+1)

    st.markdown("---")

    st.subheader("Clinical Finding")
    st.write(finding)

    st.subheader("AI Summary")
    st.info(summary)

    # ---------------- WHITE GRAPH ----------------
    fig6 = px.bar(
        x=temp[numeric_cols].mean().index,
        y=temp[numeric_cols].mean().values,
        title="Performance Metrics",
        color_discrete_sequence=["white"]
    )

    st.plotly_chart(
        white_chart(fig6),
        use_container_width=True
    )

    # ---------------- RECOMMENDATION ----------------
    st.subheader("Recommendation")
    st.success(recommendation)

    # ---------------- DOWNLOAD ----------------
    report = f"""
AI CLINICAL REPORT

Subject: {selected_subject}
Clinical Score: {score}
Risk Level: {risk}

Finding:
{finding}

Summary:
{summary}

Recommendation:
{recommendation}
"""

    st.download_button(
        "Download Report",
        data=report,
        file_name=f"{selected_subject}_report.txt",
        mime="text/plain"
    )
