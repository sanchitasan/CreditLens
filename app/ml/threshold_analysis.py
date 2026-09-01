import pandas as pd

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

from app.ml.preprocessing import prepare_data
from sklearn.linear_model import LogisticRegression


def main():
    print("CreditLens Threshold Analysis")
    print("=" * 40)

    # Load and prepare the same dataset used by the baseline model
    X_train, X_test, y_train, y_test = prepare_data()

    # Train the baseline Logistic Regression model
    model = LogisticRegression(max_iter=1000)

    model.fit(X_train, y_train)

    # Get probability of default
    default_probabilities = model.predict_proba(X_test)[:, 1]

    thresholds = [
        0.30,
        0.35,
        0.40,
        0.45,
        0.50,
        0.55,
        0.60,
        0.65,
        0.70,
    ]

    print()
    print("Threshold Analysis")
    print("=" * 40)

    print(
        f"{'Threshold':<12}"
        f"{'Precision':<12}"
        f"{'Recall':<12}"
        f"{'F1':<12}"
        f"{'FP':<8}"
        f"{'FN':<8}"
    )

    print("-" * 64)

    for threshold in thresholds:

        predictions = (
            default_probabilities >= threshold
        ).astype(int)

        precision = precision_score(
            y_test,
            predictions,
            zero_division=0,
        )

        recall = recall_score(
            y_test,
            predictions,
            zero_division=0,
        )

        f1 = f1_score(
            y_test,
            predictions,
            zero_division=0,
        )

        tn, fp, fn, tp = confusion_matrix(
            y_test,
            predictions,
        ).ravel()

        print(
            f"{threshold:<12.2f}"
            f"{precision:<12.3f}"
            f"{recall:<12.3f}"
            f"{f1:<12.3f}"
            f"{fp:<8}"
            f"{fn:<8}"
        )


if __name__ == "__main__":
    main()