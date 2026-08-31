from typing import Optional

from app.db.database import get_connection

from app.finance import FinancialProfile

from app.services.decision import (
    LendingDecision,
)


def save_credit_application(
    profile: FinancialProfile,
    result,
    lending_decision: LendingDecision,
    connection=None,
) -> int:
    """
    Save a completed credit application.

    Stores:
    - applicant financial information
    - credit assessment
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

            foir,
            emi,
            total_obligations,
            remaining_income,
            risk_level,

            decision,
            decision_reason
        )
        VALUES (
            ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?,
            ?, ?
        )
        """,
        (
            profile.monthly_income,
            profile.existing_obligations,
            profile.loan_amount,
            profile.annual_interest_rate,
            profile.tenure_years,

            result.foir,
            result.emi,
            result.total_obligations,
            result.remaining_income,
            result.risk_level,

            lending_decision.decision,
            lending_decision.reason,
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

            foir,
            emi,
            total_obligations,
            remaining_income,
            risk_level,

            decision,
            decision_reason

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

    return dict(row)


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

    if close_connection:
        connection.close()

    return applications