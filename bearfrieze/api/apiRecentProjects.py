import falcon, json, rethinkdb as r

'''
Set HTTP access control (CORS) headers
https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS
https://github.com/falconry/falcon/issues/303
'''

def corsMiddleware(request, response, params):
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Headers', 'Content-Type')
    response.set_header('Access-Control-Allow-Methods', 'GET')

class RecentProjects:

    def __init__(self, connection):
        self.connection = connection

    def on_get(self, req, resp):
        filter = (req.get_param('filter') or 'launched').capitalize()
        limit = req.get_param_as_int('limit') or 1
        projects = r.table('projectsRecently%s' % filter) \
            .order_by(r.desc('launched_at')) \
            .limit(limit) \
            .run(self.connection)
        resp.body = json.dumps(projects)

connection = r.connect('52.28.17.23', 28015, db='kickstarter')
api = falcon.API(before=[corsMiddleware])
api.add_route('/recentProjects', RecentProjects(connection))
