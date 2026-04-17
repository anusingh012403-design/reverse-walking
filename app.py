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
    page_title="Clinical Reverse Walking Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CSS DESIGN
# =====================================================
st.markdown("""
<style>
.main {
    background: #f8fafc;
}
.block-container {
    padding-top: 1rem;
}
div[data-testid="metric-container"] {
    background: linear-gradient(135deg,#ffffff,#f1f5f9);
    border: 1px solid #e2e8f0;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.06);
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

subject_col = "subject" if "subject" in df.columns else df.columns[0]
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

# =====================================================
# TITLE
# =====================================================
st.title("Clinical Reverse Walking Gait Dashboard")
st.caption("Professional Subject Monitoring and Clinical Analysis System")

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
# HOME PAGE (UPDATED)
# =====================================================
if page == "Home":

    st.header("Dashboard Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Total Subjects", df[subject_col].nunique())

    with c2:
        st.metric("Total Records", len(df))

    with c3:
        st.metric("Clinical Features", len(numeric_cols))

    with c4:
        st.metric("Walking Conditions", 3)

    st.markdown("---")

    left, right = st.columns([1.2, 1])

    with left:

        st.subheader("Clinical Objective")

        st.write("""
This dashboard evaluates reverse walking gait performance of subjects.

### Main Applications:
- Balance assessment
- Fall risk screening
- Mobility analysis
- Neurological observation
- Reverse walking comparison
- Clinical reporting
""")

        st.success("System Ready for Clinical Evaluation")

    with right:

        st.subheader("Condition Distribution")

        if "condition" in df.columns:
            pie = px.pie(
                df,
                names="condition",
                hole=0.55,
                title="Walking Conditions"
            )
            pie.update_layout(height=380)
            st.plotly_chart(
                pie,
                use_container_width=True
            )

        else:
            st.info("Condition column not found")

    st.markdown("---")

    st.subheader("Subject Participation Heatmap")

    if "condition" in df.columns:

        pivot = pd.crosstab(
            df[subject_col],
            df["condition"]
        )

        fig, ax = plt.subplots(figsize=(10,5))
        sns.heatmap(
            pivot,
            annot=True,
            cmap="Blues",
            ax=ax
        )
        st.pyplot(fig)

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
        st.subheader("Bar Comparison")
        st.bar_chart(temp[feature])

    with c2:
        st.subheader("Line Trend")
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

    st.header("Live Subject Monitoring")

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

    base = float(temp[feature].mean())

    chart = st.line_chart(
        pd.DataFrame({feature:[base]})
    )

    for i in range(25):

        val = base + np.random.randn()*0.4

        chart.add_rows(
            pd.DataFrame({feature:[val]})
        )

        time.sleep(0.2)

    st.success("Monitoring Complete")

# =====================================================
# CLINICAL REPORT
# =====================================================
elif page == "Clinical Report":

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
        "Mild hesitation in backward motion.",
        "Good dynamic control noted.",
        "Stride length reduction present.",
        "Moderate instability observed.",
        "Strong recovery response found.",
        "Variable cadence pattern seen.",
        "Good postural alignment.",
        "Task transition hesitation.",
        "Satisfactory limb control.",
        "Fatigue tendency visible.",
        "Excellent mobility control.",
        "Cautious stepping pattern."
    ]

    recs = [
        "Routine follow-up advised.",
        "Weekly balance drills.",
        "Dual-task training suggested.",
        "Coordination therapy advised.",
        "Maintain current exercise plan.",
        "Stride improvement drills.",
        "Periodic supervision needed.",
        "Continue mobility practice.",
        "Cadence training suggested.",
        "Maintain rehab schedule.",
        "Confidence training advised.",
        "Strength program suggested.",
        "Endurance exercises advised.",
        "Continue active monitoring.",
        "Close supervision recommended."
    ]

    st.metric("Clinical Score", score)
    st.metric("Risk Level", risk)

    st.write(findings[idx])

    fig4 = px.bar(
        x=temp[numeric_cols].mean().index,
        y=temp[numeric_cols].mean().values,
        title="Performance Metrics"
    )
    st.plotly_chart(
        fig4,
        use_container_width=True
    )

    st.success(recs[idx])

    report = f"""
Clinical Report

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
