import streamlit as st


def show_decision_trace(
    application: dict,
):
    """Display the CreditLens decision trace."""

    decision_trace = application.get(
        "decision_trace"
    )

    if not decision_trace:
        return

    st.subheader("Decision Trace")

    with st.expander(
        "Applicant Data",
        expanded=False,
    ):

        st.json(
            decision_trace.get(
                "applicant_data",
                {},
            )
        )

    with st.expander(
        "Financial Analysis",
        expanded=False,
    ):

        st.json(
            decision_trace.get(
                "financial_analysis",
                {},
            )
        )

    with st.expander(
        "Risk Analysis",
        expanded=False,
    ):

        st.json(
            decision_trace.get(
                "risk_analysis",
                {},
            )
        )

    with st.expander(
        "Policy Evidence",
        expanded=False,
    ):

        policy_context = decision_trace.get(
            "policy_context",
            "",
        )

        if policy_context:

            st.caption(
                "Policy evidence retrieved by CreditLens "
                "from the local policy knowledge base."
            )

            st.markdown(
                policy_context
            )

        else:

            st.info(
                "No policy evidence is available."
            )

    with st.expander(
        "Decision Logic",
        expanded=False,
    ):

        rule_risk = decision_trace.get(
            "rule_risk_level",
            "N/A",
        )

        final_risk = decision_trace.get(
            "final_risk_level",
            "N/A",
        )

        lending_decision = decision_trace.get(
            "lending_decision",
            {},
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Rule Risk",
                rule_risk,
            )

        with col2:

            st.metric(
                "Final Risk",
                final_risk,
            )

        st.write(
            "Lending Decision"
        )

        st.write(
            f"**Decision:** "
            f"{lending_decision.get('decision', 'N/A')}"
        )

        st.write(
            f"**Reason:** "
            f"{lending_decision.get('reason', 'N/A')}"
        )