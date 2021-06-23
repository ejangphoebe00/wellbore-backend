from flask import Blueprint, request, make_response, jsonify
from ..models.CraneUser import CraneUser
from ..models.Token import RevokedTokenModel
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    get_jwt_identity
    )
# reference for api changes https://flask-jwt-extended.readthedocs.io/en/stable/v4_upgrade_guide/#api-changes
from datetime import datetime, timedelta


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
        if not user.is_password_valid(password):
            # increment counter
            user.LoginErrorCount += 1
            user.update()
            return make_response(jsonify({"message":"Invalid credentials"}),400)
        if user.LoginErrorCount >= 3:
            # do something (maybe lock account and send email to user, or just send email)
            pass
        # reset counter
        user.LoginErrorCount = 0
        user.update()
        resp = jsonify({'access_token':access_token,'refresh_token':refresh_token,'message':'Login Successful'})
        return make_response(resp,200)
    except:
        return make_response(jsonify({'message':'something went wrong'}),500)


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
        print(data)
        existing_user = CraneUser.query.filter((CraneUser.UserEmailAddress == data['UserEmailAddress']) | (
            CraneUser.UserStaff_id == data['UserStaff_id'])).first()
        if existing_user:
            return make_response(jsonify({'message': 'User already exists!'}), 400)

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
                        # CraneUserID = db.Column(db.NVARCHAR(255))
                        UserPassword = CraneUser.hash_password(data['UserPassword']),
                        UserEmailAddress = data['UserEmailAddress'],
                        UserSecurityLevel_id = data['UserSecurityLevel_id'],
                        UserWebSecurityLevel_id = data['UserWebSecurityLevel_id'],
                        UserNogtrWebSecurityLevel_id = data['UserNogtrWebSecurityLevel_id'],
                        UserPremsWebSecurityLevel_id = data['UserPremsWebSecurityLevel_id'],
                        UserIntranetSecurityLevel_id = data['UserIntranetSecurityLevel_id'],
                        UserNsdWebSecurityLevel_id = data['UserNsdWebSecurityLevel_id'],
                        Comments = data['Comments'],
                        OrganisationUserName = data['OrganisationUserName'],
                        CreatedBy_id = user.CraneUser_id,
                        DefaultPassword = CraneUser.hash_password(data['DefaultPassword']),
                        )
        new_user.save()

        resp = jsonify({'message': 'account created successfully'})
        return make_response(resp, 201)
    except:
        return make_response(jsonify({'message': 'something went wrong'}), 500)


@auth_bp.route('/user/get_users', methods=['GET'])
@jwt_required()
def get_all_users():
    try:
        users = [z.serialise() for z in CraneUser.query.all()]
        return make_response(jsonify(users),200)
    except:
       return make_response(jsonify({'message':'Something went wrong'}),500)


# Edit profile
@auth_bp.route('/user/edit_profile/id', methods=['PUT'])
@jwt_required()
def edit_profile(id):
    """Edit user details."""
    try:
        if request.is_json:
            data = request.get_json(force=True)
        else:
            data = request.form

        user = CraneUser.query.get(id)
        # user.Staff_id=data['Staff_id'],
        
        user.update()

        resp = jsonify({'message': 'Details updated successfully'})
        return make_response(resp, 200)
    except:
        return make_response(jsonify({'message': 'something went wrong'}), 500)


# user logout
@auth_bp.route('/user/logout', methods=['DELETE'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    try:
        revoked_token = RevokedTokenModel(jti = jti)
        revoked_token.save()
        return make_response(jsonify({'message': 'Logout successful'}),200)
    except:
        return make_response(jsonify({'message': 'Something went wrong'}), 500)


@auth_bp.route('/user/token-refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity = current_user)
    return make_response(jsonify({'access_token': access_token}),200)
