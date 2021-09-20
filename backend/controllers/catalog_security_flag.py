from flask import Blueprint, request, make_response, jsonify
from ..models.CatalogSecurityFlag import CatalogSecurityFlag
from ..models.CraneUser import CraneUser, UserCatgoryEnum
from flask_jwt_extended import (
    jwt_required,
    get_jwt
    )
# reference for api changes https://flask-jwt-extended.readthedocs.io/en/stable/v4_upgrade_guide/#api-changes
import datetime
import traceback
from ..middleware.permissions import only_data_admin


catalog_security_flag_bp = Blueprint('catalog_security_flag_bp', __name__)

@catalog_security_flag_bp.route('/apiv1/add_catalog_security_flag',methods=['POST'])
@jwt_required()
@only_data_admin
def add_catalog_security_flag():
    data = request.get_json(force=True)

    # check for redundancies
    flag_name = CatalogSecurityFlag.query.filter_by(CatalogSecurityFlagName=data['CatalogSecurityFlagName']).first()
    if flag_name:
        return make_response(jsonify({'message':'CatalogSecurityFlagName already exists.'}),409)
    try:
        new_catalog_security_flag = CatalogSecurityFlag(
                        CatalogSecurityFlagName = data['CatalogSecurityFlagName'],
                        SortOrder = data['SortOrder'],  
                        Comments = data['Comments'],
                    )
        new_catalog_security_flag.save()
        return make_response(jsonify({'message':'Catalog Security Flag added successfuly.'}),201)
    except:
        return make_response(str(traceback.format_exc()),500)


@catalog_security_flag_bp.route('/apiv1/edit_catalog_security_flag/<int:CatalogSecurityFlag_id>',methods=['PUT'])
@jwt_required()
@only_data_admin
def edit_catalog_security_flag(CatalogSecurityFlag_id):
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()

    # check for redundancies
    flag_name = CatalogSecurityFlag.query.filter_by(CatalogSecurityFlagName=data['CatalogSecurityFlagName']).first()
    if flag_name:
        if CatalogSecurityFlag_id != flag_name.CatalogSecurityFlag_id:
            return make_response(jsonify({'message':'CatalogSecurityFlagName already exists.'}),409)
    try:
        catalog_security_flag = CatalogSecurityFlag.query.get(CatalogSecurityFlag_id)
        catalog_security_flag.CatalogSecurityFlagName = data['CatalogSecurityFlagName']
        catalog_security_flag.Comments = data['Comments']
        catalog_security_flag.SortOrder = data['SortOrder'] 
        catalog_security_flag.ModifiedOn = datetime.datetime.today()
        catalog_security_flag.ModifiedBy = user.CraneUser_id
        catalog_security_flag.update()
        return make_response(jsonify({'message':'Catalog Security Flag updated successfuly.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get single catalog_security_flag object
@catalog_security_flag_bp.route('/apiv1/get_catalog_security_flag/<int:CatalogSecurityFlag_id>',methods=['GET'])
@jwt_required()
def get_catalog_security_flag(CatalogSecurityFlag_id):
    try:
        catalog_security_flag = CatalogSecurityFlag.query.get(CatalogSecurityFlag_id)
        return make_response(jsonify(catalog_security_flag.serialise()),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@catalog_security_flag_bp.route('/apiv1/get_catalog_security_flags',methods=['GET'])
@jwt_required()
def get_all_catalog_security_flags():
    try:
        catalog_security_flags = [z.serialise() for z in CatalogSecurityFlag.query.all()]
        return make_response(jsonify(catalog_security_flags),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@catalog_security_flag_bp.route('/apiv1/delete_catalog_security_flag/<int:CatalogSecurityFlag_id>',methods=['DELETE'])
@jwt_required()
@only_data_admin
def delete_catalog_security_flag(CatalogSecurityFlag_id):
    try:
        catalog_security_flag = CatalogSecurityFlag.query.get(CatalogSecurityFlag_id)
        catalog_security_flag.delete()
        return make_response(jsonify({'message':'Catalog Security Flag successfully deleted.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)
