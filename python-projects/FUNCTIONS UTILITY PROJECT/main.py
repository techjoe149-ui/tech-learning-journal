# MAIN BRAIN

from calculator import add, subtract, multiply, divide

from converter import (
    celcius_to_fahrenheit,
    fahrenheit_to_celcius
)

from grade_system import (
    calculate_average,
    determine_grade
)

from password_checker import (
    check_password_strength
)

from utils import line, app_title


def show_menu():

    line()

    print("1. calculator")
    print("2. Temperature Converter")
    print("3. Grade System")
    print("4. password Checker")
    print("5. Exit")

    line()


def calculator_section():

    print("\n=== CALCULATOR ===")
    num1 = float(input("First number: "))
    num2 = float(input("Second number: "))

    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")

    choice = input("choose operation: ")

    if choice == "1":
        print(add(num1, num2))

    elif choice == "2":
        print(subtract(num1, num2))

    elif choice == "3":
        print(multiply(num1, num2))

    elif choice == "4":
        print(divide(num1, num2))

    else:
        print("invalid choice")


def converter_section():
    print("\n=== TEMPERATURE CONVERTER ===")

    print("1. celcius 'n Fahrenheit")
    print("2. Fahreinheit 'n Celcius")

    choice = input("choose option: ")

    if choice == "1":
        c = float(input("Enter Celcius: "))
        print("Result: ", celcius_to_fahrenheit)

    elif choice == "2":
        f = float(input("Enter Fahrenheit: "))
        print("Result: ", fahrenheit_to_celcius(f))

    else:
        print("invalid choice")


def grade_section():
    print("\n=== GRADE SYSTEM ===")
    scores = []

    for i in range(3):
        mark = float(input(f"Enter mark {i + 1}:"))

        scores.append(mark)

    avg = calculate_average(scores)
    grade = determine_grade(avg)

    print("Average: ", avg)
    print("Grade: ", grade)


def password_section():
    print("\n=== PASSWORD CHECKER ===")
    password = input("Enter password: ")
    result = check_password_strength(password)
    print("Strength: ", result)


def main():
    app_title()

    while True:

        show_menu()

        choice = input("select option: ")

        print("DEBUG:", choice)

        if choice == "1":
            calculator_section()

        elif choice == "2":
            converter_section()

        elif choice == "3":
            grade_section()

        elif choice == "4":
            password_section()

        elif choice == "5":
            print("Goodbye")
            break
        else:
            print("invalid option")


if __name__ == "__main__":

    main()
