from flask import Blueprint, request, make_response, jsonify, send_from_directory
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
from .helper_functions import send_security_alert_email, upload_file, reset_token, send_reset_email
import traceback
from ..middleware.permissions import only_data_admin, only_application_and_data_admin, only_application_admin
from ..models.PasswordReset import PasswordReset


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
            HistLogUserId = user.CraneUserId,
            LogStaffId = user.UserStaffId,
            CraneCompanyId = user.UserCompanyId,   
            LogCompanyAuthorisedUserId = user.CraneUserId,
            LogAuthorisedUserName = user.CraneUserName, 
            LoginStatusId = 0,   
            UserOnlineStatus = 1,
            LogLoginDate = datetime.now(),
            UserLoginLogName = user.CraneUserName,
            UserAcessLogName = user.CraneUserName,
            Comments = user.Comments
        )
        login_history.save()
        if user.UserCategory == UserCatgoryEnum.App_Admin:
            user_role = "Application Admin"
        elif user.UserCategory == UserCatgoryEnum.Data_Admin:
            user_role = "Data Admin"
        else:
            user_role = "Staff"
        resp = jsonify({"CraneUserId":user.CraneUserId,"user_role":user_role,'access_token':access_token,
                        'refresh_token':refresh_token,'message':'Login Successful'
                    })
        return make_response(resp,200)
    except:
        return make_response(str(traceback.format_exc()),500)


