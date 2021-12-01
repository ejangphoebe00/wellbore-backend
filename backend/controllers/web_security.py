from flask import Blueprint, request, make_response, jsonify
from ..models.CraneWebSecurityLevel import CraneWebSecurityLevel
from ..models.CraneUser import CraneUser, UserCatgoryEnum
from flask_jwt_extended import (
    jwt_required,
    get_jwt
    )
# reference for api changes https://flask-jwt-extended.readthedocs.io/en/stable/v4_upgrade_guide/#api-changes
import datetime
import traceback
from ..middleware.permissions import only_application_admin


web_security_level_bp = Blueprint('web_security_level_bp', __name__)

@web_security_level_bp.route('/apiv1/add_web_security_level',methods=['POST'])
@jwt_required()
@only_application_admin
def add_web_security_level():
    data = request.get_json(force=True)

    # check for redundancies
    level_name = CraneWebSecurityLevel.query.filter_by(WebSecurityLevelName=data['WebSecurityLevelName']).first()
    level_abbreviation = CraneWebSecurityLevel.query.filter_by(WebSecurityLevelAbbreviation=data['WebSecurityLevelAbbreviation']).first()
    if level_name:
        return make_response(jsonify({'message':'WebSecurityLevelName already exists.'}),409)
    if level_abbreviation  and level_abbreviation.WebSecurityLevelAbbreviation != None:
        return make_response(jsonify({'message':'WebSecurityLevelAbbreviation already exists.'}),409)
    try:
        new_web_security_level = CraneWebSecurityLevel(
                        WebSecurityLevelName = data['WebSecurityLevelName'],
                        WebSecurityLevelDescription = data['WebSecurityLevelDescription'],
                        WebSecurityLevelAbbreviation = data['WebSecurityLevelAbbreviation'],    
                        Comments = data['Comments'],
                    )
        new_web_security_level.save()
        return make_response(jsonify({'message':'Web security level added successfuly.'}),201)
    except:
        return make_response(str(traceback.format_exc()),500)


@web_security_level_bp.route('/apiv1/edit_web_security_level/<int:WebSecurityLevel_id>',methods=['PUT'])
@jwt_required()
@only_application_admin
def edit_web_security_level(WebSecurityLevel_id):
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()

    # check for redundancies
    level_name = CraneWebSecurityLevel.query.filter_by(WebSecurityLevelName=data['WebSecurityLevelName']).first()
    level_abbreviation = CraneWebSecurityLevel.query.filter_by(WebSecurityLevelAbbreviation=data['WebSecurityLevelAbbreviation']).first()
    if level_name:
        if WebSecurityLevel_id != level_name.WebSecurityLevel_id:
            return make_response(jsonify({'message':'WebSecurityLevelName already exists.'}),409)
    if level_abbreviation and level_abbreviation.WebSecurityLevelAbbreviation != None:
        if WebSecurityLevel_id != level_abbreviation.WebSecurityLevel_id:
            return make_response(jsonify({'message':'WebSecurityLevelAbbreviation already exists.'}),409)
    try:
        web_security_level = CraneWebSecurityLevel.query.get(WebSecurityLevel_id)
        web_security_level.WebSecurityLevelName = data['WebSecurityLevelName']
        web_security_level.WebSecurityLevelDescription = data['WebSecurityLevelDescription']
        web_security_level.WebSecurityLevelAbbreviation = data['WebSecurityLevelAbbreviation'] 
        web_security_level.Comments = data['Comments']
        web_security_level.ModifiedOn = datetime.datetime.today()
        web_security_level.ModifiedBy = user.CraneUser_id
        web_security_level.update()
        return make_response(jsonify({'message':'Web security level updated successfuly.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get single web_security_level object
@web_security_level_bp.route('/apiv1/get_web_security_level/<int:WebSecurityLevel_id>',methods=['GET'])
@jwt_required()
def get_web_security_level(WebSecurityLevel_id):
    try:
        web_security_level = CraneWebSecurityLevel.query.get(WebSecurityLevel_id)
        return make_response(jsonify(web_security_level.serialise()),200)
    except Exception as error:
        return make_response(str(traceback.format_exc()),500)


@web_security_level_bp.route('/apiv1/get_web_security_level',methods=['GET'])
@jwt_required()
def get_all_web_security_level():
    try:
        web_security_level = [z.serialise() for z in CraneWebSecurityLevel.query.all()]
        return make_response(jsonify(web_security_level),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@web_security_level_bp.route('/apiv1/delete_web_security_level/<int:WebSecurityLevel_id>',methods=['DELETE'])
@jwt_required()
@only_application_admin
def delete_web_security_level(WebSecurityLevel_id):
    try:
        web_security_level = CraneWebSecurityLevel.query.get(WebSecurityLevel_id)
        web_security_level.delete()
        return make_response(jsonify({'message':'Web security level successfully deleted.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)
