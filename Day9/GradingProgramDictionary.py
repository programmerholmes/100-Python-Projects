student_scores = {
    "Harry": 81,
    "Ron": 78,
    "Hermione": 99,
    "Draco": 74,
    "Neville": 62,
}

student_grades = {}

for key in student_scores:
    if student_scores[key] > 90 and student_scores[key] < 101:
        student_grades[key] = "Outstanding"
    elif student_scores[key] > 80 and student_scores[key] < 91:
        student_grades[key] = "Exceeds Expectations"
    elif student_scores[key] > 70 and student_scores[key] < 81:
        student_grades[key] = "Acceptable"
    elif student_scores[key] <= 70:
        student_grades[key] = "Fail"

print(student_grades)


# Scores 91 - 100: Grade = "Outstanding"
#
# Scores 81 - 90: Grade = "Exceeds Expectations"
#
# Scores 71 - 80: Grade = "Acceptable"
#
# Scores 70 or lower: Grade = "Fail"