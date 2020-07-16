from flask_sqlalchemy import SQLAlchemy
import src.webui as webui

webui.app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://ipeuser:ipeuser@localhost:5432/ipe"
webui.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(webui.app)


#  Class for table project
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    date_from = db.Column(db.Date, nullable=False)
    date_to = db.Column(db.Date, nullable=False)
    host_history = db.Column(db.Integer, nullable=True)
    retro_delete = db.Column(db.Boolean, default=False)
    scope_hosts = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<Project>'
