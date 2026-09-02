from types import SimpleNamespace
from app.finance.profile import FinancialProfile
import app.agents.orchestrator as orchestrator_module
from app.agents.financial_analyst_agent import (
    FinancialAnalysis,
)
from app.agents.policy_analyst_agent import (
    PolicyAnalysis,
)
from app.agents.risk_analyst_agent import (
    RiskAnalysis,
)
from app.agents.orchestrator import CreditLensOrchestrator
from app.finance.profile import FinancialProfile

from app.agents.final_credit_analyst_agent import (
    FinalCreditAnalystInput,
    FinalCreditAnalystOutput,
)


class FakeFinancialAgent:

    def __init__(self):
        self.received_profile = None

    def analyze(self, agent_input):

        self.received_profile = agent_input.profile

        return FinancialAnalysis(
            foir=25.0,
            emi=11122.22,
            total_obligations=31122.22,
            remaining_income=48877.78,
            risk_level="LOW",
            risk_reasons=[
                "Applicant passes basic financial rules"
            ],
        )


class FakeRiskAgent:

    def __init__(self):
        self.received_profile = None

    def analyze(self, agent_input):

        self.received_profile = agent_input.profile

        return RiskAnalysis(
            default_probability=0.03,
            ml_explanation=[
                {
                    "feature": "credit_score",
                    "contribution": -3.9,
                    "direction": "reduces default risk",
                }
            ],
        )


class FakePolicyAgent:

    def __init__(self):
        self.received = None

    def analyze(self, agent_input):

        self.received = agent_input

        return PolicyAnalysis(
            policy_context="Retrieved policy context."
        )

class FakeFinalAnalystAgent:
    def __init__(self):
        self.received_input = None

    def analyze(self, agent_input):
        self.received_input = agent_input

        return FinalCreditAnalystOutput(
            analyst_explanation="Final analyst explanation."
        )


def create_profile():

    return FinancialProfile(
        monthly_income=80000,
        existing_obligations=20000,
        loan_amount=500000,
        annual_interest_rate=12,
        tenure_years=5,
        credit_score=780,
        employment_years=5,
        previous_defaults=0,
    )

def build_profile():
    return FinancialProfile(
        monthly_income=80000,
        existing_obligations=20000,
        loan_amount=500000,
        annual_interest_rate=12,
        tenure_years=5,
        credit_score=780,
        employment_years=5,
        previous_defaults=0,
    )


def test_orchestrator_coordinates_all_agents(
    monkeypatch,
):

    financial_agent = FakeFinancialAgent()
    risk_agent = FakeRiskAgent()
    policy_agent = FakePolicyAgent()

    expected_decision = SimpleNamespace(
        decision="APPROVE",
        reason="Applicant has low credit risk.",
        risk_level="LOW",
    )

    received_decision_arguments = {}

    def fake_lending_decision_tool(
        profile,
        default_probability,
    ):

        received_decision_arguments[
            "profile"
        ] = profile

        received_decision_arguments[
            "default_probability"
        ] = default_probability

        return expected_decision

    monkeypatch.setattr(
        orchestrator_module,
        "lending_decision_tool",
        fake_lending_decision_tool,
    )

    final_analyst = FakeFinalAnalystAgent()

    orchestrator = CreditLensOrchestrator(
        financial_agent=financial_agent,
        risk_agent=risk_agent,
        policy_agent=policy_agent,
        final_analyst_agent=final_analyst,
    )

    profile = create_profile()

    result = orchestrator.assess(profile)

    # Financial agent received correct profile
    assert financial_agent.received_profile == profile

    # Risk agent received correct profile
    assert risk_agent.received_profile == profile

    # Decision received ML probability
    assert (
        received_decision_arguments[
            "profile"
        ]
        == profile
    )

    assert (
        received_decision_arguments[
            "default_probability"
        ]
        == 0.03
    )

    # Policy agent received actual decision
    assert policy_agent.received is not None

    assert policy_agent.received.foir == 25.0
    assert policy_agent.received.credit_score == 780
    assert policy_agent.received.previous_defaults == 0
    assert (
        policy_agent.received.default_probability
        == 0.03
    )
    assert (
        policy_agent.received.lending_decision
        == "APPROVE"
    )

    # Final package
    assert result.financial_analysis.foir == 25.0
    assert (
        result.risk_analysis.default_probability
        == 0.03
    )
    assert (
        result.policy_analysis.policy_context
        == "Retrieved policy context."
    )
    assert (
        result.lending_decision.decision
        == "APPROVE"
    )
    assert result.rule_risk_level == "LOW"
    assert result.final_risk_level == "LOW"


def test_orchestrator_returns_complete_package(
    monkeypatch,
):

    financial_agent = FakeFinancialAgent()
    risk_agent = FakeRiskAgent()
    policy_agent = FakePolicyAgent()

    monkeypatch.setattr(
        orchestrator_module,
        "lending_decision_tool",
        lambda profile, default_probability:
            SimpleNamespace(
                decision="APPROVE",
                reason="Applicant has low credit risk.",
                risk_level="LOW",
            ),
    )

    final_analyst = FakeFinalAnalystAgent()

    orchestrator = CreditLensOrchestrator(
        financial_agent=financial_agent,
        risk_agent=risk_agent,
        policy_agent=policy_agent,
        final_analyst_agent=final_analyst,
    )

    result = orchestrator.assess(
        create_profile()
    )

    assert result.financial_analysis is not None
    assert result.risk_analysis is not None
    assert result.policy_analysis is not None
    assert result.lending_decision is not None

def test_orchestrator_passes_complete_package_to_final_analyst(
    monkeypatch,
):
    financial_agent = FakeFinancialAgent()
    risk_agent = FakeRiskAgent()
    policy_agent = FakePolicyAgent()
    final_analyst = FakeFinalAnalystAgent()

    monkeypatch.setattr(
        "app.agents.orchestrator.lending_decision_tool",
        lambda profile, default_probability: SimpleNamespace(
            decision="APPROVE",
            reason="Applicant has low credit risk.",
            risk_level="LOW",
        ),
    )

    orchestrator = CreditLensOrchestrator(
        financial_agent=financial_agent,
        risk_agent=risk_agent,
        policy_agent=policy_agent,
        final_analyst_agent=final_analyst,
    )

    profile = build_profile()

    result = orchestrator.assess(profile)

    assert final_analyst.received_input is not None

    package = final_analyst.received_input.assessment_package

    assert package.financial_analysis is not None
    assert package.risk_analysis is not None
    assert package.policy_analysis is not None
    assert package.lending_decision is not None

    assert package.lending_decision.decision == "APPROVE"
    assert package.rule_risk_level == "LOW"
    assert package.final_risk_level == "LOW"
    assert result.analyst_explanation == (
        "Final analyst explanation."
    )