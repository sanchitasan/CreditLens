import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"

DB_PATH = DATA_DIR / "creditlens.db"


def get_connection():
    """
    Create and return a SQLite database connection.
    """

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    return sqlite3.connect(DB_PATH)


def initialize_database():
    """
    Create the credit applications table
    and apply required schema updates.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS credit_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            monthly_income REAL NOT NULL,
            existing_obligations REAL NOT NULL,
            loan_amount REAL NOT NULL,
            annual_interest_rate REAL NOT NULL,
            tenure_years REAL NOT NULL,

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

    # Check which columns already exist.
    cursor.execute(
        """
        PRAGMA table_info(credit_applications)
        """
    )

    columns = {
        row[1]
        for row in cursor.fetchall()
    }

    # Migration: add credit score.
    if "credit_score" not in columns:

        cursor.execute(
            """
            ALTER TABLE credit_applications
            ADD COLUMN credit_score REAL
            """
        )

    # Migration: add employment years.
    if "employment_years" not in columns:

        cursor.execute(
            """
            ALTER TABLE credit_applications
            ADD COLUMN employment_years REAL
            """
        )

    # Migration: add previous defaults.
    if "previous_defaults" not in columns:

        cursor.execute(
            """
            ALTER TABLE credit_applications
            ADD COLUMN previous_defaults INTEGER
            """
        )

    # Migration: add ML default probability.
    if "default_probability" not in columns:

        cursor.execute(
            """
            ALTER TABLE credit_applications
            ADD COLUMN default_probability REAL
            """
        )

    # Migration: add ML explanation.
    if "ml_explanation" not in columns:

        cursor.execute(
            """
            ALTER TABLE credit_applications
            ADD COLUMN ml_explanation TEXT
            """
        )

    # Migration: add Gemini analyst explanation.
    if "analyst_explanation" not in columns:

        cursor.execute(
            """
            ALTER TABLE credit_applications
            ADD COLUMN analyst_explanation TEXT
            """
        )

    # Migration: add decision column if necessary.
    if "decision" not in columns:

        cursor.execute(
            """
            ALTER TABLE credit_applications
            ADD COLUMN decision TEXT
            """
        )

    # Migration: add decision reason column if necessary.
    if "decision_reason" not in columns:

        cursor.execute(
            """
            ALTER TABLE credit_applications
            ADD COLUMN decision_reason TEXT
            """
        )

    # Migration: add decision trace.
    if "decision_trace" not in columns:
        cursor.execute(
            """
            ALTER TABLE credit_applications
            ADD COLUMN decision_trace TEXT
            """
        )

    connection.commit()

    connection.close()