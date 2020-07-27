import flask
from src.db.entities import Project, db, Host, Vulnerability
from datetime import date
import ipaddress


def get_many_projects(limit=50, page=0):
    try:
        # TODO: make logic of pagination
        projects = Project.query.order_by(Project.id.desc()).offset(int(limit)*abs(int(page))).limit(int(limit)).all()
        return flask.render_template('projects.html', title='projects', projects=projects)
    except:
        return "Error occured!!!"


def create_project(req):
    try:
        req_body = req.get_json()

        name = req_body['name']
        description = req_body['description']
        date_from = date.fromtimestamp(int(req_body['date_from']))
        date_to = date.fromtimestamp(int(req_body['date_to']))
        host_history = int(req_body['host_history'])
        retro_delete = int(req_body['retro_delete'])

        project = Project(name=name, description=description, date_from=date_from, date_to=date_to,
                          host_history=host_history, retro_delete=retro_delete)

        try:
            db.session.add(project)
            db.session.commit()
            return flask.make_response(flask.jsonify({"status": 1, "data": "Project created"}), 200)

        except:
            return flask.make_response(flask.jsonify({"status": 0, "error": "Error during creating project"}), 500)
    except:
        return flask.make_response(flask.jsonify({"status": 0, "error": "Incorrect input data"}), 500)


#   Scope import new and update
def import_project_scope(req):
    req_body = req.get_json()
    project_id = int(req_body['project_id'])
    scope_hosts = req_body['scope_hosts'].splitlines()
    importing_ips = []
    existing_ips = []
    hosts = []

    for ip in scope_hosts:
        # that is for converting ipv6 like 2dfc:0:0:0:0217:cbff:fe8c:0 to 2dfc::217:cbff:fe8c:0
        importing_ips.append(str(ipaddress.ip_address(ip)))

    try:
        existing_hosts = Host.query.filter_by(project_id=project_id).all()
        for ip in existing_hosts:
            existing_ips.append(ip.value)

        # get only unique ip addresses in new list
        new_hosts = list(set(importing_ips) - set(existing_ips))

        for ip in new_hosts:
            hosts.append(Host(project_id=int(project_id), value=ip.strip()))

        db.session.add_all(hosts)
        db.session.commit()
        # TODO: then add the same hosts in tables HOST_RECON
        return flask.make_response(flask.jsonify({"status": 1}), 200)
    except:
        return flask.make_response(flask.jsonify({"status": 0, "error": "Error during importing scope"}), 500)


#   Scope delete (single and multiple)
def delete_from_scope(req):
    req_body = req.get_json()
    project_id = int(req_body['project_id'])
    hosts_for_delete = list(req_body['delete_hosts'])
    ips_for_delete_prepared = []

    #  deleting spaces from ip addresses
    for ip in hosts_for_delete:
        ips_for_delete_prepared.append(ip.strip())

    try:
        search_hosts = Host.query.filter(Host.project_id == project_id, Host.value.in_(ips_for_delete_prepared)).all()
        for host in search_hosts:
            db.session.delete(host)
        db.session.commit()
        # TODO: then delete the same ip in tables HOST_RECON and HOSTS_HISTORY
        return flask.make_response(flask.jsonify({"status": 1}), 200)
    except:
        return flask.make_response(flask.jsonify({"status": 0, "error": "Error during deleting hosts"}), 500)


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
    vulns = Vulnerability.query.order_by(Vulnerability.id.desc()).all()
    return flask.render_template('project.html', title='project', project=project, vulns=vulns)
