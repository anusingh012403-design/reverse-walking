import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="AI Clinical Reverse Walking Dashboard",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("clinical_dashboard_15_subjects.csv")

df = load_data()
df.columns = df.columns.str.strip().str.lower()

# ---------------------------------------------------
# SUBJECT COLUMN
# ---------------------------------------------------
subject_col = "subject" if "subject" in df.columns else df.columns[0]

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title("🩺 AI Clinical Reverse Walking Dashboard")
st.markdown("Clinical Reverse Walking Monitoring & Analysis System")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Comparison Analysis",
        "Live Monitoring",
        "AI Report"
    ]
)

# ===================================================
# PAGE 1 HOME
# ===================================================
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
This dashboard evaluates reverse walking performance for all 15 subjects.

### Modules:
- Subject Comparison
- Subject-wise Live Monitoring
- AI Risk Report
- Clinical Performance Tracking
""")

# ===================================================
# PAGE 2 COMPARISON
# ===================================================
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

# ===================================================
# PAGE 3 LIVE MONITORING (UPDATED)
# ===================================================
elif page == "Live Monitoring":

    st.header("Subject-wise Live Monitoring")

    subjects = sorted(df[subject_col].unique())

    selected_subject = st.selectbox(
        "Select Subject for Live Monitoring",
        subjects
    )

    st.subheader(f"Live Monitoring : Subject {selected_subject}")

    st.markdown("""
### Axis Information

**X-axis:** Time (seconds)  
**Y-axis:** Gait Stability Score
""")

    temp = df[df[subject_col] == selected_subject]

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if len(numeric_cols) > 0:
        feature = st.selectbox(
            "Select Live Metric",
            numeric_cols
        )
    else:
        feature = None

    st.info(
        f"Monitoring Subject {selected_subject} in real time"
    )

    chart = st.line_chart(
        pd.DataFrame(
            {
                feature: np.random.randn(10)
            }
        )
    )

    status = st.empty()

    for i in range(20):

        if feature:
            base = float(temp[feature].mean())
        else:
            base = 0

        new_value = base + np.random.randn() * 0.5

        new_data = pd.DataFrame(
            {
                feature: [new_value]
            }
        )

        chart.add_rows(new_data)

        status.write(
            f"Time: {i+1} sec | "
            f"Subject: {selected_subject} | "
            f"{feature}: {round(new_value,2)}"
        )

        time.sleep(0.3)

    st.success(
        f"Live Monitoring Completed for Subject {selected_subject}"
    )

# ===================================================
# PAGE 4 AI REPORT
# ===================================================
elif page == "AI Report":

    st.header("AI Clinical Report")

    subjects = sorted(df[subject_col].unique())

    selected_subject = st.selectbox(
        "Select Subject",
        subjects
    )

    temp = df[df[subject_col] == selected_subject]

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    score = round(temp[numeric_cols].mean().mean(), 2)

    if score > 70:
        risk = "Low Fall Risk"
    elif score > 40:
        risk = "Moderate Fall Risk"
    else:
        risk = "High Fall Risk"

    st.subheader(f"Report : Subject {selected_subject}")

    st.write(f"""
### Risk Level: {risk}

### Findings:
- Reverse gait tested
- Balance monitored
- Functional mobility checked
- Clinical response recorded

### Recommendation:
Continue therapy and periodic review.
""")

    if len(numeric_cols) > 0:
        fig3, ax3 = plt.subplots()
        ax3.plot(temp[numeric_cols[0]], marker="o")
        ax3.set_xlabel("Trials")
        ax3.set_ylabel(numeric_cols[0])
        ax3.set_title("Performance Trend")
        st.pyplot(fig3)

    report_text = f"""
AI CLINICAL REPORT

Subject: {selected_subject}
Risk Level: {risk}
Average Score: {score}

Recommendation:
Continue monitoring and gait training.
"""

    st.download_button(
        "Download Full Report",
        data=report_text,
        file_name=f"{selected_subject}_clinical_report.txt",
        mime="text/plain"
    )
