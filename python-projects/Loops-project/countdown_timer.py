# countdown_timer.py

import time


def countdown_timer():

    seconds = int(input("Enter countdown seconds: "))

    while seconds > 0:
        print(seconds)

        time.sleep(1)

        seconds -= 1

    print("TIME UP!")
