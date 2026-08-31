from fastapi.testclient import TestClient

from app.api.main import app

from app.services.exceptions import (
    CreditApplicationError,
)


client = TestClient(app)



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

def test_create_application():

    payload = {
        "monthly_income": 80000,
        "existing_obligations": 20000,
        "loan_amount": 500000,
        "annual_interest_rate": 12,
        "tenure_years": 5,
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

def test_get_nonexistent_application():

    response = client.get(
        "/applications/999999"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Credit application not found"
    }