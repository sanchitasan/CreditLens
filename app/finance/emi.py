def calculate_emi(principal, annual_interest_rate, tenure_years):
    if principal <= 0:
        raise ValueError("Principal must be greater than zero.")

    if annual_interest_rate < 0:
        raise ValueError("Interest rate cannot be negative.")

    if tenure_years <= 0:
        raise ValueError("Tenure must be greater than zero.")

    monthly_rate = annual_interest_rate / 12 / 100
    number_of_months = tenure_years * 12

    if monthly_rate == 0:
        return principal / number_of_months

    emi = (
        principal
        * monthly_rate
        * (1 + monthly_rate) ** number_of_months
        / ((1 + monthly_rate) ** number_of_months - 1)
    )

    return emi