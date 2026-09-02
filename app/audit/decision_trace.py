from dataclasses import dataclass


@dataclass
class DecisionTrace:
    """
    Structured audit record for a CreditLens assessment.

    This object records the inputs, evidence, policy context,
    decision, and final explanation produced by the system.

    It does not calculate risk or make lending decisions.
    """

    applicant_data: dict

    financial_analysis: object

    risk_analysis: object

    policy_context: str

    rule_risk_level: str

    final_risk_level: str

    lending_decision: object

    analyst_explanation: str | None = None