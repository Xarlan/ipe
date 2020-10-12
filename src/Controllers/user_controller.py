from src.db.entities import db, User
import flask
from flask_login import login_user, current_user


def register_new_user(name, email, password, role):
    try:
        user = User(user_name=name, email=email, pass_hash=password, user_role=role)
        db.session.add(user)
        db.session.commit()
        print("Success")
    except Exception as e:
        print(e)


def get_login_page():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('get_many_projects'))
    return flask.render_template('login.html', title="Login", page="login")


def authenticate(req):
    req_body = req.get_json()
    email = str(req_body['email'])
    password = str(req_body['password'])
    user = db.session.query(User).filter(User.email == email).first()
    if user and user.check_password(password):
        login_user(user, remember=True)
        # for permanent authentication
        # flask.session.permanent = True
        return flask.make_response(flask.jsonify({"status": 1}), 200)
    else:
        return flask.make_response(flask.jsonify({"status": 2, "msg": "Incorrect user or password"}), 200)


def delete_user(email):
    try:
        user = db.session.query(User).filter(User.email == email).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            print("User successfully deleted")
    except Exception as e:
        print(e)


def change_passwd(email, password):
    try:
        user = db.session.query(User).filter(User.email == email).first()
        user.set_password(password)
        db.session.commit()
        print("Password changed")
    except Exception as e:
        print(e)
