def calculate_foir(monthly_income, monthly_obligations):
    if monthly_income <= 0:
        raise ValueError("Monthly income must be greater than zero.")

    foir = (monthly_obligations / monthly_income) * 100

    return foir