from src.webui import app
import src.Controllers.project_controller as project
import src.Controllers.vulnerability_controller as vulnerability
from flask import request

# Projects


@app.route('/projects/', methods=['GET'], defaults={'limit': 50, 'page': 0})
@app.route('/projects/<limit>/', methods=['GET'], defaults={'page': 0})
@app.route('/projects/<limit>/<page>', methods=['GET'])
# name of function the same as name of Controller method
def get_many_projects(limit, page):
    return project.get_many_projects(limit, page)


@app.route('/project/<int:id>')
def get_project(id):
    return project.get_project(id)


@app.route('/api/creteProject', methods=['POST'])
def create_project():
    return project.create_project(request)


@app.route('/api/editProject', methods=['POST'])
def edit_project():
    return project.edit_project(request)


@app.route('/api/deleteProject/', methods=['POST'])
def delete_project():
    return project.delete_project(request)


# Host
@app.route('/api/project/importScope', methods=['POST'])
def import_scope():
    return project.import_project_scope(request)


@app.route('/api/project/deleteScope', methods=['POST'])
def delete_scope():
    return project.delete_from_scope(request)

# Vulnerability
@app.route('/api/createVulnerability', methods=['POST'])
def create_vulnerability():
    return vulnerability.create_vulnerability(request)


@app.route('/api/deleteVulnerability', methods=['POST'])
def delete_vulnerability():
    return vulnerability.delete_vulnerability(request)


@app.route('/api/editVulnerability', methods=['POST'])
def edit_vulnerability():
    return vulnerability.edit_vulnerability(request)


# Attachments
