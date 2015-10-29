import schedule, time, datetime, os, sys, logging, rethinkdb as r
import scrapeRecentProjects, scrapeLiveProjects

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

def logScrape(log, f):
    try:
        f()
        log['done'] = logStamp()
    except Exception as e:
        log['fail'] = logStamp()
        log['exception'] = str(e)
    finally:
        r.table(LOGTABLE).insert(log).run(connection)

def logRecentScrape(filter, minutes):
    log = {
        'filter': filter,
        'minutes': minutes,
        'start': logStamp(),
    }
    logScrape(log, lambda: scrapeRecentProjects.scrape(filter, minutes))

def scrapeLive():
    log = {'start': logStamp()}
    logScrape(log, lambda: scrapeLiveProjects.scrape())

# https://github.com/dbader/schedule/issues/55
schedule.every().hour.at('00:00').do(lambda: logRecentScrape('launched', 65))
schedule.every().hour.at('00:05').do(lambda: logRecentScrape('funded', 65))
schedule.every().hour.at('00:10').do(scrapeLive)

while True:
    schedule.run_pending()
    time.sleep(1)
