from dataclasses import dataclass

@dataclass
class FinancialProfile:
    monthly_income: float
    existing_obligations: float
    loan_amount: float
    annual_interest_rate: float
    tenure_years: int

    credit_score: float = 650.0
    employment_years: float = 1.0
    previous_defaults: int = 0

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
        if not 300 <= self.credit_score <= 900:
            raise ValueError("Credit score must be between 300 and 900.")

        if self.employment_years < 0:
            raise ValueError("Employment years cannot be negative.")

        if self.previous_defaults < 0:
            raise ValueError("Previous defaults cannot be negative.")