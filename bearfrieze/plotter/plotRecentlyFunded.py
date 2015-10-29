import matplotlib.pyplot as plt, rethinkdb as r

connection = r.connect('52.28.17.23', 28015, db='kickstarter')
projects = r.db('kickstarter') \
    .table('projectsRecentlyFunded') \
    .order_by(index=r.desc('deadline')) \
    .pluck('goal', 'pledged') \
    .run(connection)
projects = list(projects)

x = [project['goal'] for project in projects]
y = [project['pledged'] / project['goal'] for project in projects]
plt.loglog(x, y, 'o')
plt.gca().set_ylim([0, 100])
plt.grid(True, which='both')
plt.show()
