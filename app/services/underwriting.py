def classify_risk(
    foir: float,
    remaining_income: float,
    monthly_income: float,
) -> dict:

    remaining_income_ratio = (
        remaining_income / monthly_income
    ) * 100

    reasons = []

    # Critical rules
    if foir > 50:
        reasons.append("FOIR exceeds critical threshold")

    if remaining_income_ratio < 20:
        reasons.append("Remaining income is below minimum threshold")

    if reasons:
        return {
            "risk_level": "HIGH",
            "reasons": reasons,
        }

    # Review rules
    if foir > 40:
        reasons.append("FOIR requires review")

    if remaining_income_ratio < 30:
        reasons.append("Remaining income requires review")

    if reasons:
        return {
            "risk_level": "MEDIUM",
            "reasons": reasons,
        }

    return {
        "risk_level": "LOW",
        "reasons": ["Applicant passes basic financial rules"],
    }