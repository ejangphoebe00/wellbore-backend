from flask import Blueprint, request, make_response, jsonify
from ..models.RockSamples import RockSamples, BasinsEnum
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


rock_samples_bp = Blueprint('rock_samples_bp', __name__)

@rock_samples_bp.route('/apiv1/add_rock_sample',methods=['POST'])
@jwt_required()
@only_data_admin
def add_rock_sample():
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()

    try:
        # rock_sample = RockSamples.query.filter_by(Sample_id=data['Sample_id']).first()
        # if rock_sample:
        #     return make_response(jsonify({'message':'Sample_id already exists.'}),409)
        if data['Sample_basin'] not in [element.value for element in BasinsEnum]:
            return make_response(jsonify({'message':f"{data['Sample_basin']} doesn't exist."}),400)
        new_rock_sample = RockSamples(
                        Store_id = data['Store_id'],
                        Date_collected = data['Date_collected'],
                        Date_received = data['Date_received'],
                        Sample_basin = data['Sample_basin'],
                        Sample_name = data['Sample_name'],
                        Coordinate_location = data['Coordinate_location'],
                        Petrographic_description = data['Petrographic_description'],
                        # Petrographic_analysis_reports = data['Petrographic_analysis_reports'],
                        CreatedBy_id = user.CraneUser_id
                    )
        new_rock_sample.save()
        return make_response(jsonify({'message':'Rock Sample added successfuly.'}),201)
    except:
        return make_response(str(traceback.format_exc()),500)


@rock_samples_bp.route('/apiv1/edit_rock_sample/<int:id>',methods=['PUT'])
@jwt_required()
@only_data_admin
def edit_rock_sample(id):
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()

    try:
        # rock_sample = RockSamples.query.filter_by(Sample_id=data['Sample_id']).first()
        # if rock_sample:
        #     if id != rock_sample.id:
        #         return make_response(jsonify({'message':'Sample_id already exists.'}),409)
        if data['Sample_basin'] not in [element.value for element in BasinsEnum]:
            return make_response(jsonify({'message':f"{data['Sample_basin']} doesn't exist."}),400)
        rock_sample = RockSamples.query.get(id)
        rock_sample.Store_id = data['Store_id']
        rock_sample.Date_collected = data['Date_collected']
        rock_sample.Date_received = data['Date_received']
        rock_sample.Sample_basin = data['Sample_basin']
        rock_sample.Sample_name = data['Sample_name']
        rock_sample.Coordinate_location = data['Coordinate_location']
        rock_sample.Petrographic_description = data['Petrographic_description']
        # rock_sample.Petrographic_analysis_reports = data['Petrographic_analysis_reports']
        rock_sample.Modified_by = user.CraneUser_id
        rock_sample.update()
        return make_response(jsonify({'message':'Rock sample updated successfuly.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@rock_samples_bp.route('/apiv1/get_rock_sample/<int:id>',methods=['GET'])
@jwt_required()
def get_rock_sample(id):
    try:
        # get Petrographic_analysis_reports
        reports = Files.query.filter(Files.Rock_samples_id == id, Files.Report_path!=None)
        report_names = []
        if reports:
            for report in reports:
                report_names.append(report.Report_path)

        rock_sample = RockSamples.query.get(id)
        new_rock_sample_object  = rock_sample.serialise()
        new_rock_sample_object['Petrographic_analysis_reports'] = report_names
        
        return make_response(jsonify(new_rock_sample_object),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@rock_samples_bp.route('/apiv1/get_rock_samples',methods=['GET'])
@jwt_required()
def get_all_rock_samples():
    try:
        rock_samples = [z.serialise() for z in RockSamples.query.all()]
        new_rock_samples = []
        for sample in rock_samples:
            # get Analysis_reports
            reports = Files.query.filter(Files.Rock_samples_id == sample['id'], Files.Report_path!=None)
            report_names = []
            if reports:
                for report in reports:
                    report_names.append(report.Report_path)

            sample['Petrographic_analysis_reports'] = report_names
            new_rock_samples.append(sample)
        
        return make_response(jsonify(new_rock_samples),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@rock_samples_bp.route('/apiv1/delete_rock_sample/<int:id>',methods=['DELETE'])
@jwt_required()
@only_data_admin
def delete_rock_sample(id):
    try:
        rock_sample = RockSamples.query.get(id)
        rock_sample.delete()
        return make_response(jsonify({'message':'Rock sample successfully deleted.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)
