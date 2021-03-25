import requests
import json

response = requests.get(
    "https://smart-reminder-web-app-ztisgbssmq-el.a.run.app/schedule")

with open("./data.json", "w") as file:
    file.write(json.dumps(response.json()))
