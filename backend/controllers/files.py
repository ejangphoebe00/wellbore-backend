from flask import Blueprint, request, make_response, jsonify
from ..models.CraneUser import CraneUser
from flask_jwt_extended import (
    jwt_required,
    get_jwt
    )
import traceback
from .helper_functions import upload_file
from ..models.Files import Files
from ..middleware.permissions import only_data_admin


files_bp = Blueprint('files_bp', __name__)

@files_bp.route('/apiv1/add_file/<int:sample_id>',methods=['POST'])
@jwt_required()
@only_data_admin
def add_file(sample_id):
    if request.is_json:
        data = request.get_json(force=True)
    else:
        data = request.form
    file = request.files
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()
    try:
        # get last inserted core
        # core = Cores.query.order_by(Cores.Core_sample_id.desc()).first()

        # check if file in incoming data
        report_name = None
        image = None
        Cores_id = None
        Fluid_samples_id = None
        Rock_samples_id = None
        Report_type = "Cores"
        if file:
            # cores
            if "Core_analysis_reports" in file:
                report_name = upload_file(file['Core_analysis_reports'])
            if "Core_photograph" in file:
                image = upload_file(file['Core_photograph'])
            # fluid sample
            if "Analysis_reports" in file:
                report_name = upload_file(file['Analysis_reports'])
                Report_type = "Fluid_Samples"
            # rock sample
            if "Petrographic_analysis_reports" in file:
                report_name = upload_file(file['Petrographic_analysis_reports'])
                Report_type = "Rock_Samples"

        if data:
            # cores
            if "Core_analysis_reports" in data:
                report_name = data['Core_analysis_reports']
            if "Core_photograph" in data:
                image = data['Core_photograph']
            # fluid sample
            if "Analysis_reports" in data:
                report_name = data['Analysis_reports']
                Report_type = "Fluid_Samples"
            # rock sample
            if "Petrographic_analysis_reports" in data:
                report_name = data['Petrographic_analysis_reports']
                Report_type = "Rock_Samples"

        # update foreign keys
        if Report_type == "Cores":
            Cores_id = sample_id
        elif Report_type == "Fluid_Samples":
            Fluid_samples_id = sample_id
        else:
            Rock_samples_id = sample_id


        # save file
        new_file = Files(
            Cores_id = Cores_id,
            Fluid_samples_id = Fluid_samples_id,
            Rock_samples_id = Rock_samples_id,
            Report_type = Report_type,
            Report_path = report_name,
            Photograph_path = image,
            CreatedBy_id = user.CraneUser_id
        )
        new_file.save()

        return make_response(jsonify({'message':'File added successfuly.'}),201)
    except:
        return make_response(str(traceback.format_exc()),500)


@files_bp.route('/apiv1/delete_file/<int:File_id>',methods=['DELETE'])
@jwt_required()
@only_data_admin
def delete_core(File_id):
    try:
        file = Files.query.get(File_id)
        file.delete()
        return make_response(jsonify({'message':'File successfully deleted.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)