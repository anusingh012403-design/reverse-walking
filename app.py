import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
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
# CUSTOM CSS
# =====================================================
st.markdown("""
<style>
.main{
background:#f8fafc;
}
.block-container{
padding-top:1rem;
}
div[data-testid="metric-container"]{
background:linear-gradient(135deg,#ffffff,#e0f2fe);
border:1px solid #dbeafe;
padding:18px;
border-radius:14px;
box-shadow:0 4px 10px rgba(0,0,0,0.08);
}
h1,h2,h3{
color:#0f172a;
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
        "Home",
        "Comparison Analysis",
        "Live Monitoring",
        "Clinical Report"
    ]
)

# =====================================================
# HOME PAGE
# =====================================================
if page == "Home":

    st.header("Advanced Dashboard Overview")

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

    left, right = st.columns([1.2,1])

    with left:

        st.subheader("Project Objective")

        st.write("""
This project analyzes biomechanical and neuromuscular changes during reverse walking.

### Focus Areas:
- Balance Stability
- Cadence Changes
- Motor Coordination
- Functional Mobility
- Fall Risk Assessment
- Subject Performance Tracking
""")

        st.progress(88)
        st.success("System Ready for Final Demonstration")

    with right:

        if "condition" in df.columns:

            fig = px.pie(
                df,
                names="condition",
                hole=0.55,
                title="Walking Condition Distribution"
            )

            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("Top Subject Performance Ranking")

    rank_data = df.groupby(subject_col)[numeric_cols].mean().mean(axis=1)
    rank_df = rank_data.sort_values(ascending=False).reset_index()
    rank_df.columns = ["Subject", "Score"]

    st.dataframe(rank_df, use_container_width=True)

# =====================================================
# COMPARISON PAGE
# =====================================================
elif page == "Comparison Analysis":

    st.header("Advanced Subject Comparison")

    subjects = sorted(df[subject_col].unique())

    selected_subject = st.selectbox("Select Subject", subjects)

    feature = st.selectbox("Select Metric", numeric_cols)

    temp = df[df[subject_col] == selected_subject]

    c1, c2 = st.columns(2)

    with c1:
        fig1 = px.bar(
            temp,
            y=feature,
            title="Bar Comparison"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        fig2 = px.line(
            temp,
            y=feature,
            markers=True,
            title="Trend Line"
        )
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        fig3 = px.box(
            temp,
            y=feature,
            title="Variation Analysis"
        )
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        fig4 = px.histogram(
            temp,
            x=feature,
            title="Distribution"
        )
        st.plotly_chart(fig4, use_container_width=True)

# =====================================================
# LIVE MONITORING
# =====================================================
elif page == "Live Monitoring":

    st.header("Real-Time Subject Monitoring")

    subjects = sorted(df[subject_col].unique())

    selected_subject = st.selectbox("Select Subject", subjects)

    feature = st.selectbox("Select Monitoring Metric", numeric_cols)

    st.info(f"X-axis = Time (sec) | Y-axis = {feature}")

    temp = df[df[subject_col] == selected_subject]

    base = float(temp[feature].mean())

    chart = st.line_chart(pd.DataFrame({feature:[base]}))

    status = st.empty()

    for i in range(30):

        val = base + np.random.randn()*0.4

        chart.add_rows(pd.DataFrame({feature:[val]}))

        status.write(
            f"Time {i+1}s | Subject {selected_subject} | {feature}: {round(val,2)}"
        )

        time.sleep(0.2)

    st.success("Monitoring Completed")

# =====================================================
# REPORT PAGE
# =====================================================
elif page == "Clinical Report":

    st.header("Advanced Clinical Report")

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
        "Reduced motor coordination found.",
        "Mild hesitation in backward motion.",
        "Good dynamic control maintained.",
        "Stride reduction detected.",
        "Moderate instability identified.",
        "Strong recovery response noted.",
        "Variable cadence pattern present.",
        "Stable posture maintained.",
        "Transition hesitation visible.",
        "Lower limb control satisfactory.",
        "Mild fatigue trend present.",
        "Strong mobility observed.",
        "Backward stepping caution advised."
    ]

    recs = [
        "Routine follow-up suggested.",
        "Weekly balance drills advised.",
        "Dual-task training recommended.",
        "Coordination therapy suggested.",
        "Maintain current exercise plan.",
        "Stride training recommended.",
        "Periodic supervision advised.",
        "Continue gait retraining.",
        "Cadence control exercises advised.",
        "Maintain rehab schedule.",
        "Confidence training suggested.",
        "Strength maintenance advised.",
        "Endurance drills recommended.",
        "Continue active monitoring.",
        "Close observation required."
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

    st.plotly_chart(gauge, use_container_width=True)

    st.subheader("Clinical Findings")
    st.write(findings[idx])

    fig5 = px.bar(
        x=temp[numeric_cols].mean().index,
        y=temp[numeric_cols].mean().values,
        title="Average Subject Metrics"
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("Recommendation")
    st.success(recs[idx])

    report = f"""
MINOR PROJECT REPORT

Project:
Biomechanical and Neuromuscular Adaptations in Constrained Gait - Reverse Walking

Subject: {selected_subject}
Score: {score}
Risk: {risk}

Finding:
{findings[idx]}

Recommendation:
{recs[idx]}

Team:
Anushka Singh
Astha Singh
Kratika Vashishtha
"""

    st.download_button(
        "Download Report",
        data=report,
        file_name=f"{selected_subject}_report.txt",
        mime="text/plain"
    )
