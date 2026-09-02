import httpx

from ui_app.api_client import CreditLensAPIClient


class FakeResponse:

    def __init__(self, data):
        self._data = data

    def raise_for_status(self):
        pass

    def json(self):
        return self._data


def test_create_application(monkeypatch):

    captured = {}

    def fake_post(url, json):

        captured["url"] = url
        captured["json"] = json

        return FakeResponse(
            {
                "application_id": 101,
                "credit_assessment": {
                    "foir": 25.0,
                    "emi": 11122.22,
                    "total_obligations": 31122.22,
                    "remaining_income": 48877.78,
                    "risk_level": "LOW",
                    "default_probability": 0.03,
                    "ml_explanation": [],
                },
                "lending_decision": {
                    "decision": "APPROVE",
                    "reason": "Applicant has low credit risk.",
                },
                "analyst_explanation": "Test explanation.",
            }
        )

    monkeypatch.setattr(
        httpx,
        "post",
        fake_post,
    )

    client = CreditLensAPIClient()

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

    result = client.create_application(payload)

    assert captured["url"] == (
        "http://127.0.0.1:8000/applications"
    )

    assert captured["json"] == payload

    assert result["application_id"] == 101

    assert (
        result["credit_assessment"]["risk_level"]
        == "LOW"
    )

    assert (
        result["lending_decision"]["decision"]
        == "APPROVE"
    )


def test_get_application(monkeypatch):

    captured = {}

    def fake_get(url, **kwargs):

        captured["url"] = url
        captured["kwargs"] = kwargs

        return FakeResponse(
            {
                "application_id": 101,
                "risk_level": "LOW",
                "decision": "APPROVE",
            }
        )

    monkeypatch.setattr(
        httpx,
        "get",
        fake_get,
    )

    client = CreditLensAPIClient()

    result = client.get_application(101)

    assert captured["url"] == (
        "http://127.0.0.1:8000/applications/101"
    )

    assert result["application_id"] == 101
    assert result["risk_level"] == "LOW"
    assert result["decision"] == "APPROVE"


def test_list_applications(monkeypatch):

    captured = {}

    def fake_get(url, **kwargs):

        captured["url"] = url
        captured["kwargs"] = kwargs

        return FakeResponse(
            [
                {
                    "application_id": 101,
                    "risk_level": "LOW",
                    "decision": "APPROVE",
                },
                {
                    "application_id": 102,
                    "risk_level": "HIGH",
                    "decision": "REJECT",
                },
            ]
        )

    monkeypatch.setattr(
        httpx,
        "get",
        fake_get,
    )

    client = CreditLensAPIClient()

    result = client.list_applications(
        skip=10,
        limit=20,
        risk_level="LOW",
        decision="APPROVE",
    )

    assert captured["url"] == (
        "http://127.0.0.1:8000/applications"
    )

    assert captured["kwargs"]["params"] == {
        "skip": 10,
        "limit": 20,
        "risk_level": "LOW",
        "decision": "APPROVE",
    }

    assert len(result) == 2

    assert result[0]["application_id"] == 101
    assert result[1]["application_id"] == 102


def test_list_applications_without_filters(
    monkeypatch,
):

    captured = {}

    def fake_get(url, **kwargs):

        captured["kwargs"] = kwargs

        return FakeResponse([])

    monkeypatch.setattr(
        httpx,
        "get",
        fake_get,
    )

    client = CreditLensAPIClient()

    result = client.list_applications()

    assert captured["kwargs"]["params"] == {
        "skip": 0,
        "limit": 100,
    }

    assert result == []