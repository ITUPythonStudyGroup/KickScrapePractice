import rethinkdb as r
import json
import requests

statusCode = 200
page = 1

# Scraping stuff

while statusCode == 200:
    response = requests.get("https://www.kickstarter.com/projects/search.json?search=&term=&page=" + page.__str__())
    text = response.text

    jsonParsed = json.loads(text)
    print(json.dumps(jsonParsed, indent=4))

    statusCode = response.status_code
    page += 1;
    statusCode = 300

# Database stuff
conn = r.connect("52.28.17.23", 28015, db='kickstarter')
r.table("projects").insert(jsonParsed).run(conn)

