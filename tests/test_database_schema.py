import sqlite3

from app.db.database import (
    get_connection,
    initialize_database,
)

from app.schemas.application import DecisionTraceResponse


def test_decision_trace_column_exists():

    initialize_database()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        PRAGMA table_info(credit_applications)
        """
    )

    columns = {
        row[1]
        for row in cursor.fetchall()
    }

    connection.close()

    assert "decision_trace" in columns

def test_decision_trace_response():
    trace = DecisionTraceResponse(
        applicant_data={
            "monthly_income": 80000
        },
        financial_analysis={
            "foir": 25.0,
            "emi": 11122.22,
        },
        risk_analysis={
            "default_probability": 0.03,
        },
        policy_context="FOIR policy guidance.",
        rule_risk_level="LOW",
        final_risk_level="LOW",
        lending_decision={
            "decision": "APPROVE",
            "reason": "Applicant has low credit risk.",
        },
        analyst_explanation="Applicant has low credit risk.",
    )

    assert trace.rule_risk_level == "LOW"
    assert trace.final_risk_level == "LOW"
    assert (
        trace.applicant_data["monthly_income"]
        == 80000
    )