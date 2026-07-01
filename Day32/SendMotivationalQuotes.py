import smtplib
import datetime
import random

# my_email = "YOUR_EMAIL@gmail.com"
# password = "YOUR_PASSWORD"

day = datetime.datetime.now()
today = day.weekday()
print(today)

if today == 0:
    with open("quotes.txt", "r") as f:
        all_quotes = f.readlines()
        quote = random.choice(all_quotes)
        print(quote)

        # with smtplib.SMTP("smtp.gmail.com") as connection:
        #     connection.starttls()
        #     connection.login(user=my_email, password=password)
        #     connection.sendmail(from_addr=my_email, to_addrs="RECIPIENT_EMAIL@gmail.com",
        #                         msg="Subject: Monday Motivation\n\n" + quote)
