from flask import Blueprint, request, make_response, jsonify
from ..models.CraneUser import CraneUser, UserCatgoryEnum
from ..models.Token import RevokedTokenModel
from ..models.CraneUserLoginHistory import CraneUserLoginHistory
from ..models.CraneWebSecurityLevel import CraneWebSecurityLevel
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    get_jwt_identity
    )
# reference for api changes https://flask-jwt-extended.readthedocs.io/en/stable/v4_upgrade_guide/#api-changes
from datetime import datetime, timedelta
from .helper_functions import send_security_alert_email
import traceback


auth_bp = Blueprint('auth_bp', __name__)

# user login
@auth_bp.route('/user/login', methods=['POST'])
def login():
    try:
        data = request.get_json(force=True)
        email = data['UserEmailAddress']
        user = CraneUser.query.filter(CraneUser.UserEmailAddress==email,CraneUser.DeactivateAccount==0).first()###
        password = data['Password'] #name it password, the check will be done from the model
        
        access_token = create_access_token(identity = data['UserEmailAddress'])
        refresh_token = create_refresh_token(identity = data['UserEmailAddress'])
        if not user:
            return make_response(jsonify({"message":"Account doesn't exist"}),400)
        # test if password was edited before end of 48 hours from account creation date
        current_date = datetime.now()
        account_creation_date = user.DateCreated
        if user.UserEmailAddress != "admin@pau.go.ug":
            if abs((current_date - account_creation_date).days) > 2 and user.UserPassword is None:
                return make_response(jsonify({"message":"Please contact the administrator for a password update"}),401)
        if not user.is_password_valid(password):
            # increment counter
            user.LoginErrorCount += 1
            user.update()
            if user.LoginErrorCount >= 3:
                # do something (maybe lock account and send email to user, or just send email)
                print('so many attempts')
                send_security_alert_email(email)
            return make_response(jsonify({"message":"Invalid credentials"}),400)
        # reset counter
        user.LoginErrorCount = 0
        user.UserOnlineStatus = 1
        user.update()

        # update login history
        login_history = CraneUserLoginHistory(
            HistLogUser_id = user.CraneUser_id,
            LogStaff_id = user.UserStaff_id,
            CraneCompany_id = user.UserCompany_id,   
            LogCompanyAuthorisedUser_id = user.CraneUser_id,
            LogAuthorisedUserName = user.CraneUserName, 
            LoginStatus_id = 0,   
            UserOnlineStatus = 1,
            LogLoginDate = datetime.now(),
            UserLoginLogName = user.CraneUserName,
            UserAcessLogName = user.CraneUserName,
            Comments = user.Comments
        )
        login_history.save()
        if user.UserCategory == UserCatgoryEnum.Admin:
            user_role = "Admin"
        else:
            user_role = "Staff"
        resp = jsonify({"CraneUser_id":user.CraneUser_id,"user_role":user_role,'access_token':access_token,
                        'refresh_token':refresh_token,'message':'Login Successful'
                    })
        return make_response(resp,200)
    except:
        return make_response(str(traceback.format_exc()),500)


