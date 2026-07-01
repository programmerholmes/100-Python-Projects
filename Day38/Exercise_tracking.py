import requests
from datetime import datetime
import os

#NUTRITIONIX_APP_ID = "YOUR_NUTRITIONIX_APP_ID"

#NUTRITIONIX_APP_KEY = "YOUR_NUTRITIONIX_API_KEY"

# Replacing the above with below because of environmental variables
APP_ID = os.environ["NUTRITIONIX_APP_ID"]
API_KEY = os.environ["NUTRITIONIX_APP_KEY"]

NUTRITIONIX_URL = "https://trackapi.nutritionix.com/v2/natural/exercise"

#SHEETY_ENDPOINT = "https://api.sheety.co/YOUR_SHEETY_ENDPOINT/copyOfMyWorkouts/workouts"

SHEETY_URL = os.environ["SHEETY_ENDPOINT"]

USERNAME = "YOUR_SHEETY_USERNAME"
PASSWORD = "YOUR_SHEETY_PASSWORD"

exercise_text = input("Tell me what exercise you did: ")
GENDER = "male"
WEIGHT = 65
HEIGHT = 180
AGE = 30

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE,

}

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}


response = requests.post(url=NUTRITIONIX_URL, json=parameters, headers=headers)
result = response.json()
print(result)

today = datetime.now().strftime("%d/%m/%Y")
time_now = datetime.now().strftime("%X")


# Even without the username and password, it's still working, just needs the authorization token.
headers = {
    # "username": USERNAME,
    # "password": PASSWORD,
    "Authorization": "Basic YOUR_BASE64_ENCODED_CREDENTIALS",
}

# result_user_input = response.json()["exercises"][0]["user_input"]
# result_duration_min = response.json()["exercises"][0]["duration_min"]
# result_nf_calories = response.json()["exercises"][0]["nf_calories"]

# The above is just for one but if we have more than 1 query then we should use loop and not the following

# result_user_input1 = response.json()["exercises"][1]["user_input"]
# result_duration_min1 = response.json()["exercises"][1]["duration_min"]
# result_nf_calories1 = response.json()["exercises"][1]["nf_calories"]



for exercise in result["exercises"]:
    sheet_inputs = {

        "workout": {
            "date": today,
            "time": time_now,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],

        }
    }
    sheety_response = requests.post(url=SHEETY_URL, json=sheet_inputs, auth=(USERNAME, PASSWORD),headers=headers)
    print(sheety_response.text)






