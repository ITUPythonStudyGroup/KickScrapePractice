'''
Scrape the most recent Kickstarter projects and insert them into the database.
Depending on which filter is chosen, recent will mean something different. One
filter might scrape the most recently launched projects, while another might
scrape the ones that were recently funded.

Note that this scraper will create create missing tables and indexes.

A filter name must be supplied as first argument. See the FILTERS dictionary
below for available filters.

A number of minutes must be supplied as a second argument. The scraper should
stop when it reaches a project that is older than the number of minutes.
'''

import sys, time, requests, json, rethinkdb as r

'''
The scraper uses Kickstarters unofficial API.

GUI for constructing queries:
https://www.kickstarter.com/discover/advanced

Relevant Github issue:
https://github.com/markolson/kickscraper/issues/16#issuecomment-31409151
'''

BASE = 'http://www.kickstarter.com/discover/advanced?%s'
FILTERS = {
    'launched': {
        'url': BASE % 'sort=newest&format=json&page=%d',
        'break': 'launched_at',
        'table': 'projectsRecentlyLaunched',
        'indexes': ['launched_at']
    },
    'funded': {
        'table': 'projectsRecentlyFunded',
        'url': BASE % 'state=successful&sort=end_date&format=json&page=%d',
        'break': 'deadline',
        'indexes': ['deadline']
    }
}

args = sys.argv[1:]
if len(args) < 2: sys.exit('ERROR: Insufficient number of arguments!')
f = FILTERS[args[0]]
stop = int(time.time()) - int(args[1]) * 60

'''
Here we connect to the database and ensure that the table is created and have
the desired indexes. Note that exceptions are going to be thrown on successful
runs where the table and indexes already exist, and thus we are not interested
in doing anything with the exceptions besides catching them.

https://rethinkdb.com/api/python/table_create/
https://rethinkdb.com/api/python/index_create/
'''

c = r.connect("52.28.17.23", 28015, db='kickstarter')
try: r.table_create(f['table']).run(c)
except r.ReqlRuntimeError: pass
for index in f['indexes']:
    try: r.table(f['table']).index_create(index).run(c)
    except r.ReqlRuntimeError: pass

'''
Here we are doing the actual scraping. When we reach a project that is less
recent than the previously specified number of minutes we stop scraping.

We are handling conflicts by updating any overlapping records. I'm not certain
this is necessarily optimal, but it works for now.
'''

page = 1
while True:

    response = requests.get(f['url'] % page)
    if response.status_code != 200: break
    data = json.loads(response.text)

    for project in data['projects']: print(project['name'])

    result = r.table(f['table']) \
        .insert(data['projects'], conflict="update") \
        .run(c)
    print(result)

    if data['projects'][-1][f['break']] < stop: break
    page += 1
