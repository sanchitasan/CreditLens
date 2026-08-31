from app.db.database import get_connection


def get_db_connection():
    """
    Provide a database connection for API operations.
    """

    connection = get_connection()

    try:
        yield connection

    finally:
        connection.close()