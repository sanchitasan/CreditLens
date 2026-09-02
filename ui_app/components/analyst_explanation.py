import streamlit as st


def show_analyst_explanation(
    application: dict,
):
    """Display Gemini-generated analyst commentary."""

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