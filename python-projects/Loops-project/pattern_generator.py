# pattern_generation.py


def pattern_generation():

    rows = int(input("Enter number of rows: "))

    for i in range(rows):

        for j in range(i + 1):
            print("*", end=" ")

        print()
