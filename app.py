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

[data-testid="stAppViewContainer"]{
background:linear-gradient(135deg,#ffffff,#f7f9fc,#eef3ff);
color:#111111;
}

[data-testid="stSidebar"]{
background:linear-gradient(180deg,#f1f5ff,#dfe9ff);
}

[data-testid="stHeader"]{
background:rgba(255,255,255,0);
}

h1,h2,h3,h4,h5,h6,p,label,span,div{
color:#111111 !important;
}

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

div[data-testid="metric-container"]{
background:#ffffff;
border:1px solid #d8e2ff;
border-radius:14px;
padding:16px;
box-shadow:0 4px 12px rgba(0,0,0,0.06);
}

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
# GPS DATA
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
# CHART STYLE
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
        "📊 Advanced Comparison Analysis",
        "📡 Live Monitoring",
        "📄 AI Report"
    ]
)

# ==========================================================
# HOME PAGE
# ==========================================================
if page == "🏠 Home":

    st.header("Dashboard Overview")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Subjects",15)
    c2.metric("Conditions",3)
    c3.metric("Reports",15)
    c4.metric("Metrics",len(numeric_cols))

    st.markdown("---")

    st.subheader("Project Modules")

    st.write("""
### Included Modules:

- Home Dashboard Overview  
- Advanced Comparison Analysis  
- Live Subject Monitoring  
- AI Clinical Report Generation  
- Fall Risk Prediction  
- Balance & Stability Analysis  
- Downloadable Subject Reports  
""")

    st.success("System Ready")

# ==========================================================
# COMPARISON PAGE
# ==========================================================
elif page == "📊 Advanced Comparison Analysis":

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
            title="GPS vs Condition Comparison"
        )
        st.plotly_chart(style(fig1), use_container_width=True)

        st.info("""
Lower GPS score indicates better gait mechanics.
Higher score in challenging conditions suggests increased movement deviation.
""")

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

        st.info("""
Increasing trend shows gait difficulty rising across task complexity.
Phone Reverse generally shows highest challenge.
""")

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

    st.info("""
Wider radar area reflects greater gait deviation.
Compact balanced shape indicates stable performance.
""")

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

    chart = st.line_chart(pd.DataFrame({metric:[base]}))

    for i in range(20):
        val = base + np.random.randn()*0.4
        chart.add_rows(pd.DataFrame({metric:[val]}))
        time.sleep(0.2)

# ==========================================================
# AI REPORT
# ==========================================================
elif page == "📄 AI Report":

    st.header("AI Clinical Report")

    selected = st.selectbox(
        "Select Subject",
        list(gps_data.keys())
    )

    vals = gps_data[selected]

    control = vals["Control"]
    reverse = vals["Reverse"]
    phone = vals["Phone Reverse"]

    clinical = round(max(0,100-((control+reverse+phone)/3)*6),2)
    balance = round(max(0,100-phone*5),2)
    stability = round(max(0,100-reverse*5),2)
    risk = round(((phone+reverse)/30)*100,2)

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Clinical Score",clinical)
    c2.metric("Balance Score",balance)
    c3.metric("Stability Score",stability)
    c4.metric("Fall Risk %",risk)

    fig = px.bar(
        x=["Clinical","Balance","Stability","Risk"],
        y=[clinical,balance,stability,risk],
        color=["Clinical","Balance","Stability","Risk"]
    )

    st.plotly_chart(style(fig), use_container_width=True)
