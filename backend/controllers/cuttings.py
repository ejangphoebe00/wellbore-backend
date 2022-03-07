from flask import Blueprint, request, make_response, jsonify

from backend.models.Files import Files
from ..models.Cuttings import Cuttings
from ..models.CraneUser import CraneUser, DeleteStatusEnum
from flask_jwt_extended import (
    jwt_required,
    get_jwt
    )
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
                        SampleInterval = data['SampleInterval'],
                        DateReceived = data['DateReceived'],
                        OtherDescription = data['OtherDescription'],
                        CreatedById = user.CraneUserId,
                        TopDepth = data['TopDepth'],
                        BottomDepth = data['BottomDepth'],
                        StoreIdentifier = data['StoreIdentifier'],
                        Operator = data['Operator'],
                        SamplingCompany = data['SamplingCompany'],
                        SamplingDate = data['SamplingDate'],
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
        cutting.SampleInterval = data['SampleInterval']
        cutting.DateReceived = data['DateReceived']
        cutting.OtherDescription = data['OtherDescription']
        cutting.ModifiedBy = user.CraneUserId
        cutting.TopDepth = data['TopDepth']
        cutting.BottomDepth = data['BottomDepth']
        cutting.StoreIdentifier = data['StoreIdentifier']
        cutting.Operator = data['Operator']
        cutting.SamplingCompany = data['SamplingCompany']
        cutting.SamplingDate = data['SamplingDate']
        cutting.update()
        return make_response(jsonify({'message':'Cutting updated successfuly.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@cuttings_bp.route('/apiv1/get_cutting/<int:SampleId>',methods=['GET'])
@jwt_required()
def get_cutting(SampleId):
    try:
        # get photographs
        photos = Files.query.filter(Files.CuttingsId == SampleId, Files.PhotographPath!=None)
        photo_names = []
        if photos:
            for photo in photos:
                photo_names.append(photo.PhotographPath)
        
        # get reports
        reports = Files.query.filter(Files.CuttingsId == SampleId, Files.ReportPath!=None)
        report_names = []
        if reports:
            for report in reports:
                report_names.append(report.ReportPath)

        cutting = Cuttings.query.get(SampleId)
        new_cutting_object  = cutting.serialise()
        new_cutting_object['CuttingsReport'] = report_names
        new_cutting_object['CuttingsPhotograph'] = photo_names

        return make_response(jsonify(new_cutting_object),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@cuttings_bp.route('/apiv1/get_cuttings',methods=['GET'])
@jwt_required()
def get_all_cuttings():
    try:
        cuttings = [z.serialise() for z in Cuttings.query.\
            filter((Cuttings.DeleteStatus==DeleteStatusEnum.Available) | (Cuttings.DeleteStatus==None))]
        new_cuttings = []
        for cutting in cuttings:
            # get photographs
            photos = Files.query.filter(Files.CuttingsId == cutting["SampleId"], Files.PhotographPath!=None)
            photo_names = []
            if photos:
                for photo in photos:
                    photo_names.append(photo.PhotographPath)
            
            # get reports
            reports = Files.query.filter(Files.CuttingsId == cutting["SampleId"], Files.ReportPath!=None)
            report_names = []
            if reports:
                for report in reports:
                    report_names.append(report.ReportPath)

            cutting['CuttingsReport'] = report_names
            cutting['CuttingsPhotograph'] = photo_names
            new_cuttings.append(cutting)
        return make_response(jsonify(new_cuttings),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@cuttings_bp.route('/apiv1/delete_cutting/<int:SampleId>',methods=['DELETE'])
@jwt_required()
@only_data_admin
def delete_cutting(SampleId):
    try:
        cutting = Cuttings.query.get(SampleId)
        cutting.DeleteStatus = DeleteStatusEnum.Deleted
        cutting.update()
        return make_response(jsonify({'message':'Cutting successfully deleted.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)
