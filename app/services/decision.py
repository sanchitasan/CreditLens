from dataclasses import dataclass


@dataclass
class CreditDecision:

    foir: float
    emi: float
    total_obligations: float
    remaining_income: float
    risk_level: str
    risk_reasons: list[str]
    default_probability: float = 0.0
    ml_explanation: list[dict] = None
    analyst_explanation: str | None = None

@dataclass
class LendingDecision:
    decision: str
    reason: str

def make_credit_decision(risk_level: str,default_probability=0.0, ml_explanation=None) -> LendingDecision:

    if risk_level == "LOW":
        return LendingDecision(
            decision="APPROVE",
            reason="Applicant has low credit risk.",
        )

    if risk_level == "MEDIUM":
        return LendingDecision(
            decision="MANUAL_REVIEW",
            reason="Applicant requires additional review.",
        )

    if risk_level == "HIGH":
        return LendingDecision(
            decision="REJECT",
            reason="Applicant has high credit risk.",
        )

    raise ValueError(f"Unknown risk level: {risk_level}")