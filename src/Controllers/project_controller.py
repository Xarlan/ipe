import flask
from src.db.entities import Project, db, Host, Vulnerability
from datetime import date
import ipaddress
import validators


def get_many_projects(limit=50, page=0):
    try:
        # TODO: make logic of pagination
        projects = Project.query.order_by(Project.id.desc()).offset(int(limit)*abs(int(page))).limit(int(limit)).all()
        return flask.render_template('index.html', title='Projects', page="project", layer=1, projects=projects)
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
    importing_domains = []
    existing_ips = []
    existing_domains = []
    hosts = []

    for host in scope_hosts:
        if validators.domain(str(host)):
            importing_domains.append(str(host))
        else:
            # that is for converting ipv6 like 2dfc:0:0:0:0217:cbff:fe8c:0 to 2dfc::217:cbff:fe8c:0
            importing_ips.append(str(ipaddress.ip_address(host)))

    try:
        existing_hosts = Host.query.filter_by(project_id=project_id).all()
        for host in existing_hosts:
            if host.domain and validators.domain(host.domain):
                existing_domains.append(host.domain)
            else:
                existing_ips.append(host.ip)

        # get only unique ip addresses and domains in new list
        new_ips = list(set(importing_ips) - set(existing_ips))
        new_domains = list(set(importing_domains) - set(existing_domains))

        for ip in new_ips:
            hosts.append(Host(project_id=int(project_id), ip=ip.strip()))

        for domain in new_domains:
            hosts.append(Host(project_id=int(project_id), domain=domain.strip()))

        db.session.add_all(hosts)
        db.session.commit()
        return flask.make_response(flask.jsonify({"status": 1}), 200)
    except:
        return flask.make_response(flask.jsonify({"status": 0, "error": "Error during importing scope"}), 500)


#   Scope delete (single and multiple)
def delete_from_scope(req):
    req_body = req.get_json()
    project_id = int(req_body['project_id'])
    hosts_for_delete = list(req_body['delete_hosts'])
    ips_for_delete_prepared = []
    domains_for_delete_prepared = []

    #  deleting spaces from addresses
    for host in hosts_for_delete:
        if validators.domain(str(host).strip()):
            domains_for_delete_prepared.append((host.strip()))
        else:
            ips_for_delete_prepared.append(host.strip())

    try:
        search_ips = []
        search_domains = []
        if ips_for_delete_prepared:
            search_ips = Host.query.filter(Host.project_id == project_id, Host.ip.in_(ips_for_delete_prepared)).all()
        if domains_for_delete_prepared:
            search_domains = Host.query.filter(Host.project_id == project_id, Host.domain.in_(domains_for_delete_prepared)).all()

        for host in search_ips + search_domains:
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
    vulns = Vulnerability.query.order_by(Vulnerability.id.asc()).all()
    # return flask.render_template('vulnerabilities.html', title=project.name, project=project, vulns=vulns)
    return flask.render_template('vulnerabilities.html', title=project.name, page="vulns", layer=2, project=project, project_id=project.id, vulns=vulns)


def get_scope(id):
    scope = Host.query.filter_by(project_id=id).all()
    return flask.render_template('scope.html', title="Scope", scope=scope, page="scope", layer=2, project_id=id)
