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
# BLACK THEME CSS
# =====================================================
st.markdown("""
<style>

/* Main Background */
[data-testid="stAppViewContainer"]{
background: linear-gradient(135deg,#000000,#0d0d0d,#1a1a1a);
color:white;
}

/* Header */
[data-testid="stHeader"]{
background: rgba(0,0,0,0);
}

/* Sidebar */
[data-testid="stSidebar"]{
background: linear-gradient(180deg,#050505,#111111);
}

/* Text */
h1,h2,h3,h4,h5,h6,p,label,span,div{
color:white !important;
}

/* Selectbox */
div[data-baseweb="select"] > div{
background: rgba(255,255,255,0.08)!important;
border-radius:10px;
border:1px solid rgba(255,255,255,0.18);
}

/* Metrics */
div[data-testid="metric-container"]{
background: rgba(255,255,255,0.06);
border-radius:14px;
padding:16px;
border:1px solid rgba(255,255,255,0.12);
}

/* Buttons */
button{
border-radius:10px !important;
}

/* Tables */
table{
color:white !important;
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
st.caption("Team Members: Anushka Singh | Astha Singh | Kritika Vashishtha")

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
# COMMON CHART STYLE
# =====================================================
def black_chart(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.03)",
        font_color="white",
        xaxis=dict(color="white", gridcolor="rgba(255,255,255,0.10)"),
        yaxis=dict(color="white", gridcolor="rgba(255,255,255,0.10)")
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
        st.plotly_chart(
            black_chart(fig1),
            use_container_width=True
        )

    with c2:
        fig2 = px.line(
            temp,
            y=metric,
            markers=True,
            title="Trend Line"
        )
        fig2.update_traces(
            line=dict(color="white", width=3),
            marker=dict(color="white", size=8)
        )
        st.plotly_chart(
            black_chart(fig2),
            use_container_width=True
        )

    c3,c4 = st.columns(2)

    with c3:
        fig3 = px.area(
            temp,
            y=metric,
            title="Area Chart"
        )
        fig3.update_traces(
            line=dict(color="white"),
            fillcolor="rgba(255,255,255,0.20)"
        )
        st.plotly_chart(
            black_chart(fig3),
            use_container_width=True
        )

    with c4:
        fig4 = px.scatter(
            temp,
            x=temp.index,
            y=metric,
            title="Scatter Plot",
            size=metric
        )
        fig4.update_traces(marker=dict(color="white"))
        st.plotly_chart(
            black_chart(fig4),
            use_container_width=True
        )

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

    chart = st.line_chart(
        pd.DataFrame({metric:[base]})
    )

    for i in range(25):
        val = base + np.random.randn()*0.4
        chart.add_rows(pd.DataFrame({metric:[val]}))
        time.sleep(0.2)

# =====================================================
# AI REPORT
# =====================================================
elif page == "📄 AI Clinical Report":

    st.header("AI Generated Clinical Report")

    subjects = sorted(df[subject_col].unique())

    selected_subject = st.selectbox("Select Subject", subjects)

    temp = df[df[subject_col] == selected_subject]

    score = round(temp[numeric_cols].mean().mean(),2)
    idx = subjects.index(selected_subject)

    if score >= 80:
        risk = "Low Risk"
    elif score >= 60:
        risk = "Moderate Risk"
    else:
        risk = "High Risk"

    findings = [
        "Stable reverse gait with strong balance response.",
        "Minor instability observed.",
        "Reduced coordination under demand.",
        "Mild hesitation during reverse steps.",
        "Efficient movement control noted.",
        "Shortened stride pattern present.",
        "Moderate postural sway detected.",
        "Strong recovery reactions observed.",
        "Cadence inconsistency noted.",
        "Good postural alignment maintained.",
        "Transition delay visible.",
        "Adequate limb control present.",
        "Fatigue tendency observed.",
        "Excellent mobility control.",
        "Cautious stepping strategy noted."
    ]

    recommendations = [
        "Continue present routine and monthly review.",
        "Add weekly balance drills.",
        "Coordination training recommended.",
        "Reverse step initiation practice advised.",
        "Maintain current rehabilitation plan.",
        "Stride enhancement drills suggested.",
        "Schedule physiotherapy review.",
        "Continue neuromuscular training.",
        "Cadence rhythm exercises advised.",
        "Maintain active mobility plan.",
        "Reaction-time exercises recommended.",
        "Strength maintenance advised.",
        "Endurance conditioning suggested.",
        "Continue excellent current performance.",
        "Close monitoring recommended."
    ]

    st.metric("Clinical Score", score)
    st.metric("Risk Level", risk)

    st.subheader("Clinical Finding")
    st.write(findings[idx])

    fig6 = px.bar(
        x=temp[numeric_cols].mean().index,
        y=temp[numeric_cols].mean().values,
        title="Performance Metrics",
        color_discrete_sequence=["white"]
    )

    st.plotly_chart(
        black_chart(fig6),
        use_container_width=True
    )

    st.subheader("Recommendation")
    st.success(recommendations[idx])

    report = f"""
AI CLINICAL REPORT

Subject: {selected_subject}
Clinical Score: {score}
Risk Level: {risk}

Finding:
{findings[idx]}

Recommendation:
{recommendations[idx]}
"""

    st.download_button(
        "Download Report",
        data=report,
        file_name=f"{selected_subject}_report.txt",
        mime="text/plain"
    )
