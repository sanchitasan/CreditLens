from typing import Optional
import json

from app.db.database import get_connection

from app.finance import FinancialProfile

from app.services.decision import (
    LendingDecision,
)

from dataclasses import asdict, is_dataclass

def serialize_decision_trace(decision_trace) -> str | None:
    """
    Serialize a DecisionTrace into JSON for database storage.
    """

    if decision_trace is None:
        return None

    if not is_dataclass(decision_trace):
        raise TypeError(
            "decision_trace must be a dataclass"
        )

    return json.dumps(
        asdict(decision_trace)
    )

def deserialize_decision_trace(decision_trace):
    """
    Convert stored DecisionTrace JSON into a Python dictionary.
    """

    if not decision_trace:
        return None

    if isinstance(decision_trace, str):
        return json.loads(decision_trace)

    return decision_trace

def deserialize_ml_explanation(value):
    """
    Convert stored ML explanation JSON into a list.
    """

    if not value:
        return []

    parsed = json.loads(value)

    if parsed is None:
        return []

    return parsed


def save_credit_application(
    profile: FinancialProfile,

    result,
    lending_decision: LendingDecision,
    decision_trace=None,
    connection=None,
) -> int:
    """
    Save a completed credit application.

    Stores:
    - applicant financial information
    - credit assessment
    - ML prediction and explanation
    - lending decision
    """

    owns_connection = connection is None


    if connection is None:
        connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO credit_applications (
            monthly_income,
            existing_obligations,
            loan_amount,
            annual_interest_rate,
            tenure_years,

            credit_score,
            employment_years,
            previous_defaults,

            foir,
            emi,
            total_obligations,
            remaining_income,
            risk_level,

            default_probability,
            ml_explanation,
            analyst_explanation,

            decision,
            decision_reason,
            decision_trace
        )
        VALUES (
            ?, ?, ?, ?, ?,
            ?, ?, ?,
            ?, ?, ?, ?, ?,
            ?, ?, ?,
            ?, ?, ?
        )
        """,
        (
            profile.monthly_income,
            profile.existing_obligations,
            profile.loan_amount,
            profile.annual_interest_rate,
            profile.tenure_years,

            profile.credit_score,
            profile.employment_years,
            profile.previous_defaults,

            result.foir,
            result.emi,
            result.total_obligations,
            result.remaining_income,
            result.risk_level,

            result.default_probability,
            json.dumps(result.ml_explanation),
            result.analyst_explanation,

            lending_decision.decision,
            lending_decision.reason,
            serialize_decision_trace(decision_trace),
        ),
    )

    application_id = cursor.lastrowid

    connection.commit()

    if owns_connection:
        connection.close()

    return application_id


def get_credit_application(
    application_id: int,
    connection=None,
) -> Optional[dict]:
    """
    Retrieve one credit application.
    """

    owns_connection = connection is None

    if connection is None:
        connection = get_connection()

    connection.row_factory = __import__("sqlite3").Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,

            monthly_income,
            existing_obligations,
            loan_amount,
            annual_interest_rate,
            tenure_years,

            credit_score,
            employment_years,
            previous_defaults,

            foir,
            emi,
            total_obligations,
            remaining_income,
            risk_level,

            default_probability,
            ml_explanation,
            analyst_explanation,

            decision,
            decision_reason,
            decision_trace

        FROM credit_applications

        WHERE id = ?
        """,
        (application_id,),
    )

    row = cursor.fetchone()

    if owns_connection:
        connection.close()

    if row is None:
        return None

    application = dict(row)

    application["ml_explanation"] = deserialize_ml_explanation(
        application["ml_explanation"]
    )

    application["decision_trace"] = deserialize_decision_trace(
        application["decision_trace"]
    )


    return application


def list_credit_applications(
    connection=None,
    skip=0,
    limit=10,
    risk_level=None,
    decision=None,
):
    """
    Retrieve credit applications with pagination
    and optional filtering.
    """

    close_connection = False

    if connection is None:
        connection = get_connection()
        close_connection = True

    cursor = connection.cursor()

    query = """
        SELECT *
        FROM credit_applications
    """

    conditions = []
    parameters = []

    if risk_level is not None:
        conditions.append(
            "risk_level = ?"
        )
        parameters.append(risk_level)

    if decision is not None:
        conditions.append(
            "decision = ?"
        )
        parameters.append(decision)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += """
        ORDER BY id DESC
        LIMIT ? OFFSET ?
    """

    parameters.extend([
        limit,
        skip,
    ])

    cursor.execute(
        query,
        parameters,
    )

    rows = cursor.fetchall()

    columns = [
        description[0]
        for description in cursor.description
    ]

    applications = [
        dict(zip(columns, row))
        for row in rows
    ]

    for application in applications:
        application["ml_explanation"] = deserialize_ml_explanation(
            application["ml_explanation"]
        )

        application["decision_trace"] = deserialize_decision_trace(
            application["decision_trace"]
        )



    if close_connection:
        connection.close()

    return applications