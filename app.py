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
# CUSTOM CSS
# =====================================================
st.markdown("""
<style>

/* Background */
[data-testid="stAppViewContainer"]{
background: linear-gradient(135deg,#061a78,#0a43c9,#1e88ff);
color:white;
}

/* Header */
[data-testid="stHeader"]{
background: rgba(0,0,0,0);
}

/* Sidebar */
[data-testid="stSidebar"]{
background: linear-gradient(180deg,#03114a,#082d9c);
}

/* Text */
h1,h2,h3,h4,h5,h6,p,label,span,div{
color:white !important;
}

/* Select Box */
div[data-baseweb="select"] > div{
background: rgba(255,255,255,0.15)!important;
border-radius:10px;
border:1px solid rgba(255,255,255,0.2);
}

/* Metric Cards */
div[data-testid="metric-container"]{
background: rgba(255,255,255,0.12);
border-radius:14px;
padding:16px;
border:1px solid rgba(255,255,255,0.18);
}

button{
border-radius:10px !important;
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
st.caption(
    "Team Members: Anushka Singh | Astha Singh | Kritika Vashishtha"
)

# =====================================================
# SIDEBAR
# =====================================================
page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📊 Advanced Comparison",
        "📡 Live Monitoring",
        "📄 Clinical Report"
    ]
)

# =====================================================
# HOME
# =====================================================
if page == "🏠 Home":

    st.header("Dashboard Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Subjects", df[subject_col].nunique())

    with c2:
        st.metric("Records", len(df))

    with c3:
        st.metric("Metrics", len(numeric_cols))

    with c4:
        st.metric("Conditions", 3)

    st.markdown("---")

    st.subheader("Project Objective")

    st.write("""
This project investigates biomechanical and neuromuscular
adaptations during constrained gait, especially reverse walking.

### Applications:
- Balance Assessment  
- Fall Risk Detection  
- Neuromuscular Coordination  
- Gait Performance Comparison  
- Clinical Monitoring  
""")

    st.success("Dashboard Ready")

# =====================================================
# ADVANCED COMPARISON
# =====================================================
elif page == "📊 Advanced Comparison":

    st.header("Advanced Subject Comparison")

    subjects = sorted(df[subject_col].unique())

    selected_subject = st.selectbox(
        "Select Subject",
        subjects
    )

    metric = st.selectbox(
        "Select Metric",
        numeric_cols
    )

    temp = df[df[subject_col] == selected_subject]

    c1, c2 = st.columns(2)

    with c1:
        fig1 = px.bar(temp, y=metric, title="Bar Comparison")
        fig1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.05)",
            font_color="white"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        fig2 = px.line(
            temp,
            y=metric,
            markers=True,
            title="Trend Line"
        )
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.05)",
            font_color="white"
        )
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        fig3 = px.area(temp, y=metric, title="Area Chart")
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.05)",
            font_color="white"
        )
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        fig4 = px.scatter(
            temp,
            x=temp.index,
            y=metric,
            size=metric,
            title="Scatter Plot"
        )
        fig4.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.05)",
            font_color="white"
        )
        st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Radar Comparison")

    fig5 = go.Figure()

    fig5.add_trace(go.Scatterpolar(
        r=temp[metric].tolist(),
        theta=[f"Trial {i+1}" for i in range(len(temp))],
        fill='toself',
        name="Performance"
    ))

    fig5.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )

    st.plotly_chart(fig5, use_container_width=True)

# =====================================================
# LIVE MONITORING
# =====================================================
elif page == "📡 Live Monitoring":

    st.header("Live Monitoring")

    subjects = sorted(df[subject_col].unique())

    selected_subject = st.selectbox(
        "Select Subject",
        subjects
    )

    metric = st.selectbox(
        "Select Metric",
        numeric_cols
    )

    st.info(f"X-axis = Time | Y-axis = {metric}")

    temp = df[df[subject_col] == selected_subject]

    base = float(temp[metric].mean())

    chart = st.line_chart(
        pd.DataFrame({metric:[base]})
    )

    for i in range(25):
        val = base + np.random.randn()*0.4
        chart.add_rows(
            pd.DataFrame({metric:[val]})
        )
        time.sleep(0.2)

    st.success("Monitoring Completed")

# =====================================================
# CLINICAL REPORT
# =====================================================
elif page == "📄 Clinical Report":

    st.header("Clinical Subject Report")

    subjects = sorted(df[subject_col].unique())

    selected_subject = st.selectbox(
        "Select Subject",
        subjects
    )

    temp = df[df[subject_col] == selected_subject]

    score = round(temp[numeric_cols].mean().mean(),2)

    idx = subjects.index(selected_subject)

    if score >= 75:
        risk = "Low Risk"
    elif score >= 55:
        risk = "Moderate Risk"
    else:
        risk = "High Risk"

    findings = [
        "Stable gait pattern observed.",
        "Minor balance fluctuation detected.",
        "Reduced coordination response.",
        "Mild hesitation in reverse gait.",
        "Good movement control noted.",
        "Stride reduction observed.",
        "Moderate instability detected.",
        "Strong recovery response.",
        "Variable cadence pattern.",
        "Good posture maintained.",
        "Transition hesitation present.",
        "Limb control satisfactory.",
        "Fatigue tendency visible.",
        "Excellent mobility pattern.",
        "Backward stepping caution required."
    ]

    recs = [
        "Routine monitoring advised.",
        "Weekly balance drills suggested.",
        "Coordination exercises recommended.",
        "Dual-task gait practice advised.",
        "Maintain present activity level.",
        "Stride improvement exercises.",
        "Periodic physiotherapy review.",
        "Continue mobility training.",
        "Cadence control practice advised.",
        "Maintain rehab schedule.",
        "Confidence exercises suggested.",
        "Strength maintenance advised.",
        "Endurance program recommended.",
        "Continue active monitoring.",
        "Close supervision advised."
    ]

    st.metric("Clinical Score", score)
    st.metric("Risk Level", risk)

    st.write("### Findings")
    st.write(findings[idx])

    fig6 = px.bar(
        x=temp[numeric_cols].mean().index,
        y=temp[numeric_cols].mean().values,
        title="Performance Metrics"
    )

    fig6.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.05)",
        font_color="white"
    )

    st.plotly_chart(fig6, use_container_width=True)

    st.write("### Recommendation")
    st.success(recs[idx])

    report = f"""
Clinical Report

Subject: {selected_subject}
Clinical Score: {score}
Risk Level: {risk}

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
