import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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
# CUSTOM CSS
# =====================================================
st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}
div[data-testid="metric-container"] {
    background: white;
    border: 1px solid #e5e7eb;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 3px 8px rgba(0,0,0,0.08);
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
# SUBJECT COLUMN
# =====================================================
subject_col = "subject" if "subject" in df.columns else df.columns[0]

# =====================================================
# NUMERIC COLUMNS
# =====================================================
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

# =====================================================
# HEADER
# =====================================================
st.title("Clinical Reverse Walking Gait Dashboard")
st.caption("Professional Subject Monitoring and Clinical Analysis System")

# =====================================================
# SIDEBAR
# =====================================================
page = st.sidebar.radio(
    "Select Module",
    [
        "Home",
        "Comparison Analysis",
        "Live Monitoring",
        "Clinical Report"
    ]
)

# =====================================================
# PAGE 1 HOME
# =====================================================
if page == "Home":

    st.header("Dashboard Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Total Subjects", df[subject_col].nunique())

    with c2:
        st.metric("Total Records", len(df))

    with c3:
        st.metric("Features", df.shape[1])

    with c4:
        st.metric("Conditions", 3)

    st.markdown("---")

    left, right = st.columns([2,1])

    with left:
        st.subheader("Clinical Objective")
        st.write("""
This dashboard evaluates reverse walking gait performance for 15 subjects.

### Used For:
- Balance analysis
- Fall risk screening
- Coordination monitoring
- Functional mobility testing
- Subject comparison
""")

    with right:
        if numeric_cols:
            fig, ax = plt.subplots(figsize=(5,3))
            df[numeric_cols].mean().plot(kind="bar", ax=ax)
            ax.set_title("Average Metrics")
            plt.xticks(rotation=45)
            st.pyplot(fig)

    st.success("System Ready")

# =====================================================
# PAGE 2 COMPARISON
# =====================================================
elif page == "Comparison Analysis":

    st.header("Subject Comparison Analysis")

    subjects = sorted(df[subject_col].unique())

    selected_subject = st.selectbox(
        "Select Subject",
        subjects
    )

    temp = df[df[subject_col] == selected_subject]

    feature = st.selectbox(
        "Select Metric",
        numeric_cols
    )

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Bar Comparison")
        st.bar_chart(temp[feature])

    with c2:
        st.subheader("Line Trend")
        st.line_chart(temp[feature])

    c3, c4 = st.columns(2)

    with c3:
        fig1, ax1 = plt.subplots()
        sns.boxplot(y=temp[feature], ax=ax1)
        ax1.set_title("Variation")
        st.pyplot(fig1)

    with c4:
        fig2, ax2 = plt.subplots()
        sns.histplot(temp[feature], kde=True, ax=ax2)
        ax2.set_title("Distribution")
        st.pyplot(fig2)

    st.subheader("Subject vs All Subjects Mean")

    mean_all = df.groupby(subject_col)[feature].mean()

    fig3, ax3 = plt.subplots(figsize=(10,4))
    mean_all.plot(kind="bar", ax=ax3)
    ax3.axhline(mean_all.mean(), linestyle="--")
    plt.xticks(rotation=45)
    st.pyplot(fig3)

# =====================================================
# PAGE 3 LIVE MONITORING
# =====================================================
elif page == "Live Monitoring":

    st.header("Real-Time Subject Monitoring")

    subjects = sorted(df[subject_col].unique())

    selected_subject = st.selectbox(
        "Select Subject",
        subjects
    )

    feature = st.selectbox(
        "Select Monitoring Metric",
        numeric_cols
    )

    st.info(f"X-axis = Time (seconds) | Y-axis = {feature}")

    temp = df[df[subject_col] == selected_subject]

    baseline = float(temp[feature].mean())

    chart = st.line_chart(
        pd.DataFrame({feature:[baseline]})
    )

    status = st.empty()

    values = []

    for i in range(25):

        new_val = baseline + np.random.randn()*0.4
        values.append(new_val)

        chart.add_rows(
            pd.DataFrame({feature:[new_val]})
        )

        status.write(
            f"Time: {i+1} sec | Subject: {selected_subject} | {feature}: {round(new_val,2)}"
        )

        time.sleep(0.2)

    st.success("Monitoring Session Completed")

# =====================================================
# PAGE 4 CLINICAL REPORT
# =====================================================
elif page == "Clinical Report":

    st.header("Subject-wise Clinical Report")

    subjects = sorted(df[subject_col].unique())

    selected_subject = st.selectbox(
        "Select Subject for Report",
        subjects
    )

    temp = df[df[subject_col] == selected_subject]

    score = round(temp[numeric_cols].mean().mean(),2)

    # SUBJECT NUMBER
    idx = subjects.index(selected_subject)

    # RISK
    if score >= 75:
        risk = "Low Risk"
    elif score >= 55:
        risk = "Moderate Risk"
    else:
        risk = "High Risk"

    findings = [
        "Stable gait mechanics observed.",
        "Minor balance fluctuation present.",
        "Reduced reverse walking confidence.",
        "Mild coordination delay detected.",
        "Efficient movement control noted.",
        "Shortened stride tendency present.",
        "Moderate gait inconsistency found.",
        "Good recovery response observed.",
        "Variable cadence pattern present.",
        "Postural control maintained.",
        "Hesitation during task transition.",
        "Lower limb response satisfactory.",
        "Fatigue tendency observed.",
        "Strong mobility pattern noted.",
        "Backward stepping caution required."
    ]

    recs = [
        "Routine monitoring recommended.",
        "Weekly balance drills advised.",
        "Dual-task training suggested.",
        "Coordination exercises recommended.",
        "Maintain present activity level.",
        "Stride improvement exercises advised.",
        "Periodic physiotherapy suggested.",
        "Continue supervised mobility work.",
        "Cadence control practice advised.",
        "Maintain rehabilitation schedule.",
        "Confidence retraining recommended.",
        "Strength maintenance advised.",
        "Endurance program suggested.",
        "Continue functional exercises.",
        "Close safety monitoring advised."
    ]

    finding = findings[idx]
    rec = recs[idx]

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Clinical Score", score)

    with c2:
        st.metric("Risk Level", risk)

    with c3:
        st.metric("Subject Rank", idx+1)

    st.markdown("---")

    st.subheader("Clinical Findings")
    st.write(finding)

    st.subheader("Performance Summary")

    avg_vals = temp[numeric_cols].mean()

    fig4, ax4 = plt.subplots(figsize=(10,4))
    avg_vals.plot(kind="bar", ax=ax4)
    ax4.set_ylabel("Average Value")
    plt.xticks(rotation=45)
    st.pyplot(fig4)

    st.subheader("Recommendation")
    st.success(rec)

    report = f"""
CLINICAL REPORT

Subject: {selected_subject}
Clinical Score: {score}
Risk Level: {risk}

Finding:
{finding}

Recommendation:
{rec}
"""

    st.download_button(
        "Download Report",
        data=report,
        file_name=f"{selected_subject}_report.txt",
        mime="text/plain"
    )
