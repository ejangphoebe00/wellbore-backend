from flask import Blueprint, request, make_response, jsonify
from ..models.FluidSamples import FluidSamples
from ..models.CraneUser import CraneUser, UserCatgoryEnum
from flask_jwt_extended import (
    jwt_required,
    get_jwt
    )
# reference for api changes https://flask-jwt-extended.readthedocs.io/en/stable/v4_upgrade_guide/#api-changes
import datetime
import traceback
from ..models.Files import Files
from ..middleware.permissions import only_data_admin


fluid_samples_bp = Blueprint('fluid_samples_bp', __name__)

@fluid_samples_bp.route('/apiv1/add_fluid_sample',methods=['POST'])
@jwt_required()
@only_data_admin
def add_fluid_sample():
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()

    try:
        new_fluid_sample = FluidSamples(
                        WellboreId = data['WellboreId'],
                        SamplingActivity = data['SamplingActivity'],
                        FluidCategory = data['FluidCategory'],
                        SampleType = data['SampleType'],
                        SampleBasin = data['SampleBasin'],
                        SampleVolume = data['SampleVolume'],
                        DepthObtained = data['DepthObtained'],
                        DateCollected = data['DateCollected'],
                        DateReceived = data['DateReceived'],
                        SamplingCompany = data['SamplingCompany'],
                        # Analysis_reports = data['Analysis_reports'],
                        CreatedById = user.CraneUserId
                    )
        new_fluid_sample.save()
        return make_response(jsonify({'message':'Fluid Sample added successfuly.'}),201)
    except:
        return make_response(str(traceback.format_exc()),500)


@fluid_samples_bp.route('/apiv1/edit_fluid_sample/<int:SampleId>',methods=['PUT'])
@jwt_required()
@only_data_admin
def edit_fluid_sample(SampleId):
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()

    try:
        fluid_sample = FluidSamples.query.get(SampleId)
        fluid_sample.WellboreId = data['WellboreId']
        fluid_sample.SamplingActivity = data['SamplingActivity']
        fluid_sample.FluidCategory = data['FluidCategory']
        fluid_sample.SampleType = data['SampleType']
        fluid_sample.SampleBasin = data['SampleBasin']
        fluid_sample.SampleVolume = data['SampleVolume']
        fluid_sample.DepthObtained = data['DepthObtained']
        fluid_sample.DateCollected = data['DateCollected']
        fluid_sample.DateReceived = data['DateReceived']
        fluid_sample.SamplingCompany = data['SamplingCompany']
        # fluid_sample.Analysis_reports = data['Analysis_reports']
        fluid_sample.ModifiedBy = user.CraneUserId
        fluid_sample.update()
        return make_response(jsonify({'message':'Fluid sample updated successfuly.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@fluid_samples_bp.route('/apiv1/get_fluid_sample/<int:SampleId>',methods=['GET'])
@jwt_required()
def get_fluid_sample(SampleId):
    try:
        # get Analysis_reports
        reports = Files.query.filter(Files.FluidSamplesId == SampleId, Files.ReportPath!=None)
        report_names = []
        if reports:
            for report in reports:
                report_names.append(report.ReportPath)

        fluid_sample = FluidSamples.query.get(SampleId)
        new_fluid_sample_object  = fluid_sample.serialise()
        new_fluid_sample_object['AnalysisReports'] = report_names
        
        return make_response(jsonify(new_fluid_sample_object),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@fluid_samples_bp.route('/apiv1/get_fluid_samples',methods=['GET'])
@jwt_required()
def get_all_fluid_samples():
    try:
        fluid_samples = [z.serialise() for z in FluidSamples.query.all()]
        new_fluid_sample = []
        for sample in fluid_samples:
            # get Analysis_reports
            reports = Files.query.filter(Files.FluidSamplesId == sample['SampleId'], Files.ReportPath!=None)
            report_names = []
            if reports:
                for report in reports:
                    report_names.append(report.ReportPath)

            sample['AnalysisReports'] = report_names
            new_fluid_sample.append(sample)

        return make_response(jsonify(fluid_samples),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@fluid_samples_bp.route('/apiv1/delete_fluid_sample/<int:SampleId>',methods=['DELETE'])
@jwt_required()
@only_data_admin
def delete_fluid_sample(SampleId):
    try:
        fluid_sample = FluidSamples.query.get(SampleId)
        fluid_sample.delete()
        return make_response(jsonify({'message':'Fluid sample successfully deleted.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)