# User registration
@auth_bp.route('/user/registration', methods=['POST'])
@jwt_required()
@only_application_and_data_admin
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

        staff = CraneUser.query.filter(CraneUser.UserStaffId == data['UserStaffId']).first()
        if staff and staff.UserStaffId != None:
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
                        # UserCategory = data['UserCategory'],
                        UserCompanyId = data['UserCompanyId'],
                        UserPremsUserId = data['UserPremsUserId'],
                        UserStaffId = data['UserStaffId'],
                        OrganisationName = data['OrganisationName'],
                        CredentialsSent = 1,
                        UserEmailAddress = data['UserEmailAddress'],
                        UserSecurityLevelId = data['UserSecurityLevelId'],
                        UserWebSecurityLevelId = data['UserWebSecurityLevelId'],#should come from websecurity model as forign key
                        UserNogtrWebSecurityLevelId = data['UserNogtrWebSecurityLevelId'],
                        UserPremsWebSecurityLevelId = data['UserPremsWebSecurityLevelId'],
                        UserIntranetSecurityLevelId = data['UserIntranetSecurityLevelId'],
                        UserNsdWebSecurityLevelId = data['UserNsdWebSecurityLevelId'],
                        Comments = data['Comments'],
                        OrganisationUserName = data['OrganisationUserName'],
                        CreatedById = user.CraneUserId,
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
@only_application_and_data_admin
def get_all_users():
    try:
        users = [z.serialise() for z in CraneUser.query.filter(CraneUser.DeactivateAccount == 0)]
        return make_response(jsonify(users),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@auth_bp.route('/user/get_user/<int:CraneUserId>', methods=['GET'])
@jwt_required()
def get_user(CraneUserId):
    try:
        user = CraneUser.query.get(CraneUserId)
        return make_response(jsonify(user.serialise()),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# deactivate account
@auth_bp.route('/user/deactivate_account/<int:CraneUserId>', methods=['PUT'])
@jwt_required()
@only_application_admin
def deactivate_account(CraneUserId):
    try:
        user = CraneUser.query.get(CraneUserId)
        user.DeactivateAccount = 1
        user.update()
        return make_response(jsonify({'message':'Account successfully Deactivated'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)
      

# reactivate account
@auth_bp.route('/user/reactivate_account/<int:CraneUserId>', methods=['PUT'])
@jwt_required()
@only_application_admin
def reactivate_account(CraneUserId):
    try:
        user = CraneUser.query.get(CraneUserId)
        user.DeactivateAccount = 0
        user.update()
        return make_response(jsonify({'message':'Account successfully Reactivated'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get deactivated accounts
@auth_bp.route('/user/deactivated_accounts', methods=['GET'])
@jwt_required()
@only_application_and_data_admin
def get_deactivated_accounts():
    try:
        accounts = CraneUser.query.filter(CraneUser.DeactivateAccount==1).all()
        accounts = [account.serialise() for account in accounts]
        return make_response(jsonify(accounts),200)
    except:
        return make_response(str(traceback.format_exc()),500)

# update user role and permissions
@auth_bp.route('/user/update_user_role/<int:CraneUserId>', methods=['PUT'])
@jwt_required()
@only_application_admin
def update_user_role(CraneUserId):
    data = request.get_json(force=True)
    try:
        user = CraneUser.query.get(CraneUserId)
        user.UserCategory = data['UserCategory']
        user.update()
        return make_response(jsonify({'message':'User Role successfully Updated'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# Edit profile
@auth_bp.route('/user/edit_profile/<int:CraneUserId>', methods=['PUT'])
@jwt_required()
def edit_profile(CraneUserId):
    """Edit user details."""
    try:
        if request.is_json:
            data = request.get_json(force=True)
        else:
            data = request.form

        # user whose records are going to be updated
        user = CraneUser.query.get(CraneUserId)
        # logged in user details
        current_user_email = get_jwt()
        loggedin_user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()
        # if the logged in user is an admin
        if loggedin_user.UserCategory == UserCatgoryEnum.Data_Admin:
            # check for redundancy
            staff = CraneUser.query.filter(CraneUser.UserStaffId == data['UserStaffId']).first()
            if staff and staff.UserStaffId != None:
                if CraneUserId != staff.CraneUserId:
                    return make_response(jsonify({'message': 'StaffID already exists!'}), 400)

            staff_name = CraneUser.query.filter(CraneUser.CraneUserName==data['CraneUserName']).first()
            if staff_name:
                if CraneUserId != staff_name.CraneUserId:
                    return make_response(jsonify({'message': 'Username already exists!'}), 400)

            user.FirstName = data['FirstName']
            user.MiddleName = data['MiddleName']
            user.Surname = data['Surname']
            user.LUID = data['LUID']
            user.CraneUserName = data['CraneUserName']
            user.LoginID = data['LoginID']
            user.LoginIDAlias = data['LoginIDAlias']
            # user.UserCategory = data['UserCategory']
            user.UserCompanyId = data['UserCompanyId']
            user.UserPremsUserId = data['UserPremsUserId']
            user.UserStaffId = data['UserStaffId']
            user.OrganisationName = data['OrganisationName']
            user.UserEmailAddress = data['UserEmailAddress']
            user.UserSecurityLevelId = data['UserSecurityLevelId']
            user.UserWebSecurityLevelId = data['UserWebSecurityLevelId']
            user.UserNogtrWebSecurityLevelId = data['UserNogtrWebSecurityLevelId']
            user.UserPremsWebSecurityLevelId = data['UserPremsWebSecurityLevelId']
            user.UserIntranetSecurityLevelId = data['UserIntranetSecurityLevelId']
            user.UserNsdWebSecurityLevelId = data['UserNsdWebSecurityLevelId']
            user.Comments = data['Comments']
            user.OrganisationUserName = data['OrganisationUserName']
            user.ActivationChangeComment = data['ActivationChangeComment']
            user.ActivationChangeDate = datetime.now()        
            user.ModifiedBy = loggedin_user.CraneUserId
            # if user can't log in due to expired password
            if data.get("DefaultPassword") != None and data["DefaultPassword"] != user.DefaultPassword:
                user.DefaultPassword = CraneUser.hash_password(data['DefaultPassword'])
                user.DateCreated = datetime.now()
            # if admin is updating their own records
            if user.CraneUserId == loggedin_user.CraneUserId:
                if user.UserPassword != data.get('UserPassword'):
                    user.UserPassword = CraneUser.hash_password(data.get('UserPassword')) if data.get('UserPassword') else None
                    user.PasswordChangeDate = datetime.now() if data.get('UserPassword') else user.PasswordChangeDate
            else:
                resp = jsonify({'message': 'You are not allowed to change the user password of an account that is not yours'})
                return make_response(resp, 400)
        else:
            # check for redundancy
            staff_name = CraneUser.query.filter(CraneUser.CraneUserName==data['CraneUserName']).first()
            if staff_name:
                if CraneUserId != staff_name.CraneUserId:
                    return make_response(jsonify({'message': 'Username already exists!'}), 400)
            # user.FirstName = data['FirstName']
            # user.MiddleName = data['MiddleName']
            # user.Surname = data['Surname']
            user.UserEmailAddress = data['UserEmailAddress']
            user.CraneUserName = data['CraneUserName']
            if user.UserPassword != data['UserPassword']:
                user.UserPassword = CraneUser.hash_password(data['UserPassword'])
                user.PasswordChangeDate = datetime.now()        
        user.update()

        resp = jsonify({'message': 'Details updated successfully'})
        return make_response(resp, 200)
    except:
        return make_response(str(traceback.format_exc()),500)


# user logout
@auth_bp.route('/user/logout/<int:CraneUserId>', methods=['DELETE'])
@jwt_required()
def logout(CraneUserId):
    jti = get_jwt()['jti']
    user = CraneUser.query.get(CraneUserId)
    try:
        revoked_token = RevokedTokenModel(jti = jti)
        revoked_token.save()

        # update user object
        user.LastSeen = datetime.now()
        user.UserOnlineStatus = 0
        user.update()

        # update login history (update last inserted)
        login_history = CraneUserLoginHistory.query.filter(CraneUserLoginHistory.HistLogUserId==CraneUserId)[-1]
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
@only_application_and_data_admin
def get_users_logs():
    try:
        logs = [z.serialise() for z in CraneUserLoginHistory.query.all()]
        return make_response(jsonify(logs),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get logs per user
@auth_bp.route('/user/get_user_logs/<int:CraneUserId>', methods=['GET'])
@jwt_required()
def get_user_logs(CraneUserId):
    try:
        logs = [z.serialise() for z in CraneUserLoginHistory.query.filter(CraneUserLoginHistory.HistLogUserId == CraneUserId)]
        return make_response(jsonify(logs),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@auth_bp.route('/user/upload_profile_picture/<int:CraneUserId>', methods=['POST'])
@jwt_required()
def upload_profile_picture(CraneUserId):
    try:
        data = request.files
        user = CraneUser.query.get(CraneUserId)
        profileImage = upload_file(data['ProfilePicture'])
        user.ProfilePicture = profileImage
        user.update()
        return make_response(jsonify({'message': "Profile picture successfully uploaded"}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@auth_bp.route('/user/get_profileImage/<int:CraneUserId>', methods=['GET'])
@jwt_required()
def get_profileImage(CraneUserId):
    try:
        user = CraneUser.query.get(CraneUserId)
        # upload_path = "/static/files"
        # filename = str(user.ProfilePicture).split('/')[-1]
        # print(filename)
        # return send_from_directory(upload_path, filename)
        return make_response(jsonify({'ProfilePicture': user.ProfilePicture}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# forgot password
# url is UI link for a password reset form
@auth_bp.route('/user/forgot_password_email_request/<string:url>',methods=['POST'])
def recover_password_email(url):
    '''email request for password recovery'''
    if request.is_json:
        data = request.get_json(force=True)
    else:
        data = request.form
    token = str(reset_token())
    user = CraneUser.query.filter_by(UserEmailAddress=data['UserEmailAddress']).first()
    if not user:
        return make_response(jsonify({'message': 'The email you supplied is not registered with us, please check your email and try again.'}),404)
    
    # unused token
    existing_record_inactive = PasswordReset.query.filter_by(CraneUserId=user.CraneUserId, HasActivated=False).first()
    if existing_record_inactive:
        creation_date = existing_record_inactive.CreationDate
        today = datetime.utcnow()
        delta = today - creation_date
        if delta.days > 1:
            existing_record_inactive.HasActivated = True
            existing_record_inactive.save()
            return make_response(jsonify({'message': 'Expired token, please restart the password reset process.'}))
    
    existing_record_active = PasswordReset.query.filter_by(CraneUserId=user.CraneUserId, HasActivated=True).first()
    if existing_record_active:
        send_reset_email(data['UserEmailAddress'],str(url))
        existing_record_active.ResetKey = token
        existing_record_active.HasActivated = False
        existing_record_active.update()
    else:
        send_reset_email(data['UserEmailAddress'],str(url))
        reset_password = PasswordReset(
            CraneUserId = user.CraneUserId,
            ResetKey = token,
        )
        reset_password.save()
    
    return make_response(jsonify({'message': 'An email has been sent with instructions to reset your password.'}),200)

# save  new password
@auth_bp.route('/user/store_updated_password/<int:CraneUserId>', methods=['POST'])
def store_reset_password(CraneUserId):
    '''update password'''
    data = request.get_json(force=True)

    user = CraneUser.query.get(CraneUserId)
    user.UserPassword = CraneUser.hash_password(data['Password']),
    user.save()

    existing_record = PasswordReset.query.filter_by(CraneUserId=CraneUserId).first()
    existing_record.HasActivated = True
    existing_record.save()
    
    return make_response(jsonify({'message': 'Your password was successfully updated.'}),200)


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
            UserCategory = UserCatgoryEnum.App_Admin,
            UserCompanyId = None,
            UserPremsUserId = None,
            UserStaffId = 1,
            OrganisationName = "Petroleum Authority of Uganda",
            CredentialsSent = 1,
            UserEmailAddress = "admin@pau.go.ug",
            UserSecurityLevelId = None,
            UserWebSecurityLevelId = 1,#should come from websecurity model as forign key
            UserNogtrWebSecurityLevelId = None,
            UserPremsWebSecurityLevelId = None,
            UserIntranetSecurityLevelId = None,
            UserNsdWebSecurityLevelId = None,
            Comments = None,
            OrganisationUserName = "PAU",
            CreatedById = None,
            DeactivateAccount = 0,
            LoginErrorCount = 0,
            DefaultPassword = CraneUser.hash_password("admin"),
        )
        new_user.save()
    return
