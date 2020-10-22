from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import INET
import src.webui as webui
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from src.webui import login_manager

db = webui.db

# class for table Vuln_ref
class VulnRef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey('host.id', ondelete='CASCADE'))
    vuln_id = db.Column(db.Integer, db.ForeignKey('vulnerability.id', ondelete='CASCADE'))

    def __repr__(self):
        return '<VulnRef %r>' % self.id


#  Class for table host
class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'))
    ip = db.Column(INET, nullable=True)
    domain = db.Column(db.String, nullable=True)

    # relationships for CASCADE delete
    host = relationship(VulnRef, backref="host", cascade="all, delete", passive_deletes=True)

    def __repr__(self):
        return '<Host>'


class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=True)
    path = db.Column(db.String, nullable=False)
    filename = db.Column(db.String, nullable=False)
    vuln_id = db.Column(db.Integer, db.ForeignKey('vulnerability.id', ondelete='CASCADE'))

    def  __repr__(self):
        return '<Attachment>'


#  Class for table vulnerability
class Vulnerability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'))
    object = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    full_path = db.Column(db.String, nullable=False)
    criticality = db.Column(db.Integer, default=1)
    probability = db.Column(db.Integer, default=1)
    final_criticality = db.Column(db.Integer, default=1)
    description = db.Column(db.Text, nullable=False)
    risk = db.Column(db.Text, nullable=False)
    details = db.Column(db.Text, nullable=False)
    recommendation = db.Column(db.Text, nullable=False)
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    request = db.Column(db.Text, nullable=True)
    response = db.Column(db.Text, nullable=True)

    # relationships for CASCADE delete
    vuln_ref = relationship(VulnRef, backref="vulnerability", cascade="all, delete", passive_deletes=True)
    attach = relationship(Attachment, backref="vulnerability", cascade="all, delete", passive_deletes=True)

    def __repr__(self):
        return '<Vulnerability %r>' % self.id


#  Class for table project
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    date_from = db.Column(db.Date, nullable=False)
    date_to = db.Column(db.Date, nullable=False)
    host_history = db.Column(db.Integer, nullable=True)
    retro_delete = db.Column(db.Boolean, default=False)

    # relationships for CASCADE delete
    host = relationship(Host, backref="project", cascade="all, delete", passive_deletes=True)
    vulnerability = relationship(Vulnerability, backref="project", cascade="all, delete", passive_deletes=True)

    def __repr__(self):
        return '<Project>'


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    pass_hash = db.Column(db.String, nullable=False)
    user_role = db.Column(db.Integer, default=1)

    vulnerability = relationship(Vulnerability, backref="user")

    def __init__(self, **kwargs):
        self.user_name = kwargs.get("user_name")
        self.email = kwargs.get("email")
        self.pass_hash = generate_password_hash(kwargs.get("pass_hash"))
        self.user_role = kwargs.get("user_role")

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)

    def set_password(self, password):
        self.pass_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pass_hash, password)