from pydantic import BaseModel, Field


class LoanApplicationRequest(BaseModel):

    monthly_income: float = Field(
        gt=0,
        description="Applicant's monthly income in INR",
    )

    existing_obligations: float = Field(
        ge=0,
        description="Existing monthly debt obligations in INR",
    )

    loan_amount: float = Field(
        gt=0,
        description="Requested loan amount in INR",
    )

    annual_interest_rate: float = Field(
        gt=0,
        le=50,
        description="Annual interest rate as a percentage",
    )

    tenure_years: float = Field(
        gt=0,
        le=30,
        description="Loan tenure in years",
    )


class CreditAssessmentResponse(BaseModel):
    foir: float
    emi: float
    total_obligations: float
    remaining_income: float
    risk_level: str


class LendingDecisionResponse(BaseModel):
    decision: str
    reason: str


class LoanApplicationCreateResponse(BaseModel):
    application_id: int
    credit_assessment: CreditAssessmentResponse
    lending_decision: LendingDecisionResponse


class LoanApplicationResponse(BaseModel):
    application_id: int

    monthly_income: float
    existing_obligations: float
    loan_amount: float
    annual_interest_rate: float
    tenure_years: float

    foir: float
    emi: float
    total_obligations: float
    remaining_income: float
    risk_level: str

    decision: str | None = None
    decision_reason: str | None = None


class CreditAssessmentResponse(BaseModel):
    foir: float
    emi: float
    total_obligations: float
    remaining_income: float
    risk_level: str


class LendingDecisionResponse(BaseModel):
    decision: str
    reason: str


class LoanApplicationCreateResponse(BaseModel):
    application_id: int
    credit_assessment: CreditAssessmentResponse
    lending_decision: LendingDecisionResponse


class LoanApplicationResponse(BaseModel):
    application_id: int

    monthly_income: float
    existing_obligations: float
    loan_amount: float
    annual_interest_rate: float
    tenure_years: float

    foir: float
    emi: float
    total_obligations: float
    remaining_income: float
    risk_level: str

    decision: str | None = None
    decision_reason: str | None = None