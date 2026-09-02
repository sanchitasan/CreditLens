import httpx
import streamlit as st

from api_client import CreditLensAPIClient
from components.application_card import show_application_card
from components.assessment import show_assessment
from theme import render_page_header


def show_applications(client: CreditLensAPIClient):
    """Display previously assessed credit applications."""

    selected_application = st.session_state.get(
        "selected_application"
    )

    if selected_application is not None:

        if st.button("← Back to Applications"):

            st.session_state.pop(
                "selected_application",
                None,
            )

            st.rerun()

        st.divider()

        show_assessment(
            selected_application
        )

        return

    render_page_header(
        "Application History",
        "Review previously assessed credit applications.",
    )

    st.subheader("Filters")

    col1, col2 = st.columns(2)

    with col1:

        risk_filter = st.selectbox(
            "Risk Level",
            [
                "All",
                "LOW",
                "MEDIUM",
                "HIGH",
            ],
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
            f"CreditLens API returned an error: "
            f"{error.response.status_code}"
        )

        return

    if not applications:

        st.info(
            "No applications match the selected filters."
        )

        return

    st.write(
        f"Showing {len(applications)} application(s)"
    )

    st.divider()

    for application in applications:

        clicked = show_application_card(
            application,
            show_button=True,
        )

        if clicked:

            try:

                with st.spinner(
                    "Loading assessment..."
                ):

                    selected_application = (
                        client.get_application(
                            application[
                                "application_id"
                            ]
                        )
                    )

                st.session_state[
                    "selected_application"
                ] = selected_application

                st.rerun()

            except httpx.RequestError:

                st.error(
                    "Unable to connect to the CreditLens API."
                )

                return

            except httpx.HTTPStatusError as error:

                st.error(
                    "CreditLens API returned an error: "
                    f"{error.response.status_code}"
                )

                return