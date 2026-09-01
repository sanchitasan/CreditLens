import numpy as np

from app.ml.model import CreditRiskModel


def test_feature_contributions():

    X_train = np.array([
        [80000, 20000, 500000, 12, 5, 750, 4, 0],
        [40000, 30000, 900000, 18, 7, 600, 1, 2],
        [90000, 10000, 300000, 10, 5, 800, 8, 0],
        [50000, 25000, 700000, 15, 6, 650, 2, 1],
    ])

    y_train = np.array([
        0,
        1,
        0,
        1,
    ])

    feature_names = [
        "monthly_income",
        "existing_obligations",
        "loan_amount",
        "annual_interest_rate",
        "tenure_years",
        "credit_score",
        "employment_years",
        "previous_defaults",
    ]

    model = CreditRiskModel()

    model.train(
        X_train,
        y_train,
    )

    X_applicant = np.array([
        [
            80000,
            20000,
            500000,
            12,
            5,
            750,
            4,
            0,
        ]
    ])

    contributions = model.get_feature_contributions(
        X_applicant,
        feature_names,
    )

    assert len(contributions) == 8

    assert "loan_amount" in contributions

    assert "credit_score" in contributions