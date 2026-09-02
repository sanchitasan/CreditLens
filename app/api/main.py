from fastapi import (
    Depends,
    FastAPI,
    HTTPException,

    Request,
    status,
    Query
)

from typing import Optional


from app.api.dependencies import get_db_connection

from fastapi.responses import JSONResponse
from app.services.exceptions import (
    CreditApplicationError,
)

from app.schemas.application import (
    LoanApplicationRequest,
    LoanApplicationCreateResponse,
    LoanApplicationResponse,
)

from app.finance.profile import FinancialProfile

from app.services.application_service import (
    process_credit_application,
)

from app.db.repository import (
    get_credit_application,
    list_credit_applications,
)


app = FastAPI(
    title="CreditLens API",
    description="Credit assessment and loan application API",
    version="1.0.0",
)

@app.exception_handler(CreditApplicationError)
async def credit_application_error_handler(
    request: Request,
    exc: CreditApplicationError,
):
    return JSONResponse(
        status_code=422,
        content={
            "error": "credit_application_error",
            "message": exc.message,
        },
    )

@app.exception_handler(Exception)
async def unexpected_error_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": (
                "An unexpected error occurred "
                "while processing the request."
            ),
        },
    )


@app.get("/")
def root():
    return {
        "message": "CreditLens API is running"
    }


@app.post(
    "/applications",
    response_model=LoanApplicationCreateResponse,
    status_code=status.HTTP_201_CREATED,)
def create_application(
    application: LoanApplicationRequest,
    connection=Depends(get_db_connection),
):
    profile = FinancialProfile(
        monthly_income=application.monthly_income,
        existing_obligations=application.existing_obligations,
        loan_amount=application.loan_amount,
        annual_interest_rate=application.annual_interest_rate,
        tenure_years=application.tenure_years,
        credit_score=application.credit_score,
        employment_years=application.employment_years,
        previous_defaults=application.previous_defaults,
    )

    (
        application_id,
        assessment,
        lending_decision,
    ) = process_credit_application(
        profile,
        connection=connection
    )

    return {
        "application_id": application_id,

        "credit_assessment": {
            "foir": assessment.foir,
            "emi": assessment.emi,
            "total_obligations": assessment.total_obligations,
            "remaining_income": assessment.remaining_income,
            "risk_level": assessment.risk_level,
            "default_probability": assessment.default_probability,
            "ml_explanation": assessment.ml_explanation,

        },

        "lending_decision": {
            "decision": lending_decision.decision,
            "reason": lending_decision.reason,
        },
        "analyst_explanation": assessment.analyst_explanation,
    }


@app.get(
    "/applications/{application_id}",
    response_model=LoanApplicationResponse,
)
def get_application(
        application_id: int,
        connection=Depends(get_db_connection)):

    application = get_credit_application(
        application_id,
        connection=connection
    )

    if application is None:

        raise HTTPException(
            status_code=404,
            detail="Credit application not found",
        )

    return LoanApplicationResponse(
        application_id=application["id"],

        monthly_income=application["monthly_income"],
        existing_obligations=application["existing_obligations"],
        loan_amount=application["loan_amount"],
        annual_interest_rate=application["annual_interest_rate"],
        tenure_years=application["tenure_years"],

        credit_score=application["credit_score"],
        employment_years=application["employment_years"],
        previous_defaults=application["previous_defaults"],

        foir=application["foir"],
        emi=application["emi"],
        total_obligations=application["total_obligations"],
        remaining_income=application["remaining_income"],
        risk_level=application["risk_level"],

        default_probability=application["default_probability"],
        ml_explanation=application["ml_explanation"],
        analyst_explanation=application["analyst_explanation"],

        decision=application["decision"],
        decision_reason=application["decision_reason"],

        decision_trace=application["decision_trace"],
    )


@app.get(
    "/applications",
    response_model=list[LoanApplicationResponse],
)
def get_applications(
    skip: int = Query(
        0,
        ge=0,
        description="Number of applications to skip",
    ),
    limit: int = Query(
        10,
        ge=1,
        le=100,
        description="Maximum number of applications to return",
    ),
    risk_level: Optional[str] = Query(
        None,
        description="Filter by risk level",
        pattern="^(LOW|MEDIUM|HIGH)$",
    ),
    decision: Optional[str] = Query(
        None,
        description="Filter by lending decision",
        pattern="^(APPROVE|MANUAL_REVIEW|REJECT)$",
    ),
    connection=Depends(get_db_connection),
):
    applications = list_credit_applications(
        connection=connection,
        skip=skip,
        limit=limit,
        risk_level=risk_level,
        decision=decision,
    )

    return [
        LoanApplicationResponse(
            application_id=application["id"],

            monthly_income=application["monthly_income"],
            existing_obligations=application["existing_obligations"],
            loan_amount=application["loan_amount"],
            annual_interest_rate=application["annual_interest_rate"],
            tenure_years=application["tenure_years"],

            credit_score=application["credit_score"],
            employment_years=application["employment_years"],
            previous_defaults=application["previous_defaults"],

            foir=application["foir"],
            emi=application["emi"],
            total_obligations=application["total_obligations"],
            remaining_income=application["remaining_income"],
            risk_level=application["risk_level"],

            default_probability=application["default_probability"],
            ml_explanation=application["ml_explanation"],
            analyst_explanation=application["analyst_explanation"],

            decision=application["decision"],
            decision_reason=application["decision_reason"],
            decision_trace=application["decision_trace"],
        )
        for application in applications
    ]