from flask import Blueprint, request, make_response, jsonify
from ..models.FileFormat import FileFormat
from ..models.CraneUser import CraneUser, UserCatgoryEnum
from flask_jwt_extended import (
    jwt_required,
    get_jwt
    )
# reference for api changes https://flask-jwt-extended.readthedocs.io/en/stable/v4_upgrade_guide/#api-changes
import datetime
import traceback


file_format_bp = Blueprint('file_format_bp', __name__)

@file_format_bp.route('/apiv1/add_file_format',methods=['POST'])
@jwt_required()
def add_file_format():
    data = request.get_json(force=True)

    # check for redundancies
    file_format = FileFormat.query.filter_by(FileFormatName=data['FileFormatName']).first()
    if file_format:
        return make_response(jsonify({'message':'FileFormatName already exists.'}),409)
    try:
        new_file_format = FileFormat(
                        FileFormatName = data['FileFormatName'],
                        SortOrder = data['SortOrder'],
                        Comments = data['Comments'],
                    )
        new_file_format.save()
        return make_response(jsonify({'message':'File Format added successfuly.'}),201)
    except:
        return make_response(str(traceback.format_exc()),500)


@file_format_bp.route('/apiv1/edit_file_format/<int:FileFormat_id>',methods=['PUT'])
@jwt_required()
def edit_file_format(FileFormat_id):
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()

    # check for redundancies
    file_format = FileFormat.query.filter_by(FileFormatName=data['FileFormatName']).first()
    if FileFormat_id != file_format.FileFormat_id:
        return make_response(jsonify({'message':'FileFormatName already exists.'}),409)
    try:
        file_format = FileFormat.query.get(FileFormat_id)
        file_format.FileFormatName = data['FileFormatName']
        file_format.Comments = data['Comments']
        file_format.SortOrder = data['SortOrder']
        file_format.ModifiedOn = datetime.datetime.today()
        file_format.ModifiedBy = user.CraneUser_id
        file_format.update()
        return make_response(jsonify({'message':'File Format updated successfuly.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get single file_format object
@file_format_bp.route('/apiv1/get_file_format/<int:FileFormat_id>',methods=['GET'])
@jwt_required()
def get_file_format(FileFormat_id):
    try:
        file_format = FileFormat.query.get(FileFormat_id)
        return make_response(jsonify(file_format.serialise()),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@file_format_bp.route('/apiv1/get_file_formats',methods=['GET'])
@jwt_required()
def get_all_file_formats():
    try:
        file_formats = [z.serialise() for z in FileFormat.query.all()]
        return make_response(jsonify(file_formats),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@file_format_bp.route('/apiv1/delete_file_format/<int:FileFormat_id>',methods=['DELETE'])
@jwt_required()
def delete_file_format(FileFormat_id):
    try:
        file_format = FileFormat.query.get(FileFormat_id)
        file_format.delete()
        return make_response(jsonify({'message':'File Format successfully deleted.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)
