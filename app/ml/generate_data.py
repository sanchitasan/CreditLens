import os

import numpy as np
import pandas as pd


RANDOM_SEED = 42
NUMBER_OF_APPLICATIONS = 10000


def generate_credit_dataset(
    number_of_applications=NUMBER_OF_APPLICATIONS,
    random_seed=RANDOM_SEED,
):
    """
    Generate a synthetic historical credit dataset.

    The dataset simulates loan applications and whether
    the applicant eventually defaulted.
    """

    rng = np.random.default_rng(random_seed)

    # ---------------------------------------------------------
    # Basic applicant financial information
    # ---------------------------------------------------------

    monthly_income = rng.lognormal(
        mean=np.log(60000),
        sigma=0.45,
        size=number_of_applications,
    )

    monthly_income = np.clip(
        monthly_income,
        20000,
        500000,
    )

    existing_obligations = (
        monthly_income
        * rng.uniform(
            0.05,
            0.55,
            size=number_of_applications,
        )
    )

    loan_amount = rng.uniform(
        100000,
        2000000,
        size=number_of_applications,
    )

    annual_interest_rate = rng.uniform(
        8,
        20,
        size=number_of_applications,
    )

    tenure_years = rng.integers(
        1,
        8,
        size=number_of_applications,
    )

    # ---------------------------------------------------------
    # Credit history
    # ---------------------------------------------------------

    credit_score = np.clip(
        rng.normal(
            loc=700,
            scale=70,
            size=number_of_applications,
        ),
        300,
        850,
    )

    employment_years = np.clip(
        rng.exponential(
            scale=5,
            size=number_of_applications,
        ),
        0,
        40,
    )

    previous_defaults = rng.poisson(
        lam=0.25,
        size=number_of_applications,
    )

    previous_defaults = np.clip(
        previous_defaults,
        0,
        5,
    )

    # ---------------------------------------------------------
    # EMI calculation
    # ---------------------------------------------------------

    monthly_rate = annual_interest_rate / 12 / 100

    number_of_payments = tenure_years * 12

    emi = np.where(
        monthly_rate == 0,
        loan_amount / number_of_payments,
        loan_amount
        * monthly_rate
        * (1 + monthly_rate) ** number_of_payments
        / (
            (1 + monthly_rate) ** number_of_payments
            - 1
        ),
    )

    # ---------------------------------------------------------
    # Derived financial features
    # ---------------------------------------------------------

    foir = (
        existing_obligations
        / monthly_income
        * 100
    )

    total_obligations = (
        existing_obligations + emi
    )

    remaining_income = (
        monthly_income
        - total_obligations
    )

    # ---------------------------------------------------------
    # Synthetic default probability
    # ---------------------------------------------------------
    #
    # This is intentionally probabilistic.
    #
    # Lower credit score       -> higher risk
    # Higher FOIR              -> higher risk
    # Previous defaults        -> higher risk
    # Lower employment history -> higher risk
    #
    # We also add random noise so the target is
    # not perfectly predictable.
    # ---------------------------------------------------------

    risk_signal = (
        -2.5
        + 0.035 * (foir - 30)
        + 0.008 * (650 - credit_score)
        + 0.65 * previous_defaults
        - 0.04 * employment_years
        + 0.000002 * (
            loan_amount - 500000
        )
    )

    noise = rng.normal(
        0,
        0.8,
        size=number_of_applications,
    )

    risk_signal = risk_signal + noise

    default_probability = (
        1
        / (
            1 + np.exp(-risk_signal)
        )
    )

    default = rng.binomial(
        1,
        default_probability,
    )

    # ---------------------------------------------------------
    # Build DataFrame
    # ---------------------------------------------------------

    dataset = pd.DataFrame(
        {
            "monthly_income": monthly_income,
            "existing_obligations": existing_obligations,
            "loan_amount": loan_amount,
            "annual_interest_rate": annual_interest_rate,
            "tenure_years": tenure_years,
            "credit_score": credit_score,
            "employment_years": employment_years,
            "previous_defaults": previous_defaults,
            "foir": foir,
            "emi": emi,
            "total_obligations": total_obligations,
            "remaining_income": remaining_income,
            "default": default,
        }
    )

    return dataset


def main():
    """
    Generate and save the synthetic dataset.
    """

    dataset = generate_credit_dataset()

    os.makedirs(
        "data",
        exist_ok=True,
    )

    output_path = (
        "data/credit_applications.csv"
    )

    dataset.to_csv(
        output_path,
        index=False,
    )

    print(
        f"Dataset created successfully: "
        f"{output_path}"
    )

    print(
        f"Rows: {len(dataset)}"
    )

    print(
        f"Columns: {len(dataset.columns)}"
    )

    print("\nDefault distribution:")

    print(
        dataset["default"].value_counts(
            normalize=True
        )
    )

    print("\nDataset preview:")

    print(
        dataset.head()
    )


if __name__ == "__main__":
    main()