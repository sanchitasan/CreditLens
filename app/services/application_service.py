from app.finance.profile import FinancialProfile

from app.services.credit_assessment import (
    assess_credit,
)

from app.services.decision import (
    make_credit_decision,
)

from app.db.repository import (
    save_credit_application,
)

from app.services.exceptions import (
    CreditApplicationError,
)

from app.ml.inference import (
    predict_default_probability,explain_default_prediction,
)

from app.ml.explanation import (
    explain_prediction,
)

from app.services.underwriting import (
    combine_risk_assessment,
)

from app.llm.credit_analyst import (
    CreditAnalyst,
    CreditAnalystInput,
)

from app.llm.gemini_client import (
    GeminiClient,
)

def process_credit_application(
    profile: FinancialProfile,
    connection=None,
):
    """
    Complete credit application workflow.

    Steps:
    1. Validate applicant profile
    2. Perform credit assessment
    3. Determine lending decision
    4. Save application
    5. Return application ID, assessment and decision
    """

    # Step 1: Validate financial information
    profile.validate()

    # Step 2: Perform financial and risk assessment
    try:

        assessment = assess_credit(profile)

    except ValueError as error:

        raise CreditApplicationError(
            str(error)
        ) from error

    # Step 3: Generate ML default probability
    features = [
        profile.monthly_income,
        profile.existing_obligations,
        profile.loan_amount,
        profile.annual_interest_rate,
        profile.tenure_years,
        profile.credit_score,
        profile.employment_years,
        profile.previous_defaults,
    ]

    default_probability = predict_default_probability(
        features
    )

    # Generate feature-level ML explanation
    contributions = explain_default_prediction(
        features
    )

    ml_explanation = explain_prediction(
        contributions,
        top_n=3,
    )

    final_risk_level = combine_risk_assessment(
        assessment.risk_level,
        default_probability,
    )

    assessment.risk_level = final_risk_level
    assessment.default_probability = default_probability
    assessment.ml_explanation = ml_explanation

    # Step 5: Determine final lending decision
    lending_decision = make_credit_decision(
        assessment.risk_level,
        assessment.default_probability,
    )

    analyst_input = CreditAnalystInput(
        monthly_income=profile.monthly_income,
        existing_obligations=profile.existing_obligations,
        loan_amount=profile.loan_amount,
        annual_interest_rate=profile.annual_interest_rate,
        tenure_years=profile.tenure_years,
        credit_score=profile.credit_score,
        employment_years=profile.employment_years,
        previous_defaults=profile.previous_defaults,

        foir=assessment.foir,
        emi=assessment.emi,
        total_obligations=assessment.total_obligations,
        remaining_income=assessment.remaining_income,
        risk_level=assessment.risk_level,
        default_probability=assessment.default_probability,
        ml_explanation=assessment.ml_explanation,

        lending_decision=lending_decision.decision,
        decision_reason=lending_decision.reason,
    )

    analyst = CreditAnalyst(
        GeminiClient()
    )

    analyst_explanation = analyst.analyze(
        analyst_input
    )
    assessment.analyst_explanation = analyst_explanation

    # Step 6: Save application
    application_id = save_credit_application(
        profile,
        assessment,
        lending_decision,
        connection=connection,
    )

    # Step 7: Return complete result
    return (
        application_id,
        assessment,
        lending_decision,
    )