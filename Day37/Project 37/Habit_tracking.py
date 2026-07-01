import requests
from datetime import datetime


USERNAME = "YOUR_PIXELA_USERNAME"
TOKEN = "YOUR_PIXELA_TOKEN"
GRAPH_ID = "graph1"

pixela_endpoint = "https://pixe.la/v1/users"

user_params = {

    "token":TOKEN,
    "username":USERNAME,
    "agreeTermsOfService":"yes",
    "notMinor":"yes"
}

# response = requests.post(url=pixela_endpoint, json= user_params)
# print(response.text)

graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graph_config = {

    "id" : GRAPH_ID,
    "name": "Meditation graph",
    "unit": "mins",
    "type": "float",
    "color": "shibafu"
}

headers = {
    "X-USER-TOKEN": TOKEN
}

# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# print(response.text)

pixel_creation_endpoint = f"{graph_endpoint}/{GRAPH_ID}"
# OR pixel_creation_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"        Same thing

today = datetime.now()  # for yesterday datetime(year=2025, month=8, day=10)
# print(today.strftime("%Y%m%d"))


pixel_config = {

    "date": today.strftime("%Y%m%d"),
    "quantity": input("How many minutes did you meditate today? "),
}

response = requests.post(url=pixel_creation_endpoint, json=pixel_config, headers=headers)
print(response.text)

update_pixel_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{today.strftime('%Y%m%d')}"

update_pixel_config = {
    "quantity": "8"
}

# response = requests.put(url=update_pixel_endpoint, json=update_pixel_config, headers=headers)
# print(response.text)


delete_pixel_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{today.strftime('%Y%m%d')}"

# response = requests.delete(url=delete_pixel_endpoint, headers=headers)
# print(response.text)