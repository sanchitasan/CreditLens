import httpx
import streamlit as st

from api_client import CreditLensAPIClient


st.set_page_config(
    page_title="CreditLens",
    page_icon="💳",
    layout="wide",
)


def show_dashboard(client: CreditLensAPIClient):
    """Display the CreditLens dashboard."""

    st.title("CreditLens")

    st.caption(
        "AI-Powered Credit Underwriting & Risk Intelligence Platform"
    )

    st.divider()

    st.header("Application Dashboard")

    try:
        applications = client.list_applications()

    except httpx.RequestError:
        st.error(
            "Unable to connect to the CreditLens API. "
            "Make sure the FastAPI server is running."
        )
        return

    except httpx.HTTPStatusError as error:
        st.error(
            f"CreditLens API returned an error: "
            f"{error.response.status_code}"
        )
        return

    if not applications:
        st.info(
            "No credit applications have been submitted yet."
        )
        return

    st.write(
        f"Total applications: **{len(applications)}**"
    )

    st.subheader("Recent Applications")

    for application in applications:

        st.write(
            f"Application #{application['application_id']}"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Income",
                f"₹{application['monthly_income']:,.0f}",
            )

        with col2:
            st.metric(
                "Loan Amount",
                f"₹{application['loan_amount']:,.0f}",
            )

        with col3:
            st.metric(
                "Risk",
                application["risk_level"],
            )

        with col4:
            st.metric(
                "Decision",
                application["decision"] or "N/A",
            )

        st.divider()


def show_new_application(
    client: CreditLensAPIClient,
):
    """Display and process a new credit application."""

    st.title("New Credit Application")

    st.caption(
        "Enter the applicant's financial and credit information "
        "to perform a credit assessment."
    )

    st.divider()

    with st.form("credit_application_form"):

        st.subheader("Financial Information")

        col1, col2 = st.columns(2)

        with col1:
            monthly_income = st.number_input(
                "Monthly Income (₹)",
                min_value=1.0,
                value=80000.0,
                step=1000.0,
            )

            existing_obligations = st.number_input(
                "Existing Monthly Obligations (₹)",
                min_value=0.0,
                value=20000.0,
                step=1000.0,
            )

            loan_amount = st.number_input(
                "Requested Loan Amount (₹)",
                min_value=1.0,
                value=500000.0,
                step=10000.0,
            )

        with col2:
            annual_interest_rate = st.number_input(
                "Annual Interest Rate (%)",
                min_value=0.01,
                max_value=50.0,
                value=12.0,
                step=0.5,
            )

            tenure_years = st.number_input(
                "Loan Tenure (Years)",
                min_value=0.1,
                max_value=30.0,
                value=5.0,
                step=1.0,
            )

        st.divider()

        st.subheader("Credit Profile")

        col1, col2, col3 = st.columns(3)

        with col1:
            credit_score = st.number_input(
                "Credit Score",
                min_value=300.0,
                max_value=900.0,
                value=750.0,
                step=1.0,
            )

        with col2:
            employment_years = st.number_input(
                "Employment Experience (Years)",
                min_value=0.0,
                value=4.0,
                step=0.5,
            )

        with col3:
            previous_defaults = st.number_input(
                "Previous Defaults",
                min_value=0,
                value=0,
                step=1,
            )

        st.divider()

        submitted = st.form_submit_button(
            "Assess Credit",
            use_container_width=True,
        )

    if not submitted:
        return

    payload = {
        "monthly_income": monthly_income,
        "existing_obligations": existing_obligations,
        "loan_amount": loan_amount,
        "annual_interest_rate": annual_interest_rate,
        "tenure_years": tenure_years,
        "credit_score": credit_score,
        "employment_years": employment_years,
        "previous_defaults": previous_defaults,
    }

    with st.spinner(
        "Running CreditLens credit assessment..."
    ):
        try:
            result = client.create_application(
                payload
            )

        except httpx.RequestError:
            st.error(
                "Unable to connect to the CreditLens API. "
                "Make sure the FastAPI server is running."
            )
            return

        except httpx.HTTPStatusError as error:

            if error.response.status_code == 422:
                st.error(
                    "The application data was rejected "
                    "by the CreditLens API."
                )
            else:
                st.error(
                    "The CreditLens API returned an "
                    f"error ({error.response.status_code})."
                )

            return

    application_id = result["application_id"]

    try:
        application = client.get_application(
            application_id
        )

    except httpx.RequestError:
        st.error(
            "The application was created, but the "
            "assessment could not be retrieved."
        )
        return

    except httpx.HTTPStatusError as error:
        st.error(
            "The application was created, but the "
            f"assessment retrieval failed "
            f"({error.response.status_code})."
        )
        return

    st.session_state["assessment"] = application

    st.success(
        "Credit application assessed successfully."
    )

    show_assessment(application)


