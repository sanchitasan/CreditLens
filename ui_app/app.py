import streamlit as st

from api_client import CreditLensAPIClient
from screens.dashboard import show_dashboard
from screens.new_application import show_new_application
from screens.applications import show_applications
from theme import apply_theme, render_sidebar


st.set_page_config(
    page_title="CreditLens",
    page_icon="💳",
    layout="wide",
)


def main():
    apply_theme()

    page = render_sidebar()

    client = CreditLensAPIClient()

    if page == "Dashboard":
        show_dashboard(client)

    elif page == "New Application":
        show_new_application(client)

    elif page == "Applications":
        show_applications(client)


if __name__ == "__main__":
    main()