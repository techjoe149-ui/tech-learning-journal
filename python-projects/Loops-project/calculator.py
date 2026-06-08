# calculator_section

def calculator():
    while True:
        print("\n--- CALCULATOR ---")
        print("1. Add ")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Exit Calculator")

        choice = input("Choose option: ")
        if choice == "5":
            break
        num1 = float(input("Enter first number: "))
        num2 = float(input(" Enter second number"))

        if choice == "1":
            print(f"Answer: {num1 + num2}")

        elif choice == "2":
            print(f"Answer: {num1 - num2}")

        elif choice == "3":
            print(f"Answer: {num1 * num2}")

        elif choice == "4":
            if num2 == 0:
                print("error")
                continue
            print(f"Answer: {num1 / num2}")

        else:
            print("invalid option.")

    calculator()
