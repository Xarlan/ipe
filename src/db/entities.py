from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import INET
import src.webui as webui
from sqlalchemy.orm import relationship

webui.app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ipeuser:ipeuser@localhost:5432/ipe"
webui.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(webui.app)


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
# TODO: after creating table User add field "creator" (Integer - id of user)
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