# User registration
@auth_bp.route('/user/registration', methods=['POST'])
@jwt_required()
def register_user():
    """Create a user."""
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()
    try:
        if request.is_json:
            data = request.get_json(force=True)
        else:
            data = request.form
        existing_user = CraneUser.query.filter(CraneUser.UserEmailAddress == data['UserEmailAddress']).first()
        if existing_user:
            return make_response(jsonify({'message': 'User already exists!'}), 400)

        if CraneUser.query.filter(CraneUser.UserStaff_id == data['UserStaff_id']).first():
            return make_response(jsonify({'message': 'StaffID already exists!'}), 400)

        if CraneUser.query.filter(CraneUser.CraneUserName==data['CraneUserName']).first():
            return make_response(jsonify({'message': 'Username already exists!'}), 400)

        # create new user
        new_user = CraneUser(
                        FirstName = data['FirstName'],
                        MiddleName = data['MiddleName'],
                        Surname = data['Surname'],
                        LUID = data['LUID'],
                        CraneUserName = data['CraneUserName'],
                        LoginID = data['LoginID'],
                        LoginIDAlias = data['LoginIDAlias'],
                        UserCategory = data['UserCategory'],
                        UserCompany_id = data['UserCompany_id'],
                        UserPremsUser_id = data['UserPremsUser_id'],
                        UserStaff_id = data['UserStaff_id'],
                        OrganisationName = data['OrganisationName'],
                        CredentialsSent = 1,
                        UserEmailAddress = data['UserEmailAddress'],
                        UserSecurityLevel_id = data['UserSecurityLevel_id'],
                        UserWebSecurityLevel_id = data['UserWebSecurityLevel_id'],#should come from websecurity model as forign key
                        UserNogtrWebSecurityLevel_id = data['UserNogtrWebSecurityLevel_id'],
                        UserPremsWebSecurityLevel_id = data['UserPremsWebSecurityLevel_id'],
                        UserIntranetSecurityLevel_id = data['UserIntranetSecurityLevel_id'],
                        UserNsdWebSecurityLevel_id = data['UserNsdWebSecurityLevel_id'],
                        Comments = data['Comments'],
                        OrganisationUserName = data['OrganisationUserName'],
                        CreatedBy_id = user.CraneUser_id,
                        DeactivateAccount = 0,
                        LoginErrorCount = 0,
                        DefaultPassword = CraneUser.hash_password(data['DefaultPassword']),
                    )
        new_user.save()

        resp = jsonify({'message': 'account created successfully'})
        return make_response(resp, 201)
    except:
        return make_response(str(traceback.format_exc()),500)


