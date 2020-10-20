# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/

from flask import Flask
from flask_login import LoginManager
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from src.routes import routes