from finance import calculate_foir


income = 80000
obligations = 20000

foir = calculate_foir(income, obligations)

print(f"FOIR: {foir:.2f}%")