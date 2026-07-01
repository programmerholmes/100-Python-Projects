# names = ["Adil", "Basit", "Caroline", "Daud", "Ehtesham", "Fatima"]
# import random
# student_score = {student: random.randint(0, 100) for student in names}
#
# passed_students = {student: score for (student, score) in student_score.items() if score >= 60}
# print(passed_students)


# counting the letters in a word

sentence = "What is the Airspeed Velocity of an Unladen Swallow?"
new_sentence = sentence.split()

result = {key: len(key) for key in new_sentence}
print(result)


# converting celsuis into fahrenheit

weather_c = {
    "Monday": 12,
    "Tuesday": 14,
    "Wednesday": 15,
    "Thursday": 14,
    "Friday": 21,
    "Saturday": 22,
    "Sunday": 24,
}

weather_f = {key: (value * (9/5) + 32) for (key, value) in weather_c.items()}

print(weather_f)
