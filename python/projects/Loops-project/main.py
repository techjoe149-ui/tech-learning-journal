# main.py

import time
from calculator import calculator
from password_checker import password_checker
from multiplication_game import multiplication_game
from pattern_generator import pattern_generation
from countdown_timer import countdown_timer
from helpers import line, app_title


def show_menu():

    line()

    print("\n==== LOOPS PROJECTS ====")
    print("1. calculator")
    print("2. password checker")
    print("3. multiplication game")
    print("4. pattern generator")
    print("5. countdown timer")
    print("6. exit")

    line()


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


def password_checker():
    while True:

        password = input("Create password: ")

        if len(password) < 8 and "does not have at least one capital letter":
            print("password incomplete")
            continue
        has_number = False

        for character in password:
            if character.isdigit():
                has_number = True

        if has_number:
            print("strong password.")
            break
        else:
            print("Password must contain a number and at least one capital letter.")


def multiplication_game():

    import random
    score = 0

    for round_number in range(5):

        number1 = random.randint(1, 10)
        number2 = random.randint(1, 10)

        answer = int(input(f"{number1} * {number2} = "))

        if answer == number1 * number2:
            print("correct!")
            score += 1

        else:
            print("wrong.")

        print(f"\nFinal Score: {score}/5")


def pattern_generator():

    rows = int(input("Enter number of rows: "))

    for i in range(rows):

        for j in range(i + 1):
            print("*", end=" ")

        print()


def countdown_timer():

    seconds = int(input("Enter countdown seconds: "))

    while seconds > 0:
        print(seconds)

        time.sleep(1)

        seconds -= 1

    print("TIME UP!")


def main():

    while True:

        print("\n===== LOOPS PROJECT =====")
        print("1. calculator")
        print("2. password checker")
        print("3. multiplication game")
        print("4. pattern generator")
        print("5. countdown timer")
        print("6. exit")

        choice = input("choose option: ")
        if choice == "1":
            calculator()

        elif choice == "2":
            password_checker()

        elif choice == "3":
            multiplication_game()

        elif choice == "4":
            pattern_generation()
        elif choice == "5":
            countdown_timer()

        elif choice == "6":
            print("see you next time !!")
            break

        else:
            print("invalid option.")


main()
