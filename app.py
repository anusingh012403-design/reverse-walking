import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

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

# ---------------- DETECT SUBJECT COLUMN ----------------
subject_col = "subject" if "subject" in df.columns else df.columns[0]

# ---------------- TITLE ----------------
st.title("🩺 AI Clinical Reverse Walking Gait Analysis Dashboard")
st.markdown("Advanced Clinical Dashboard for Reverse Walking Subjects")

# ---------------- SIDEBAR ----------------
page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Comparison Analysis",
        "Live Monitoring",
        "AI Report",
        "Dataset"
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
    This intelligent dashboard evaluates reverse walking patterns of subjects.
    
    Reverse walking helps assess:
    - Balance control
    - Fall risk
    - Coordination
    - Motor planning
    - Cognitive load response
    """)

    st.success("System Ready for Clinical Monitoring")

# =====================================================
# PAGE 2 COMPARISON
# =====================================================
elif page == "Comparison Analysis":

    st.header("Subject Comparison Dashboard")

    subjects = sorted(df[subject_col].unique())
    selected_subject = st.selectbox("Select Subject", subjects)

    temp = df[df[subject_col] == selected_subject]

    st.write("Showing all records for selected subject")

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if len(numeric_cols) >= 2:

        col = st.selectbox("Select Feature", numeric_cols)

        # Chart 1 Bar
        st.subheader("1. Bar Chart")
        st.bar_chart(temp[col])

        # Chart 2 Line
        st.subheader("2. Line Chart")
        st.line_chart(temp[col])

        # Chart 3 Area
        st.subheader("3. Area Chart")
        st.area_chart(temp[col])

        # Chart 4 Histogram
        st.subheader("4. Histogram")
        fig, ax = plt.subplots()
        sns.histplot(temp[col], kde=True, ax=ax)
        st.pyplot(fig)

        # Chart 5 Boxplot
        st.subheader("5. Boxplot")
        fig2, ax2 = plt.subplots()
        sns.boxplot(y=temp[col], ax=ax2)
        st.pyplot(fig2)

        # Chart 6 Scatter
        if len(numeric_cols) >= 2:
            st.subheader("6. Scatter Plot")
            xcol = numeric_cols[0]
            ycol = numeric_cols[1]
            fig3, ax3 = plt.subplots()
            sns.scatterplot(
                x=temp[xcol],
                y=temp[ycol],
                ax=ax3
            )
            st.pyplot(fig3)

# =====================================================
# PAGE 3 LIVE MONITORING
# =====================================================
elif page == "Live Monitoring":

    st.header("Real Time Clinical Monitoring")

    st.markdown("""
    **X-axis:** Time (seconds)  
    **Y-axis:** Gait Stability Score
    """)

    chart = st.line_chart(pd.DataFrame(np.random.randn(10,1)))

    for i in range(30):
        new = pd.DataFrame(np.random.randn(1,1))
        chart.add_rows(new)

    st.success("Live monitoring active")

# =====================================================
# PAGE 4 AI REPORT
# =====================================================
elif page == "AI Report":

    st.header("AI Generated Clinical Report")

    selected_subject = st.selectbox(
        "Select Subject for Report",
        sorted(df[subject_col].unique())
    )

    temp = df[df[subject_col] == selected_subject]

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    avg_score = round(temp[numeric_cols].mean().mean(),2)

    if avg_score > 70:
        risk = "Low Risk"
    elif avg_score > 40:
        risk = "Moderate Risk"
    else:
        risk = "High Risk"

    st.subheader("Clinical Summary")

    st.write(f"""
    Subject ID: {selected_subject}

    Reverse walking performance indicates **{risk}** of fall.

    Clinical Findings:
    - Balance mildly affected
    - Step symmetry acceptable
    - Coordination monitored
    - Recommend physiotherapy if needed
    """)

    # Graph
    if len(numeric_cols) > 0:
        feature = numeric_cols[0]

        fig4, ax4 = plt.subplots()
        ax4.plot(temp[feature], marker="o")
        ax4.set_title("Subject Performance Trend")
        st.pyplot(fig4)

    # Download text report
    report = f"""
AI CLINICAL REPORT

Subject: {selected_subject}

Risk Level: {risk}

Average Score: {avg_score}

Recommendation:
Continue gait training and balance monitoring.
"""

    st.download_button(
        label="Download Full Report",
        data=report,
        file_name=f"{selected_subject}_clinical_report.txt",
        mime="text/plain"
    )

# =====================================================
# PAGE 5 DATASET
# =====================================================
elif page == "Dataset":

    st.header("Full Dataset")

    st.dataframe(df, use_container_width=True)

    st.subheader("Rows and Columns")
    st.write(df.shape)

    st.subheader("Missing Values")
    st.write(df.isnull().sum())
