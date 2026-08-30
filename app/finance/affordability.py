def calculate_affordability(
    monthly_income,
    existing_obligations,
    proposed_emi
):
    if monthly_income <= 0:
        raise ValueError("Monthly income must be greater than zero.")

    if existing_obligations < 0:
        raise ValueError("Existing obligations cannot be negative.")

    if proposed_emi < 0:
        raise ValueError("Proposed EMI cannot be negative.")

    total_obligations = existing_obligations + proposed_emi

    foir = (total_obligations / monthly_income) * 100

    remaining_income = monthly_income - total_obligations

    return {
        "total_obligations": total_obligations,
        "foir": foir,
        "remaining_income": remaining_income,
    }