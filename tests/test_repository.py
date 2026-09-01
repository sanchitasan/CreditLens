import sqlite3

from app.db import repository

from app.db.repository import (
    get_credit_application,
    list_credit_applications,
    save_credit_application,
)

from app.finance import FinancialProfile

from app.services.decision import (
    CreditDecision,
    LendingDecision,
)


def create_test_database(database_path):
    """
    Create a temporary database for repository tests.
    """

    connection = sqlite3.connect(database_path)

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE credit_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            monthly_income REAL NOT NULL,
            existing_obligations REAL NOT NULL,
            loan_amount REAL NOT NULL,
            annual_interest_rate REAL NOT NULL,
            tenure_years INTEGER NOT NULL,
            
            credit_score REAL,
            employment_years REAL,
            previous_defaults INTEGER,

            foir REAL NOT NULL,
            emi REAL NOT NULL,
            total_obligations REAL NOT NULL,
            remaining_income REAL NOT NULL,

            risk_level TEXT NOT NULL,

            default_probability REAL,
            ml_explanation TEXT,
            analyst_explanation TEXT,

            decision TEXT,
            decision_reason TEXT
        )
        """
    )

    connection.commit()

    connection.close()


def create_profile():
    """
    Create a sample financial profile.
    """

    return FinancialProfile(
        monthly_income=80000,
        existing_obligations=20000,
        loan_amount=500000,
        annual_interest_rate=12,
        tenure_years=5,
    )


def create_decision():
    """
    Create a sample credit assessment.
    """

    return CreditDecision(
        foir=25.0,
        emi=11122.22,
        total_obligations=31122.22,
        remaining_income=48877.78,
        risk_level="LOW",
        risk_reasons=[
            "FOIR is within the acceptable range."
        ],
    )


def create_lending_decision():
    """
    Create a sample lending decision.
    """

    return LendingDecision(
        decision="APPROVE",
        reason="Applicant has low credit risk.",
    )


def test_save_credit_application(
    tmp_path,
    monkeypatch,
):
    """
    Verify that an application can be saved.
    """

    test_database = (
        tmp_path / "test_creditlens.db"
    )

    create_test_database(test_database)

    monkeypatch.setattr(
        repository,
        "get_connection",
        lambda: sqlite3.connect(test_database),
    )

    profile = create_profile()

    result = create_decision()

    lending_decision = create_lending_decision()

    application_id = save_credit_application(
        profile,
        result,
        lending_decision,
    )

    assert application_id == 1


def test_get_credit_application(
    tmp_path,
    monkeypatch,
):
    """
    Verify that one application can be retrieved.
    """

    test_database = (
        tmp_path / "test_creditlens.db"
    )

    create_test_database(test_database)

    monkeypatch.setattr(
        repository,
        "get_connection",
        lambda: sqlite3.connect(test_database),
    )

    profile = create_profile()

    result = create_decision()

    lending_decision = create_lending_decision()

    application_id = save_credit_application(
        profile,
        result,
        lending_decision,
    )

    application = get_credit_application(
        application_id
    )

    assert application is not None

    assert application["id"] == 1

    assert application["monthly_income"] == 80000

    assert (
        application["existing_obligations"]
        == 20000
    )

    assert application["loan_amount"] == 500000

    assert (
        application["annual_interest_rate"]
        == 12
    )

    assert application["tenure_years"] == 5

    assert application["foir"] == 25.0

    assert (
        round(application["emi"], 2)
        == 11122.22
    )

    assert application["risk_level"] == "LOW"

    assert application["decision"] == "APPROVE"

    assert (
        application["decision_reason"]
        == "Applicant has low credit risk."
    )


def test_get_nonexistent_application(
    tmp_path,
    monkeypatch,
):
    """
    Verify that a missing application
    returns None.
    """

    test_database = (
        tmp_path / "test_creditlens.db"
    )

    create_test_database(test_database)

    monkeypatch.setattr(
        repository,
        "get_connection",
        lambda: sqlite3.connect(test_database),
    )

    application = get_credit_application(999)

    assert application is None


def test_list_credit_applications(
    tmp_path,
    monkeypatch,
):
    """
    Verify that multiple applications
    can be retrieved.
    """

    test_database = (
        tmp_path / "test_creditlens.db"
    )

    create_test_database(test_database)

    monkeypatch.setattr(
        repository,
        "get_connection",
        lambda: sqlite3.connect(test_database),
    )

    # First application

    profile_1 = create_profile()

    result_1 = create_decision()

    lending_decision_1 = create_lending_decision()

    first_id = save_credit_application(
        profile_1,
        result_1,
        lending_decision_1,
    )

    # Second application

    profile_2 = FinancialProfile(
        monthly_income=60000,
        existing_obligations=10000,
        loan_amount=300000,
        annual_interest_rate=10,
        tenure_years=5,
    )

    result_2 = CreditDecision(
        foir=31.5,
        emi=6374.0,
        total_obligations=16374.0,
        remaining_income=43626.0,
        risk_level="LOW",
        risk_reasons=[
            "FOIR is within the acceptable range."
        ],
    )

    lending_decision_2 = create_lending_decision()

    second_id = save_credit_application(
        profile_2,
        result_2,
        lending_decision_2,
    )

    applications = list_credit_applications()

    assert len(applications) == 2

    # Newest application should appear first.

    assert applications[0]["id"] == second_id

    assert applications[1]["id"] == first_id

    assert applications[0]["decision"] == "APPROVE"

    assert (
        applications[0]["decision_reason"]
        == "Applicant has low credit risk."
    )