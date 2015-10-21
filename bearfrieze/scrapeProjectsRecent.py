'''
Scrape the most recently launched Kickstarter projects and insert them into the
database.

An ISO 8601 date may be given as first argument. The scraper should stop when it
reaches a project that was launched before that date.

If no arguments are supplied the scraper should run until it reaches a project
that was launched before the newest project in the database.
'''

import sys, moment, requests, json, rethinkdb as r

connection = r.connect("52.28.17.23", 28015, db='kickstarter')

stop = 0
args = sys.argv[1:]
if len(args):
    stop = moment.date(args[0], '%Y-%m-%d').epoch()
else:
    stop = r.table('projectsRecent') \
        .order_by(r.desc('launched_at')) \
        .pluck('launched_at') \
        .limit(1) \
        .run(connection)[0]['launched_at']

# https://github.com/markolson/kickscraper/issues/16#issuecomment-31409151
urlProjects = 'http://www.kickstarter.com/discover/recently-launched?format=json&page=%d'
page = 1

while True:

    response = requests.get(urlProjects % page)
    if response.status_code != 200: break
    data = json.loads(response.text)

    for project in data['projects']: print(project['name'])

    result = r.table('projectsRecent') \
        .insert(data['projects'], conflict="update") \
        .run(connection)
    print(result)

    if data['projects'][-1]['launched_at'] < stop: break
    page += 1
