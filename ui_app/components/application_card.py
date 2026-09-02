import streamlit as st

from theme import COLORS, render_risk_badge


def show_application_card(
    application: dict,
    show_button: bool = False,
) -> bool:
    """
    Display a compact application summary.

    Returns True when the View Assessment button
    is clicked.
    """

    application_id = application[
        "application_id"
    ]

    with st.container(border=True):

        st.markdown(
            f"""
            <div style="
                font-family: 'Source Serif 4', serif;
                font-size: 1.1rem;
                font-weight: 600;
                color: {COLORS["ink"]};
                margin-bottom: 0.6rem;
            ">
                Application #{application_id}
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.caption("Income")

            st.markdown(
                f"""<span style="font-family:'IBM Plex Mono',monospace;
                color:{COLORS["ink"]};">
                ₹{application['monthly_income']:,.0f}
                </span>""",
                unsafe_allow_html=True,
            )

        with col2:

            st.caption("Loan amount")

            st.markdown(
                f"""<span style="font-family:'IBM Plex Mono',monospace;
                color:{COLORS["ink"]};">
                ₹{application['loan_amount']:,.0f}
                </span>""",
                unsafe_allow_html=True,
            )

        with col3:

            st.caption("Risk")

            render_risk_badge(
                application["risk_level"]
            )

        with col4:

            st.caption("Decision")

            decision = application.get(
                "decision",
                "N/A",
            )

            decision_color = {
                "APPROVE": COLORS["approve"],
                "MANUAL_REVIEW": COLORS["review"],
                "REJECT": COLORS["reject"],
            }.get(
                decision,
                COLORS["ink_soft"],
            )

            st.markdown(
                f"""<span style="font-family:'IBM Plex Mono',monospace;
                font-size: 0.85rem; font-weight: 500;
                color:{decision_color};">
                {decision}
                </span>""",
                unsafe_allow_html=True,
            )

        if show_button:

            return st.button(
                "View Assessment",
                key=f"view_{application_id}",
            )

    return False