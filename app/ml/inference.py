from app.ml.model_persistence import load_model
from app.ml.preprocessing import FEATURES


def predict_default_probability(features):
    """
    Load the trained credit-risk model
    and return default probability.
    """

    model = load_model()

    probabilities = model.predict_probability(
        [features]
    )

    return float(probabilities[0])


def explain_default_prediction(features):
    """
    Return feature-level contributions for
    the default prediction.
    """

    model = load_model()

    contributions = model.get_feature_contributions(
        [features],
        FEATURES,
    )

    return contributions