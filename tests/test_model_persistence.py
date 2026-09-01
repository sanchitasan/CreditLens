from app.ml.model import CreditRiskModel
from app.ml.model_persistence import save_model, load_model


def test_model_can_be_saved_and_loaded(tmp_path, monkeypatch):

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

    test_model_path = (
        tmp_path / "test_model.joblib"
    )

    monkeypatch.setattr(
        "app.ml.model_persistence.MODEL_PATH",
        test_model_path,
    )

    save_model(model)

    loaded_model = load_model()

    probabilities = (
        loaded_model.predict_probability(
            X_train
        )
    )

    assert len(probabilities) == 4

    assert all(
        0 <= probability <= 1
        for probability in probabilities
    )