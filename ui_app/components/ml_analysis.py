import streamlit as st


def show_ml_analysis(
    application: dict,
):
    """Display ML default-risk analysis."""

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

    if not ml_explanation:

        st.info(
            "No ML feature explanation is available."
        )

        return

    st.write(
        "Key Risk Drivers"
    )

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