
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


# def login():
#     # create default user/admin
#     users = CraneUser.query.all()
#     if users is None:
#         # create default web security level
#         new_web_security_level = CraneWebSecurityLevel(
#                     WebSecurityLevelName = "sample name",
#                     WebSecurityLevelDescription = "sample description",
#                     WebSecurityLevelAbbreviation = "abc",    
#                     Comments = None,
#                 )
#         new_web_security_level.save()

#         # create new user
#         new_user = CraneUser(
#             FirstName = 'Admin',
#             MiddleName = 'Admin',
#             Surname = None,
#             LUID = None,
#             CraneUserName = 'Admin',
#             LoginID = None,
#             LoginIDAlias = None,
#             UserCategory = 'Admin',
#             UserCompany_id = None,
#             UserPremsUser_id = None,
#             UserStaff_id = 1,
#             OrganisationName = "Petroleum Authority of Uganda",
#             CredentialsSent = 1,
#             UserEmailAddress = "admin@gmail.com",
#             UserSecurityLevel_id = None,
#             UserWebSecurityLevel_id = 1,#should come from websecurity model as forign key
#             UserNogtrWebSecurityLevel_id = None,
#             UserPremsWebSecurityLevel_id = None,
#             UserIntranetSecurityLevel_id = None,
#             UserNsdWebSecurityLevel_id = None,
#             Comments = None,
#             OrganisationUserName = "PAU",
#             CreatedBy_id = None,
#             DeactivateAccount = 0,
#             LoginErrorCount = 0,
#             DefaultPassword = CraneUser.hash_password("admin"),
#         )
#         new_user.save()
