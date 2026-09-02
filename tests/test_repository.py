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
import json

from app.audit.decision_trace import DecisionTrace
from app.db.database import get_connection, initialize_database

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
            decision_reason TEXT,
            
            decision_trace TEXT
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
        risk_level="LOW",
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


def test_save_credit_application_persists_decision_trace():

    initialize_database()

    connection = get_connection()

    profile = FinancialProfile(
        monthly_income=80000,
        existing_obligations=20000,
        loan_amount=500000,
        annual_interest_rate=12,
        tenure_years=5,
        credit_score=780,
        employment_years=5,
        previous_defaults=0,
    )

    result = create_decision()

    lending_decision = LendingDecision(
        decision="APPROVE",
        reason="Applicant has low credit risk.",
        risk_level="LOW",
    )

    trace = DecisionTrace(
        applicant_data={
            "monthly_income": 80000,
        },
        financial_analysis=result,
        risk_analysis={
            "default_probability": 0.03,
        },
        policy_context="FOIR guidelines.",
        rule_risk_level="LOW",
        final_risk_level="LOW",
        lending_decision=lending_decision,
        analyst_explanation="Applicant has low risk.",
    )

    application_id = save_credit_application(
        profile=profile,
        result=result,
        lending_decision=lending_decision,
        decision_trace=trace,
        connection=connection,
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT decision_trace
        FROM credit_applications
        WHERE id = ?
        """,
        (application_id,),
    )

    stored_trace = cursor.fetchone()[0]

    connection.close()

    assert stored_trace is not None

    parsed_trace = json.loads(stored_trace)

    assert parsed_trace["applicant_data"]["monthly_income"] == 80000
    assert parsed_trace["rule_risk_level"] == "LOW"
    assert parsed_trace["final_risk_level"] == "LOW"
    assert parsed_trace["policy_context"] == "FOIR guidelines."


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

def test_get_credit_application_returns_decision_trace(
    tmp_path,
    monkeypatch,
):
    """
    Verify that a persisted DecisionTrace
    can be retrieved as structured data.
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

    trace = DecisionTrace(
        applicant_data={
            "monthly_income": 80000,
        },
        financial_analysis=result,
        risk_analysis={
            "default_probability": 0.03,
        },
        policy_context="FOIR guidelines.",
        rule_risk_level="LOW",
        final_risk_level="LOW",
        lending_decision=lending_decision,
        analyst_explanation="Applicant has low risk.",
    )

    application_id = save_credit_application(
        profile=profile,
        result=result,
        lending_decision=lending_decision,
        decision_trace=trace,
    )

    application = get_credit_application(
        application_id
    )

    assert application is not None

    assert application["decision_trace"] is not None

    retrieved_trace = application["decision_trace"]

    assert (
        retrieved_trace["applicant_data"]["monthly_income"]
        == 80000
    )

    assert (
        retrieved_trace["rule_risk_level"]
        == "LOW"
    )

    assert (
        retrieved_trace["final_risk_level"]
        == "LOW"
    )

    assert (
        retrieved_trace["policy_context"]
        == "FOIR guidelines."
    )

    assert (
        retrieved_trace["analyst_explanation"]
        == "Applicant has low risk."
    )

def test_save_credit_application_rolls_back_on_database_error(
    tmp_path,
):
    """
    Verify that a failed application insert
    rolls back the database transaction.
    """

    test_database = (
        tmp_path / "test_creditlens.db"
    )

    create_test_database(test_database)

    connection = sqlite3.connect(test_database)

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TRIGGER fail_credit_application_insert
        BEFORE INSERT ON credit_applications
        BEGIN
            SELECT RAISE(
                ABORT,
                'forced database failure'
            );
        END;
        """
    )

    connection.commit()

    profile = create_profile()
    result = create_decision()
    lending_decision = create_lending_decision()

    try:
        save_credit_application(
            profile=profile,
            result=result,
            lending_decision=lending_decision,
            connection=connection,
        )

        assert False, (
            "Expected database insert to fail"
        )

    except sqlite3.DatabaseError as error:
        assert "forced database failure" in str(error)

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM credit_applications
        """
    )

    application_count = cursor.fetchone()[0]

    connection.close()

    assert application_count == 0