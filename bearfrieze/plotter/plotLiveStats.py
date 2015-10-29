import time, matplotlib.pyplot as plt, rethinkdb as r

connection = r.connect('52.28.17.23', 28015, db='kickstarter').repl()
def getStats(p):
    return r.table('projectsLive') \
        .get_all(p['id'], index='id') \
        .pluck('scraped', 'pledged') \
        .order_by('scraped') \
        .coerce_to('array')

# projects = r.table('projectsRecentlyLaunched') \
#     .order_by(index=r.desc('deadline')) \
#     .between(r.minval, int(time.time()), index='deadline') \
#     .map(lambda p: {'project': p, 'stats': getStats(p)}) \
#     .run()

projects = r.table('projectsRecentlyLaunched') \
    .sample(2000) \
    .map(lambda p: {'project': p, 'stats': getStats(p)}) \
    .run()

def getLine(project, stats):
    duration = project['deadline'] - project['launched_at']
    return [
        list(map(lambda s: (s['scraped'][1] - project['launched_at']) / duration, stats)),
        list(map(lambda s: s['pledged'] / project['goal'], stats)),
    ]

for project in projects:
    if len(project['stats']) > 0:
        plt.plot(*getLine(**project))
plt.show()
