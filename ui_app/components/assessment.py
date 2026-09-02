import streamlit as st

from components.financial_metrics import (
    show_financial_metrics,
)
from components.ml_analysis import (
    show_ml_analysis,
)
from components.analyst_explanation import (
    show_analyst_explanation,
)
from components.decision_trace import (
    show_decision_trace,
)
from theme import render_decision_status


def show_assessment(application: dict):
    """Display the complete credit assessment."""

    st.title("Credit Assessment")

    st.caption(
        f"Application #{application['application_id']}"
    )

    st.divider()

    decision = application.get(
        "decision",
        "N/A",
    )

    risk_level = application.get(
        "risk_level",
        "N/A",
    )

    reason = application.get(
        "decision_reason",
        "No decision reason available.",
    )

    render_decision_status(
        decision=decision,
        risk_level=risk_level,
        reason=reason,
    )

    st.divider()

    show_financial_metrics(
        application
    )

    st.divider()

    show_ml_analysis(
        application
    )

    st.divider()

    show_analyst_explanation(
        application
    )

    st.divider()

    show_decision_trace(
        application
    )