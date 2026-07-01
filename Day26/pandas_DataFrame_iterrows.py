import pandas

student_score = {
    "student": ["Angela","mike","tyson"],
    "score": [56, 80, 98]
}

print(student_score)

student_data_frame = pandas.DataFrame(student_score)

print(student_data_frame)

for (key, value) in student_data_frame.items():
    print(key)
    print(value)

for (index, row) in student_data_frame.iterrows():
    print(index)
    print(row)
    print(row.student)
    print(row.score)

