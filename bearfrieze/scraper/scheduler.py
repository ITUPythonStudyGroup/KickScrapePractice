import schedule, time, os
from scrapeRecentProjects import scrape

def scrapeLaunched(): scrape('launched', 65)
def scrapeFunded(): scrape('funded', 65)

schedule.every().hour.do(scrapeLaunched)
schedule.every().hour.do(scrapeFunded)

schedule.run_all()

while True:
    schedule.run_pending()
    time.sleep(1)
