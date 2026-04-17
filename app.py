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
# PREMIUM BLACK THEME + FIXED DROPDOWN VISIBILITY
# ==========================================================
st.markdown("""
<style>

/* App */
[data-testid="stAppViewContainer"]{
background:linear-gradient(135deg,#000000,#111111,#1d1d1d);
color:white;
}

/* Sidebar */
[data-testid="stSidebar"]{
background:linear-gradient(180deg,#050505,#111111);
}

/* Header */
[data-testid="stHeader"]{
background:rgba(0,0,0,0);
}

/* Text */
h1,h2,h3,h4,h5,h6,p,label,span,div{
color:white !important;
}

/* SELECT BOX FIX */
div[data-baseweb="select"] > div{
background:#ffffff !important;
color:#000000 !important;
border-radius:10px;
border:2px solid #555;
}

div[data-baseweb="select"] span{
color:#000000 !important;
font-weight:700 !important;
}

/* Metrics cards */
div[data-testid="metric-container"]{
background:#151515;
border:1px solid #333;
border-radius:14px;
padding:16px;
}

/* Buttons */
.stButton>button{
background:#ffffff;
color:#000000;
font-weight:700;
border-radius:8px;
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
# REAL REPORT BASED GPS DATA (3 CONDITIONS)
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
# PAGE 1 HOME
# ==========================================================
if page == "🏠 Home":

    st.header("Dashboard Overview")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Subjects",15)
    c2.metric("Conditions",3)
    c3.metric("Reports",15)
    c4.metric("Metrics",len(numeric_cols))

    st.markdown("---")

    st.write("""
### Modules Included

- Real Comparison Analysis  
- Live Monitoring  
- AI Clinical Reports  
- Downloadable Reports  
- Fall Risk Detection  
""")

# ==========================================================
# PAGE 2 COMPARISON ANALYSIS
# ==========================================================
elif page == "📊 Comparison Analysis":

    st.header("Advanced Comparison Analysis")

    selected = st.selectbox(
        "Select Subject",
        list(gps_data.keys())
    )

    vals = gps_data[selected]

    graph_df = pd.DataFrame({
        "Condition":["Control","Reverse","Phone Reverse"],
        "GPS":[vals["Control"],vals["Reverse"],vals["Phone Reverse"]]
    })

    # -------------------------------------------
    # TOP INSIGHT
    # -------------------------------------------
    deterioration = round(
        ((vals["Phone Reverse"] - vals["Control"]) /
         vals["Control"]) * 100,2
    )

    st.info(
        f"Performance deviation increased by {deterioration}% from Control to Dual-task Reverse Walking."
    )

    # -------------------------------------------
    # GRAPH 1 BAR
    # -------------------------------------------
    c
