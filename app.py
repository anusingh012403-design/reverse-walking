import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
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
.main {
    background-color:#f8fafc;
}
.block-container {
    padding-top:1rem;
}
div[data-testid="metric-container"] {
    background: linear-gradient(135deg,#ffffff,#eef2ff);
    border:1px solid #e5e7eb;
    border-radius:14px;
    padding:16px;
    box-shadow:0px 4px 10px rgba(0,0,0,0.08);
}
h1,h2,h3 {
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

# =====================================================
# COLUMN DETECTION
# =====================================================
subject_col = "subject" if "subject" in df.columns else df.columns[0]
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

# =====================================================
# HEADER
# =====================================================
st.title("Biomechanical and Neuromuscular Adaptations in Constrained Gait")
st.subheader('"Reverse Walking"')

st.caption("""
Minor Project Dashboard

Team Members:
Anushka Singh | Astha Singh | Kratika Vashishtha
""")

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

    st.header("Project Overview")

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

        st.subheader("Objective")

        st.write("""
This minor project studies gait adaptations during reverse walking.

### Focus Areas:
- Balance Control
- Cadence Changes
- Stride Length
- Joint Coordination
- Movement Stability
- Functional Performance
""")

        st.success("System Ready for Demonstration")

    with right:

        if "condition" in df.columns:

            fig = px.pie(
                df,
                names="condition",
                hole=0.55,
                title="Walking Conditions"
            )

            fig.update_layout(height=380)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

# =====================================================
# COMPARISON PAGE
# =====================================================
elif page == "Comparison Analysis":

    st.header("Subject Comparison")

    subjects = sorted(df[subject_col].unique())

    selected_subject = st.selectbox(
        "Select Subject",
        subjects
    )

    feature = st.selectbox(
        "Select Metric",
        numeric_cols
    )

    temp = df[df[subject_col] == selected_subject]

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Bar Chart")
        st.bar_chart(temp[feature])

    with c2:
        st.subheader("Line Chart")
        st.line_chart(temp[feature])

    c3, c4 = st.columns(2)

    with c3:
        fig2, ax2 = plt.subplots()
        sns.boxplot(y=temp[feature], ax=ax2)
        st.pyplot(fig2)

    with c4:
        fig3, ax3 = plt.subplots()
        sns.histplot(temp[feature], kde=True, ax=ax3)
        st.pyplot(fig3)

# =====================================================
# LIVE MONITORING
# =====================================================
elif page == "Live Monitoring":

    st.header("Live Monitoring")

    subjects = sorted(df[subject_col].unique())

    selected_subject = st.selectbox(
        "Select Subject",
        subjects
    )

    feature = st.selectbox(
        "Select Metric",
        numeric_cols
    )

    st.info(f"X-axis = Time (sec) | Y-axis = {feature}")

    temp = df[df[subject_col] == selected_subject]

    baseline = float(temp[feature].mean())

    chart = st.line_chart(
        pd.DataFrame({feature:[baseline]})
    )

    for i in range(20):

        val = baseline + np.random.randn()*0.4

        chart.add_rows(
            pd.DataFrame({feature:[val]})
        )

        time.sleep(0.2)

    st.success("Monitoring Completed")

# =====================================================
# CLINICAL REPORT
# =====================================================
elif page == "Clinical Report":

    st.header("Subject-wise Report")

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
        "Stable reverse gait observed.",
        "Minor balance variation detected.",
        "Reduced coordination response.",
        "Delayed movement initiation.",
        "Good control maintained.",
        "Short stride tendency found.",
        "Moderate instability present.",
        "Good recovery ability.",
        "Variable cadence pattern.",
        "Stable posture maintained.",
        "Movement hesitation seen.",
        "Lower limb response good.",
        "Mild fatigue pattern.",
        "Strong mobility observed.",
        "Careful stepping pattern."
    ]

    recs = [
        "Routine follow-up advised.",
        "Balance drills recommended.",
        "Dual-task practice suggested.",
        "Coordination exercises advised.",
        "Maintain current activity.",
        "Stride training recommended.",
        "Periodic supervision needed.",
        "Continue mobility drills.",
        "Cadence practice advised.",
        "Maintain training plan.",
        "Confidence training suggested.",
        "Strength work advised.",
        "Endurance training suggested.",
        "Continue active routine.",
        "Close monitoring advised."
    ]

    c1, c2 = st.columns(2)

    with c1:
        st.metric("Clinical Score", score)

    with c2:
        st.metric("Risk Level", risk)

    st.markdown("---")

    st.subheader("Findings")
    st.write(findings[idx])

    fig4 = px.bar(
        x=temp[numeric_cols].mean().index,
        y=temp[numeric_cols].mean().values,
        title="Average Metrics"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

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
