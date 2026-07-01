import requests
from bs4 import BeautifulSoup
import lxml
import smtplib

AMAZON_URL = "https://www.amazon.com/Instant-Pot-Duo-Evo-Plus/dp/B07W55DDFB/ref=sr_1_1?qid=1597662463"
headers = {
    "accept_language": "en-US,en;q=0.9",
    "user_agent":	"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"

}

response = requests.get(url=AMAZON_URL, headers=headers)

amazon_webpage = response.text

soup = BeautifulSoup(amazon_webpage, "lxml")
# print(soup.prettify())


prices = soup.find_all(class_="a-offscreen")

price_list = []
for price in prices:
    pricing = price.getText().split('$')[1]
    price_list.append(pricing)

our_price = price_list[0]
print(our_price)

my_email = "your_email@example.com"
password = "YOUR_PASSWORD"



if (float(our_price) > 40):
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs=my_email, msg=f"Subject: You can buy now!\n\n {soup.title.text} is now $ {our_price} \n\n {AMAZON_URL}").encode("utf-8")
