from flask import Blueprint, request, make_response, jsonify
from ..models.FileSecurityGrade import FileSecurityGrade
from ..models.CraneUser import CraneUser, UserCatgoryEnum
from flask_jwt_extended import (
    jwt_required,
    get_jwt
    )
# reference for api changes https://flask-jwt-extended.readthedocs.io/en/stable/v4_upgrade_guide/#api-changes
import datetime
import traceback


file_security_grade_bp = Blueprint('file_security_grade_bp', __name__)

@file_security_grade_bp.route('/apiv1/add_file_security_grade',methods=['POST'])
@jwt_required()
def add_file_security_grade():
    data = request.get_json(force=True)

    # check for redundancies
    grade_name = FileSecurityGrade.query.filter_by(FileSecurityGradeName=data['FileSecurityGradeName']).first()
    if grade_name:
        return make_response(jsonify({'message':'FileSecurityGradeName already exists.'}),409)
    try:
        new_file_security_grade = FileSecurityGrade(
                        FileSecurityGradeName = data['FileSecurityGradeName'],
                        SortOrder = data['SortOrder'],  
                        Comments = data['Comments'],
                    )
        new_file_security_grade.save()
        return make_response(jsonify({'message':'File Security Grade added successfuly.'}),201)
    except:
        return make_response(str(traceback.format_exc()),500)


@file_security_grade_bp.route('/apiv1/edit_file_security_grade/<int:FileSecurityGrade_id>',methods=['PUT'])
@jwt_required()
def edit_file_security_grade(FileSecurityGrade_id):
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()

    # check for redundancies
    grade_name = FileSecurityGrade.query.filter_by(FileSecurityGradeName=data['FileSecurityGradeName']).first()
    if FileSecurityGrade_id != grade_name.FileSecurityGrade_id:
        return make_response(jsonify({'message':'FileSecurityGradeName already exists.'}),409)
    try:
        file_security_grade = FileSecurityGrade.query.get(FileSecurityGrade_id)
        file_security_grade.FileSecurityGradeName = data['FileSecurityGradeName']
        file_security_grade.Comments = data['Comments']
        file_security_grade.SortOrder = data['SortOrder']
        file_security_grade.ModifiedOn = datetime.datetime.today()
        file_security_grade.ModifiedBy = user.CraneUser_id
        file_security_grade.update()
        return make_response(jsonify({'message':'File Security Grade updated successfuly.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get single file_security_grade object
@file_security_grade_bp.route('/apiv1/get_file_security_grade/<int:FileSecurityGrade_id>',methods=['GET'])
@jwt_required()
def get_file_security_grade(FileSecurityGrade_id):
    try:
        file_security_grade = FileSecurityGrade.query.get(FileSecurityGrade_id)
        return make_response(jsonify(file_security_grade.serialise()),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@file_security_grade_bp.route('/apiv1/get_file_security_grades',methods=['GET'])
@jwt_required()
def get_all_file_security_grades():
    try:
        file_security_grades = [z.serialise() for z in FileSecurityGrade.query.all()]
        return make_response(jsonify(file_security_grades),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@file_security_grade_bp.route('/apiv1/delete_file_security_grade/<int:FileSecurityGrade_id>',methods=['DELETE'])
@jwt_required()
def delete_file_security_grade(FileSecurityGrade_id):
    try:
        file_security_grade = FileSecurityGrade.query.get(FileSecurityGrade_id)
        file_security_grade.delete()
        return make_response(jsonify({'message':'File Security Grade successfully deleted.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)
