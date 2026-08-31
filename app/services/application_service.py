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

    # Step 3: Convert risk level into lending decision
    lending_decision = make_credit_decision(
        assessment.risk_level
    )

    # Step 4: Save the financial assessment
    application_id = save_credit_application(
        profile,
        assessment,
        lending_decision,
        connection=connection,
    )

    # Step 5: Return complete result
    return (
        application_id,
        assessment,
        lending_decision,
    )