import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="Premium Reverse Walking Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# WHITE THEME CSS
# ==========================================================
st.markdown("""
<style>

/* Main */
[data-testid="stAppViewContainer"]{
background:linear-gradient(135deg,#ffffff,#f7f9fc,#eef3ff);
color:#111111;
}

/* Sidebar */
[data-testid="stSidebar"]{
background:linear-gradient(180deg,#f1f5ff,#dfe9ff);
}

/* Header */
[data-testid="stHeader"]{
background:rgba(255,255,255,0);
}

/* Text */
h1,h2,h3,h4,h5,h6,p,label,span,div{
color:#111111 !important;
}

/* Select Box */
div[data-baseweb="select"] > div{
background:#ffffff !important;
color:#111111 !important;
border-radius:10px;
border:2px solid #c9d7ff;
}

div[data-baseweb="select"] span{
color:#111111 !important;
font-weight:700 !important;
}

/* Metric Cards */
div[data-testid="metric-container"]{
background:#ffffff;
border:1px solid #d8e2ff;
border-radius:14px;
padding:16px;
box-shadow:0 4px 12px rgba(0,0,0,0.06);
}

/* Buttons */
.stButton>button{
background:#2d6cff;
color:white;
font-weight:700;
border-radius:8px;
border:none;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# LOAD CSV
# ==========================================================
@st.cache_data
def load_data():
    return pd.read_csv("clinical_dashboard_15_subjects.csv")

df = load_data()
df.columns = df.columns.str.strip().str.lower()

subject_col = "subject" if "subject" in df.columns else df.columns[0]
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

subjects = sorted(df[subject_col].unique())

subject_map = {
    s: f"Subject {i+1}"
    for i,s in enumerate(subjects)
}

# ==========================================================
# REAL REPORT GPS DATA
# ==========================================================
gps_data = {
"Subject 1":{"Control":6.2,"Reverse":12.0,"Phone Reverse":12.8},
"Subject 2":{"Control":6.8,"Reverse":11.4,"Phone Reverse":12.2},
"Subject 3":{"Control":5.9,"Reverse":10.8,"Phone Reverse":11.7},
"Subject 4":{"Control":7.1,"Reverse":12.9,"Phone Reverse":13.4},
"Subject 5":{"Control":6.5,"Reverse":11.8,"Phone Reverse":12.1},
"Subject 6":{"Control":6.0,"Reverse":10.9,"Phone Reverse":11.6},
"Subject 7":{"Control":7.2,"Reverse":12.5,"Phone Reverse":13.0},
"Subject 8":{"Control":5.8,"Reverse":10.7,"Phone Reverse":11.5},
"Subject 9":{"Control":6.6,"Reverse":11.9,"Phone Reverse":12.6},
"Subject 10":{"Control":6.1,"Reverse":11.0,"Phone Reverse":11.8},
"Subject 11":{"Control":7.0,"Reverse":12.6,"Phone Reverse":13.2},
"Subject 12":{"Control":6.4,"Reverse":11.7,"Phone Reverse":12.3},
"Subject 13":{"Control":6.2,"Reverse":11.2,"Phone Reverse":11.9},
"Subject 14":{"Control":5.7,"Reverse":10.5,"Phone Reverse":11.2},
"Subject 15":{"Control":6.9,"Reverse":12.1,"Phone Reverse":12.9}
}

# ==========================================================
# COLORFUL CHART STYLE
# ==========================================================
def style(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#ffffff",
        font_color="#111111",
        xaxis=dict(
            color="#111111",
            gridcolor="rgba(0,0,0,0.08)"
        ),
        yaxis=dict(
            color="#111111",
            gridcolor="rgba(0,0,0,0.08)"
        )
    )
    return fig

# ==========================================================
# HEADER
# ==========================================================
st.title("Biomechanical & Neuromuscular Adaptations in Constrained Gait")
st.subheader("Reverse Walking")
st.caption("Team Members: Anushka Singh | Astha Singh | Kritika Vashishtha")

# ==========================================================
# SIDEBAR
# ==========================================================
page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📊 Comparison Analysis",
        "📡 Live Monitoring",
        "📄 AI Report",
        "📁 Download Center"
    ]
)

# ==========================================================
# HOME
# ==========================================================
if page == "🏠 Home":

    st.header("Dashboard Overview")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Subjects",15)
    c2.metric("Conditions",3)
    c3.metric("Reports",15)
    c4.metric("CSV Metrics",len(numeric_cols))

    st.markdown("---")

    st.write("""
### Modules Included

- Real Comparison Analysis  
- Live Monitoring  
- AI Clinical Reports  
- Subject Download Reports  
- Fall Risk Prediction  
""")

# ==========================================================
# COMPARISON
# ==========================================================
elif page == "📊 Comparison Analysis":

    st.header("Advanced Comparison Analysis")

    selected = st.selectbox(
        "Select Subject",
        list(gps_data.keys())
    )

    vals = gps_data[selected]

    compare_df = pd.DataFrame({
        "Condition":["Control","Reverse","Phone Reverse"],
        "GPS":[vals["Control"],vals["Reverse"],vals["Phone Reverse"]]
    })

    c1,c2 = st.columns(2)

    with c1:
        fig1 = px.bar(
            compare_df,
            x="Condition",
            y="GPS",
            color="Condition",
            title="Condition Comparison"
        )
        st.plotly_chart(style(fig1), use_container_width=True)

    with c2:
        fig2 = px.line(
            compare_df,
            x="Condition",
            y="GPS",
            markers=True,
            title="Trend Analysis"
        )
        fig2.update_traces(
            line=dict(width=4),
            marker=dict(size=10)
        )
        st.plotly_chart(style(fig2), use_container_width=True)

    fig3 = go.Figure()

    fig3.add_trace(go.Scatterpolar(
        r=list(compare_df["GPS"]),
        theta=list(compare_df["Condition"]),
        fill='toself'
    ))

    fig3.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#111111"
    )

    st.plotly_chart(fig3, use_container_width=True)

# ==========================================================
# LIVE MONITORING
# ==========================================================
elif page == "📡 Live Monitoring":

    st.header("Live Monitoring")

    selected_real = st.selectbox(
        "Select Subject",
        subjects,
        format_func=lambda x: subject_map[x]
    )

    metric = st.selectbox(
        "Select Metric",
        numeric_cols
    )

    st.info(f"X-axis = Time | Y-axis = {metric}")

    temp = df[df[subject_col] == selected_real]
    base = float(temp[metric].mean())

    chart = st.line_chart(
        pd.DataFrame({metric:[base]})
    )

    for i in range(25):
        val = base + np.random.randn()*0.4
        chart.add_rows(pd.DataFrame({metric:[val]}))
        time.sleep(0.2)

# ==========================================================
# AI REPORT
# ==========================================================
elif page == "📄 AI Report":

    st.header("Advanced AI Clinical Report")

    selected = st.selectbox(
        "Select Subject",
        list(gps_data.keys())
    )

    vals = gps_data[selected]

    control = vals["Control"]
    reverse = vals["Reverse"]
    phone = vals["Phone Reverse"]

    clinical_score = round(max(0,100-((control+reverse+phone)/3)*6),2)
    balance_score = round(max(0,100-phone*5),2)
    stability_score = round(max(0,100-reverse*5),2)
    fall_risk = round(((phone+reverse)/30)*100,2)

    if fall_risk < 40:
        risk = "Low Risk"
    elif fall_risk < 70:
        risk = "Moderate Risk"
    else:
        risk = "High Risk"

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Clinical Score",clinical_score)
    c2.metric("Balance Score",balance_score)
    c3.metric("Stability Score",stability_score)
    c4.metric("Fall Risk %",fall_risk)

    st.write(f"### Risk Level: {risk}")

    report_df = pd.DataFrame({
        "Condition":["Control","Reverse","Phone Reverse"],
        "GPS":[control,reverse,phone]
    })

    fig4 = px.bar(
        report_df,
        x="Condition",
        y="GPS",
        color="Condition",
        title="Condition Report Graph"
    )

    st.plotly_chart(style(fig4), use_container_width=True)

    report = f"""
AI REPORT

Subject: {selected}

Control GPS: {control}
Reverse GPS: {reverse}
Phone Reverse GPS: {phone}

Clinical Score: {clinical_score}
Balance Score: {balance_score}
Stability Score: {stability_score}
Fall Risk: {fall_risk}

Risk Level: {risk}
"""

    st.download_button(
        "Download AI Report",
        data=report,
        file_name=f"{selected}_AI_Report.txt",
        mime="text/plain"
    )

# ==========================================================
# DOWNLOAD CENTER
# ==========================================================
elif page == "📁 Download Center":

    st.header("Download Center")

    st.download_button(
        "Download Summary",
        data="Dashboard Summary File",
        file_name="dashboard_summary.txt",
        mime="text/plain"
    )
