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
                        Wellbore_id = data['Wellbore_id'],
                        Sampling_activity = data['Sampling_activity'],
                        Fluid_category = data['Fluid_category'],
                        Sample_type = data['Sample_type'],
                        Sample_volume = data['Sample_volume'],
                        Depth_obtained = data['Depth_obtained'],
                        Date_collected = data['Date_collected'],
                        Date_received = data['Date_received'],
                        Sampling_company = data['Sampling_company'],
                        # Analysis_reports = data['Analysis_reports'],
                        CreatedBy_id = user.CraneUser_id
                    )
        new_fluid_sample.save()
        return make_response(jsonify({'message':'Fluid Sample added successfuly.'}),201)
    except:
        return make_response(str(traceback.format_exc()),500)


@fluid_samples_bp.route('/apiv1/edit_fluid_sample/<int:Sample_id>',methods=['PUT'])
@jwt_required()
@only_data_admin
def edit_fluid_sample(Sample_id):
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()

    try:
        fluid_sample = FluidSamples.query.get(Sample_id)
        fluid_sample.Wellbore_id = data['Wellbore_id']
        fluid_sample.Sampling_activity = data['Sampling_activity']
        fluid_sample.Fluid_category = data['Fluid_category']
        fluid_sample.Sample_type = data['Sample_type']
        fluid_sample.Sample_volume = data['Sample_volume']
        fluid_sample.Depth_obtained = data['Depth_obtained']
        fluid_sample.Date_collected = data['Date_collected']
        fluid_sample.Date_received = data['Date_received']
        fluid_sample.Sampling_company = data['Sampling_company']
        # fluid_sample.Analysis_reports = data['Analysis_reports']
        fluid_sample.Modified_by = user.CraneUser_id
        fluid_sample.update()
        return make_response(jsonify({'message':'Fluid sample updated successfuly.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@fluid_samples_bp.route('/apiv1/get_fluid_sample/<int:Sample_id>',methods=['GET'])
@jwt_required()
def get_fluid_sample(Sample_id):
    try:
        # get Analysis_reports
        reports = Files.query.filter(Files.Fluid_samples_id == Sample_id, Files.Report_path!=None)
        report_names = []
        if reports:
            for report in reports:
                report_names.append(report.Report_path)

        fluid_sample = FluidSamples.query.get(Sample_id)
        new_fluid_sample_object  = fluid_sample.serialise()
        new_fluid_sample_object['Analysis_reports'] = report_names
        
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
            reports = Files.query.filter(Files.Fluid_samples_id == sample['Sample_id'], Files.Report_path!=None)
            report_names = []
            if reports:
                for report in reports:
                    report_names.append(report.Report_path)

            sample['Analysis_reports'] = report_names
            new_fluid_sample.append(sample)

        return make_response(jsonify(fluid_samples),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@fluid_samples_bp.route('/apiv1/delete_fluid_sample/<int:Sample_id>',methods=['DELETE'])
@jwt_required()
@only_data_admin
def delete_fluid_sample(Sample_id):
    try:
        fluid_sample = FluidSamples.query.get(Sample_id)
        fluid_sample.delete()
        return make_response(jsonify({'message':'Fluid sample successfully deleted.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)
