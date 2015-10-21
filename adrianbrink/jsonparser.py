import json
import requests

statusCode = 200
page = 0

while statusCode == 200:
    response = requests.get("https://www.kickstarter.com/projects/agfa/agfa-and-something-weird" + page.__str__())
    text = response.text

    jsonParsed = json.loads(text)
    print(json.dumps(jsonParsed, indent=4))

    statusCode = response.status_code
    page += 1

