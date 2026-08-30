from finance import calculate_foir


def show_welcome():
    print("\n" + "=" * 45)
    print("           CREDITLENS v0.1")
    print("          Finance Assistant")
    print("=" * 45)

    print("\nI can currently help with:")
    print("- FOIR calculation")
    print("- Basic finance concepts")
    print("- Help")


def calculate_foir_flow():
    print("\n--- FOIR Calculator ---")

    try:
        income = float(input("Enter monthly income: "))
        obligations = float(input("Enter monthly obligations: "))

        foir = calculate_foir(income, obligations)

        print(f"\nFOIR = {foir:.2f}%")

    except ValueError as error:
        print(f"\nError: {error}")


def process_message(message):
    message = message.lower().strip()

    if "foir" in message:
        return "foir"

    if message in ["hello", "hi", "hey"]:
        return "greeting"

    if message in ["help", "what can you do"]:
        return "help"

    if message in ["exit", "quit", "bye"]:
        return "exit"

    return "unknown"


def main():
    show_welcome()

    while True:
        message = input("\nYou: ")

        intent = process_message(message)

        if intent == "greeting":
            print("CreditLens: Hello! How can I help you?")

        elif intent == "foir":
            calculate_foir_flow()

        elif intent == "help":
            print("\nCreditLens can currently:")
            print("1. Calculate FOIR")
            print("2. Explain basic finance concepts")

        elif intent == "exit":
            print("CreditLens: Goodbye!")
            break

        else:
            print(
                "CreditLens: I don't understand that yet. "
                "Try asking about FOIR or type 'help'."
            )


if __name__ == "__main__":
    main()