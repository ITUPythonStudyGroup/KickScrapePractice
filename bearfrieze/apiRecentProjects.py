import falcon, json, rethinkdb as r

class RecentProjects:

    def __init__(self, connection):
        self.connection = connection

    def on_get(self, req, resp):
        filter = req.get_param('filter').capitalize() or 'Launched'
        limit = req.get_param_as_int('limit') or 1
        projects = r.table('projectsRecently%s' % filter) \
            .order_by(r.desc('launched_at')) \
            .limit(limit) \
            .run(self.connection)
        resp.body = json.dumps(projects)

connection = r.connect("52.28.17.23", 28015, db='kickstarter')
api = falcon.API()
api.add_route('/recentProjects', RecentProjects(connection))
