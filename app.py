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
    page_title="AI Clinical Reverse Walking Dashboard",
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
st.title("🩺 AI Clinical Reverse Walking Dashboard")
st.markdown("Smart Clinical Monitoring & Subject-wise AI Reporting")

# =====================================================
# SIDEBAR
# =====================================================
page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Comparison Analysis",
        "Live Monitoring",
        "AI Report"
    ]
)

# =====================================================
# PAGE 1 HOME
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
This dashboard is developed for reverse walking gait analysis.

### Includes:
- Subject Comparison
- Live Monitoring
- AI Generated Subject Reports
- Clinical Recommendations
""")

# =====================================================
# PAGE 2 COMPARISON
# =====================================================
elif page == "Comparison Analysis":

    st.header("Subject Comparison")

    subjects = sorted(df[subject_col].unique())
    selected_subject = st.selectbox("Select Subject", subjects)

    temp = df[df[subject_col] == selected_subject]

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if len(numeric_cols) > 0:

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
# PAGE 3 LIVE MONITORING
# =====================================================
elif page == "Live Monitoring":

    st.header("Subject-wise Live Monitoring")

    subjects = sorted(df[subject_col].unique())

    selected_subject = st.selectbox(
        "Select Subject",
        subjects
    )

    st.markdown("""
### Axis Information

**X-axis:** Time (seconds)  
**Y-axis:** Gait Stability Score
""")

    temp = df[df[subject_col] == selected_subject]

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    feature = st.selectbox(
        "Select Monitoring Metric",
        numeric_cols
    )

    chart = st.line_chart(
        pd.DataFrame({feature: np.random.randn(10)})
    )

    for i in range(20):

        base = float(temp[feature].mean())
        value = base + np.random.randn() * 0.4

        chart.add_rows(
            pd.DataFrame({feature: [value]})
        )

        time.sleep(0.25)

    st.success("Monitoring Completed")

# =====================================================
# PAGE 4 AI REPORT (UPDATED)
# =====================================================
elif page == "AI Report":

    st.header("AI Generated Subject Report")

    subjects = sorted(df[subject_col].unique())

    selected_subject = st.selectbox(
        "Select Subject for Report",
        subjects
    )

    temp = df[df[subject_col] == selected_subject]

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    score = round(temp[numeric_cols].mean().mean(), 2)

    # ---------------- RISK ----------------
    if score >= 75:
        risk = "Low Fall Risk"
        recommendation = """
- Continue regular physical activity
- Maintain gait training exercises
- Monthly monitoring sufficient
- No immediate intervention required
"""
    elif score >= 50:
        risk = "Moderate Fall Risk"
        recommendation = """
- Begin balance improvement exercises
- Weekly gait review suggested
- Strength training recommended
- Clinical reassessment after 30 days
"""
    else:
        risk = "High Fall Risk"
        recommendation = """
- Immediate physiotherapy referral
- Supervised walking advised
- Balance support devices may help
- Detailed neurological evaluation suggested
"""

    # ---------------- FINDINGS ----------------
    st.subheader(f"Subject Report : {selected_subject}")

    st.write(f"""
### Clinical Score: {score}

### Risk Level: {risk}

### Findings:
- Reverse walking pattern assessed
- Dynamic balance response evaluated
- Functional mobility reviewed
- Subject specific gait performance measured
""")

    # ---------------- NEW GRAPH (RADAR STYLE SUBSTITUTE) ----------------
    st.subheader("Performance Metrics Comparison")

    if len(numeric_cols) >= 4:

        graph_cols = numeric_cols[:4]
        values = temp[graph_cols].mean().values

        fig3, ax3 = plt.subplots(figsize=(8,4))
        ax3.bar(graph_cols, values)
        ax3.set_ylabel("Average Score")
        ax3.set_xlabel("Clinical Metrics")
        ax3.set_title("Subject Metric Summary")
        st.pyplot(fig3)

    elif len(numeric_cols) > 0:

        fig4, ax4 = plt.subplots(figsize=(8,4))
        ax4.bar(numeric_cols, temp[numeric_cols].mean().values)
        ax4.set_title("Metric Summary")
        st.pyplot(fig4)

    # ---------------- RECOMMENDATION ----------------
    st.subheader("AI Recommendation")

    st.write(recommendation)

    # ---------------- DOWNLOAD REPORT ----------------
    report_text = f"""
AI CLINICAL REPORT

Subject: {selected_subject}

Clinical Score: {score}
Risk Level: {risk}

Findings:
Reverse gait assessed.
Balance reviewed.
Mobility analyzed.

Recommendations:
{recommendation}
"""

    st.download_button(
        label="Download Full Report",
        data=report_text,
        file_name=f"{selected_subject}_ai_report.txt",
        mime="text/plain"
    )
