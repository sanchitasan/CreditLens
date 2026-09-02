from app.finance.profile import FinancialProfile

from app.services.application_service import (
    process_credit_application,
)


class FakeRAGResult:

    def __init__(self, content):
        self.payload = {
            "content": content
        }


class FakeFactorQueryBuilder:

    def __init__(self):
        self.received_values = None

    def build(
        self,
        foir,
        credit_score,
        previous_defaults,
        default_probability,
        lending_decision,
    ):
        self.received_values = {
            "foir": foir,
            "credit_score": credit_score,
            "previous_defaults": previous_defaults,
            "default_probability": default_probability,
            "lending_decision": lending_decision,
        }

        return [
            "FOIR policy",
            "credit score policy",
            "previous default policy",
            "ML default probability policy",
            "APPROVE lending decision policy",
        ]


class FakeFactorRetriever:

    def __init__(self):
        self.received_queries = None
        self.received_limit = None

    def retrieve(self, queries, limit_per_query=1):
        self.received_queries = queries
        self.received_limit = limit_per_query

        return [
            FakeRAGResult(
                "FOIR below 30% is considered low financial obligation risk."
            )
        ]


class FakeRAGContextBuilder:

    def build(self, results):
        return results[0].payload["content"]


def test_process_credit_application(monkeypatch):

    class FakeCreditAnalyst:
        received_application = None

        def __init__(self, *args, **kwargs):
            pass

        def analyze(self, assessment):
            FakeCreditAnalyst.received_application = assessment
            return "Applicant has low credit risk."

    monkeypatch.setattr(
        "app.services.application_service.CreditAnalyst",
        FakeCreditAnalyst,
    )

    profile = FinancialProfile(
        monthly_income=80000,
        existing_obligations=20000,
        loan_amount=500000,
        annual_interest_rate=12,
        tenure_years=5,
    )

    rag_factor_query_builder = FakeFactorQueryBuilder()
    rag_factor_retriever = FakeFactorRetriever()

    (
        application_id,
        assessment,
        lending_decision,
    ) = process_credit_application(
        profile,
        rag_context_builder=FakeRAGContextBuilder(),
        rag_factor_query_builder=rag_factor_query_builder,
        rag_factor_retriever=rag_factor_retriever,
    )

    assert application_id > 0

    assert assessment.foir == 25.0

    assert round(assessment.emi, 2) == 11122.22

    assert assessment.total_obligations > 0

    assert assessment.remaining_income > 0

    assert assessment.risk_level == "LOW"

    assert lending_decision.decision == "APPROVE"

    assert (
        lending_decision.reason
        == "Applicant has low credit risk."
    )

    # Verify factor query builder received the final application values.

    assert (
        rag_factor_query_builder.received_values["foir"]
        == 25.0
    )

    assert (
        rag_factor_query_builder.received_values["credit_score"]
        == profile.credit_score
    )

    assert (
        rag_factor_query_builder.received_values["previous_defaults"]
        == profile.previous_defaults
    )

    assert (
        rag_factor_query_builder.received_values["default_probability"]
        == assessment.default_probability
    )

    assert (
        rag_factor_query_builder.received_values["lending_decision"]
        == lending_decision.decision
    )

    assert (
            FakeCreditAnalyst.received_application.policy_context
            == "FOIR below 30% is considered low financial obligation risk."
    )

    # Verify factor-level retrieval was actually called.

    assert len(rag_factor_retriever.received_queries) == 5

    assert rag_factor_retriever.received_limit == 1