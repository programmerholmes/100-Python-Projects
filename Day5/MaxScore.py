student_scores = input("Input a list of student score: ").split()

for i in range(0, len(student_scores)):
    student_scores[i] = int(student_scores[i])
print(student_scores)
print(type(student_scores))

max = 0

for score in range(0, len(student_scores)):
    if max < student_scores[score]:
        max = student_scores[score]

print(f"The highest score in the class is: {max}")