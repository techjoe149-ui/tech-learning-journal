# calculations.py

def calculate_average(score1, score2):

    average = (score1 + score2) / 2

    return average


def calculate_grade(score):
    if score >= 70:
        return "A"
    elif score >= 60:
        return "B"
    elif score >= 50:
        return "C"
    else:
        return "Fail"
