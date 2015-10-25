import matplotlib.pyplot as plt
import rethinkdb as r

MAX = 10e4

connection = r.connect('52.28.17.23', 28015, db='kickstarter')
projects = r.db('kickstarter') \
    .table('projectsRecentlyFunded') \
    .order_by(index=r.desc('deadline')) \
    .pluck('goal', 'pledged') \
    .run(connection)
projects = list(projects)

# x = [project['goal'] for project in projects]
# y = [project['pledged'] for project in projects]
# plt.scatter(x,y)
# plt.plot([0, MAX], [0, MAX])
# plt.axis((0, MAX, 0, MAX))
# plt.gca().set_aspect('equal', adjustable='box')
# plt.grid(True)
# plt.show()

x = [project['goal'] for project in projects]
y = [project['pledged'] / project['goal'] for project in projects]
plt.loglog(x, y, 'o')
plt.gca().set_ylim([0, 100])
plt.grid(True, which='both')
plt.show()
