# main.py

import student_data

from calculations import calculate_average
from calculations import calculate_grade
from display import display_skills
from display import display_profile

from utilities import check_skill
from constants import COUNTRY
from constants import PASS_MARK


def main():

    print("==== STUDENT TECH PROFILE SYSTEM ====\n")

    python_score = student_data.python_score
    sql_score = student_data.sql_score
    average = calculate_average(python_score, sql_score)
    grade = calculate_grade(average)

    print("student name : ", student_data.student_name)
    print("age: ", student_data.student_age)
    print("COUNTRY: ", COUNTRY)
    print("Average score: ", average)
    print("Grade: ", grade)
    print("Pass Mark: ", PASS_MARK)

    display_skills(student_data.skills)
    display_profile(student_data.student_profile)
    has_python = check_skill("Python", student_data.skills)

    print("\n Has Python Skill: ", has_python)
    print("\n Program Finished Successfully.")

    if __name__ == "__main__":
        main()
