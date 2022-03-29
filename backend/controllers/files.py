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
from .. import db


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
            file_list_len = 0
            if type(file.get("CoreAnalysisReports")) is list or type(file.get("CorePhotograph")) is list\
                or type(file.get("AnalysisReports")) is list or type(file.get("RockPhotograph")) is list\
                    or type(file.get("CuttingsPhotograph")) is list or type(file.get("FluidPhotograph")) is list\
                        or type(file.get("PetrographicAnalysisReports")) is list\
                             or type(file.get("CuttingsReport")) is list:
                
                # cores
                if "CoreAnalysisReports" in file:
                    if len(file['CoreAnalysisReports']) > file_list_len:
                        file_list_len = len(file['CoreAnalysisReports'])
                if "CorePhotograph" in file:
                    if len(file['CorePhotograph']) > file_list_len:
                        file_list_len = len(file['CorePhotograph'])
                # fluid sample
                if "AnalysisReports" in file:
                    if len(file['AnalysisReports']) > file_list_len:
                        file_list_len = len(file['AnalysisReports'])
                if "FluidPhotograph" in file:
                    if len(file['FluidPhotograph']) > file_list_len:
                        file_list_len = len(file['FluidPhotograph'])
                # rock sample
                if "PetrographicAnalysisReports" in file:
                    if len(file['PetrographicAnalysisReports']) > file_list_len:
                        file_list_len = len(file['PetrographicAnalysisReports'])
                if "RockPhotograph" in file:
                    if len(file['RockPhotograph']) > file_list_len:
                        file_list_len = len(file['RockPhotograph'])
                # cuttings
                if "CuttingsReport" in file:
                    if len(file['CuttingsReport']) > file_list_len:
                        file_list_len = len(file['CuttingsReport'])
                if "CuttingsPhotograph" in file:
                    if len(file['CuttingsPhotograph']) > file_list_len:
                        file_list_len = len(file['CuttingsPhotograph'])

                for i in range(file_list_len):
                    # cores
                    if "CoreAnalysisReports" in file:
                        report_name = upload_file(file['CoreAnalysisReports'][i])
                    if "CorePhotograph" in file:
                        image = upload_file(file['CorePhotograph'][i])
                    # fluid sample
                    if "AnalysisReports" in file:
                        report_name = upload_file(file['AnalysisReports'][i])
                        Report_type = "Fluid_Samples"
                    if "FluidPhotograph" in file:
                        image = upload_file(file['FluidPhotograph'][i])
                        Report_type = "Fluid_Samples"
                    # rock sample
                    if "PetrographicAnalysisReports" in file:
                        report_name = upload_file(file['PetrographicAnalysisReports'][i])
                        Report_type = "Rock_Samples"
                    if "RockPhotograph" in file:
                        image = upload_file(file['RockPhotograph'][i])
                        Report_type = "Rock_Samples"
                    # cuttings
                    if "CuttingsReport" in file:
                        report_name = upload_file(file['CuttingsReport'][i])
                        Report_type = "Cuttings"
                    if "CuttingsPhotograph" in file:
                        image = upload_file(file['CuttingsPhotograph'][i])
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
                    db.session.add(new_file)
            else:
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
                db.session.add(new_file)

        if data:
            list_len = 0
            if type(data.get('CoreAnalysisReports')) is list or type(data.get('CorePhotograph')) is list\
                    or type(data.get('AnalysisReports')) is list or type(data.get('FluidPhotograph')) is list\
                        or type(data.get('PetrographicAnalysisReports')) is list or type(data.get('RockPhotograph')) is list\
                            or type(data.get('CuttingsReport')) is list or type(data.get('CuttingsPhotograph')) is list:
                
                # cores
                if "CoreAnalysisReports" in data:
                    if len(data['CoreAnalysisReports']) > list_len:
                        list_len = len(data['CoreAnalysisReports'])
                if "CorePhotograph" in data:
                    if len(data['CorePhotograph']) > list_len:
                        list_len = len(data['CorePhotograph'])
                # fluid sample
                if "AnalysisReports" in data:
                    if len(data['AnalysisReports']) > list_len:
                        list_len = len(data['AnalysisReports'])
                if "FluidPhotograph" in data:
                    if len(data['FluidPhotograph']) > list_len:
                        list_len = len(data['FluidPhotograph'])
                # rock sample
                if "PetrographicAnalysisReports" in data:
                    if len(data['PetrographicAnalysisReports']) > list_len:
                        list_len = len(data['PetrographicAnalysisReports'])
                if "RockPhotograph" in data:
                    if len(data['RockPhotograph']) > list_len:
                        list_len = len(data['RockPhotograph'])
                # cuttings
                if "CuttingsReport" in data:
                    if len(data['CuttingsReport']) > list_len:
                        list_len = len(data['CuttingsReport'])
                if "CuttingsPhotograph" in data:
                    if len(data['CuttingsPhotograph']) > list_len:
                        list_len = len(data['CuttingsPhotograph'])

                for i in range(list_len):
                    # cores
                    if "CoreAnalysisReports" in data:
                        report_name = data['CoreAnalysisReports'][i]
                    if "CorePhotograph" in data:
                        image = data['CorePhotograph'][i]
                    # fluid sample
                    if "AnalysisReports" in data:
                        report_name = data['AnalysisReports'][i]
                        Report_type = "Fluid_Samples"
                    if "FluidPhotograph" in data:
                        image = data['FluidPhotograph'][i]
                        Report_type = "Fluid_Samples"
                    # rock sample
                    if "PetrographicAnalysisReports" in data:
                        report_name = data['PetrographicAnalysisReports'][i]
                        Report_type = "Rock_Samples"
                    if "RockPhotograph" in data:
                        image = data['RockPhotograph'][i]
                        Report_type = "Rock_Samples"
                    # cuttings
                    if "CuttingsReport" in data:
                        report_name = data['CuttingsReport'][i]
                        Report_type = "Cuttings"
                    if "CuttingsPhotograph" in data:
                        image = data['CuttingsPhotograph'][i]
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
                    db.session.add(new_file)
            else:
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
                db.session.add(new_file)
        
        # save everything
        db.session.commit()

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