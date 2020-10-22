from src.webui import app, login_manager
import src.Controllers.project_controller as project
import src.Controllers.vulnerability_controller as vulnerability
import src.Controllers.attachment_controller as attachment
import src.Controllers.report_controller as report
import src.Controllers.user_controller as user
from flask import request, redirect, url_for
from flask_login import login_required, logout_user


# Projects
@app.route('/', methods=['GET'], defaults={'limit': 50, 'page': 1})
@app.route('/projects/', methods=['GET'], defaults={'limit': 50, 'page': 1})
@app.route('/projects/<int:limit>/', methods=['GET'], defaults={'page': 1})
@app.route('/projects/<int:limit>/<int:page>', methods=['GET'])
@login_required
# name of function the same as name of Controller method
def get_many_projects(limit, page):
    return project.get_many_projects(limit, page)


@app.route('/project/<int:id>')
@login_required
def get_project(id):
    return project.get_project(id)


@app.route('/api/createProject', methods=['POST'])
@login_required
def create_project():
    return project.create_project(request)


@app.route('/api/editProject', methods=['POST'])
@login_required
def edit_project():
    return project.edit_project(request)


@app.route('/api/deleteProject/', methods=['POST'])
@login_required
def delete_project():
    return project.delete_project(request)


# Host
@app.route('/scope/<int:id>')
@login_required
def get_scope(id):
    return project.get_scope(id)


@app.route('/api/project/importScope', methods=['POST'])
@login_required
def import_scope():
    return project.import_project_scope(request)


@app.route('/api/project/deleteScope', methods=['POST'])
@login_required
def delete_scope():
    return project.delete_from_scope(request)

# Vulnerability
@app.route('/vulnerability/<int:id>')
@login_required
def get_vulnerability(id):
    return vulnerability.get_vulnerability(id)


@app.route('/api/createVulnerability', methods=['POST'])
@login_required
def create_vulnerability():
    return vulnerability.create_vulnerability(request)


@app.route('/api/deleteVulnerability', methods=['POST'])
@login_required
def delete_vulnerability():
    return vulnerability.delete_vulnerability(request)


@app.route('/api/editVulnerability', methods=['POST'])
@login_required
def edit_vulnerability():
    return vulnerability.edit_vulnerability(request)


# Attachment
@app.route('/api/uploadFile', methods=['POST'])
@login_required
def upload_file():
    return attachment.upload_file(request)


@app.route('/api/getAttach/<filename_id>', methods=['GET'])
@login_required
def get_attach(filename_id):
    return attachment.get_attach(filename_id)


@app.route('/api/deleteAttach/', methods=['POST'])
@login_required
def delete_attach():
    return attachment.delete_attach(request)

# Report
@app.route('/report/vuln/<project_id>')
@login_required
def generate_report_vuln(project_id):
    return report.generate_report(project_id, 1)


@app.route('/report/host/<project_id>')
@login_required
def generate_report_host(project_id):
    return report.generate_report(project_id, 2)


@app.route('/report/user/<project_id>')
@login_required
def generate_report_user(project_id):
    return report.generate_report(project_id, 3)


# User
@app.route('/login/')
def get_login_page():
    return user.get_login_page()


@app.route('/authenticate', methods=['POST'])
def authenticate():
    return user.authenticate(request)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("get_login_page"))


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for("get_login_page"))


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("get_login_page"))