import json
import urllib.request
import rethinkdb as r

r.connect("52.28.17.23", 28015, db='kickstarter').repl()

def scrape(start,end):
    for page in range(start, end):
        url = "https://www.kickstarter.com/projects/search.json?search=&term=&page=" + str(page)
        jsonString = urllib.request.urlopen(url).read().decode("utf-8")
        jsonParsed = json.loads(jsonString)
        insert2db(jsonParsed['projects'])


def insert2db(projects): #expects a list of project dictionaries
    result = r.table('projects').insert(projects, conflict="update").run()
    print(result)

def printIds():
    cursor = r.table("projects").pluck('id').run()
    for document in cursor:
        print(document["id"])

def printProjectURLs():
    cursor = r.table("projects").pluck('urls').run()
    for document in cursor:
        print(document["urls"]["web"]["project"])

# scrape(0,200)
printIds()
printProjectURLs()
