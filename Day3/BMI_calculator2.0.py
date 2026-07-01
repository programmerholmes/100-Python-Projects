height = input("Enter your height in meters: ")
weight = input("Enter your weight in kilograms: ")


BMI = int(weight) / (float(height) ** float(height))
print(int(BMI))

if BMI < 18.5:
    print("You are underweight.")
elif (BMI >= 18.5) and BMI < 25:
    print("You have a normal weight.")
elif (BMI > 25) and BMI < 30:
    print("You are overweight.")
elif (BMI > 30) and BMI < 35:
    print("You are obese.")
elif BMI > 35:
    print("You are clinically obese.")
else:
    print("You are out of the league!")
