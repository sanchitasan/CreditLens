def explain_prediction(
    contributions: dict,
    top_n: int = 3,
):
    """
    Explain an ML prediction using the strongest
    feature contributions.

    Positive contribution:
        pushes the model toward default.

    Negative contribution:
        pushes the model away from default.
    """

    sorted_contributions = sorted(
        contributions.items(),
        key=lambda item: abs(item[1]),
        reverse=True,
    )

    top_features = sorted_contributions[:top_n]

    explanation = []

    for feature, contribution in top_features:

        if contribution > 0:
            direction = "increases default risk"
        else:
            direction = "reduces default risk"

        explanation.append(
            {
                "feature": feature,
                "contribution": round(
                    float(contribution),
                    4,
                ),
                "direction": direction,
            }
        )

    return explanation