@auth_bp.route('/user/get_users', methods=['GET'])
@jwt_required()
def get_all_users():
    try:
        users = [z.serialise() for z in CraneUser.query.filter(CraneUser.DeactivateAccount == 0)]
        return make_response(jsonify(users),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@auth_bp.route('/user/get_user/<int:CraneUser_id>', methods=['GET'])
@jwt_required()
def get_user(CraneUser_id):
    try:
        user = CraneUser.query.get(CraneUser_id)
        return make_response(jsonify(user.serialise()),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# deactivate account
@auth_bp.route('/user/deactivate_account/<int:CraneUser_id>', methods=['PUT'])
@jwt_required()
def deactivate_account(CraneUser_id):
    try:
        user = CraneUser.query.get(CraneUser_id)
        user.DeactivateAccount = 1
        user.update()
        return make_response(jsonify({'message':'Account successfully Deactivated'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# Edit profile
@auth_bp.route('/user/edit_profile/<int:CraneUser_id>', methods=['PUT'])
@jwt_required()
def edit_profile(CraneUser_id):
    """Edit user details."""
    try:
        if request.is_json:
            data = request.get_json(force=True)
        else:
            data = request.form

        # user whose records are going to be updated
        user = CraneUser.query.get(CraneUser_id)
        # logged in user details
        current_user_email = get_jwt()
        loggedin_user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()
        # if the logged in user is an admin
        if loggedin_user.UserCategory == UserCatgoryEnum.Admin :
            user.FirstName = data['FirstName']
            user.MiddleName = data['MiddleName']
            user.Surname = data['Surname']
            user.LUID = data['LUID']
            user.CraneUserName = data['CraneUserName']
            user.LoginID = data['LoginID']
            user.LoginIDAlias = data['LoginIDAlias']
            user.UserCategory = data['UserCategory']
            user.UserCompany_id = data['UserCompany_id']
            user.UserPremsUser_id = data['UserPremsUser_id']
            user.UserStaff_id = data['UserStaff_id']
            user.OrganisationName = data['OrganisationName']
            user.UserEmailAddress = data['UserEmailAddress']
            user.UserSecurityLevel_id = data['UserSecurityLevel_id']
            user.UserWebSecurityLevel_id = data['UserWebSecurityLevel_id']
            user.UserNogtrWebSecurityLevel_id = data['UserNogtrWebSecurityLevel_id']
            user.UserPremsWebSecurityLevel_id = data['UserPremsWebSecurityLevel_id']
            user.UserIntranetSecurityLevel_id = data['UserIntranetSecurityLevel_id']
            user.UserNsdWebSecurityLevel_id = data['UserNsdWebSecurityLevel_id']
            user.Comments = data['Comments']
            user.OrganisationUserName = data['OrganisationUserName']
            user.ActivationChangeComment = data['ActivationChangeComment']
            user.ActivationChangeDate = datetime.now()        
            user.ModifiedBy = loggedin_user.CraneUser_id
            # if user can't log in due to expired password
            if data.get("DefaultPassword") != None and data["DefaultPassword"] != user.DeafaultPassword:
                user.DefaultPassword = CraneUser.hash_password(data['DefaultPassword'])
                user.DateCreated = datetime.now()
            # if admin is updating their own records
            if user.CraneUser_id == loggedin_user.CraneUser_id:
                user.UserPassword = CraneUser.hash_password(data.get('UserPassword')) if data.get('UserPassword') else None
                user.PasswordChangeDate = datetime.now() if data.get('UserPassword') else user.PasswordChangeDate
            else:
                resp = jsonify({'message': 'You are not allowed to change the user password of an account that is not yours'})
                return make_response(resp, 400)
        else:
            # user.FirstName = data['FirstName']
            # user.MiddleName = data['MiddleName']
            # user.Surname = data['Surname']
            user.UserEmailAddress = data['UserEmailAddress']
            user.UserPassword = CraneUser.hash_password(data['UserPassword'])
            user.PasswordChangeDate = datetime.now()        
        user.update()

        resp = jsonify({'message': 'Details updated successfully'})
        return make_response(resp, 200)
    except:
        return make_response(str(traceback.format_exc()),500)


# user logout
@auth_bp.route('/user/logout/<int:CraneUser_id>', methods=['DELETE'])
@jwt_required()
def logout(CraneUser_id):
    jti = get_jwt()['jti']
    user = CraneUser.query.get(CraneUser_id)
    try:
        revoked_token = RevokedTokenModel(jti = jti)
        revoked_token.save()

        # update user object
        user.LastSeen = datetime.now()
        user.UserOnlineStatus = 0
        user.update()

        # update login history (update last inserted)
        login_history = CraneUserLoginHistory.query.filter(CraneUserLoginHistory.HistLogUser_id==CraneUser_id)[-1]
        login_history.LogLogoutDate = datetime.now()
        login_history.update()
        return make_response(jsonify({'message': 'Logout successful'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@auth_bp.route('/user/token-refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity = current_user)
    return make_response(jsonify({'access_token': access_token}),200)


@auth_bp.route('/user/get_users_logs', methods=['GET'])
@jwt_required()
def get_users_logs():
    try:
        logs = [z.serialise() for z in CraneUserLoginHistory.query.all()]
        return make_response(jsonify(logs),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get logs per user
@auth_bp.route('/user/get_user_logs/<int:CraneUser_id>', methods=['GET'])
@jwt_required()
def get_user_logs(CraneUser_id):
    try:
        logs = [z.serialise() for z in CraneUserLoginHistory.query.filter(CraneUserLoginHistory.HistLogUser_id == CraneUser_id)]
        return make_response(jsonify(logs),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# user helper functions
def create_default_user_and_security_level():
    # create default user/admin
    users = CraneUser.query.all()
    if not users:
        # create default web security level
        new_web_security_level = CraneWebSecurityLevel(
                    WebSecurityLevelName = "Admin",
                    WebSecurityLevelDescription = "Administrator",
                    WebSecurityLevelAbbreviation = "Admin",    
                    Comments = None,
                )
        new_web_security_level.save()

        # create default user
        new_user = CraneUser(
            FirstName = 'Admin',
            MiddleName = 'Admin',
            Surname = "None",
            LUID = None,
            CraneUserName = 'Admin',
            LoginID = None,
            LoginIDAlias = None,
            UserCategory = 'Admin',
            UserCompany_id = None,
            UserPremsUser_id = None,
            UserStaff_id = 1,
            OrganisationName = "Petroleum Authority of Uganda",
            CredentialsSent = 1,
            UserEmailAddress = "admin@pau.go.ug",
            UserSecurityLevel_id = None,
            UserWebSecurityLevel_id = 1,#should come from websecurity model as forign key
            UserNogtrWebSecurityLevel_id = None,
            UserPremsWebSecurityLevel_id = None,
            UserIntranetSecurityLevel_id = None,
            UserNsdWebSecurityLevel_id = None,
            Comments = None,
            OrganisationUserName = "PAU",
            CreatedBy_id = None,
            DeactivateAccount = 0,
            LoginErrorCount = 0,
            DefaultPassword = CraneUser.hash_password("admin"),
        )
        new_user.save()
    return
