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

    # ML features
    credit_score: float = Field(
        default=650.0,
        ge=300,
        le=900,
        description="Applicant's credit score",
    )

    employment_years: float = Field(
        default=1.0,
        ge=0,
        description="Years of employment",
    )

    previous_defaults: int = Field(
        default=0,
        ge=0,
        description="Number of previous loan defaults",
    )


class CreditAssessmentResponse(BaseModel):

    foir: float
    emi: float
    total_obligations: float
    remaining_income: float
    risk_level: str

    # ML prediction
    default_probability: float
    ml_explanation: list[dict] = Field(default_factory=list)



class LendingDecisionResponse(BaseModel):

    decision: str
    reason: str


class LoanApplicationCreateResponse(BaseModel):

    application_id: int

    credit_assessment: CreditAssessmentResponse

    lending_decision: LendingDecisionResponse

    analyst_explanation: str | None = None


class LoanApplicationResponse(BaseModel):

    application_id: int

    # Applicant financial information
    monthly_income: float
    existing_obligations: float
    loan_amount: float
    annual_interest_rate: float
    tenure_years: float

    # ML input features
    # Optional because older database records may not contain them.
    credit_score: float | None = None
    employment_years: float | None = None
    previous_defaults: int | None = None

    # Credit assessment
    foir: float
    emi: float
    total_obligations: float
    remaining_income: float
    risk_level: str

    # ML output
    default_probability: float | None = None
    ml_explanation: list[dict] = Field(default_factory=list)
    analyst_explanation: str | None = None

    # Lending decision
    decision: str | None = None
    decision_reason: str | None = None

    decision_trace: DecisionTraceResponse | None = None

class DecisionTraceResponse(BaseModel):

    applicant_data: dict

    financial_analysis: dict

    risk_analysis: dict

    policy_context: str

    rule_risk_level: str

    final_risk_level: str

    lending_decision: dict

    analyst_explanation: str | None = None