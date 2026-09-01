from app.ml.inference import predict_default_probability


class FakeModel:

    def predict_probability(self, features):
        return [0.72]


def test_predict_default_probability(monkeypatch):

    monkeypatch.setattr(
        "app.ml.inference.load_model",
        lambda: FakeModel(),
    )

    features = [
        80000,
        20000,
        500000,
        12,
        5,
        750,
        4,
        0,
    ]

    probability = predict_default_probability(
        features
    )

    assert probability == 0.72
    assert 0 <= probability <= 1