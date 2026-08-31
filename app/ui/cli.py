from app.finance.profile import FinancialProfile
from app.services.application_service import process_credit_application
from app.db.repository import (
    get_credit_application,
    list_credit_applications,
)


def get_float(prompt: str) -> float:
    """
    Safely collect a numeric value from the user.
    """

    while True:
        try:
            value = float(input(prompt))

            if value < 0:
                print("Value cannot be negative.")
                continue

            return value

        except ValueError:
            print("Please enter a valid number.")


def create_application():
    """
    Collect applicant information and process a credit application.
    """

    print("\n")
    print("=" * 50)
    print("        NEW CREDIT APPLICATION")
    print("=" * 50)

    monthly_income = get_float(
        "Monthly income (₹): "
    )

    existing_obligations = get_float(
        "Existing monthly obligations (₹): "
    )

    loan_amount = get_float(
        "Requested loan amount (₹): "
    )

    annual_interest_rate = get_float(
        "Annual interest rate (%): "
    )

    tenure_years = get_float(
        "Loan tenure (years): "
    )

    try:

        profile = FinancialProfile(
            monthly_income=monthly_income,
            existing_obligations=existing_obligations,
            loan_amount=loan_amount,
            annual_interest_rate=annual_interest_rate,
            tenure_years=tenure_years,
        )

        application_id, result = process_credit_application(
            profile
        )

        print("\n")
        print("=" * 50)
        print("           CREDIT ASSESSMENT")
        print("=" * 50)

        print(
            f"FOIR              : {result.foir:.2f}%"
        )

        print(
            f"EMI               : ₹{result.emi:,.2f}"
        )

        print(
            f"Total obligations  : "
            f"₹{result.total_obligations:,.2f}"
        )

        print(
            f"Remaining income   : "
            f"₹{result.remaining_income:,.2f}"
        )

        print(
            f"Risk level         : {result.risk_level}"
        )

        print("\nRisk reasons:")

        for reason in result.risk_reasons:
            print(f"- {reason}")

        print("\n")
        print("=" * 50)
        print("Application processed successfully.")
        print(f"Application ID: {application_id}")
        print("=" * 50)

    except ValueError as error:

        print(f"\nInput error: {error}")


def view_application():
    """
    Retrieve and display one credit application.
    """

    print("\n")
    print("=" * 50)
    print("          VIEW APPLICATION")
    print("=" * 50)

    application_id = int(
        get_float("Application ID: ")
    )

    application = get_credit_application(
        application_id
    )

    if application is None:

        print(
            f"\nNo application found "
            f"with ID {application_id}."
        )

        return

    print("\nApplication Details")
    print("-" * 50)

    print(f"ID                  : {application['id']}")
    print(
        f"Monthly income      : "
        f"₹{application['monthly_income']:,.2f}"
    )
    print(
        f"Existing obligations: "
        f"₹{application['existing_obligations']:,.2f}"
    )
    print(
        f"Loan amount         : "
        f"₹{application['loan_amount']:,.2f}"
    )
    print(
        f"Interest rate       : "
        f"{application['annual_interest_rate']:.2f}%"
    )
    print(
        f"Tenure              : "
        f"{application['tenure_years']:.0f} years"
    )
    print(
        f"FOIR                : "
        f"{application['foir']:.2f}%"
    )
    print(
        f"EMI                 : "
        f"₹{application['emi']:,.2f}"
    )
    print(
        f"Total obligations   : "
        f"₹{application['total_obligations']:,.2f}"
    )
    print(
        f"Remaining income    : "
        f"₹{application['remaining_income']:,.2f}"
    )
    print(
        f"Risk level          : "
        f"{application['risk_level']}"
    )


def application_history():
    """
    Display all stored credit applications.
    """

    print("\n")
    print("=" * 70)
    print("                APPLICATION HISTORY")
    print("=" * 70)

    applications = list_credit_applications()

    if not applications:

        print("\nNo applications found.")

        return

    for application in applications:

        print(
            f"\nID: {application['id']}"
        )

        print(
            f"Income: "
            f"₹{application['monthly_income']:,.2f}"
        )

        print(
            f"Loan: "
            f"₹{application['loan_amount']:,.2f}"
        )

        print(
            f"FOIR: "
            f"{application['foir']:.2f}%"
        )

        print(
            f"Risk: "
            f"{application['risk_level']}"
        )

        print("-" * 70)


def run_cli():
    """
    Main CreditLens command-line interface.
    """

    while True:

        print("\n")
        print("=" * 50)
        print("                CREDITLENS")
        print("          Credit Assessment System")
        print("=" * 50)

        print("\n1. New Credit Application")
        print("2. View Application")
        print("3. Application History")
        print("4. Exit")

        choice = input(
            "\nSelect an option: "
        ).strip()

        if choice == "1":

            create_application()

        elif choice == "2":

            view_application()

        elif choice == "3":

            application_history()

        elif choice == "4":

            print("\nThank you for using CreditLens.")

            break

        else:

            print(
                "\nInvalid option. "
                "Please select 1-4."
            )