def show_applications(client: CreditLensAPIClient):
    """Display the application history page."""

    st.title("Application History")

    st.write(
        "Review previously assessed credit applications."
    )

    # ---------------------------------------------------------
    # Filters
    # ---------------------------------------------------------

    st.subheader("Filters")

    col1, col2 = st.columns(2)

    with col1:
        risk_filter = st.selectbox(
            "Risk Level",
            ["All", "LOW", "MEDIUM", "HIGH"],
        )

    with col2:
        decision_filter = st.selectbox(
            "Decision",
            [
                "All",
                "APPROVE",
                "MANUAL_REVIEW",
                "REJECT",
            ],
        )

    # ---------------------------------------------------------
    # Fetch applications
    # ---------------------------------------------------------

    try:
        applications = client.list_applications(
            risk_level=(
                None
                if risk_filter == "All"
                else risk_filter
            ),
            decision=(
                None
                if decision_filter == "All"
                else decision_filter
            ),
        )

    except httpx.RequestError:
        st.error(
            "Unable to connect to the CreditLens API. "
            "Make sure the FastAPI server is running."
        )
        return

    except httpx.HTTPStatusError as error:
        st.error(
            "CreditLens API returned an error: "
            f"{error.response.status_code}"
        )
        return

    # ---------------------------------------------------------
    # Empty state
    # ---------------------------------------------------------

    if not applications:
        st.info(
            "No applications match the selected filters."
        )
        return

    # ---------------------------------------------------------
    # Application count
    # ---------------------------------------------------------

    st.write(
        f"Showing {len(applications)} application(s)"
    )

    st.divider()

    # ---------------------------------------------------------
    # Application list
    # ---------------------------------------------------------

    for application in applications:

        application_id = application["application_id"]

        with st.container(border=True):

            st.subheader(
                f"Application #{application_id}"
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.caption("Income")
                st.write(
                    f"₹{application['monthly_income']:,.0f}"
                )

            with col2:
                st.caption("Loan Amount")
                st.write(
                    f"₹{application['loan_amount']:,.0f}"
                )

            with col3:
                st.caption("Risk")
                st.write(
                    application["risk_level"]
                )

            with col4:
                st.caption("Decision")
                st.write(
                    application.get(
                        "decision",
                        "N/A",
                    )
                )

            if st.button(
                "View Assessment",
                key=f"view_{application_id}",
            ):
                st.session_state[
                    "selected_application_id"
                ] = application_id

                st.session_state[
                    "selected_application"
                ] = application

                st.rerun()

    # ---------------------------------------------------------
    # Selected application
    # ---------------------------------------------------------

    selected_application = st.session_state.get(
        "selected_application"
    )

    if selected_application is None:
        return

    st.divider()

    show_assessment(
        selected_application
    )

def show_assessment(
    application: dict,
):
    """Display a complete credit assessment."""

    st.title("Credit Assessment")

    st.caption(
        f"Application #{application['application_id']}"
    )

    st.divider()

    # ---------------------------------------------------------
    # Decision Summary
    # ---------------------------------------------------------

    decision = application.get("decision") or "N/A"
    risk_level = application.get("risk_level") or "N/A"

    if decision == "APPROVE":
        st.success(
            f"APPROVED — {risk_level} RISK"
        )

    elif decision == "MANUAL_REVIEW":
        st.warning(
            f"MANUAL REVIEW — {risk_level} RISK"
        )

    elif decision == "REJECT":
        st.error(
            f"REJECTED — {risk_level} RISK"
        )

    else:
        st.info(
            f"{decision} — {risk_level} RISK"
        )

    st.write(
        application.get(
            "decision_reason",
            "No decision reason available.",
        )
    )

    st.divider()

    # ---------------------------------------------------------
    # Financial Analysis
    # ---------------------------------------------------------

    st.subheader("Financial Analysis")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "FOIR",
            f"{application['foir']:.2f}%",
        )

    with col2:
        st.metric(
            "Monthly EMI",
            f"₹{application['emi']:,.2f}",
        )

    with col3:
        st.metric(
            "Total Obligations",
            f"₹{application['total_obligations']:,.2f}",
        )

    with col4:
        st.metric(
            "Remaining Income",
            f"₹{application['remaining_income']:,.2f}",
        )

    st.divider()

    # ---------------------------------------------------------
    # ML Risk Analysis
    # ---------------------------------------------------------

    st.subheader("ML Risk Analysis")

    default_probability = application.get(
        "default_probability"
    )

    if default_probability is not None:

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Default Probability",
                f"{default_probability * 100:.2f}%",
            )

        with col2:
            st.caption(
                "ML model output used as a risk signal "
                "by the underwriting layer."
            )

    ml_explanation = application.get(
        "ml_explanation",
        [],
    )

    if ml_explanation:

        st.write("Key Risk Drivers")

        for factor in ml_explanation:

            feature = factor.get(
                "feature",
                "Unknown feature",
            )

            contribution = factor.get(
                "contribution"
            )

            direction = factor.get(
                "direction",
                "",
            )

            if contribution is None:

                st.write(
                    f"**{feature}** — {direction}"
                )

                continue

            if contribution < 0:
                label = "Reduces default risk"

            elif contribution > 0:
                label = "Increases default risk"

            else:
                label = "Neutral"

            col1, col2, col3 = st.columns(
                [2, 1, 3]
            )

            with col1:
                st.write(
                    f"**{feature}**"
                )

            with col2:
                st.write(
                    f"{contribution:.2f}"
                )

            with col3:
                st.write(label)

    else:

        st.info(
            "No ML feature explanation is available."
        )

    st.divider()

    # ---------------------------------------------------------
    # AI Credit Analyst
    # ---------------------------------------------------------

    st.subheader("AI Credit Analyst")

    st.caption(
        "Gemini-generated analyst commentary grounded "
        "in the supplied assessment and retrieved policy evidence."
    )

    analyst_explanation = application.get(
        "analyst_explanation"
    )

    if analyst_explanation:

        st.markdown(
            analyst_explanation
        )

    else:

        st.info(
            "No AI analyst explanation is available."
        )

    st.divider()

    # ---------------------------------------------------------
    # Decision Trace
    # ---------------------------------------------------------

    decision_trace = application.get(
        "decision_trace"
    )

    if not decision_trace:
        return

    st.subheader("Decision Trace")

    # Applicant Data
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

    # Financial Analysis
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

    # Risk Analysis
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

    # Policy Evidence
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

    # Decision Logic
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

        st.write("Lending Decision")

        st.write(
            f"**Decision:** "
            f"{lending_decision.get('decision', 'N/A')}"
        )

        st.write(
            f"**Reason:** "
            f"{lending_decision.get('reason', 'N/A')}"
        )

def main():
    """Run the CreditLens Streamlit application."""

    client = CreditLensAPIClient()

    st.sidebar.title("CreditLens")

    st.sidebar.caption(
        "Credit Intelligence Platform"
    )

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "New Application",
            "Applications",
        ],
    )

    st.sidebar.divider()

    st.sidebar.caption(
        "Local CreditLens Environment"
    )

    if page == "Dashboard":
        show_dashboard(client)

    elif page == "New Application":
        show_new_application(client)

    elif page == "Applications":
        show_applications(client)


if __name__ == "__main__":
    main()