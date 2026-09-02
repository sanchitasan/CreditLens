from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.api.main import app

from app.services.exceptions import (
    CreditApplicationError,
)
from app.agents.financial_analyst_agent import FinancialAnalysis
from app.agents.risk_analyst_agent import RiskAnalysis
from app.agents.policy_analyst_agent import PolicyAnalysis
from app.services.decision import LendingDecision
from app.audit.decision_trace import DecisionTrace


class FakeOrchestrator:

    def assess(self, profile):

        financial_analysis = FinancialAnalysis(
            foir=25.0,
            emi=11122.22,
            total_obligations=31122.22,
            remaining_income=48877.78,
            risk_level="LOW",
            risk_reasons=[
                "Applicant passes basic financial rules"
            ],
        )

        risk_analysis = RiskAnalysis(
            default_probability=0.03,
            ml_explanation=[
                {
                    "feature": "credit_score",
                    "contribution": -3.9,
                    "direction": "reduces default risk",
                }
            ],
        )

        policy_analysis = PolicyAnalysis(
            policy_context="Retrieved policy context."
        )

        lending_decision = LendingDecision(
            decision="APPROVE",
            reason="Applicant has low credit risk.",
            risk_level="LOW",
        )

        decision_trace = DecisionTrace(
            applicant_data={
                "monthly_income": profile.monthly_income,
                "existing_obligations": profile.existing_obligations,
                "loan_amount": profile.loan_amount,
                "annual_interest_rate": profile.annual_interest_rate,
                "tenure_years": profile.tenure_years,
            },
            financial_analysis=financial_analysis,
            risk_analysis=risk_analysis,
            policy_context=policy_analysis.policy_context,
            rule_risk_level="LOW",
            final_risk_level="LOW",
            lending_decision=lending_decision,
            analyst_explanation="Applicant has low credit risk.",
        )

        return SimpleNamespace(
            financial_analysis=financial_analysis,
            risk_analysis=risk_analysis,
            policy_analysis=policy_analysis,
            lending_decision=lending_decision,
            rule_risk_level="LOW",
            final_risk_level="LOW",
            analyst_explanation=(
                "Fake analyst explanation for testing."
            ),
            decision_trace=decision_trace,
        )

client = TestClient(
    app,
    raise_server_exceptions=False,
)

def test_list_applications():

    response = client.get("/applications")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_nonexistent_application():

    response = client.get(
        "/applications/999999"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Credit application not found"
    }

