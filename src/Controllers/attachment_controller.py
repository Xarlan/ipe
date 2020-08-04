import flask
import os
from src.db.entities import db, Attachment
from time import time
from random import choice
from string import ascii_letters

UPLOAD_FOLDER = os.path.abspath(os.curdir) + '/upload/'
# UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def upload_file(req):
    try:
        file = req.files['attach']
        vuln_id = req.form['vuln_id']
        description = req.form['description']

        if file and allowed_file(file.filename):
            # filename = random 20 chars length string + timestamp + extension
            filename = (''.join(choice(ascii_letters) for i in range(20))) + str(int(time())) + '.'\
                       + file.filename.rsplit('.', 1)[1]
            directory_path = UPLOAD_FOLDER + str(vuln_id)

            if not os.path.exists(directory_path):
                os.mkdir(directory_path)
            file.save(os.path.join(directory_path, filename))
            attachment = Attachment(description=description, path=directory_path + '/' + filename, filename=filename,
                                    vuln_id=int(vuln_id))

            try:
                db.session.add(attachment)
                db.session.commit()
                return flask.make_response(flask.jsonify({"status": 1}), 200)

            except:
                return flask.make_response(flask.jsonify({"status": 0, "error": "Error during adding attachment"}), 500)
    except:
        return flask.make_response(flask.jsonify({"status": 0, "error": "Incorrect input data"}), 500)


def get_attach(filename):
    attachment = Attachment.query.get_or_404(filename)
    return flask.send_from_directory(attachment.path, attachment.filename)


def delete_attach(req):
    try:
        req_body = req.get_json()
        filename = req_body['filename']
        attachment = Attachment.query.get_or_404(filename)
        os.remove(attachment.path)

        try:
            db.session.delete(attachment)
            db.session.commit()
            return flask.make_response(flask.jsonify({"status": 1}), 200)

        except:
            return flask.make_response(flask.jsonify({"status": 0, "error": "Error during deleting attachment"}), 500)
    except:
        return flask.make_response(flask.jsonify({"status": 0, "error": "Error occured during processing input data."}),
                                   500)


# method for deleting folder with attachments; execute on delete of vulnerability
def delete_folder(vul_id):
    os.rmdir(UPLOAD_FOLDER + str(vul_id))
    return True
