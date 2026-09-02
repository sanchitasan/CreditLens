import httpx
import streamlit as st

from api_client import CreditLensAPIClient
from components.application_card import show_application_card
from theme import render_page_header


def show_dashboard(client: CreditLensAPIClient):
    """Display the CreditLens dashboard."""

    render_page_header(
        "CreditLens",
        "AI-Powered Credit Underwriting & Risk Intelligence Platform",
    )

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
        show_application_card(
            application,
            show_button=False,
        )