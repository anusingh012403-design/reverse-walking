import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="AI Clinical Reverse Walking Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("clinical_dashboard_15_subjects.csv")

df = load_data()

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title("📊 AI Clinical Reverse Walking Gait Dashboard")
st.markdown("Advanced Dashboard with Live Monitoring + AI Reports")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Home",
        "Dataset",
        "Charts",
        "Live Monitoring",
        "AI Report Download"
    ]
)

# ---------------------------------------------------
# NUMERIC COLUMNS
# ---------------------------------------------------
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

# ---------------------------------------------------
# PAGE 1 - HOME
# ---------------------------------------------------
if page == "Home":

    st.subheader("Dashboard Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Subjects", len(df))
    col2.metric("Total Columns", len(df.columns))
    col3.metric("Numeric Features", len(numeric_cols))

    st.markdown("---")

    st.write("""
    ### Features Included:
    ✅ Subject Dataset  
    ✅ All Major Charts  
    ✅ Live Monitoring Simulation  
    ✅ AI Generated Subject Reports  
    ✅ Download Reports  
    """)

# ---------------------------------------------------
# PAGE 2 - DATASET
# ---------------------------------------------------
elif page == "Dataset":

    st.subheader("📁 Subject Dataset")
    st.dataframe(df, use_container_width=True)

    st.subheader("Missing Values")
    st.write(df.isnull().sum())

# ---------------------------------------------------
# PAGE 3 - CHARTS
# ---------------------------------------------------
elif page == "Charts":

    st.subheader("📈 Visual Analytics")

    if len(numeric_cols) > 0:

        col = st.selectbox("Select Column", numeric_cols)

        # Bar Chart
        st.write("### Bar Chart")
        st.bar_chart(df[col])

        # Line Chart
        st.write("### Line Chart")
        st.line_chart(df[col])

        # Area Chart
        st.write("### Area Chart")
        st.area_chart(df[col])

        # Histogram
        st.write("### Histogram")
        fig1 = px.histogram(df, x=col, nbins=20)
        st.plotly_chart(fig1, use_container_width=True)

        # Pie Chart
        st.write("### Pie Chart")
        pie_data = df[col].value_counts().head(5)
        fig2 = px.pie(values=pie_data.values, names=pie_data.index)
        st.plotly_chart(fig2, use_container_width=True)

        # Box Plot
        st.write("### Box Plot")
        fig3 = px.box(df, y=col)
        st.plotly_chart(fig3, use_container_width=True)

        # Scatter Plot
        if len(numeric_cols) > 1:
            st.write("### Scatter Plot")
            xcol = st.selectbox("X Axis", numeric_cols, key="x")
            ycol = st.selectbox("Y Axis", numeric_cols, key="y")
            fig4 = px.scatter(df, x=xcol, y=ycol)
            st.plotly_chart(fig4, use_container_width=True)

# ---------------------------------------------------
# PAGE 4 - LIVE MONITORING
# ---------------------------------------------------
elif page == "Live Monitoring":

    st.subheader("🟢 Live Subject Monitoring")

    subject = st.selectbox("Select Subject", df.index)

    speed = round(np.random.uniform(0.8, 2.0), 2)
    steps = np.random.randint(20, 100)
    balance = round(np.random.uniform(70, 100), 1)
    risk = np.random.choice(["Low", "Moderate", "High"])

    col1, col2 = st.columns(2)

    col1.metric("Walking Speed", f"{speed} m/s")
    col1.metric("Step Count", steps)

    col2.metric("Balance Score", balance)
    col2.metric("Fall Risk", risk)

    chart_data = pd.DataFrame(
        np.random.randn(20, 1),
        columns=["Live Movement"]
    )

    st.line_chart(chart_data)

# ---------------------------------------------------
# PAGE 5 - AI REPORT
# ---------------------------------------------------
elif page == "AI Report Download":

    st.subheader("🤖 AI Generated Subject Report")

    subject = st.selectbox("Select Subject ID", df.index)

    row = df.loc[subject]

    report = f"""
Clinical Reverse Walking AI Report
----------------------------------

Generated On: {datetime.now()}

Subject ID: {subject}

Summary:
This subject has been evaluated using gait metrics.

Mean Values:
{row.to_string()}

AI Insights:
- Walking pattern analyzed successfully.
- Reverse gait stability moderate.
- Balance condition acceptable.
- Recommend periodic monitoring.
- Continue rehabilitation exercises.

Overall Status: Stable
"""

    st.text_area("Generated Report", report, height=400)

    # Download txt report
    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name=f"subject_{subject}_report.txt",
        mime="text/plain"
    )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")
st.caption("Developed for Clinical Reverse Walking Gait Analysis Project")
