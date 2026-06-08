# multiplication game.py

import random


def multiplication_game():

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
