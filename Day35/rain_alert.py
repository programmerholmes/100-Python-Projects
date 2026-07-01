import requests
import os
from twilio.rest import Client

# api_key = "YOUR_OWM_API_KEY"
api_key = os.environ.get("OWM_API_KEY")
account_sid = "YOUR_TWILIO_ACCOUNT_SID"
# auth_token = "YOUR_TWILIO_AUTH_TOKEN"
auth_token = os.environ.get("AUTH_TOKEN")

parameters = {

    "lat": 34.052235,
    "lon": -118.243683,
    "appid": api_key,
    # "exclude":,        can also be used
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/weather", params=parameters)
response.raise_for_status()
print(response.status_code)
data = response.json()
print(data)
weather_id = data["weather"][0]["id"]
print(weather_id)

if weather_id < 801:
    # client = Client(account_sid, auth_token)
    # message = client.messages \
    #     .create(
    #     body="It's going to rain today, Remember to bring an ☔",
    #     from_='YOUR_TWILIO_NUMBER',    # MY TWILIO NUMBER
    #     to='+1234567890'         # RECIPIENT'S NUMBER
    # )

    # print(message.status)
    print("hello")