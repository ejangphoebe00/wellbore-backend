from flask import Blueprint, request, make_response, jsonify
from ..models.Core import Cores
from .. models.Wellbore import Wellbore
from .. models.Files import Files
from ..models.CraneUser import CraneUser, UserCatgoryEnum
from flask_jwt_extended import (
    jwt_required,
    get_jwt
    )
# reference for api changes https://flask-jwt-extended.readthedocs.io/en/stable/v4_upgrade_guide/#api-changes
import datetime
import traceback
from ..middleware.permissions import only_data_admin


core_bp = Blueprint('core_bp', __name__)

@core_bp.route('/apiv1/add_core',methods=['POST'])
@jwt_required()
@only_data_admin
def add_core():
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()

    # check for redundancies
    core_number = Cores.query.filter_by(CoreNumber=data['CoreNumber']).first()
    # core_name = Cores.query.filter_by(WellboreCoreName=data['WellboreCoreName']).first()
    if core_number and core_number.CoreNumber != None:
        return make_response(jsonify({'message':'CoreNumber already exists.'}),409)
    # if core_name and core_name.WellboreCoreName != None:
    #     return make_response(jsonify({'message':'WellboreCoreName already exists.'}),409)
    try:
        new_core = Cores(
                        Wellbore_id = data['Wellbore_id'],#comes from welbore
                        CoreTypeName = data['CoreTypeName'],
                        CoreNumber = data['CoreNumber'],
                        CoringDate = data['CoringDate'],
                        WBCoringContractor_id = data['WBCoringContractor_id'], # should come from company
                        CoreTopMD = data['CoreTopMD'],
                        CoreBtmMD = data['CoreBtmMD'],
                        CoreTopTVD = data['CoreTopTVD'],
                        CoreBtmTVD = data['CoreBtmTVD'],
                        CutLength = data['CutLength'],
                        CutLengthTVD = data['CutLengthTVD'],
                        RecoveredLength = data['RecoveredLength'],
                        PercentageCoreRecovery = Cores.calculate_percentage_core_recovery(data['CutLength'],data['RecoveredLength']),
                        CoreTopStratLitho_id = data['CoreTopStratLitho_id'], # should come from stratlitho
                        CoreBottomStratLitho_id = data['CoreBottomStratLitho_id'], # should come from stratlitho
                        CorePictureSoftcopyPath = data['CorePictureSoftcopyPath'],
                        CorePictureHyperlink = data['CorePictureHyperlink'],
                        PictureUploadDate = data['PictureUploadDate'],
                        CoreReportSoftcopyPath = data['CoreReportSoftcopyPath'],
                        CoreReportHyperlink = data['CoreReportHyperlink'],
                        ReportUploadDate = data['ReportUploadDate'],
                        # ReportFormat_id = data['ReportFormat_id'],#should come from file format
                        ReportFileSize = data['ReportFileSize'],
                        # CoreReportSecurityGrade_id = data['CoreReportSecurityGrade_id'],#comes from file security grade
                        ReportOpenDueDate = data['ReportOpenDueDate'],
                        ReportDocumentTitle = data['ReportDocumentTitle'],
                        ReportReceivedDate = data['ReportReceivedDate'],
                        ReportDocumentDate = data['ReportDocumentDate'],
                        ReportDocumentName = data['ReportDocumentName'],
                        # WellboreCoreName = data['WellboreCoreName'],
                        Comments = data['Comments'],
                        CreatedBy_id = user.CraneUser_id,
                        DateCreated = datetime.datetime.now()
                    )
        new_core.save()
        return make_response(jsonify({'message':'Welbore Core added successfuly.'}),201)
    except:
        return make_response(str(traceback.format_exc()),500)


