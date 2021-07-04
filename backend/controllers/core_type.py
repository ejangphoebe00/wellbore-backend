from flask import Blueprint, request, make_response, jsonify
from ..models.CoreType import CoreType
from ..models.CraneUser import CraneUser, UserCatgoryEnum
from flask_jwt_extended import (
    jwt_required,
    get_jwt
    )
# reference for api changes https://flask-jwt-extended.readthedocs.io/en/stable/v4_upgrade_guide/#api-changes
import datetime


core_type_bp = Blueprint('core_type_bp', __name__)

@core_type_bp.route('/apiv1/add_core_type',methods=['POST'])
@jwt_required()
def add_core_type():
    data = request.get_json(force=True)
    try:
        new_core_type = CoreType(
                        CoreTypeName = data['CoreTypeName'],
                        SortOrder = data['SortOrder'],  
                        Comments = data['Comments'],
                    )
        new_core_type.save()
        return make_response(jsonify({'message':'Core Type added successfuly.'}),201)
    except:
        return make_response(jsonify({'message':'Something went wrong'}),500)


@core_type_bp.route('/apiv1/edit_core_type/<int:CoreType_id>',methods=['PUT'])
@jwt_required()
def edit_core_type(CoreType_id):
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()
    try:
        core_type = CoreType.query.get(CoreType_id)
        core_type.CoreTypeName = data['CoreTypeName']
        core_type.Comments = data['Comments']
        core_type.ModifiedOn = datetime.datetime.today()
        core_type.ModifiedBy = user.CraneUser_id
        core_type.update()
        return make_response(jsonify({'message':'Core Type updated successfuly.'}),200)
    except:
        return make_response(jsonify({'message':'Something went wrong'}),500)


# get single core_type object
@core_type_bp.route('/apiv1/get_core_type/<int:CoreType_id>',methods=['GET'])
@jwt_required()
def get_core_type(CoreType_id):
    try:
        core_type = CoreType.query.get(CoreType_id)
        return make_response(jsonify(core_type.serialise()),200)
    except:
       return make_response(jsonify({'message':'Something went wrong'}),500)


@core_type_bp.route('/apiv1/get_core_types',methods=['GET'])
@jwt_required()
def get_all_core_types():
    try:
        core_types = [z.serialise() for z in CoreType.query.all()]
        return make_response(jsonify(core_types),200)
    except:
       return make_response(jsonify({'message':'Something went wrong'}),500)


@core_type_bp.route('/apiv1/delete_core_type/<int:CoreType_id>',methods=['DELETE'])
@jwt_required()
def delete_core_type(CoreType_id):
    try:
        core_type = CoreType.query.get(CoreType_id)
        core_type.delete()
        return make_response(jsonify({'message':'Core Type successfully deleted.'}),200)
    except:
       return make_response(jsonify({'message':'Something went wrong'}),500) 
