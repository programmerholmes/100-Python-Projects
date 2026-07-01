student_heights = input("Input a list of student heights ").split()
for n in range(0, len(student_heights)):
    student_heights[n] = int(student_heights[n])
print(student_heights)

sum = 0
for i in range(0, len(student_heights)):   # or for i in student_heights:
    sum = sum + student_heights[i]
print(i + 1)

average_height = sum / (i + 1)
print(round(average_height, 2))