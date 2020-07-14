import flask

from webui import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Team'}
    return flask.render_template('index.html', title='begin', user=user)