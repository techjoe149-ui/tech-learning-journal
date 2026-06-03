# grade_system.py

def calculate_average(scores):
    return sum(scores) / len(scores)

def determine_grade(average):

    if average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"