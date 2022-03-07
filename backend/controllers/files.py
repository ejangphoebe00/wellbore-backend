from flask import Blueprint, request, make_response, jsonify
from ..models.CraneUser import CraneUser
from flask_jwt_extended import (
    jwt_required,
    get_jwt
    )
import traceback
from .helper_functions import upload_file, remove_file
from ..models.Files import Files
from ..middleware.permissions import only_data_admin


files_bp = Blueprint('files_bp', __name__)

@files_bp.route('/apiv1/add_file/<int:sampleId>',methods=['POST'])
@jwt_required()
@only_data_admin
def add_file(sampleId):
    if request.is_json:
        data = request.get_json(force=True)
    else:
        data = request.form
    file = request.files
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()
    try:
        report_name = None
        image = None
        CoresId = None
        Fluid_samplesId = None
        Rock_samplesId = None
        Cuttings_samplesId = None
        Report_type = "Cores"
        if file:
            # cores
            if "CoreAnalysisReports" in file:
                report_name = upload_file(file['CoreAnalysisReports'])
            if "CorePhotograph" in file:
                image = upload_file(file['CorePhotograph'])
            # fluid sample
            if "AnalysisReports" in file:
                report_name = upload_file(file['AnalysisReports'])
                Report_type = "Fluid_Samples"
            if "FluidPhotograph" in file:
                image = upload_file(file['FluidPhotograph'])
                Report_type = "Fluid_Samples"
            # rock sample
            if "PetrographicAnalysisReports" in file:
                report_name = upload_file(file['PetrographicAnalysisReports'])
                Report_type = "Rock_Samples"
            if "RockPhotograph" in file:
                image = upload_file(file['RockPhotograph'])
                Report_type = "Rock_Samples"
            # cuttings
            if "CuttingsReport" in file:
                report_name = upload_file(file['CuttingsReport'])
                Report_type = "Cuttings"
            if "CuttingsPhotograph" in file:
                image = upload_file(file['CuttingsPhotograph'])
                Report_type = "Cuttings"

        if data:
            # cores
            if "CoreAnalysisReports" in data:
                report_name = data['CoreAnalysisReports']
            if "CorePhotograph" in data:
                image = data['CorePhotograph']
            # fluid sample
            if "AnalysisReports" in data:
                report_name = data['AnalysisReports']
                Report_type = "Fluid_Samples"
            if "FluidPhotograph" in data:
                image = data['FluidPhotograph']
                Report_type = "Fluid_Samples"
            # rock sample
            if "PetrographicAnalysisReports" in data:
                report_name = data['PetrographicAnalysisReports']
                Report_type = "Rock_Samples"
            if "RockPhotograph" in data:
                image = data['RockPhotograph']
                Report_type = "Rock_Samples"
            # cuttings
            if "CuttingsReport" in data:
                report_name = data['CuttingsReport']
                Report_type = "Cuttings"
            if "CuttingsPhotograph" in data:
                image = data['CuttingsPhotograph']
                Report_type = "Cuttings"

        # update foreign keys
        if Report_type == "Cores":
            CoresId = sampleId
        elif Report_type == "Fluid_Samples":
            Fluid_samplesId = sampleId
        elif Report_type == "Cuttings":
            Cuttings_samplesId = sampleId
        else:
            Rock_samplesId = sampleId


        # save file
        new_file = Files(
            CoresId = CoresId,
            FluidSamplesId = Fluid_samplesId,
            RockSamplesId = Rock_samplesId,
            CuttingsId = Cuttings_samplesId,
            ReportType = Report_type,
            ReportPath = report_name,
            PhotographPath = image,
            CreatedById = user.CraneUserId
        )
        new_file.save()

        return make_response(jsonify({'message':'File added successfuly.'}),201)
    except:
        return make_response(str(traceback.format_exc()),500)


@files_bp.route('/apiv1/delete_file/<int:FileId>',methods=['DELETE'])
@jwt_required()
@only_data_admin
def delete_file(FileId):
    try:
        file = Files.query.get(FileId)
        file.delete()
        if file.ReportPath is not None:
            outcome = remove_file(file.ReportPath)
        if file.PhotographPath is not None:
            outcome = remove_file(file.PhotographPath)

        return make_response(jsonify({'message':outcome}),200)
    except:
        return make_response(str(traceback.format_exc()),500)