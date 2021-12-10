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
from ..middleware.permissions import only_data_admin


cuttings_bp = Blueprint('cuttings_bp', __name__)

@cuttings_bp.route('/apiv1/add_cutting',methods=['POST'])
@jwt_required()
@only_data_admin
def add_cutting():
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()

    try:
        new_cutting = Cuttings(
                        WellboreId = data['WellboreId'],
                        SampleBoxNumber = data['SampleBoxNumber'],
                        CuttingCategory = data['CuttingCategory'],
                        SampleType = data['SampleType'],
                        MinimumDepth = data['MinimumDepth'],
                        MaximumDepth = data['MaximumDepth'],
                        SampleInterval = data['SampleInterval'],
                        DateReceived = data['DateReceived'],
                        OtherDescription = data['OtherDescription'],
                        CreatedById = user.CraneUserId
                    )
        new_cutting.save()
        return make_response(jsonify({'message':'Cutting added successfuly.'}),201)
    except:
        return make_response(str(traceback.format_exc()),500)


@cuttings_bp.route('/apiv1/edit_cutting/<int:SampleId>',methods=['PUT'])
@jwt_required()
@only_data_admin
def edit_cutting(SampleId):
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()

    try:
        cutting = Cuttings.query.get(SampleId)
        cutting.WellboreId = data['WellboreId']
        cutting.SampleBoxNumber = data['SampleBoxNumber']
        cutting.CuttingCategory = data['CuttingCategory']
        cutting.SampleType = data['SampleType']
        cutting.MinimumDepth = data['MinimumDepth']
        cutting.MaximumDepth = data['MaximumDepth']
        cutting.SampleInterval = data['SampleInterval']
        cutting.DateReceived = data['DateReceived']
        cutting.OtherDescription = data['OtherDescription']
        cutting.ModifiedBy = user.CraneUserId
        cutting.update()
        return make_response(jsonify({'message':'Cutting updated successfuly.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@cuttings_bp.route('/apiv1/get_cutting/<int:SampleId>',methods=['GET'])
@jwt_required()
def get_cutting(SampleId):
    try:
        cutting = Cuttings.query.get(SampleId)
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


@cuttings_bp.route('/apiv1/delete_cutting/<int:SampleId>',methods=['DELETE'])
@jwt_required()
@only_data_admin
def delete_cutting(SampleId):
    try:
        cutting = Cuttings.query.get(SampleId)
        cutting.delete()
        return make_response(jsonify({'message':'Cutting successfully deleted.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)
