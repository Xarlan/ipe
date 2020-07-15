import flask


def get_all_projects():
    user = {'username': 'Team'}
    return flask.render_template('index.html', title='begin', user=user)


def create_project():
    return 'OK'


def edit_project():
    return 'OK'


def delete_project():
    return 'OK'
