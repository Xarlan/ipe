import flask
from src.db.entities import Project, db
from datetime import date


def get_all_projects():
    user = {'username': 'Team'}
    return flask.render_template('index.html', title='begin', user=user)


def create_project(req):
    try:
        req_body = req.get_json()

        # Make some sanitize of data
        name = req_body['name']
        description = req_body['description']
        date_from = date.fromtimestamp(int(req_body['date_from']))
        date_to = date.fromtimestamp(int(req_body['date_to']))
        host_history = int(req_body['host_history'])
        retro_delete = int(req_body['retro_delete'])
        scope_hosts = req_body['scope_hosts']

        project = Project(name=name, description=description, date_from=date_from, date_to=date_to,
                          host_history=host_history, retro_delete=retro_delete, scope_hosts=scope_hosts)

        try:
            db.session.add(project)
            db.session.commit()
            return flask.Response(response='{"data": "Project created"}',
                                  status=200,
                                  mimetype="application/json")

        except:
            return "Error occured!!!"
    except:
        return "Error occured!!!"


def edit_project():
    return 'OK'


def delete_project():
    return 'OK'
