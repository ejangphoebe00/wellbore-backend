from flask import Blueprint, request, make_response, jsonify
from ..models.Cores import Cores
from ..models.CraneUser import CraneUser, UserCatgoryEnum
from flask_jwt_extended import (
    jwt_required,
    get_jwt
    )
# reference for api changes https://flask-jwt-extended.readthedocs.io/en/stable/v4_upgrade_guide/#api-changes
import datetime
import traceback
from ..models.Files import Files


cores_bp = Blueprint('cores_bp', __name__)

@cores_bp.route('/apiv1/add_core',methods=['POST'])
@jwt_required()
def add_core():
    if request.is_json:
            data = request.get_json(force=True)
    else:
        data = request.form
    
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()
    
    try:
        core = Cores.query.filter_by(Core_number=data['Core_number']).first()
        if core:
            return make_response(jsonify({'message':'Core_number already exists.'}),409)
        new_core = Cores(
                        Coring_contractor = data['Coring_contractor'],
                        Wellbore_id = data['Wellbore_id'],
                        Core_number = data['Core_number'],
                        Coring_date = data['Coring_date'],
                        Top_MD = data['Top_MD'], #depth
                        Bottom_MD = data['Bottom_MD'], #depth
                        Cut_length = data['Cut_length'],
                        Percentage_recovery = data['Percentage_recovery'],
                        Top_formation = data['Top_formation'],
                        Bottom_formation = data['Bottom_formation'],
                        # Core_photograph = data['Core_photograph'],
                        # Core_analysis_reports = data['Core_analysis_reports'],
                        CreatedBy_id = user.CraneUser_id
                    )
        new_core.save()
        return make_response(jsonify({'message':'Core added successfuly.'}),201)
    except:
        return make_response(str(traceback.format_exc()),500)



@cores_bp.route('/apiv1/edit_core/<int:Core_sample_id>',methods=['PUT'])
@jwt_required()
def edit_core(Core_sample_id):
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()

    try:
        core = Cores.query.filter_by(Core_number=data['Core_number']).first()
        if core:
            if Core_sample_id != core.Core_sample_id:
                return make_response(jsonify({'message':'Core_number already exists.'}),409)
        core = Cores.query.get(Core_sample_id)
        core.Coring_contractor = data['Coring_contractor']
        core.Wellbore_id = data['Wellbore_id']
        core.Core_number = data['Core_number']
        core.Coring_date = data['Coring_date']
        core.Top_MD = data['Top_MD']
        core.Bottom_MD = data['Bottom_MD']
        core.Cut_length = data['Cut_length']
        core.Percentage_recovery = data['Percentage_recovery']
        core.Top_formation = data['Top_formation']
        core.Bottom_formation = data['Bottom_formation']
        # core.Core_photograph = data['Core_photograph']
        # core.Core_analysis_reports = data['Core_analysis_reports']
        core.Modified_by = user.CraneUser_id
        core.update()
        return make_response(jsonify({'message':'Core updated successfuly.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@cores_bp.route('/apiv1/get_core/<int:Core_sample_id>',methods=['GET'])
@jwt_required()
def get_core(Core_sample_id):
    try:
        # get Core_photographs
        photos = Files.query.filter(Files.Cores_id == Core_sample_id, Files.Photograph_path!=None)
        photo_names = []
        if photos:
            for photo in photos:
                photo_names.append(photo.Photograph_path)
        
        # get Core_analysis_reports
        reports = Files.query.filter(Files.Cores_id == Core_sample_id, Files.Report_path!=None)
        report_names = []
        if reports:
            for report in reports:
                report_names.append(report.Report_path)

        core = Cores.query.get(Core_sample_id)
        new_core_object  = core.serialise()
        new_core_object['Core_analysis_reports'] = report_names
        new_core_object['Core_photographs'] = photo_names

        return make_response(jsonify(new_core_object),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@cores_bp.route('/apiv1/get_cores',methods=['GET'])
@jwt_required()
def get_all_cores():
    try:
        cores = [z.serialise() for z in Cores.query.all()]
        new_cores = []
        for core in cores:
            # get Core_photographs
            photos = Files.query.filter(Files.Cores_id == core["Core_sample_id"], Files.Photograph_path!=None)
            photo_names = []
            if photos:
                for photo in photos:
                    photo_names.append(photo.Photograph_path)
            
            # get Core_analysis_reports
            reports = Files.query.filter(Files.Cores_id == core["Core_sample_id"], Files.Report_path!=None)
            report_names = []
            if reports:
                for report in reports:
                    report_names.append(report.Report_path)

            core['Core_analysis_reports'] = report_names
            core['Core_photographs'] = photo_names
            new_cores.append(core)

        # cores = [z.serialise() for z in Cores.query.all()]
        return make_response(jsonify(new_cores),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@cores_bp.route('/apiv1/delete_core/<int:Core_sample_id>',methods=['DELETE'])
@jwt_required()
def delete_core(Core_sample_id):
    try:
        core = Cores.query.get(Core_sample_id)
        core.delete()
        return make_response(jsonify({'message':'Core successfully deleted.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)
