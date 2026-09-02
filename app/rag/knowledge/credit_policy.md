# CreditLens Lending Policy

## 1. Purpose

This policy defines the basic credit-risk guidelines used by CreditLens
for evaluating loan applications.

The policy is intended to support consistent and explainable credit
assessment.

## 2. FOIR Guidelines

Fixed Obligation to Income Ratio (FOIR) represents the applicant's
existing monthly obligations relative to monthly income.

FOIR is calculated as:

FOIR = Existing Monthly Obligations / Monthly Income × 100

General risk guidance:

- FOIR below 30%: Low financial obligation risk
- FOIR from 30% to 50%: Moderate financial obligation risk
- FOIR above 50%: High financial obligation risk

FOIR should not be considered in isolation. Other applicant and loan
characteristics should also be evaluated.

## 3. Credit Score Guidelines

Credit score is an important indicator of historical credit behaviour.

General guidance:

- Score of 750 or above: Strong credit profile
- Score from 650 to 749: Moderate credit profile
- Score below 650: Higher credit risk

Credit score should be considered together with income, obligations,
loan amount, employment history, and previous defaults.

## 4. Previous Defaults

Previous loan defaults are an important negative indicator.

Applicants with previous defaults should receive additional risk
assessment.

Multiple previous defaults may justify manual review or rejection,
depending on the overall risk profile.

## 5. ML Default Probability

CreditLens uses a machine-learning model to estimate the probability
of loan default.

The ML probability is an additional risk signal and should not
automatically determine the lending decision by itself.

The probability should be interpreted together with deterministic
financial rules and applicant information.

## 6. Lending Decisions

CreditLens supports three lending outcomes:

### APPROVE

Used when the overall applicant risk is within acceptable limits and
there are no significant risk indicators requiring further review.

### MANUAL_REVIEW

Used when the application contains meaningful risk indicators but
does not clearly justify automatic rejection.

### REJECT

Used when the overall risk is considered unacceptably high according
to the applicable assessment rules.

## 7. Explainability

Credit decisions should be explainable.

An explanation should identify the relevant financial or credit factors
that influenced the assessment.

ML predictions and analyst explanations should support the decision,
not replace the underlying financial assessment.

## 8. Policy Limitation

This document represents a simplified CreditLens demonstration
policy.

It is not a real financial institution's underwriting policy and
should not be treated as regulatory or lending advice.