def test_create_application(monkeypatch):

    monkeypatch.setattr(
        "app.services.application_service.create_creditlens_orchestrator",
        lambda: FakeOrchestrator(),
    )

    payload = {
        "monthly_income": 80000,
        "existing_obligations": 20000,
        "loan_amount": 500000,
        "annual_interest_rate": 12,
        "tenure_years": 5,
        "credit_score": 750,
        "employment_years": 4,
        "previous_defaults": 0,
    }

    response = client.post(
        "/applications",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert "application_id" in data

    assert (
        data["credit_assessment"]["risk_level"]
        == "LOW"
    )

    assert (
        data["lending_decision"]["decision"]
        == "APPROVE"
    )
    assert (
            data["analyst_explanation"]
            == "Fake analyst explanation for testing."
    )

def test_list_applications_returns_decision_trace(monkeypatch):

    monkeypatch.setattr(
        "app.services.application_service.create_creditlens_orchestrator",
        lambda: FakeOrchestrator(),
    )

    payload = {
        "monthly_income": 80000,
        "existing_obligations": 20000,
        "loan_amount": 500000,
        "annual_interest_rate": 12,
        "tenure_years": 5,
        "credit_score": 750,
        "employment_years": 4,
        "previous_defaults": 0,
    }

    # Create an application first.
    create_response = client.post(
        "/applications",
        json=payload,
    )

    assert create_response.status_code == 201

    application_id = create_response.json()["application_id"]

    # Retrieve applications through the list endpoint.
    response = client.get("/applications")

    assert response.status_code == 200

    applications = response.json()

    assert isinstance(applications, list)

    # Find the application we just created.
    application = next(
        application
        for application in applications
        if application["application_id"] == application_id
    )

    # Verify the audit trace is exposed.
    assert application["decision_trace"] is not None

    trace = application["decision_trace"]

    assert (
        trace["applicant_data"]["monthly_income"]
        == 80000
    )

    assert trace["rule_risk_level"] == "LOW"

    assert trace["final_risk_level"] == "LOW"

    assert (
        trace["policy_context"]
        == "Retrieved policy context."
    )

    assert (
        trace["analyst_explanation"]
        == "Applicant has low credit risk."
    )

def test_negative_income_rejected():

    payload = {
        "monthly_income": -80000,
        "existing_obligations": 20000,
        "loan_amount": 500000,
        "annual_interest_rate": 12,
        "tenure_years": 5,
    }

    response = client.post(
        "/applications",
        json=payload,
    )

    assert response.status_code == 422

def test_zero_loan_amount_rejected():

    payload = {
        "monthly_income": 80000,
        "existing_obligations": 20000,
        "loan_amount": 0,
        "annual_interest_rate": 12,
        "tenure_years": 5,
    }

    response = client.post(
        "/applications",
        json=payload,
    )

    assert response.status_code == 422

def test_excessive_interest_rate_rejected():

    payload = {
        "monthly_income": 80000,
        "existing_obligations": 20000,
        "loan_amount": 500000,
        "annual_interest_rate": 51,
        "tenure_years": 5,
    }

    response = client.post(
        "/applications",
        json=payload,
    )

    assert response.status_code == 422

def test_excessive_tenure_rejected():

    payload = {
        "monthly_income": 80000,
        "existing_obligations": 20000,
        "loan_amount": 500000,
        "annual_interest_rate": 12,
        "tenure_years": 31,
    }

    response = client.post(
        "/applications",
        json=payload,
    )

    assert response.status_code == 422

def test_root_endpoint():

    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "CreditLens API is running"
    }

def test_get_application_returns_persisted_decision_trace(
    monkeypatch,
):

    monkeypatch.setattr(
        "app.services.application_service.create_creditlens_orchestrator",
        lambda: FakeOrchestrator(),
    )

    payload = {
        "monthly_income": 80000,
        "existing_obligations": 20000,
        "loan_amount": 500000,
        "annual_interest_rate": 12,
        "tenure_years": 5,
        "credit_score": 750,
        "employment_years": 4,
        "previous_defaults": 0,
    }

    # Step 1: Create application.
    create_response = client.post(
        "/applications",
        json=payload,
    )

    assert create_response.status_code == 201

    application_id = (
        create_response.json()["application_id"]
    )

    # Step 2: Retrieve the same application.
    response = client.get(
        f"/applications/{application_id}"
    )

    assert response.status_code == 200

    data = response.json()

    # Step 3: Verify the persisted audit trace.
    assert data["application_id"] == application_id

    assert data["decision_trace"] is not None

    trace = data["decision_trace"]

    # Applicant evidence.
    assert (
        trace["applicant_data"]["monthly_income"]
        == 80000
    )

    assert (
        trace["applicant_data"]["existing_obligations"]
        == 20000
    )

    assert (
        trace["applicant_data"]["loan_amount"]
        == 500000
    )

    # Risk assessment.
    assert trace["rule_risk_level"] == "LOW"

    assert trace["final_risk_level"] == "LOW"

    # Policy evidence.
    assert (
        trace["policy_context"]
        == "Retrieved policy context."
    )

    # Final explanation.
    assert (
        trace["analyst_explanation"]
        == "Applicant has low credit risk."
    )

def test_unexpected_error_returns_500(monkeypatch):
    def failing_process_credit_application(
        profile,
        connection=None,
    ):
        raise RuntimeError(
            "unexpected internal failure"
        )

    monkeypatch.setattr(
        "app.api.main.process_credit_application",
        failing_process_credit_application,
    )

    payload = {
        "monthly_income": 80000,
        "existing_obligations": 20000,
        "loan_amount": 500000,
        "annual_interest_rate": 12,
        "tenure_years": 5,
        "credit_score": 750,
        "employment_years": 4,
        "previous_defaults": 0,
    }

    response = client.post(
        "/applications",
        json=payload,
    )

    assert response.status_code == 500

    assert response.json() == {
        "error": "internal_server_error",
        "message": (
            "An unexpected error occurred "
            "while processing the request."
        ),
    }

