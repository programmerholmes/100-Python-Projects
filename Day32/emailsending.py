import smtplib

my_email = "YOUR_EMAIL@gmail.com"
password = "YOUR_PASSWORD"

with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()           # responsible for encrypting and securing connection
    connection.login(user=my_email, password=password)
    connection.sendmail(from_addr=my_email, to_addrs="RECIPIENT_EMAIL@gmail.com",
                        msg="Subject: Hello\n\nFirst mail like this, pretty cool huh?!!")
