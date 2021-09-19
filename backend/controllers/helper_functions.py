
from flask_mail import Message
from .. import mail
from uuid import uuid4
from flask import url_for, current_app
from ..models.CraneUser import CraneUser
from ..models.CraneWebSecurityLevel import CraneWebSecurityLevel
from werkzeug.utils import secure_filename
import os

def reset_token():
    return uuid4()

def send_security_alert_email(email):
    msg = Message('Welbore Security Alert!',
                  recipients=[email])
    msg.body = f'''Someone has been trying to access your account, head over to the Welbore site and change your password.
If this was you, kindly ignore this message.
'''
    mail.send(msg)

def upload_file(file):
    # print(file.mimetype, file.content_length, file.name, file.filename, file.content_type, file.stream, file.headers)
    if file.filename == "":
        return None
    filename = secure_filename(file.filename)
    path = "backend/static/files"
    file.save(os.path.join(current_app.root_path,"static/files",filename))
    # print(os.path.join(path,filename))
    file_path = path+"/"+filename
    return file_path