def test_list_applications_filters_by_risk_level(monkeypatch):

    monkeypatch.setattr(
        "app.services.application_service.create_creditlens_orchestrator",
        lambda: FakeOrchestrator(),
    )

    payload = {
        "monthly_income": 80000,
        "existing_obligations": 20000,
        "loan_amount": 500000,
        "annual_interest_rate": 12,
        "tenure_years": 5,
        "credit_score": 750,
        "employment_years": 4,
        "previous_defaults": 0,
    }

    create_response = client.post(
        "/applications",
        json=payload,
    )

    assert create_response.status_code == 201

    response = client.get(
        "/applications?risk_level=LOW"
    )

    assert response.status_code == 200

    applications = response.json()

    assert isinstance(applications, list)

    for application in applications:
        assert application["risk_level"] == "LOW"


def test_list_applications_filters_by_decision(monkeypatch):

    monkeypatch.setattr(
        "app.services.application_service.create_creditlens_orchestrator",
        lambda: FakeOrchestrator(),
    )

    payload = {
        "monthly_income": 80000,
        "existing_obligations": 20000,
        "loan_amount": 500000,
        "annual_interest_rate": 12,
        "tenure_years": 5,
        "credit_score": 750,
        "employment_years": 4,
        "previous_defaults": 0,
    }

    create_response = client.post(
        "/applications",
        json=payload,
    )

    assert create_response.status_code == 201

    response = client.get(
        "/applications?decision=APPROVE"
    )

    assert response.status_code == 200

    applications = response.json()

    assert isinstance(applications, list)

    for application in applications:
        assert application["decision"] == "APPROVE"


def test_list_applications_pagination(monkeypatch):

    monkeypatch.setattr(
        "app.services.application_service.create_creditlens_orchestrator",
        lambda: FakeOrchestrator(),
    )

    payload = {
        "monthly_income": 80000,
        "existing_obligations": 20000,
        "loan_amount": 500000,
        "annual_interest_rate": 12,
        "tenure_years": 5,
        "credit_score": 750,
        "employment_years": 4,
        "previous_defaults": 0,
    }

    # Create multiple applications.
    for _ in range(3):
        response = client.post(
            "/applications",
            json=payload,
        )

        assert response.status_code == 201

    response = client.get(
        "/applications?skip=0&limit=2"
    )

    assert response.status_code == 200

    applications = response.json()

    assert isinstance(applications, list)

    assert len(applications) <= 2


def test_list_applications_rejects_negative_skip():

    response = client.get(
        "/applications?skip=-1"
    )

    assert response.status_code == 422


def test_list_applications_rejects_excessive_limit():

    response = client.get(
        "/applications?limit=101"
    )

    assert response.status_code == 422


def test_list_applications_rejects_invalid_risk_level():

    response = client.get(
        "/applications?risk_level=INVALID"
    )

    assert response.status_code == 422


def test_list_applications_rejects_invalid_decision():

    response = client.get(
        "/applications?decision=INVALID"
    )

    assert response.status_code == 422


def test_create_application_response_contains_complete_assessment(
    monkeypatch,
):

    monkeypatch.setattr(
        "app.services.application_service.create_creditlens_orchestrator",
        lambda: FakeOrchestrator(),
    )

    payload = {
        "monthly_income": 80000,
        "existing_obligations": 20000,
        "loan_amount": 500000,
        "annual_interest_rate": 12,
        "tenure_years": 5,
        "credit_score": 750,
        "employment_years": 4,
        "previous_defaults": 0,
    }

    response = client.post(
        "/applications",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assessment = data["credit_assessment"]

    assert assessment["foir"] == 25.0
    assert assessment["emi"] == 11122.22
    assert assessment["total_obligations"] == 31122.22
    assert assessment["remaining_income"] == 48877.78
    assert assessment["risk_level"] == "LOW"
    assert assessment["default_probability"] == 0.03

    assert assessment["ml_explanation"] == [
        {
            "feature": "credit_score",
            "contribution": -3.9,
            "direction": "reduces default risk",
        }
    ]


