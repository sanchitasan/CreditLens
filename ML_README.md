# CreditLens - Machine Learning Module

## Purpose

The Machine Learning module extends CreditLens from a rule-based credit
assessment system into a data-driven credit-risk prediction system.

The objective is to estimate the probability that a loan applicant will
default, using applicant financial and credit attributes.

This module is designed as an **employer-facing ML component**, not just
a model-training notebook.

------------------------------------------------------------------------

## Current Dataset

The generated dataset is stored as:

`data/credit_applications.csv`

Current dataset characteristics observed during EDA:

-   Rows: 10,000
-   Columns: 13
-   Target: `default`
-   Non-default applications: 7,768
-   Default applications: 2,232
-   Observed default rate: approximately 22.3%

### Main Features

  Feature                  Meaning
  ------------------------ -----------------------------------------------
  `monthly_income`         Applicant monthly income
  `existing_obligations`   Existing monthly financial obligations
  `loan_amount`            Requested loan amount
  `annual_interest_rate`   Annual interest rate
  `tenure_years`           Requested loan tenure
  `credit_score`           Applicant credit score
  `employment_years`       Employment stability
  `previous_defaults`      Number of previous defaults
  `foir`                   Fixed Obligation to Income Ratio
  `emi`                    Proposed monthly EMI
  `total_obligations`      Existing obligations + proposed EMI
  `remaining_income`       Income remaining after obligations
  `default`                Target variable: 0 = non-default, 1 = default

------------------------------------------------------------------------

## EDA Findings So Far

### 1. Class distribution

The dataset contains:

-   7,768 non-default records
-   2,232 default records

This means the target is **imbalanced but not extremely rare**. Accuracy
alone should therefore not be the primary model metric.

### 2. Credit score

Average credit score observed:

-   Non-default: \~705
-   Default: \~676

Lower credit scores are associated with a higher observed default rate.

### 3. FOIR

Observed default rate by FOIR band:

  FOIR        Default Rate
  --------- --------------
  `<20`             16.10%
  `20-30`           17.13%
  `30-40`           23.43%
  `40-50`           28.58%
  `50+`             35.69%

This shows a clear domain relationship: higher repayment burden is
associated with higher default risk.

### 4. Previous defaults

Observed default rate:

    Previous Defaults   Default Rate
  ------------------- --------------
                    0         20.21%
                    1         28.40%
                    2         39.11%
                    3         63.36%

Previous repayment problems are therefore a strong risk signal.

------------------------------------------------------------------------

## ML Roadmap

The ML development will proceed in controlled stages.

### Stage 1 --- EDA

-   Validate target distribution
-   Identify meaningful feature relationships
-   Check outliers
-   Check missing values
-   Check duplicate records
-   Study correlations
-   Detect suspicious or leakage-prone features

### Stage 2 --- Feature Engineering

Create features only when they represent information available at the
time of credit assessment.

Examples:

-   obligation-to-income ratios
-   loan-to-income ratio
-   EMI-to-income ratio
-   employment stability bands
-   previous-default indicators

Avoid features that are calculated using post-loan outcomes.

### Stage 3 --- Train/Test Split

Split the data before fitting transformations or models.

The test set must remain untouched until final evaluation.

For classification, use a **stratified split** so the
default/non-default proportion is preserved.

### Stage 4 --- Baseline Model

Start with **Logistic Regression**.

Why:

-   interpretable
-   strong baseline for binary classification
-   produces probabilities
-   coefficients can be inspected
-   suitable for credit-risk explanations

### Stage 5 --- Model Comparison

Compare the baseline with tree-based models such as:

-   Decision Tree
-   Random Forest
-   Gradient Boosting

The objective is not simply to maximize accuracy.

### Stage 6 --- Evaluation

Primary metrics:

-   ROC-AUC
-   Precision
-   Recall
-   F1-score
-   Confusion Matrix
-   PR-AUC when appropriate

For credit risk, **recall for the default class** is especially
important because missing a risky applicant can be more costly than
manually reviewing an applicant who turns out to be safe.

### Stage 7 --- Probability and Thresholding

The model should produce:

`P(default | applicant features)`

The final lending decision should not automatically equal:

`probability > 0.5`

Instead, the threshold should be selected according to business cost,
risk appetite, and operational capacity.

### Stage 8 --- Explainability

The final system should explain why an applicant received a high-risk
prediction.

Possible approaches:

-   Logistic Regression coefficients
-   permutation importance
-   SHAP for more advanced explainability

### Stage 9 --- Integration

The ML model will eventually connect to the existing CreditLens service
layer.

Target architecture:

`API → Application Service → Financial Feature Engineering → ML Risk Model → Risk Score → Lending Decision → Repository`

The existing deterministic credit calculations such as FOIR and EMI
remain valuable. ML should complement them rather than blindly replace
them.

### Stage 10 --- Production Readiness

Before deployment:

-   persist the model
-   version the model
-   validate input schema
-   monitor prediction distributions
-   monitor data drift
-   monitor model performance when labels become available
-   log model version and prediction metadata
-   protect against training/serving feature mismatch

------------------------------------------------------------------------

## Important ML Principles

### Avoid data leakage

Only use information available when the loan decision is made.

### Do not optimize only for accuracy

A model predicting every applicant as non-default can achieve high
accuracy on an imbalanced dataset while being useless for risk
management.

### Separate prediction from decision

The ML model predicts risk.

The lending policy decides:

-   APPROVE
-   MANUAL_REVIEW
-   REJECT

Keeping these responsibilities separate makes the system easier to audit
and change.

### Validate synthetic-data assumptions

This dataset is synthetic. Strong patterns in the generated data do not
automatically prove that the same relationships exist in real lending
portfolios.

------------------------------------------------------------------------

## Final ML Goal

CreditLens should evolve from:

`Rule-based credit assessment`

to:

`Rule-based financial analysis + ML default prediction + explainable lending decision`

and eventually into:

`Multi-agent AI credit underwriting platform`

The ML model is one component of the larger system, not the entire
system.
