import schedule, time, os, sys, logging
from scrapeRecentProjects import scrape

def scrapeLaunched(): scrape('launched', 65)
def scrapeFunded(): scrape('funded', 65)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

schedule.every().hour.do(scrapeLaunched)
schedule.every().hour.do(scrapeFunded)

schedule.run_all()

while True:
    schedule.run_pending()
    time.sleep(1)
