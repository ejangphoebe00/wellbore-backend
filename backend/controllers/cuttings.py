from flask import Blueprint, request, make_response, jsonify
from ..models.Cuttings import Cuttings
from ..models.CraneUser import CraneUser, UserCatgoryEnum
from flask_jwt_extended import (
    jwt_required,
    get_jwt
    )
# reference for api changes https://flask-jwt-extended.readthedocs.io/en/stable/v4_upgrade_guide/#api-changes
import datetime
import traceback


cuttings_bp = Blueprint('cuttings_bp', __name__)

@cuttings_bp.route('/apiv1/add_cutting',methods=['POST'])
@jwt_required()
def add_cutting():
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()

    try:
        new_cutting = Cuttings(
                        Wellbore_id = data['Wellbore_id'],
                        Sample_box_number = data['Sample_box_number'],
                        Cutting_category = data['Cutting_category'],
                        Sample_type = data['Sample_type'],
                        Minimum_depth = data['Minimum_depth'],
                        Maximum_depth = data['Maximum_depth'],
                        Sample_interval = data['Sample_interval'],
                        Date_received = data['Date_received'],
                        Other_description = data['Other_description'],
                        CreatedBy_id = user.CraneUser_id
                    )
        new_cutting.save()
        return make_response(jsonify({'message':'Cutting added successfuly.'}),201)
    except:
        return make_response(str(traceback.format_exc()),500)


@cuttings_bp.route('/apiv1/edit_cutting/<int:Sample_id>',methods=['PUT'])
@jwt_required()
def edit_cutting(Sample_id):
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()

    try:
        cutting = Cuttings.query.get(Sample_id)
        cutting.Wellbore_id = data['Wellbore_id']
        cutting.Sample_box_number = data['Sample_box_number']
        cutting.Cutting_category = data['Cutting_category']
        cutting.Sample_type = data['Sample_type']
        cutting.Minimum_depth = data['Minimum_depth']
        cutting.Maximum_depth = data['Maximum_depth']
        cutting.Sample_interval = data['Sample_interval']
        cutting.Date_received = data['Date_received']
        cutting.Other_description = data['Other_description']
        cutting.Modified_by = user.CraneUser_id
        cutting.update()
        return make_response(jsonify({'message':'Cutting updated successfuly.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@cuttings_bp.route('/apiv1/get_cutting/<int:Sample_id>',methods=['GET'])
@jwt_required()
def get_cutting(Sample_id):
    try:
        cutting = Cuttings.query.get(Sample_id)
        return make_response(jsonify(cutting.serialise()),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@cuttings_bp.route('/apiv1/get_cuttings',methods=['GET'])
@jwt_required()
def get_all_cuttings():
    try:
        cuttings = [z.serialise() for z in Cuttings.query.all()]
        return make_response(jsonify(cuttings),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@cuttings_bp.route('/apiv1/delete_cutting/<int:Sample_id>',methods=['DELETE'])
@jwt_required()
def delete_cutting(Sample_id):
    try:
        cutting = Cuttings.query.get(Sample_id)
        cutting.delete()
        return make_response(jsonify({'message':'Cutting successfully deleted.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)
