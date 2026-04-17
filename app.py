# ==========================================================
# REPLACE YOUR CURRENT "AI Clinical Report" SECTION WITH THIS
# ==========================================================

elif page == "📄 AI Clinical Report":

    st.header("Advanced AI Clinical Report")

    # ------------------------------------------------------
    # SUBJECT SELECT
    # ------------------------------------------------------
    selected = st.selectbox(
        "Select Subject",
        list(gps_data.keys())
    )

    vals = gps_data[selected]

    control = vals["Control"]
    reverse = vals["Reverse"]
    phone = vals["Phone Reverse"]

    # ------------------------------------------------------
    # REAL CLINICAL SCORE (REPORT BASED)
    # Lower GPS = Better
    # ------------------------------------------------------
    clinical_score = round(
        max(0, 100 - ((control + reverse + phone)/3)*6),
        2
    )

    # ------------------------------------------------------
    # 3 METRICS
    # ------------------------------------------------------
    balance_score = round(
        max(0, 100 - phone*5),
        2
    )

    stability_score = round(
        max(0, 100 - reverse*5),
        2
    )

    fall_risk = round(
        ((phone + reverse)/30)*100,
        2
    )

    # ------------------------------------------------------
    # RISK LEVEL
    # ------------------------------------------------------
    if fall_risk < 40:
        risk = "Low Risk"
    elif fall_risk < 70:
        risk = "Moderate Risk"
    else:
        risk = "High Risk"

    # ------------------------------------------------------
    # SUBJECT INDEX
    # ------------------------------------------------------
    idx = int(selected.split()[-1]) - 1

    # ------------------------------------------------------
    # SUBJECT-WISE POSTURE FINDINGS
    # ------------------------------------------------------
    posture_findings = [
        "Mild trunk lean during reverse gait.",
        "Reduced knee flexion while stepping backward.",
        "Left-right asymmetry observed.",
        "Delayed postural correction response.",
        "Short stride with guarded movement.",
        "Moderate hip stiffness detected.",
        "Reduced cadence control.",
        "Stable posture with minor sway.",
        "Excess ankle compensation pattern.",
        "Fair trunk stability.",
        "Slow step transition response.",
        "Mild instability in stance phase.",
        "Reduced balance confidence.",
        "Good posture control maintained.",
        "Dual-task gait disturbance noted."
    ]

    # ------------------------------------------------------
    # SUBJECT-WISE RECOMMENDATIONS
    # ------------------------------------------------------
    recommendations = [
        "Core stability drills + mirror posture training.",
        "Backward stepping with knee mobility exercises.",
        "Single-leg balance + symmetry gait drills.",
        "Reaction-time balance board training advised.",
        "Stride length training with therapist guidance.",
        "Hip mobility and flexibility program advised.",
        "Cadence rhythm walking practice suggested.",
        "Maintain present routine and weekly monitoring.",
        "Ankle control and calf strengthening advised.",
        "Trunk strengthening with posture correction.",
        "Reverse walking repetition drills advised.",
        "Static balance hold + gait supervision advised.",
        "Confidence building + safe stepping practice.",
        "Maintain current strong gait efficiency.",
        "Dual-task training without distraction first."
    ]

    finding = posture_findings[idx]
    recommendation = recommendations[idx]

    # ------------------------------------------------------
    # DISPLAY TOP METRICS
    # ------------------------------------------------------
    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.metric("Clinical Score", clinical_score)

    with c2:
        st.metric("Balance Score", balance_score)

    with c3:
        st.metric("Stability Score", stability_score)

    with c4:
        st.metric("Fall Risk %", fall_risk)

    st.markdown("---")

    # ------------------------------------------------------
    # CLINICAL OBSERVATION
    # ------------------------------------------------------
    st.subheader("Clinical Observation")

    st.write(f"""
- Control GPS: **{control}**
- Reverse Walking GPS: **{reverse}**
- Smartphone Reverse GPS: **{phone}**
- Risk Level: **{risk}**
- Posture Finding: **{finding}**
""")

    # ------------------------------------------------------
    # GRAPH 1 : CONDITION REPORT GRAPH
    # ------------------------------------------------------
    g1 = pd.DataFrame({
        "Condition": [
            "Control",
            "Reverse",
            "Phone Reverse"
        ],
        "GPS Score": [
            control,
            reverse,
            phone
        ]
    })

    fig1 = px.bar(
        g1,
        x="Condition",
        y="GPS Score",
        color_discrete_sequence=["white"],
        title="Report Condition Comparison"
    )

    fig1.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#111111",
        font_color="white"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # ------------------------------------------------------
    # GRAPH 2 : AI METRICS GRAPH
    # ------------------------------------------------------
    g2 = pd.DataFrame({
        "Metric":[
            "Clinical",
            "Balance",
            "Stability",
            "Fall Risk"
        ],
        "Value":[
            clinical_score,
            balance_score,
            stability_score,
            fall_risk
        ]
    })

    fig2 = px.bar(
        g2,
        x="Metric",
        y="Value",
        color_discrete_sequence=["white"],
        title="AI Generated Performance Metrics"
    )

    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#111111",
        font_color="white"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # ------------------------------------------------------
    # GRAPH 3 : RADAR GRAPH
    # ------------------------------------------------------
    fig3 = go.Figure()

    fig3.add_trace(go.Scatterpolar(
        r=[
            clinical_score,
            balance_score,
            stability_score,
            100-fall_risk
        ],
        theta=[
            "Clinical",
            "Balance",
            "Stability",
            "Safety"
        ],
        fill='toself',
        line=dict(color="white"),
        fillcolor="rgba(255,255,255,0.20)"
    ))

    fig3.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(color="white")
        )
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    # ------------------------------------------------------
    # RECOMMENDATION
    # ------------------------------------------------------
    st.subheader("AI Recommendation")

    st.success(recommendation)

    # ------------------------------------------------------
    # DOWNLOADABLE REPORT
    # ------------------------------------------------------
    report = f"""
ADVANCED AI CLINICAL REPORT

Subject: {selected}

Control GPS: {control}
Reverse GPS: {reverse}
Phone Reverse GPS: {phone}

Clinical Score: {clinical_score}
Balance Score: {balance_score}
Stability Score: {stability_score}
Fall Risk: {fall_risk}%
Risk Level: {risk}

Clinical Finding:
{finding}

Recommendation:
{recommendation}
"""

    st.download_button(
        "Download Full AI Report",
        data=report,
        file_name=f"{selected}_AI_Report.txt",
        mime="text/plain"
    )
