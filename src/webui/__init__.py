# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/

from flask import Flask

app = Flask(__name__)
# max size of upload attachment
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

from src.routes import routes