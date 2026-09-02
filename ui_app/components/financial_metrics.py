import streamlit as st


def show_financial_metrics(
    application: dict,
):
    """Display deterministic financial analysis."""

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