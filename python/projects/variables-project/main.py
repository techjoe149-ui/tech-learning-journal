# Student Grade Calculator

student_name = input("Enter student name: ")

math_marks = int(input("Math marks: "))
science_marks = int(input("science marks: "))
english_marks = int(input("english marks: "))

total = math_marks + science_marks + english_marks
average = total / 3

if average >= 80:
    grade = "A"
elif average >= 70:
    grade = "B"
elif average >= 60:
    grade = "C"
elif average >= 50:
    grade = "D"
else:
    grade = "E"
if average >= 50:
    status = "Pass"
else:
    status = "Fail"

print("\n--- RESULT ---")
print("student:", student_name)
print("Average:", average)
print("Grade:", grade)
print("status:", status)
