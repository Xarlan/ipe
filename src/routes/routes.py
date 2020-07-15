from src.webui import app
import src.Controllers.project_controller as project

# Projects


@app.route('/')
# name of function the same as name of Controller method
def get_all_projects():
    return project.get_all_projects()


@app.route('/creteProject', methods=['POST'])
def create_project():
    return project.create_project()


@app.route('/editProject', methods=['POST'])
def edit_project():
    return project.edit_project()


# Host


# Vulnerability
