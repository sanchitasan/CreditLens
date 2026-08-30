def calculate_dti(total_debt, annual_income):
    return total_debt / annual_income


if __name__ == "__main__":
    debt = 5000000
    income = 1000000

    dti = calculate_dti(debt, income)

    print("Debt-to-Income Ratio:", dti)