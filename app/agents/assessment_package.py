from dataclasses import dataclass


@dataclass
class CreditAssessmentPackage:
    financial_analysis: object
    risk_analysis: object
    policy_analysis: object
    lending_decision: object
    rule_risk_level: str
    final_risk_level: str
    analyst_explanation: str | None = None
