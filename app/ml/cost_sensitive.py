import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

from app.ml.preprocessing import prepare_data


def evaluate_costs(
    y_true,
    probabilities,
    fn_cost,
    fp_cost,
):
    """
    Evaluate different probability thresholds
    using business costs for false negatives
    and false positives.
    """

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

    results = []

    for threshold in thresholds:

        predictions = (
            probabilities >= threshold
        ).astype(int)

        tn, fp, fn, tp = confusion_matrix(
            y_true,
            predictions,
        ).ravel()

        total_cost = (
            fn * fn_cost
            + fp * fp_cost
        )

        results.append(
            {
                "threshold": threshold,
                "false_positives": fp,
                "false_negatives": fn,
                "precision": (
                    tp / (tp + fp)
                    if (tp + fp) > 0
                    else 0
                ),
                "recall": (
                    tp / (tp + fn)
                    if (tp + fn) > 0
                    else 0
                ),
                "total_cost": total_cost,
            }
        )

    return pd.DataFrame(results)


def main():

    print("CreditLens Cost-Sensitive Threshold Analysis")
    print("=" * 50)

    X_train, X_test, y_train, y_test = (
        prepare_data()
    )

    model = LogisticRegression(
        max_iter=1000
    )

    model.fit(
        X_train,
        y_train,
    )

    probabilities = model.predict_proba(
        X_test
    )[:, 1]

    scenarios = {
        "Risk-Sensitive": {
            "fn_cost": 10,
            "fp_cost": 1,
        },
        "Balanced": {
            "fn_cost": 5,
            "fp_cost": 1,
        },
        "Customer-Friendly": {
            "fn_cost": 2,
            "fp_cost": 1,
        },
    }

    for scenario_name, costs in scenarios.items():

        print()
        print(scenario_name)
        print("-" * 50)

        results = evaluate_costs(
            y_true=y_test,
            probabilities=probabilities,
            fn_cost=costs["fn_cost"],
            fp_cost=costs["fp_cost"],
        )

        print(
            f"{'Threshold':<12}"
            f"{'FP':<8}"
            f"{'FN':<8}"
            f"{'Precision':<12}"
            f"{'Recall':<10}"
            f"{'Cost':<10}"
        )

        print("-" * 60)

        for _, row in results.iterrows():

            print(
                f"{row['threshold']:<12.2f}"
                f"{int(row['false_positives']):<8}"
                f"{int(row['false_negatives']):<8}"
                f"{row['precision']:<12.3f}"
                f"{row['recall']:<10.3f}"
                f"{row['total_cost']:<10.0f}"
            )

        best_row = results.loc[
            results["total_cost"].idxmin()
        ]

        print()
        print("Recommended Threshold:")
        print(
            f"{best_row['threshold']:.2f}"
        )

        print(
            f"Minimum Business Cost: "
            f"{best_row['total_cost']:.0f}"
        )


if __name__ == "__main__":
    main()