import requests
import datetime
import smtplib
import time

MY_lat = 34.052235
MY_LONG = -118.243683
MY_EMAIL = "your_email@example.com"
PASS = "YOUR_PASSWORD"

def iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    # if response.status_code == 400:
    #     raise Exception("That resource does not exist.")
    # elif response.status_code == 401:
    #     raise Exception("You are not authorised to access this data.")
    # INSTEAD

    response.raise_for_status()

    data = response.json()
    longitude = float(data["iss_position"]["longitude"])
    latitude = float(data["iss_position"]["latitude"])

    iss_position = (longitude, latitude)
    print(f"The ISS location is: {iss_position}")

    if MY_lat - 5 <= latitude <= MY_lat + 5 and MY_LONG - 5 <= longitude <= MY_LONG + 5:
        return True


def is_night():
    parameters = {
        "lat": MY_lat,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    print(data)
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    print(sunrise)
    print(sunset)

    now = datetime.datetime.now().hour
    #print(now)
    #print(now.hour)

    if now >= sunset or now <= sunrise:
        return True


while True:
    time.sleep(60)
    if iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIL, PASS)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL,
                            msg="Subject:Look Up\n\nThe ISS is above you in the sky.")
