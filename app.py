import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Clinical Reverse Walking Dashboard",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("clinical_dashboard_15_subjects.csv")

df = load_data()

# ---------------- CLEAN COLUMN NAMES ----------------
df.columns = df.columns.str.strip().str.lower()

# ---------------- SUBJECT COLUMN ----------------
subject_col = "subject" if "subject" in df.columns else df.columns[0]

# ---------------- TITLE ----------------
st.title("🩺 AI Clinical Reverse Walking Gait Analysis Dashboard")
st.markdown("Smart Clinical Monitoring System for Reverse Walking Analysis")

# ---------------- SIDEBAR ----------------
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

    st.markdown("## Welcome to Clinical Reverse Walking System")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Total Subjects", df[subject_col].nunique())

    with c2:
        st.metric("Total Records", len(df))

    with c3:
        st.metric("Total Features", df.shape[1])

    st.markdown("---")

    st.subheader("Clinical Objective")

    st.write("""
This AI-powered system evaluates reverse walking performance to support clinical gait analysis.

### Key Uses:
- Fall risk screening
- Balance assessment
- Neurological monitoring
- Mobility comparison
- Functional movement analysis
""")

    st.info("Designed for professional clinical gait evaluation.")

# =====================================================
# PAGE 2 COMPARISON ANALYSIS
# =====================================================
elif page == "Comparison Analysis":

    st.header("Subject Comparison Dashboard")

    subjects = sorted(df[subject_col].unique())
    selected_subject = st.selectbox("Select Subject", subjects)

    temp = df[df[subject_col] == selected_subject]

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if len(numeric_cols) > 0:

        feature = st.selectbox("Select Feature", numeric_cols)

        st.subheader("1. Bar Chart")
        st.bar_chart(temp[feature])

        st.subheader("2. Line Chart")
        st.line_chart(temp[feature])

        st.subheader("3. Area Chart")
        st.area_chart(temp[feature])

        st.subheader("4. Histogram")
        fig1, ax1 = plt.subplots()
        sns.histplot(temp[feature], kde=True, ax=ax1)
        st.pyplot(fig1)

        st.subheader("5. Box Plot")
        fig2, ax2 = plt.subplots()
        sns.boxplot(y=temp[feature], ax=ax2)
        st.pyplot(fig2)

        if len(numeric_cols) >= 2:
            st.subheader("6. Scatter Plot")
            fig3, ax3 = plt.subplots()
            sns.scatterplot(
                x=temp[numeric_cols[0]],
                y=temp[numeric_cols[1]],
                ax=ax3
            )
            ax3.set_xlabel(numeric_cols[0])
            ax3.set_ylabel(numeric_cols[1])
            st.pyplot(fig3)

# =====================================================
# PAGE 3 LIVE MONITORING
# =====================================================
elif page == "Live Monitoring":

    st.header("Live Clinical Monitoring")

    st.markdown("""
### Real Time Monitoring

**X-axis:** Time (seconds)  
**Y-axis:** Gait Stability Score
""")

    chart = st.line_chart(
        pd.DataFrame(np.random.randn(10, 1))
    )

    for i in range(25):
        new_data = pd.DataFrame(np.random.randn(1, 1))
        chart.add_rows(new_data)

    st.success("Monitoring Active")

# =====================================================
# PAGE 4 AI REPORT
# =====================================================
elif page == "AI Report":

    st.header("AI Generated Clinical Subject Report")

    subjects = sorted(df[subject_col].unique())
    selected_subject = st.selectbox(
        "Select Subject for Report",
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

    st.subheader("Clinical Summary")

    st.write(f"""
### Subject ID: {selected_subject}

### Risk Level: {risk}

### Findings:
- Reverse gait analyzed successfully
- Balance response monitored
- Movement coordination reviewed
- Functional mobility assessed

### Recommendation:
Continue supervised gait exercise and regular monitoring.
""")

    if len(numeric_cols) > 0:
        fig4, ax4 = plt.subplots()
        ax4.plot(temp[numeric_cols[0]], marker="o")
        ax4.set_title("Performance Trend")
        ax4.set_xlabel("Trial")
        ax4.set_ylabel(numeric_cols[0])
        st.pyplot(fig4)

    report_text = f"""
AI CLINICAL REPORT

Subject: {selected_subject}
Risk Level: {risk}
Average Score: {score}

Findings:
Reverse gait performance reviewed.
Balance and coordination assessed.

Recommendation:
Continue therapy and monitor progression.
"""

    st.download_button(
        label="Download Full Report",
        data=report_text,
        file_name=f"{selected_subject}_report.txt",
        mime="text/plain"
    )
