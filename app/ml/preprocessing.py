from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Dataset location
DATA_PATH = PROJECT_ROOT / "data" / "credit_applications.csv"


# Features available to the ML model at application time.
FEATURES = [
    "monthly_income",
    "existing_obligations",
    "loan_amount",
    "annual_interest_rate",
    "tenure_years",
    "credit_score",
    "employment_years",
    "previous_defaults",
]

TARGET = "default"


def load_dataset() -> pd.DataFrame:
    """
    Load the CreditLens ML dataset.
    """

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    return df


def prepare_data():
    """
    Prepare features and target and perform a stratified
    train/test split.
    """

    df = load_dataset()

    # Verify that required columns exist.
    required_columns = FEATURES + [TARGET]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Select only the features we want for the baseline model.
    X = df[FEATURES]

    # Target variable.
    y = df[TARGET]

    # Stratified split preserves the default/non-default ratio.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    return X_train, X_test, y_train, y_test


def main():
    """
    Run the preprocessing stage and display basic information.
    """

    X_train, X_test, y_train, y_test = prepare_data()

    print("CreditLens ML Data Preparation")
    print("=" * 40)

    print("\nFeatures:")
    for feature in FEATURES:
        print(f"- {feature}")

    print("\nTarget:")
    print(f"- {TARGET}")

    print("\nTraining shape:")
    print(X_train.shape)

    print("\nTesting shape:")
    print(X_test.shape)

    print("\nTraining target distribution:")
    print(y_train.value_counts())
    print(y_train.value_counts(normalize=True))

    print("\nTesting target distribution:")
    print(y_test.value_counts())
    print(y_test.value_counts(normalize=True))


if __name__ == "__main__":
    main()