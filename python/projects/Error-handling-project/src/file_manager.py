# file manager.py

def save_balance(balance):

    with open("balance.txt", "w") as file:
        file.write(str(balance))


def load_balance():

    try:

        with open("balance.txt", "r") as file:

            return float(file.read())

    except FileNotFoundError:

        return 1000
