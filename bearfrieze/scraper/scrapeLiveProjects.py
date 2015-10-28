import sys, time, json, requests, rethinkdb as r

'''
There is quite a bit of stuff going on here. This is an attempt at summarizing.

We want to scrape all the live projects on Kickstarter. More specifically, we
want to scrape all these projects regularly to establish a timeline of their
progress.

The reason why we aren't scraping all the projects indivdually is that it would
be a ton of requests. There is currently ~6000 live projects, and scraping all
of those one by one would require at least 6000 requests. They probably wont be
happy about that, and making a ton of requests is not something we would like to
do (bad in terms of time and resources).

At the start I thought it was enought to query the projects ending
soon and then go through all the pages, but it turned out there was a page cap
at 200. With 20 projects per page, that was not sufficient.

The solution for now is to go through the main categories and go through the
pages for each category until projects that aren't live start to show up. That
seems to be working satisfactory.

To be continued.
'''

URL = 'http://www.kickstarter.com/discover/advanced?sort=end_date&format=json&category_id=%d&page=%d'
DB = {
    'host': '52.28.17.23',
    'port': 28015,
    'db': 'kickstarter',
}
TABLE = 'projectsLive'
PRIMARY = 'scraped'
INDEXES = ['launched_at', 'deadline']
CATEGORIES = [1, 3, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 26]

def addScraped(project):
    project['scraped'] = [project['id'], int(time.time())]
    return project

def scrape():

    connection = r.connect(**DB).repl()

    if TABLE not in r.table_list().run():
        r.table_create(TABLE, primary_key=PRIMARY).run()
    for index in (set(INDEXES) - set(r.table(TABLE).index_list().run())):
        r.table(TABLE).index_create(index).run()

    for category in CATEGORIES:
        page = 1
        while True:
            response = requests.get(URL % (category, page))
            if response.status_code != 200: break
            projects = json.loads(response.text)['projects']
            projects = list(map(addScraped, projects))
            live = list(filter(lambda p: p['state'] == 'live', projects))
            result = r.table(TABLE).insert(live, conflict="replace").run()
            if len(projects) != len(live): break
            page += 1
        print('Scraped %d pages for category %d' % (page, category))

    connection.close()

def main(argv):
    scrape()

if __name__ == "__main__":
    main(sys.argv)
