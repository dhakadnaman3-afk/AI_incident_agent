import streamlit as st
import json
from datetime import datetime

from incident_agent import build_graph


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Incident Agent",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    .stApp {
        background-color: #0b1120;
        color: #e5e7eb;
    }

    .main-title {
        font-size: 38px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
    }

    .card-title {
        font-size: 18px;
        font-weight: 600;
        color: #f8fafc;
        margin-bottom: 12px;
    }

    .metric-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 12px;
        padding: 18px;
        text-align: center;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #38bdf8;
    }

    .metric-label {
        color: #94a3b8;
        font-size: 14px;
    }

    .incident-box {
        background: #1e293b;
        border-left: 4px solid #ef4444;
        padding: 15px;
        border-radius: 8px;
        color: #e2e8f0;
    }

    .success-box {
        background: #052e16;
        border-left: 4px solid #22c55e;
        padding: 15px;
        border-radius: 8px;
    }

    .warning-box {
        background: #422006;
        border-left: 4px solid #f59e0b;
        padding: 15px;
        border-radius: 8px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "incident" not in st.session_state:
    st.session_state.incident = ""


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🚨 AI Incident Agent")

    st.markdown("---")

    st.markdown("### Navigation")

    page = st.radio(
        "Go to",
        [
            "Dashboard",
            "New Incident",
            "Audit Trail"
        ]
    )

    st.markdown("---")

    st.markdown("### System Status")

    st.success("● Agent Online")

    st.info("LangGraph Engine Ready")


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🚨 AI Incident Response Center</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered incident diagnosis, remediation and audit monitoring'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">1</div>
            <div class="metric-label">Active Incident</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">AI</div>
            <div class="metric-label">Diagnosis Engine</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">ON</div>
            <div class="metric-label">Monitoring</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">100%</div>
            <div class="metric-label">Audit Coverage</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # Current incident
    st.markdown("""
    <div class="card">
        <div class="card-title">🚨 Current Incident</div>
    </div>
    """, unsafe_allow_html=True)

    incident_text = (
        "ALERT: payments-service p99 latency spiked to 4200ms "
        "(baseline 180ms).\n\n"
        "Error logs show: connection pool exhausted repeated 340 times "
        "in last 5 minutes.\n\n"
        "DB CPU utilization at 92%. No recent deployments in last 2 hours."
    )

    st.markdown(
        f'<div class="incident-box">{incident_text}</div>',
        unsafe_allow_html=True
    )

    st.markdown("")

    # Result section
    if st.session_state.result:

        result = st.session_state.result

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("""
            <div class="card">
                <div class="card-title">🔍 AI Diagnosis</div>
            """, unsafe_allow_html=True)

            st.write(
                result.get(
                    "diagnosis",
                    "No diagnosis available."
                )
            )

            st.markdown("</div>", unsafe_allow_html=True)

        with col2:

            st.markdown("""
            <div class="card">
                <div class="card-title">🛠️ Proposed Fix</div>
            """, unsafe_allow_html=True)

            st.write(
                result.get(
                    "proposed_fix",
                    "No fix proposed."
                )
            )

            st.markdown("</div>", unsafe_allow_html=True)

    else:

        st.info(
            "No incident analysis available. "
            "Go to 'New Incident' to analyze an incident."
        )


# ============================================================
# NEW INCIDENT
# ============================================================

elif page == "New Incident":

    st.subheader("🚨 Create New Incident")

    st.write(
        "Paste your incident alert, logs or monitoring information below."
    )

    incident = st.text_area(
        "Incident Report",
        value=(
            "ALERT: payments-service p99 latency spiked to 4200ms "
            "(baseline 180ms).\n"
            "Error logs show connection pool exhausted repeatedly.\n"
            "DB CPU utilization is at 92%."
        ),
        height=220
    )

    st.markdown("")

    if st.button(
        "🔍 Analyze Incident",
        type="primary",
        use_container_width=True
    ):

        if not incident.strip():

            st.error("Please enter an incident report.")

        else:

            with st.spinner("AI Agent is analyzing the incident..."):

                try:

                    graph = build_graph()

                    initial_state = {
                        "incident_report": incident,
                        "diagnosis": None,
                        "proposed_fix": None,
                        "confidence": None,
                        "approved": None,
                        "execution_result": None,
                        "audit_trail": []
                    }

                    result = graph.invoke(initial_state)

                    st.session_state.result = result
                    st.session_state.incident = incident

                    st.success(
                        "Incident analysis completed successfully."
                    )

                except Exception as e:

                    st.error(
                        f"Agent execution failed: {str(e)}"
                    )

    # Show result
    if st.session_state.result:

        result = st.session_state.result

        st.markdown("---")

        st.subheader("🔍 AI Analysis")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### Diagnosis")

            diagnosis = result.get("diagnosis")

            if diagnosis:
                st.info(diagnosis)
            else:
                st.warning("No diagnosis returned.")

        with col2:

            st.markdown("### Confidence")

            confidence = result.get("confidence")

            if confidence is not None:

                try:
                    confidence_value = float(confidence)

                    st.progress(
                        min(max(confidence_value, 0.0), 1.0)
                    )

                    st.write(
                        f"Confidence: {confidence_value:.2%}"
                    )

                except:

                    st.write(confidence)

            else:

                st.warning("Confidence unavailable.")

        st.markdown("")

        st.subheader("🛠️ Proposed Remediation")

        proposed_fix = result.get("proposed_fix")

        if proposed_fix:

            st.code(
                str(proposed_fix),
                language="bash"
            )

        else:

            st.warning("No remediation proposed.")

        # Approval
        st.markdown("---")

        st.subheader("👤 Human Approval")

        st.warning(
            "Review the proposed remediation before execution."
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "✅ Approve Fix",
                use_container_width=True
            ):

                st.success(
                    "Fix approved. Execution can proceed."
                )

        with col2:

            if st.button(
                "❌ Reject Fix",
                use_container_width=True
            ):

                st.error(
                    "Fix rejected. No execution performed."
                )


# ============================================================
# AUDIT TRAIL
# ============================================================

elif page == "Audit Trail":

    st.subheader("📜 Audit Trail")

    if st.session_state.result:

        audit = st.session_state.result.get(
            "audit_trail",
            []
        )

        if audit:

            for index, event in enumerate(audit, 1):

                with st.expander(
                    f"Event {index}"
                ):

                    if isinstance(event, dict):

                        st.json(event)

                    else:

                        st.write(event)

        else:

            st.info(
                "No audit events available for the current incident."
            )

    else:

        st.info(
            "Run an incident analysis first to generate audit events."
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "AI Incident Agent • Powered by Python + LangGraph + Streamlit"
)