import schedule, time, datetime, os, sys, logging, rethinkdb as r
from scrapeRecentProjects import scrape

LOGTABLE = 'logScrape'

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

connection = r.connect("52.28.17.23", 28015, db='kickstarter')
try: r.table_create(LOGTABLE).run(connection)
except r.ReqlRuntimeError: pass

def logStamp():
    return {
        'iso': datetime.datetime.utcnow().isoformat(),
        'epoch': int(time.time()),
    }
def logScrape(filter, minutes):
    log = {
        'filter': filter,
        'minutes': minutes,
        'start': logStamp(),
    }
    try:
        scrape(filter, minutes)
        log['done'] = logStamp()
    except Exception as e:
        log['fail'] = logStamp()
        log['exception'] = str(e)
    finally:
        r.table(LOGTABLE).insert(log).run(connection)

def scrapeLaunched():
    logScrape('launched', 65)
def scrapeFunded():
    logScrape('funded', 65)

schedule.every().hour.do(scrapeLaunched)
schedule.every().hour.do(scrapeFunded)

schedule.run_all()

while True:
    schedule.run_pending()
    time.sleep(1)
