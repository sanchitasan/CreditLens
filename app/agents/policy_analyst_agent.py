from dataclasses import dataclass

from app.tools.policy_retrieval_tool import policy_retrieval_tool


@dataclass
class PolicyAnalysis:
    """Policy analysis produced by the Policy Analyst Agent."""

    policy_context: str


@dataclass
class PolicyAnalystInput:
    """Input provided to the Policy Analyst Agent."""

    foir: float
    credit_score: float
    previous_defaults: int
    default_probability: float
    lending_decision: str


class PolicyAnalystAgent:
    """
    Specialized agent responsible for retrieving
    relevant credit policy context.

    It does not make or override the lending decision.
    """

    def analyze(
        self,
        agent_input: PolicyAnalystInput,
    ) -> PolicyAnalysis:

        policy_context = policy_retrieval_tool(
            foir=agent_input.foir,
            credit_score=agent_input.credit_score,
            previous_defaults=agent_input.previous_defaults,
            default_probability=agent_input.default_probability,
            lending_decision=agent_input.lending_decision,
        )

        return PolicyAnalysis(
            policy_context=policy_context,
        )