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
    page_title="Biomechanical & Neuromuscular Adaptations Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# BLACK THEME CSS
# =====================================================
st.markdown("""
<style>
[data-testid="stAppViewContainer"]{
background: linear-gradient(135deg,#000000,#0f0f0f,#1c1c1c);
color:white;
}
[data-testid="stSidebar"]{
background:linear-gradient(180deg,#050505,#121212);
}
[data-testid="stHeader"]{
background:rgba(0,0,0,0);
}
h1,h2,h3,h4,h5,h6,p,label,span,div{
color:white !important;
}
div[data-baseweb="select"] > div{
background:#1c1c1c!important;
border:1px solid #333;
border-radius:10px;
}
div[data-testid="metric-container"]{
background:#151515;
border:1px solid #333;
border-radius:12px;
padding:15px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD CSV
# =====================================================
@st.cache_data
def load_data():
    return pd.read_csv("clinical_dashboard_15_subjects.csv")

df = load_data()
df.columns = df.columns.str.strip().str.lower()

subject_col = "subject" if "subject" in df.columns else df.columns[0]
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

subjects = sorted(df[subject_col].unique())

# =====================================================
# SUBJECT DISPLAY
# =====================================================
subject_map = {
    s: f"Subject {i+1}"
    for i,s in enumerate(subjects)
}

# =====================================================
# HEADER
# =====================================================
st.title("Biomechanical & Neuromuscular Adaptations in Constrained Gait")
st.subheader("Reverse Walking")
st.caption("Team Members: Anushka Singh | Astha Singh | Kritika Vashishtha")

# =====================================================
# SIDEBAR
# =====================================================
page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📊 Comparison",
        "📡 Live Monitoring",
        "📄 AI Report",
        "📁 Download Center"
    ]
)

# =====================================================
# CHART STYLE
# =====================================================
def style(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#111111",
        font_color="white",
        xaxis=dict(
            color="white",
            gridcolor="rgba(255,255,255,0.10)"
        ),
        yaxis=dict(
            color="white",
            gridcolor="rgba(255,255,255,0.10)"
        )
    )
    return fig

# =====================================================
# PAGE 1 HOME
# =====================================================
if page == "🏠 Home":

    st.header("Dashboard Overview")

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.metric("Subjects", len(subjects))

    with c2:
        st.metric("Records", len(df))

    with c3:
        st.metric("Metrics", len(numeric_cols))

    with c4:
        st.metric("Conditions", 3)

    st.markdown("---")

    st.write("""
### Project Objective

This dashboard evaluates biomechanical and neuromuscular adaptations during reverse walking gait.

### Modules Included:

- Subject Comparison  
- Live Monitoring  
- AI Clinical Reports  
- Downloadable Reports  
- Performance Tracking  
""")

# =====================================================
# PAGE 2 COMPARISON
# =====================================================
elif page == "📊 Comparison":

    st.header("Advanced Comparison")

    selected = st.selectbox(
        "Select Subject",
        subjects,
        format_func=lambda x: subject_map[x]
    )

    metric = st.selectbox(
        "Select Metric",
        numeric_cols
    )

    temp = df[df[subject_col] == selected]

    c1,c2 = st.columns(2)

    with c1:
        fig1 = px.bar(
            temp,
            y=metric,
            color_discrete_sequence=["white"],
            title="Bar Comparison"
        )
        st.plotly_chart(style(fig1), use_container_width=True)

    with c2:
        fig2 = px.line(
            temp,
            y=metric,
            markers=True,
            title="Trend Line"
        )
        fig2.update_traces(
            line=dict(color="white", width=3),
            marker=dict(color="white")
        )
        st.plotly_chart(style(fig2), use_container_width=True)

    c3,c4 = st.columns(2)

    with c3:
        fig3 = px.scatter(
            temp,
            x=temp.index,
            y=metric,
            size=metric,
            title="Scatter Plot"
        )
        fig3.update_traces(marker=dict(color="white"))
        st.plotly_chart(style(fig3), use_container_width=True)

    with c4:
        fig4 = px.area(
            temp,
            y=metric,
            title="Area Chart"
        )
        fig4.update_traces(
            line=dict(color="white"),
            fillcolor="rgba(255,255,255,0.20)"
        )
        st.plotly_chart(style(fig4), use_container_width=True)

# =====================================================
# PAGE 3 LIVE MONITORING
# =====================================================
elif page == "📡 Live Monitoring":

    st.header("Live Monitoring")

    selected = st.selectbox(
        "Select Subject",
        subjects,
        format_func=lambda x: subject_map[x]
    )

    metric = st.selectbox(
        "Select Metric",
        numeric_cols
    )

    st.info(f"X-axis = Time | Y-axis = {metric}")

    temp = df[df[subject_col] == selected]

    base = float(temp[metric].mean())

    chart = st.line_chart(
        pd.DataFrame({metric:[base]})
    )

    for i in range(25):
        val = base + np.random.randn()*0.4
        chart.add_rows(
            pd.DataFrame({metric:[val]})
        )
        time.sleep(0.2)

# =====================================================
# PAGE 4 AI REPORT
# =====================================================
elif page == "📄 AI Report":

    st.header("AI Clinical Report")

    selected = st.selectbox(
        "Select Subject",
        subjects,
        format_func=lambda x: subject_map[x]
    )

    temp = df[df[subject_col] == selected]

    mean_val = temp[numeric_cols].mean().mean()
    std_val = temp[numeric_cols].std().mean()

    clinical_score = round(mean_val,2)

    stability = round(
        max(0,100 - std_val*10),
        2
    )

    balance = round(
        min(100, mean_val*5),
        2
    )

    fall_risk = round(
        100 - ((stability + balance)/2),
        2
    )

    if fall_risk < 30:
        risk = "Low Risk"
    elif fall_risk < 60:
        risk = "Moderate Risk"
    else:
        risk = "High Risk"

    idx = subjects.index(selected)

    recs = [
        "Maintain current training routine.",
        "Add balance board exercises.",
        "Core strengthening advised.",
        "Reverse gait supervised practice.",
        "Posture drills recommended.",
        "Hip mobility training advised.",
        "Cadence practice suggested.",
        "Maintain present performance.",
        "Trunk control drills advised.",
        "Continue mobility exercises.",
        "Reaction stepping drills advised.",
        "Strength endurance training.",
        "Weekly therapist review.",
        "Excellent gait performance maintained.",
        "Dual-task gait training advised."
    ]

    recommendation = recs[idx]

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.metric("Clinical Score", clinical_score)

    with c2:
        st.metric("Balance Score", balance)

    with c3:
        st.metric("Stability Score", stability)

    with c4:
        st.metric("Fall Risk %", fall_risk)

    st.markdown("---")

    st.write(f"### Risk Level: {risk}")
    st.success(recommendation)

    graph_df = pd.DataFrame({
        "Metric":[
            "Clinical",
            "Balance",
            "Stability",
            "Risk"
        ],
        "Value":[
            clinical_score,
            balance,
            stability,
            fall_risk
        ]
    })

    fig = px.bar(
        graph_df,
        x="Metric",
        y="Value",
        color_discrete_sequence=["white"]
    )

    st.plotly_chart(style(fig), use_container_width=True)

    report = f"""
AI CLINICAL REPORT

Subject: {subject_map[selected]}

Clinical Score: {clinical_score}
Balance Score: {balance}
Stability Score: {stability}
Fall Risk: {fall_risk}
Risk Level: {risk}

Recommendation:
{recommendation}
"""

    st.download_button(
        "Download Subject Report",
        data=report,
        file_name=f"{subject_map[selected]}_report.txt",
        mime="text/plain"
    )

# =====================================================
# PAGE 5 DOWNLOAD CENTER
# =====================================================
elif page == "📁 Download Center":

    st.header("Download Center")

    st.write("""
Download project reports and subject reports here.
""")

    all_report = "Combined Clinical Dashboard Summary"

    st.download_button(
        "Download Summary Report",
        data=all_report,
        file_name="dashboard_summary.txt",
        mime="text/plain"
    )

    st.success("Reports ready for download.")
