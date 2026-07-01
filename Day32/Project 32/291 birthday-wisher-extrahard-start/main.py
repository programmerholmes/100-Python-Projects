##################### Extra Hard Starting Project ######################

# 1. Update the birthdays.csv

# 2. Check if today matches a birthday in the birthdays.csv

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv

# 4. Send the letter generated in step 3 to that person's email address.


import smtplib
import datetime
import random
import pandas


my_email = "YOUR_EMAIL@gmail.com"
password = "YOUR_PASSWORD"

now = datetime.datetime.now()
weekday = now.weekday()
print(weekday)
birthday_month = now.month
print(birthday_month)
day = now.day
print(day)

data = pandas.read_csv("birthdays.csv")
print(data)
# print(data["month"] == 7)
# print(data[data["month"] == 7])

email_list = data["email"].to_list()


names_list = data["name"].to_list()
print(names_list)

month_list = data["month"].to_list()
print("the months are: ", month_list)

day_list = data["day"].to_list()
print("the days are: ", day_list)
letter = ["letter_templates/letter_1.txt", "letter_templates/letter_2.txt", "letter_templates/letter_3.txt"]

for i in range(len(month_list)):
    if month_list[i] == birthday_month and day_list[i] == day:
        select = random.choice(letter)
        with open(select, "r") as f:
            greets = f.read()
            mission = greets.replace("[NAME]", names_list[i])
            print(mission)

        # with smtplib.SMTP("smtp.gmail.com") as connection:
        #     connection.starttls()
        #     connection.login(user=my_email, password=password)
        #     connection.sendmail(from_addr=my_email,
        #                         to_addrs=email_list[i],
        #                         msg=f"Subject: Happy Birthday\n\n {mission}")
        #
