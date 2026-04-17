import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Constrained Gait Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS
# =====================================================
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg,#081b6b,#0b4fd9,#1da1f2);
    color: white;
}

/* Main container */
.block-container {
    padding-top: 1rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.15);
}

/* Text */
h1,h2,h3,h4,h5,p,label,span {
    color: white !important;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.12) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 10px;
}

/* Dropdown text */
div[data-baseweb="select"] * {
    color: white !important;
}

/* Metric cards */
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.12);
    border-radius: 14px;
    padding: 18px;
    border: 1px solid rgba(255,255,255,0.18);
}

/* Buttons */
.stButton>button {
    background:#ffffff22;
    color:white;
    border-radius:10px;
    border:1px solid #ffffff33;
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
st.title("Constrained Gait")
st.subheader('"Reverse Walking"')
st.caption("Minor Project Dashboard")

# =====================================================
# SIDEBAR
# =====================================================
page = st.sidebar.radio(
    "Select Module",
    [
        "Home",
        "Advanced Subject Comparison",
        "Live Monitoring",
        "Clinical Report"
    ]
)

# =====================================================
# HOME
# =====================================================
if page == "Home":

    st.header("Dashboard Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Subjects", df[subject_col].nunique())

    with c2:
        st.metric("Records", len(df))

    with c3:
        st.metric("Features", len(numeric_cols))

    with c4:
        st.metric("Conditions", 3)

    st.markdown("---")

    st.write("""
### Clinical Uses
- Reverse walking assessment  
- Balance monitoring  
- Fall risk detection  
- Subject comparison  
- Clinical reporting  
""")

# =====================================================
# ADVANCED SUBJECT COMPARISON
# =====================================================
elif page == "Advanced Subject Comparison":

    st.header("Advanced Subject Comparison")

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

    # ---------------- ROW 1 ----------------
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Bar Comparison")

        fig1 = px.bar(
            temp,
            y=feature,
            title="Bar Comparison"
        )
        fig1.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.06)",
            font_color="white"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.subheader("Trend Line")

        fig2 = px.line(
            temp,
            y=feature,
            markers=True,
            title="Trend Line"
        )
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.06)",
            font_color="white"
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ---------------- ROW 2 ----------------
    c3, c4 = st.columns(2)

    with c3:
        st.subheader("Pie Distribution")

        fig3 = px.pie(
            values=temp[feature],
            names=temp.index,
            hole=0.5
        )
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        st.subheader("Area Chart")

        fig4 = px.area(
            temp,
            y=feature
        )
        fig4.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.06)",
            font_color="white"
        )
        st.plotly_chart(fig4, use_container_width=True)

    # ---------------- ROW 3 ----------------
    c5, c6 = st.columns(2)

    with c5:
        st.subheader("Scatter Plot")

        fig5 = px.scatter(
            temp,
            x=temp.index,
            y=feature,
            size=feature
        )
        fig5.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.06)",
            font_color="white"
        )
        st.plotly_chart(fig5, use_container_width=True)

    with c6:
        st.subheader("Radar Chart")

        vals = temp[feature].tolist()

        fig6 = go.Figure()

        fig6.add_trace(go.Scatterpolar(
            r=vals,
            theta=[f"Trial {i+1}" for i in range(len(vals))],
            fill='toself'
        ))

        fig6.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)"
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )

        st.plotly_chart(fig6, use_container_width=True)

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

    st.info(f"X-axis = Time | Y-axis = {feature}")

    temp = df[df[subject_col] == selected_subject]

    base = float(temp[feature].mean())

    chart = st.line_chart(
        pd.DataFrame({feature:[base]})
    )

    for i in range(25):
        val = base + np.random.randn()*0.5
        chart.add_rows(pd.DataFrame({feature:[val]}))
        time.sleep(0.2)

    st.success("Monitoring Complete")

# =====================================================
# CLINICAL REPORT
# =====================================================
elif page == "Clinical Report":

    st.header("Clinical Report")

    subjects = sorted(df[subject_col].unique())

    selected_subject = st.selectbox(
        "Select Subject",
        subjects
    )

    temp = df[df[subject_col] == selected_subject]

    score = round(temp[numeric_cols].mean().mean(),2)

    if score >= 75:
        risk = "Low Risk"
    elif score >= 55:
        risk = "Moderate Risk"
    else:
        risk = "High Risk"

    st.metric("Clinical Score", score)
    st.metric("Risk Level", risk)

    fig7 = px.bar(
        x=temp[numeric_cols].mean().index,
        y=temp[numeric_cols].mean().values,
        title="Performance Summary"
    )
    fig7.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.06)",
        font_color="white"
    )
    st.plotly_chart(fig7, use_container_width=True)

    report = f"""
Clinical Report

Subject: {selected_subject}
Score: {score}
Risk Level: {risk}
"""

    st.download_button(
        "Download Report",
        data=report,
        file_name=f"{selected_subject}_report.txt",
        mime="text/plain"
    )
