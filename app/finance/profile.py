from dataclasses import dataclass

@dataclass
class FinancialProfile:
    monthly_income: float
    existing_obligations: float
    loan_amount: float
    annual_interest_rate: float
    tenure_years: int

    def validate(self):
        if self.monthly_income <= 0:
            raise ValueError("Monthly income must be greater than zero.")

        if self.existing_obligations < 0:
            raise ValueError("Existing obligations cannot be negative.")

        if self.loan_amount <= 0:
            raise ValueError("Loan amount must be greater than zero.")

        if self.annual_interest_rate < 0:
            raise ValueError("Interest rate cannot be negative.")

        if self.tenure_years <= 0:
            raise ValueError("Tenure must be greater than zero.")