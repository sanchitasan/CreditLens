from pathlib import Path

import joblib


MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "credit_risk_model.joblib"
)


def save_model(model):
    """
    Save the trained CreditLens model.
    """

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        model,
        MODEL_PATH,
    )


def load_model():
    """
    Load the trained CreditLens model.
    """

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)