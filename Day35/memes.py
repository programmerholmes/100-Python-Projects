import requests

response = requests.get(url="https://api.chucknorris.io/jokes/random")
response.raise_for_status()
data = response.json()
print(data)

