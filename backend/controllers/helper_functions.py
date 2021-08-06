
from flask_mail import Message
from .. import mail
from uuid import uuid4
from flask import url_for
from ..models.CraneUser import CraneUser
from ..models.CraneWebSecurityLevel import CraneWebSecurityLevel

def reset_token():
    return uuid4()

def send_security_alert_email(email):
    msg = Message('Welbore Security Alert!',
                  recipients=[email])
    msg.body = f'''Someone has been trying to access your account, head over to the Welbore site and change your password.
If this was you, kindly ignore this message.
'''
    mail.send(msg)
