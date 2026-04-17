import streamlit as st
import sqlite3
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from io import BytesIO
from datetime import datetime
import time

st.set_page_config(page_title='Advanced Gait Dashboard', layout='wide', page_icon='📊')

@st.cache_data
def load_data():
    try:
        return pd.read_csv('clinical_dashboard_15_subjects.csv')
    except:
        np.random.seed(42)
        return pd.DataFrame({
            'Subject':[f'S{i}' for i in range(1,16)],
            'Speed':np.random.uniform(0.5,2.0,15),
            'Stride':np.random.uniform(50,120,15),
            'Balance':np.random.uniform(60,100,15),
            'Cadence':np.random.uniform(70,130,15)
        })

df=load_data()
num_cols=df.select_dtypes(include=np.number).columns.tolist()

st.sidebar.title('Navigation')
password=st.sidebar.text_input('Login Password', type='password')
if password and password!='admin123':
    st.sidebar.error('Incorrect password')
    st.stop()
conn=sqlite3.connect('patients.db', check_same_thread=False)
conn.execute("CREATE TABLE IF NOT EXISTS patients(name TEXT, age TEXT, notes TEXT)")
page=st.sidebar.radio('S

if page=='🏠 Overview':
    st.title('🏠 Dashboard Overview')
    c1,c2,c3=st.columns(3)
    c1.metric('Subjects',len(df))
    c2.metric('Features',df.shape[1])
    c3.metric('Updated',datetime.now().strftime('%H:%M:%S'))
    st.dataframe(df,use_container_width=True)
    if num_cols:
        st.plotly_chart(px.scatter_matrix(df,dimensions=num_cols,title='Feature Relationships'),use_container_width=True)

elif page=='📈 Analytics':
    st.title('📈 Advanced Analytics')
    feature=st.selectbox('Choose Metric',num_cols)
    c1,c2=st.columns(2)
    with c1:
        st.plotly_chart(px.histogram(df,x=feature,marginal='box',title='Distribution'),use_container_width=True)
    with c2:
        st.plotly_chart(px.bar(df,x=df.columns[0],y=feature,title='Subject Comparison'),use_container_width=True)
    corr=df[num_cols].corr()
    st.plotly_chart(px.imshow(corr,text_auto=True,title='Correlation Heatmap'),use_container_width=True)

elif page=='🟢 Live Monitoring':
    st.title('🟢 Live Monitoring')
    placeholder=st.empty()
    chart=st.empty()
    run=st.button('Start Simulation')
    if run:
        vals=[]
        for i in range(30):
            val=float(np.random.normal(80,5))
            vals.append(val)
            placeholder.metric('Current Stability Score',round(val,2))
            live=pd.DataFrame({'t':list(range(len(vals))),'score':vals})
            chart.plotly_chart(px.line(live,x='t',y='score',title='Real-time Signal'),use_container_width=True)
            time.sleep(0.2)

elif page=='🤖 AI Report':
    st.title('🤖 AI Generated Report')
    if num_cols:
        X=StandardScaler().fit_transform(df[num_cols])
        model=IsolationForest(contamination=0.1,random_state=42)
        preds=model.fit_predict(X)
        anomalies=(preds==-1).sum()
        report=f'''# Clinical Gait Report\n\nGenerated: {datetime.now()}\n\n## Summary\n- Total subjects: {len(df)}\n- Numeric metrics analyzed: {len(num_cols)}\n- Potential anomalies detected: {anomalies}\n\n## Insights\n- Average speed: {df[num_cols[0]].mean():.2f}\n- Highest variability metric: {df[num_cols].std().idxmax()}\n- Recommended review subjects with outlier patterns.\n\n## Recommendation\nContinue reverse walking drills and periodic reassessment.'''
        st.markdown(report)
        st.download_button('Download Report (.txt)',report,file_name='ai_report.txt')

elif page=='⬇️ Downloads':
    st.title('⬇️ Downloads Center')
    csv=df.to_csv(index=False).encode('utf-8')
    st.download_button('Download Dataset CSV',csv,'dataset.csv','text/csv')
    summary=df.describe(include='all').to_csv().encode('utf-8')
    st.download_button('Download Summary CSV',summary,'summary.csv','text/csv')
    st.info('You can also download AI report from the AI Report page.')
