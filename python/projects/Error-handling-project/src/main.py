# main.py

from bank import deposit, withdraw

from file_manager import (
    load_balance,
    save_balance

)

from custom_exceptions import (

    InvalidAmountError,
    InsufficientFundsError
)


def menu():

    print("\n=== BANKING SYSTEM ===")
    print("1. Deposit")
    print("2. withdraw")
    print("3. View Balance")
    print("4. Exit")


balance = load_balance()

while True:

    menu()

    choice = input("Choose option: ")

    if choice == "3":

        print(f"Balance: {balance}")

    elif choice == "1":

        try:

            amount = float(input("Deposit amount:"))

            balance = deposit(balance, amount)

            save_balance(balance)

            print("Deposit successful.")

        except ValueError:

            print("Numbers only.")

        except InvalidAmountError as error:

            print(error)

    elif choice == "2":

        amount = float(input("withdrawal amount: "))

        balance = withdraw(balance, amount)

        save_balance(balance)

        print("withdrawal successful.")

    elif choice == "4":

        print("Thank you for banking with us .")
        break

    else:
        print("Invalid option.")