@core_bp.route('/apiv1/edit_core/<int:WellboreCore_id>',methods=['PUT'])
@jwt_required()
@only_data_admin
def edit_core(WellboreCore_id):
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()
    # check for redundancies
    core_number = Cores.query.filter_by(CoreNumber=data['CoreNumber']).first()
    # core_name = Cores.query.filter_by(WellboreCoreName=data['WellboreCoreName']).first()
    if core_number and core_number.CoreNumber != None:
        if WellboreCore_id != core_number.WellboreCore_id:
            return make_response(jsonify({'message':'CoreNumber already exists.'}),409)
    # if core_name and core_name.WellboreCoreName != None:
    #     if WellboreCore_id != core_name.WellboreCore_id:
    #         return make_response(jsonify({'message':'WellboreCoreName already exists.'}),409)
    try:
        core = Cores.query.get(WellboreCore_id)
        core.Wellbore_id = data['Wellbore_id']
        core.CoreNumber = data['CoreNumber']
        core.CoreTypeName = data['CoreTypeName']
        core.CoringDate = data['CoringDate']
        core.WBCoringContractor_id = data['WBCoringContractor_id']
        core.CoreTopMD = data['CoreTopMD']
        core.CoreBtmMD = data['CoreBtmMD']
        core.CoreTopTVD = data['CoreTopTVD']
        core.CoreBtmTVD = data['CoreBtmTVD']
        core.CutLength = data['CutLength']
        core.CutLengthTVD = data['CutLengthTVD']
        core.RecoveredLength = data['RecoveredLength']
        core.PercentageCoreRecovery = Cores.calculate_percentage_core_recovery(data['CutLength'],data['RecoveredLength'])
        core.CoreTopStratLitho_id = data['CoreTopStratLitho_id']
        core.CoreBottomStratLitho_id = data['CoreBottomStratLitho_id']
        core.CorePictureSoftcopyPath = data['CorePictureSoftcopyPath']
        core.CorePictureHyperlink = data['CorePictureHyperlink']
        core.PictureUploadDate = data['PictureUploadDate']
        core.CoreReportSoftcopyPath = data['CoreReportSoftcopyPath']
        core.CoreReportHyperlink = data['CoreReportHyperlink']
        core.ReportUploadDate = data['ReportUploadDate']
        # core.ReportFormat_id = data['ReportFormat_id']
        core.ReportFileSize = data['ReportFileSize']
        # core.CoreReportSecurityGrade_id = data['CoreReportSecurityGrade_id']
        core.ReportOpenDueDate = data['ReportOpenDueDate']
        core.ReportDocumentTitle = data['ReportDocumentTitle']
        core.ReportReceivedDate = data['ReportReceivedDate']
        core.ReportDocumentDate = data['ReportDocumentDate']
        core.ReportDocumentName = data['ReportDocumentName']
        # core.WellboreCoreName = data['WellboreCoreName']
        core.Comments = data['Comments']
        core.ModifiedOn = datetime.datetime.today()
        core.ModifiedBy = user.CraneUser_id
        core.update()
        return make_response(jsonify({'message':'Welbore Core updated successfuly.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get single core object
@core_bp.route('/apiv1/get_core/<int:WellboreCore_id>',methods=['GET'])
@jwt_required()
def get_core(WellboreCore_id):
    try:
        # get Core_photographs
        photos = Files.query.filter(Files.Cores_id == WellboreCore_id, Files.Photograph_path!=None)
        photo_names = []
        if photos:
            for photo in photos:
                photo_names.append(photo.Photograph_path)
        
        # get Core_analysis_reports
        reports = Files.query.filter(Files.Cores_id == WellboreCore_id, Files.Report_path!=None)
        report_names = []
        if reports:
            for report in reports:
                report_names.append(report.Report_path)

        core = Cores.query.get(WellboreCore_id)
        new_core_object  = core.serialise()
        new_core_object['Core_analysis_reports'] = report_names
        new_core_object['Core_photographs'] = photo_names

        return make_response(jsonify(new_core_object),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@core_bp.route('/apiv1/get_cores',methods=['GET'])
@jwt_required()
def get_all_cores():
    try:
        cores = [z.serialise() for z in Cores.query.all()]
        new_cores = []
        for core in cores:
            # get Core_photographs
            photos = Files.query.filter(Files.Cores_id == core["WellboreCore_id"], Files.Photograph_path!=None)
            photo_names = []
            if photos:
                for photo in photos:
                    photo_names.append(photo.Photograph_path)
            
            # get Core_analysis_reports
            reports = Files.query.filter(Files.Cores_id == core["WellboreCore_id"], Files.Report_path!=None)
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


@core_bp.route('/apiv1/delete_core/<int:WellboreCore_id>',methods=['DELETE'])
@jwt_required()
@only_data_admin
def delete_core(WellboreCore_id):
    try:
        core = Cores.query.get(WellboreCore_id)
        core.delete()
        return make_response(jsonify({'message':'Welbore Core successfully deleted.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)
