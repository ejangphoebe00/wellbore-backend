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
        # rock_sample = RockSamples.query.filter_by(SampleId=data['SampleId']).first()
        # if rock_sample:
        #     return make_response(jsonify({'message':'SampleId already exists.'}),409)
        if data['SampleBasin'] not in [element.value for element in BasinsEnum]:
            return make_response(jsonify({'message':f"{data['SampleBasin']} basin doesn't exist."}),400)
        new_rock_sample = RockSamples(
                        StoreId = data['StoreId'],
                        DateCollected = data['DateCollected'],
                        DateReceived = data['DateReceived'],
                        SampleBasin = data['SampleBasin'],
                        SampleName = data['SampleName'],
                        SamplePurpose = data['SamplePurpose'],
                        OtherSpecifiedSamplePurpose = data['OtherSpecifiedSamplePurpose'],
                        Latitude = data['Latitude'],
                        Longitude = data['Longitude'],
                        Operator = data['Operator'],
                        PetrographicDescription = data['PetrographicDescription'],
                        # Petrographic_analysis_reports = data['Petrographic_analysis_reports'],
                        CreatedById = user.CraneUserId
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
        # rock_sample = RockSamples.query.filter_by(SampleId=data['SampleId']).first()
        # if rock_sample:
        #     if id != rock_sample.id:
        #         return make_response(jsonify({'message':'SampleId already exists.'}),409)
        if data['SampleBasin'] not in [element.value for element in BasinsEnum]:
            return make_response(jsonify({'message':f"{data['SampleBasin']} basin doesn't exist."}),400)
        rock_sample = RockSamples.query.get(id)
        rock_sample.StoreId = data['StoreId']
        rock_sample.DateCollected = data['DateCollected']
        rock_sample.DateReceived = data['DateReceived']
        rock_sample.SampleBasin = data['SampleBasin']
        rock_sample.SampleName = data['SampleName']
        rock_sample.SamplePurpose = data['SamplePurpose']
        rock_sample.OtherSpecifiedSamplePurpose = data['OtherSpecifiedSamplePurpose']
        rock_sample.Latitude = data['Latitude']
        rock_sample.Longitude = data['Longitude']
        rock_sample.Operator = data['Operator']
        rock_sample.PetrographicDescription = data['PetrographicDescription']
        # rock_sample.Petrographic_analysis_reports = data['Petrographic_analysis_reports']
        rock_sample.ModifiedBy = user.CraneUserId
        rock_sample.update()
        return make_response(jsonify({'message':'Rock sample updated successfuly.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@rock_samples_bp.route('/apiv1/get_rock_sample/<int:id>',methods=['GET'])
@jwt_required()
def get_rock_sample(id):
    try:
        # get photographs
        photos = Files.query.filter(Files.RockSamplesId == id, Files.PhotographPath!=None)
        photo_names = []
        if photos:
            for photo in photos:
                photo_names.append(photo.PhotographPath)

        # get Petrographic_analysis_reports
        reports = Files.query.filter(Files.RockSamplesId == id, Files.ReportPath!=None)
        report_names = []
        if reports:
            for report in reports:
                report_names.append(report.ReportPath)

        rock_sample = RockSamples.query.get(id)
        new_rock_sample_object  = rock_sample.serialise()
        new_rock_sample_object['PetrographicAnalysisReports'] = report_names
        new_rock_sample_object['RockPhotograph'] = photo_names
        
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
            # get photographs
            photos = Files.query.filter(Files.RockSamplesId == sample["id"], Files.PhotographPath!=None)
            photo_names = []
            if photos:
                for photo in photos:
                    photo_names.append(photo.PhotographPath)

            # get Analysis_reports
            reports = Files.query.filter(Files.RockSamplesId == sample['id'], Files.ReportPath!=None)
            report_names = []
            if reports:
                for report in reports:
                    report_names.append(report.ReportPath)

            sample['PetrographicAnalysisReports'] = report_names
            sample['RockPhotograph'] = photo_names
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
