from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from app.ml.preprocessing import prepare_data


def build_model():
    """
    Build the baseline Logistic Regression model.

    StandardScaler is fitted only on the training data
    through the sklearn Pipeline.
    """

    model = Pipeline(
        steps=[
            (
                "scaler",
                StandardScaler(),
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    random_state=42,
                ),
            ),
        ]
    )

    return model


def train_model():
    """
    Train the Logistic Regression baseline.
    """

    X_train, X_test, y_train, y_test = prepare_data()

    model = build_model()

    model.fit(
        X_train,
        y_train,
    )

    return model, X_train, X_test, y_train, y_test


def evaluate_model(
    model,
    X_test,
    y_test,
):
    """
    Evaluate the trained model.
    """

    predictions = model.predict(X_test)

    probabilities = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    roc_auc = roc_auc_score(
        y_test,
        probabilities,
    )

    matrix = confusion_matrix(
        y_test,
        predictions,
    )

    print("\nModel Evaluation")
    print("=" * 40)

    print(f"\nAccuracy: {accuracy:.4f}")

    print(f"ROC-AUC: {roc_auc:.4f}")

    print("\nConfusion Matrix:")
    print(matrix)

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            target_names=[
                "Non-default",
                "Default",
            ],
        )
    )

    return {
        "accuracy": accuracy,
        "roc_auc": roc_auc,
        "confusion_matrix": matrix,
    }


def inspect_coefficients(model):
    """
    Display Logistic Regression coefficients.

    Positive coefficient:
        increases predicted default probability.

    Negative coefficient:
        decreases predicted default probability.
    """

    classifier = model.named_steps["classifier"]

    feature_names = model.named_steps[
        "scaler"
    ].feature_names_in_

    coefficients = classifier.coef_[0]

    print("\nFeature Coefficients")
    print("=" * 40)

    for feature, coefficient in sorted(
        zip(feature_names, coefficients),
        key=lambda item: abs(item[1]),
        reverse=True,
    ):
        print(
            f"{feature:25s} {coefficient:+.4f}"
        )


def main():
    """
    Train and evaluate the CreditLens
    Logistic Regression baseline.
    """

    model, X_train, X_test, y_train, y_test = train_model()

    print("CreditLens ML Baseline")
    print("=" * 40)

    print(f"\nTraining rows: {len(X_train)}")
    print(f"Testing rows: {len(X_test)}")

    evaluate_model(
        model,
        X_test,
        y_test,
    )

    inspect_coefficients(model)


if __name__ == "__main__":
    main()