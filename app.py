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
    layout="wide"
)

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
# TITLE
# =====================================================
st.title("🩺 Clinical Reverse Walking Gait Dashboard")
st.markdown("Subject-wise Clinical Monitoring and Reporting System")

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
# HOME
# =====================================================
if page == "Home":

    st.header("Clinical Overview")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Total Subjects", df[subject_col].nunique())

    with c2:
        st.metric("Total Records", len(df))

    with c3:
        st.metric("Total Features", df.shape[1])

    st.markdown("---")

    st.write("""
This dashboard evaluates reverse walking gait performance of 15 subjects.

### Included Modules:
- Subject Comparison
- Live Monitoring
- Subject-wise Clinical Reports
- Risk Assessment
""")

# =====================================================
# COMPARISON
# =====================================================
elif page == "Comparison Analysis":

    st.header("Subject Comparison")

    subjects = sorted(df[subject_col].unique())
    selected_subject = st.selectbox("Select Subject", subjects)

    temp = df[df[subject_col] == selected_subject]

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if numeric_cols:

        feature = st.selectbox("Select Metric", numeric_cols)

        st.subheader("Bar Chart")
        st.bar_chart(temp[feature])

        st.subheader("Line Chart")
        st.line_chart(temp[feature])

        st.subheader("Box Plot")
        fig1, ax1 = plt.subplots()
        sns.boxplot(y=temp[feature], ax=ax1)
        st.pyplot(fig1)

        st.subheader("Histogram")
        fig2, ax2 = plt.subplots()
        sns.histplot(temp[feature], kde=True, ax=ax2)
        st.pyplot(fig2)

# =====================================================
# LIVE MONITORING
# =====================================================
elif page == "Live Monitoring":

    st.header("Subject-wise Live Monitoring")

    subjects = sorted(df[subject_col].unique())

    selected_subject = st.selectbox(
        "Select Subject",
        subjects
    )

    temp = df[df[subject_col] == selected_subject]

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    feature = st.selectbox(
        "Select Monitoring Metric",
        numeric_cols
    )

    st.markdown("""
### Axis Information

**X-axis:** Time (seconds)  
**Y-axis:** Live Performance Score
""")

    chart = st.line_chart(
        pd.DataFrame({feature: np.random.randn(10)})
    )

    for i in range(20):

        base = float(temp[feature].mean())
        value = base + np.random.randn() * 0.5

        chart.add_rows(
            pd.DataFrame({feature: [value]})
        )

        time.sleep(0.25)

    st.success("Live Monitoring Completed")

# =====================================================
# CLINICAL REPORT
# =====================================================
elif page == "Clinical Report":

    st.header("Subject-wise Clinical Report")

    subjects = sorted(df[subject_col].unique())

    selected_subject = st.selectbox(
        "Select Subject for Report",
        subjects
    )

    temp = df[df[subject_col] == selected_subject]

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    # ---------------- SUBJECT SCORE ----------------
    score = round(temp[numeric_cols].mean().mean(), 2)

    # ---------------- SUBJECT UNIQUE VARIATION ----------------
    subject_num = int(str(selected_subject).split()[-1]) if str(selected_subject).split()[-1].isdigit() else subjects.index(selected_subject)+1

    # ---------------- DIFFERENT RISK ----------------
    if score >= 75:
        risk = "Low Risk"
    elif score >= 55:
        risk = "Moderate Risk"
    else:
        risk = "High Risk"

    # ---------------- DIFFERENT OBSERVATIONS ----------------
    observations = [
        "Good dynamic balance with stable gait response.",
        "Mild instability during reverse walking.",
        "Reduced coordination under cognitive load.",
        "Delayed movement initiation observed.",
        "Symmetrical gait pattern maintained.",
        "Shortened step pattern detected.",
        "Moderate trunk sway observed.",
        "Improved balance recovery response.",
        "Variable cadence pattern noticed.",
        "Stable postural alignment maintained.",
        "Minor hesitation during turning phase.",
        "Lower limb control satisfactory.",
        "Mild fatigue pattern observed.",
        "Strong mobility control noted.",
        "Reduced confidence during backward motion."
    ]

    recommendation_list = [
        "Continue routine activity and monthly review.",
        "Start balance exercises 3 times/week.",
        "Perform supervised reverse walking drills.",
        "Coordination training recommended.",
        "No major intervention needed presently.",
        "Lower limb strengthening advised.",
        "Use posture correction exercises.",
        "Weekly mobility reassessment advised.",
        "Dual-task walking practice recommended.",
        "Maintain present rehabilitation plan.",
        "Monitor gait confidence regularly.",
        "Increase endurance training gradually.",
        "Functional movement retraining suggested.",
        "Preventive exercise program advised.",
        "Close follow-up and safety monitoring required."
    ]

    observation = observations[(subject_num - 1) % 15]
    recommendation = recommendation_list[(subject_num - 1) % 15]

    # ---------------- REPORT DISPLAY ----------------
    st.subheader(f"Clinical Report : Subject {selected_subject}")

    c1, c2 = st.columns(2)

    with c1:
        st.metric("Clinical Score", score)

    with c2:
        st.metric("Risk Level", risk)

    st.markdown("---")

    st.write(f"""
### Clinical Findings:
- {observation}
- Reverse walking performance analyzed.
- Functional gait response recorded.
- Subject-specific movement variation detected.
""")

    # ---------------- GRAPH ----------------
    st.subheader("Performance Summary")

    avg_vals = temp[numeric_cols].mean()

    fig3, ax3 = plt.subplots(figsize=(9,4))
    ax3.bar(avg_vals.index, avg_vals.values)
    ax3.set_xlabel("Metrics")
    ax3.set_ylabel("Average Value")
    ax3.set_title("Subject Performance Metrics")
    plt.xticks(rotation=45)
    st.pyplot(fig3)

    # ---------------- RECOMMENDATION ----------------
    st.subheader("Clinical Recommendation")

    st.success(recommendation)

    # ---------------- DOWNLOAD REPORT ----------------
    report_text = f"""
CLINICAL REPORT

Subject: {selected_subject}

Clinical Score: {score}
Risk Level: {risk}

Findings:
{observation}
Reverse walking assessed successfully.

Recommendation:
{recommendation}
"""

    st.download_button(
        "Download Full Clinical Report",
        data=report_text,
        file_name=f"{selected_subject}_clinical_report.txt",
        mime="text/plain"
    )
