from dataclasses import dataclass
from typing import Any

from app.llm.llm_client import LLMClient


@dataclass
class CreditAnalystInput:
    """
    Structured information provided to the LLM Credit Analyst.

    These values come from CreditLens' existing
    deterministic and ML components.
    """

    monthly_income: float
    existing_obligations: float
    loan_amount: float
    annual_interest_rate: float
    tenure_years: float

    credit_score: float
    employment_years: float
    previous_defaults: int

    foir: float
    emi: float
    total_obligations: float
    remaining_income: float

    risk_level: str
    default_probability: float

    ml_explanation: list[dict[str, Any]]

    lending_decision: str
    decision_reason: str


def build_credit_analyst_prompt(
    application: CreditAnalystInput,
) -> str:
    """
    Build the prompt supplied to the Credit Analyst LLM.

    The LLM explains the supplied credit assessment.
    It does not calculate financial metrics or override
    the lending decision.
    """

    return f"""
You are a Credit Analyst working inside the CreditLens
lending decision-support system.

Your responsibility is to analyze and explain the
credit assessment produced by CreditLens.

IMPORTANT RULES:

1. Use only the information provided below.
2. Do not invent applicant information.
3. Do not recalculate EMI, FOIR, or default probability.
4. Treat the supplied financial calculations as authoritative.
5. Treat the ML default probability as an ML risk signal,
   not as a guaranteed prediction.
6. Do not override the lending decision produced by the
   existing CreditLens decision engine.
7. Clearly distinguish positive factors from risk factors.
8. Explain the assessment in professional lending language.
9. Do not make unsupported claims.
10. Mention uncertainty when appropriate.

APPLICANT INFORMATION

Monthly income: ₹{application.monthly_income:.0f}
Existing monthly obligations: ₹{application.existing_obligations:.0f}
Requested loan amount: ₹{application.loan_amount:.0f}
Annual interest rate: {application.annual_interest_rate:.0f}%
Loan tenure: {application.tenure_years:.0f} years
Credit score: {application.credit_score:.0f}
Employment history: {application.employment_years:.0f} years
Previous defaults: {application.previous_defaults}

CREDIT ASSESSMENT

FOIR: {application.foir:.2f}%
EMI: ₹{application.emi:,.2f}
Total obligations: ₹{application.total_obligations:,.2f}
Remaining income: ₹{application.remaining_income:,.2f}

Rule-based risk level: {application.risk_level}

ML default probability:
{application.default_probability:.4f}

ML EXPLANATION

{application.ml_explanation}

LENDING DECISION

Decision: {application.lending_decision}

Decision reason:
{application.decision_reason}

TASK

Provide a concise credit analyst assessment containing:

1. Overall assessment
2. Positive factors
3. Risk factors
4. Explanation of the ML risk signal
5. Decision context
6. Important limitations or uncertainty

Do not introduce any information that is not present
in the supplied application data.
""".strip()


class CreditAnalyst:
    """
    Credit Analyst responsible for generating
    a human-readable explanation of an existing
    credit assessment.

    The analyst does not calculate financial metrics
    and does not make the lending decision.
    """

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    def analyze(
        self,
        application: CreditAnalystInput,
    ) -> str:
        """
        Generate a credit analyst explanation
        using the configured LLM client.
        """

        prompt = build_credit_analyst_prompt(
            application
        )

        return self.llm_client.generate(prompt)