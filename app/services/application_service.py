from app.finance.profile import FinancialProfile

from app.db.repository import (
    save_credit_application,
)

from app.services.exceptions import (
    CreditApplicationError,
)

from app.agents.factory import (
    create_creditlens_orchestrator,
)


def process_credit_application(
    profile: FinancialProfile,
    connection=None,
):
    """
    Complete credit application workflow.

    Steps:
    1. Validate applicant profile
    2. Run the multi-agent credit assessment
    3. Persist the assessment
    4. Return application ID, assessment and decision
    """

    # Step 1: Validate financial information
    try:
        profile.validate()

        # Step 2: Run complete multi-agent assessment
        orchestrator = create_creditlens_orchestrator()

        package = orchestrator.assess(profile)

    except ValueError as error:
        raise CreditApplicationError(
            str(error)
        ) from error

    # Step 3: Project the multi-agent package
    # into the existing persistence contract.
    assessment = package.financial_analysis

    assessment.default_probability = (
        package.risk_analysis.default_probability
    )

    assessment.ml_explanation = (
        package.risk_analysis.ml_explanation
    )

    assessment.analyst_explanation = (
        package.analyst_explanation
    )

    # The database's risk_level represents
    # the final risk level used for the decision.
    assessment.risk_level = (
        package.final_risk_level
    )

    lending_decision = (
        package.lending_decision
    )

    # Step 4: Save application
    application_id = save_credit_application(
        profile,
        assessment,
        lending_decision,
        decision_trace=package.decision_trace,
        connection=connection,
    )

    # Step 5: Return complete result
    return (
        application_id,
        assessment,
        lending_decision,
    )