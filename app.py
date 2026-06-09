import streamlit as st

st.set_page_config(
page_title="Careem Delivery Intelligence Copilot",
layout="wide"
)

st.title("🚀 Careem Delivery Intelligence Copilot")

st.subheader(
"Predict delivery risks before they impact launch timelines."
)

updates = st.text_area(
"Paste Project Updates",
height=300
)

if st.button("Analyze Delivery"):


    if not updates.strip():
        st.warning("Please paste project updates.")
        st.stop()

    text = updates.lower()

    risk_count = 0
    positive_points = 0
    negative_points = 0

    risks = []
    dependencies = []
    recommendations = []

    # -------------------------
    # Positive Delivery Signals
    # -------------------------

    progress_count = text.count("progress")
    milestone_count = text.count("milestone")
    completed_count = text.count("completed")

    positive_points += progress_count * 2
    positive_points += milestone_count * 5
    positive_points += completed_count * 3

    # -------------------------
    # Risk Detection
    # -------------------------

    if "vendor" in text:
        risks.append("HIGH - Vendor dependency risk")
        recommendations.append("Escalate vendor dependency")
        negative_points += 10
        risk_count += 1

    if "blocker" in text or "paused" in text:
        risks.append("HIGH - Execution blocker detected")
        recommendations.append("Prioritize blocker resolution")
        negative_points += 15
        risk_count += 1

    if "dependency" in text or "waiting" in text:
        dependencies.append("Cross-team dependency identified")
        recommendations.append("Track dependency daily")
        negative_points += 5
        risk_count += 1

    if "leave" in text or "resource" in text:
        risks.append("MEDIUM - Resource availability risk")
        recommendations.append("Allocate backup resources")
        negative_points += 5
        risk_count += 1

    if "risk" in text:
        risks.append("MEDIUM - Emerging delivery risks detected")
        recommendations.append("Review mitigation plan")
        negative_points += 5
        risk_count += 1

    if "defect" in text:
        risks.append("MEDIUM - Quality risk")
        recommendations.append("Prioritize defect resolution")
        negative_points += 10
        risk_count += 1

    # -------------------------
    # Confidence Calculation
    # -------------------------

    confidence = 75 + positive_points - negative_points

    if confidence > 95:
        confidence = 95

    if confidence < 20:
        confidence = 20

    # -------------------------
    # Health Status
    # -------------------------

    if confidence >= 85:
        health = "🟢 Green"
    elif confidence >= 65:
        health = "🟡 Amber"
    else:
        health = "🔴 Red"

    # -------------------------
    # Delay Forecast
    # -------------------------

    if risk_count >= 5:
        delay = "1 Sprint"
    elif risk_count >= 3:
        delay = "3-5 Days"
    else:
        delay = "On Track"

    # -------------------------
    # Metrics
    # -------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Project Health", health)

    with col2:
        st.metric("Delivery Confidence", f"{confidence}%")

    with col3:
        st.metric("Risk Count", risk_count)

    with col4:
        st.metric("Forecast Delay", delay)

    # -------------------------
    # Risks
    # -------------------------

    st.subheader("Key Risks")

    if risks:
        for risk in risks:
            st.write(f"• {risk}")
    else:
        st.write("No major risks detected")

    # -------------------------
    # Dependencies
    # -------------------------

    st.subheader("Dependencies")

    if dependencies:
        for dep in dependencies:
            st.write(f"• {dep}")
    else:
        st.write("No critical dependencies detected")

    # -------------------------
    # Impacted Teams
    # -------------------------

    st.subheader("Impacted Teams")

    impacted = []

    if "vendor" in text:
        impacted.extend(["Backend", "Mobile"])

    if "dependency" in text:
        impacted.append("QA")

    if "blocker" in text:
        impacted.append("Backend")

    for team in sorted(set(impacted)):
        st.write(f"• {team}")

    # -------------------------
    # Recommendations
    # -------------------------

    st.subheader("Recommended Actions")

    if recommendations:
        for rec in sorted(set(recommendations)):
            st.write(f"• {rec}")
    else:
        st.write("Continue monitoring")

    # -------------------------
    # Executive Summary
    # -------------------------

    st.subheader("Executive Summary")

    if health == "🟢 Green":
        summary = """
        Delivery remains on track. Progress across engineering,
        product, and QA workstreams is healthy with no significant
        schedule threats identified.
        """

    elif health == "🟡 Amber":
        summary = """
        Delivery remains achievable but requires active management
        of dependencies and emerging execution risks. Vendor delays
        and cross-team dependencies may impact downstream activities
        if not addressed proactively.
        """

    else:
        summary = """
        Delivery is at risk due to multiple dependency, resource,
        and execution concerns. Immediate intervention is recommended
        to avoid schedule slippage.
        """

    st.write(summary)

