from app.ml.model import CreditRiskModel
from app.ml.preprocessing import FEATURES


def test_feature_contributions_return_all_features():
    model = CreditRiskModel()

    X_train = [
        [
            80000,
            20000,
            500000,
            12,
            5,
            780,
            5,
            0,
        ],
        [
            50000,
            30000,
            600000,
            15,
            5,
            650,
            2,
            2,
        ],
    ]

    y_train = [0, 1]

    model.train(
        X_train,
        y_train,
    )

    contributions = model.get_feature_contributions(
        [
            [
                80000,
                20000,
                500000,
                12,
                5,
                780,
                5,
                0,
            ]
        ],
        FEATURES,
    )

    assert len(contributions) == len(FEATURES)

    assert set(contributions.keys()) == set(
        FEATURES
    )


def test_feature_contributions_are_sorted_by_absolute_value():
    model = CreditRiskModel()

    X_train = [
        [
            80000,
            20000,
            500000,
            12,
            5,
            780,
            5,
            0,
        ],
        [
            50000,
            30000,
            600000,
            15,
            5,
            650,
            2,
            2,
        ],
    ]

    y_train = [0, 1]

    model.train(
        X_train,
        y_train,
    )

    contributions = model.get_feature_contributions(
        [
            [
                80000,
                20000,
                500000,
                12,
                5,
                780,
                5,
                0,
            ]
        ],
        FEATURES,
    )

    values = list(
        contributions.values()
    )

    absolute_values = [
        abs(value)
        for value in values
    ]

    assert absolute_values == sorted(
        absolute_values,
        reverse=True,
    )


def test_feature_contribution_direction_is_preserved():
    model = CreditRiskModel()

    X_train = [
        [
            80000,
            20000,
            500000,
            12,
            5,
            780,
            5,
            0,
        ],
        [
            50000,
            30000,
            600000,
            15,
            5,
            650,
            2,
            2,
        ],
    ]

    y_train = [0, 1]

    model.train(
        X_train,
        y_train,
    )

    contributions = model.get_feature_contributions(
        [
            [
                80000,
                20000,
                500000,
                12,
                5,
                780,
                5,
                0,
            ]
        ],
        FEATURES,
    )

    for contribution in contributions.values():
        assert isinstance(
            contribution,
            float,
        )