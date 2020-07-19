import flask
from src.db.entities import Project, db
from datetime import date


def get_many_projects(limit=50, page=0):
    try:
        projects = Project.query.order_by(Project.id.desc()).offset(int(limit)*abs(int(page))).limit(int(limit)).all()
        return flask.render_template('projects.html', title='projects', projects=projects)
    except:
        return "Error occured!!!"


def create_project(req):
    try:
        req_body = req.get_json()

        # TODO: Make some sanitize of data
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
            return flask.make_response(flask.jsonify({"data": "Project created"}), 200)

        except:
            return flask.make_response(flask.jsonify({"status": 0, "error": "Error during creating project"}), 500)
    except:
        return flask.make_response(flask.jsonify({"status": 0, "error": "Incorrect input data"}), 500)


def edit_project(req):
    try:
        req_body = req.get_json()
        project = Project.query.get(int(req_body['project_id']))

        project.name = req_body['name']
        project.description = req_body['description']
        project.date_from = date.fromtimestamp(int(req_body['date_from']))
        project.date_to = date.fromtimestamp(int(req_body['date_to']))
        project.host_history = int(req_body['host_history'])
        project.retro_delete = int(req_body['retro_delete'])
        project.scope_hosts = req_body['scope_hosts']

        try:
            db.session.commit()
            return flask.make_response(flask.jsonify({"status": 1}), 200)
        except:
            return flask.make_response(flask.jsonify({"status": 0, "error": "Error occured during editing project"}), 500)
    except:
        return flask.make_response(flask.jsonify({"status": 0, "error": "Incorrect input data"}), 500)



def delete_project(req):
    try:
        req_body = req.get_json()
        project_id = int(req_body['project_id'])
        project = Project.query.get_or_404(project_id)

        try:
            db.session.delete(project)
            db.session.commit()
            return flask.make_response(flask.jsonify({"status": 1}), 200)

        except:
            return flask.make_response(flask.jsonify({"status": 0, "error": "Error during deleting project"}), 500)

    except:
        return flask.make_response(flask.jsonify({"status": 0, "error": "Error occured during processing input data."}), 500)


def get_project(id):
    project = Project.query.get_or_404(id)
    return flask.render_template('project.html', title='project', project=project)