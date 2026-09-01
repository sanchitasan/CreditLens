from app.ml.model import CreditRiskModel


def test_credit_risk_model_training():

    X_train = [
        [100000, 10000],
        [30000, 20000],
        [90000, 5000],
        [25000, 25000],
    ]

    y_train = [
        0,
        1,
        0,
        1,
    ]

    model = CreditRiskModel()

    model.train(
        X_train,
        y_train,
    )

    probabilities = model.predict_probability(
        X_train
    )

    assert len(probabilities) == 4

    assert all(
        0 <= probability <= 1
        for probability in probabilities
    )


def test_credit_risk_model_prediction():

    X_train = [
        [100000, 10000],
        [30000, 20000],
        [90000, 5000],
        [25000, 25000],
    ]

    y_train = [
        0,
        1,
        0,
        1,
    ]

    model = CreditRiskModel()

    model.train(
        X_train,
        y_train,
    )

    predictions = model.predict(
        X_train,
        threshold=0.50,
    )

    assert len(predictions) == 4

    assert all(
        prediction in [0, 1]
        for prediction in predictions
    )