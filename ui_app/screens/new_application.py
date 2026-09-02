import httpx
import streamlit as st

from api_client import CreditLensAPIClient
from components.assessment import show_assessment
from theme import render_page_header


def show_new_application(client: CreditLensAPIClient):
    """Display and process a new credit application."""

    render_page_header(
        "New Credit Application",
        "Create and assess a new lending application.",
    )

    with st.form("credit_application_form"):

        st.subheader(
            "Applicant Financial Information"
        )

        col1, col2 = st.columns(2)

        with col1:

            monthly_income = st.number_input(
                "Monthly Income",
                min_value=1.0,
                value=50000.0,
                step=5000.0,
            )

            existing_obligations = st.number_input(
                "Existing Monthly Obligations",
                min_value=0.0,
                value=0.0,
                step=1000.0,
            )

            loan_amount = st.number_input(
                "Loan Amount",
                min_value=1.0,
                value=500000.0,
                step=50000.0,
            )

            annual_interest_rate = st.number_input(
                "Annual Interest Rate (%)",
                min_value=0.01,
                max_value=50.0,
                value=12.0,
                step=0.5,
            )

        with col2:

            tenure_years = st.number_input(
                "Loan Tenure (Years)",
                min_value=0.1,
                max_value=30.0,
                value=5.0,
                step=1.0,
            )

            credit_score = st.number_input(
                "Credit Score",
                min_value=300.0,
                max_value=900.0,
                value=650.0,
                step=10.0,
            )

            employment_years = st.number_input(
                "Employment Experience (Years)",
                min_value=0.0,
                value=1.0,
                step=0.5,
            )

            previous_defaults = st.number_input(
                "Previous Defaults",
                min_value=0,
                value=0,
                step=1,
            )

        submitted = st.form_submit_button(
            "Assess Credit Application",
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

    try:

        with st.spinner(
            "Assessing credit application..."
        ):

            response = client.create_application(
                payload
            )

            application_id = response[
                "application_id"
            ]

            application = client.get_application(
                application_id
            )

        st.session_state[
            "assessment"
        ] = application

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

    show_assessment(application)