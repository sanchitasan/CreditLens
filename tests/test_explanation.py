from app.ml.explanation import explain_prediction


def test_explain_prediction():

    contributions = {
        "loan_amount": 1.02,
        "existing_obligations": 0.52,
        "credit_score": -0.51,
        "monthly_income": -0.44,
    }

    explanation = explain_prediction(
        contributions,
        top_n=3,
    )

    assert len(explanation) == 3

    assert explanation[0]["feature"] == "loan_amount"

    assert (
        explanation[0]["direction"]
        == "increases default risk"
    )

    assert (
        explanation[2]["direction"]
        == "reduces default risk"
    )