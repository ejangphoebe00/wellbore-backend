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
                        WellborePAUID = data['WellborePAUID'],#comes from welbore
                        WelboreCoreName = data['WelboreCoreName'],
                        CoreTypeName = data['CoreTypeName'],
                        CoreNumber = data['CoreNumber'],
                        CoringDate = data['CoringDate'],
                        WBCoringContractorId = data['WBCoringContractorId'], # should come from company
                        CoreTopMD = data['CoreTopMD'],
                        CoreBtmMD = data['CoreBtmMD'],
                        CoreTopTVD = data['CoreTopTVD'],
                        CoreBtmTVD = data['CoreBtmTVD'],
                        CutLength = data['CutLength'],
                        CutLengthTVD = data['CutLengthTVD'],
                        RecoveredLength = data['RecoveredLength'],
                        PercentageCoreRecovery = Cores.calculate_percentage_core_recovery(data['CutLength'],data['RecoveredLength']),
                        CoreTopStratLithoId = data['CoreTopStratLithoId'], # should come from stratlitho
                        CoreBottomStratLithoId = data['CoreBottomStratLithoId'], # should come from stratlitho
                        CorePictureSoftcopyPath = data['CorePictureSoftcopyPath'],
                        CorePictureHyperlink = data['CorePictureHyperlink'],
                        PictureUploadDate = data['PictureUploadDate'],
                        CoreReportSoftcopyPath = data['CoreReportSoftcopyPath'],
                        CoreReportHyperlink = data['CoreReportHyperlink'],
                        ReportUploadDate = data['ReportUploadDate'],
                        ReportFileFormat = data['ReportFileFormat'],
                        ReportFileSize = data['ReportFileSize'],
                        ReportSecurityGrade = data['ReportSecurityGrade'],
                        ReportOpenDueDate = data['ReportOpenDueDate'],
                        ReportDocumentTitle = data['ReportDocumentTitle'],
                        ReportReceivedDate = data['ReportReceivedDate'],
                        ReportDocumentDate = data['ReportDocumentDate'],
                        ReportDocumentName = data['ReportDocumentName'],
                        # WellboreCoreName = data['WellboreCoreName'],
                        Comments = data['Comments'],
                        CreatedById = user.CraneUserId,
                        DateCreated = datetime.datetime.now()
                    )
        new_core.save()
        return make_response(jsonify({'message':'Welbore Core added successfuly.'}),201)
    except:
        return make_response(str(traceback.format_exc()),500)


@core_bp.route('/apiv1/edit_core/<int:WellboreCoreId>',methods=['PUT'])
@jwt_required()
@only_data_admin
def edit_core(WellboreCoreId):
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()
    # check for redundancies
    core_number = Cores.query.filter_by(CoreNumber=data['CoreNumber']).first()
    # core_name = Cores.query.filter_by(WellboreCoreName=data['WellboreCoreName']).first()
    if core_number and core_number.CoreNumber != None:
        if WellboreCoreId != core_number.WellboreCoreId:
            return make_response(jsonify({'message':'CoreNumber already exists.'}),409)
    # if core_name and core_name.WellboreCoreName != None:
    #     if WellboreCoreId != core_name.WellboreCoreId:
    #         return make_response(jsonify({'message':'WellboreCoreName already exists.'}),409)
    try:
        core = Cores.query.get(WellboreCoreId)
        core.WellborePAUID = data['WellborePAUID'] #comes from welbore
        core.WelboreCoreName = data['WelboreCoreName']
        core.CoreNumber = data['CoreNumber']
        core.CoreTypeName = data['CoreTypeName']
        core.CoringDate = data['CoringDate']
        core.WBCoringContractorId = data['WBCoringContractorId']
        core.CoreTopMD = data['CoreTopMD']
        core.CoreBtmMD = data['CoreBtmMD']
        core.CoreTopTVD = data['CoreTopTVD']
        core.CoreBtmTVD = data['CoreBtmTVD']
        core.CutLength = data['CutLength']
        core.CutLengthTVD = data['CutLengthTVD']
        core.RecoveredLength = data['RecoveredLength']
        core.PercentageCoreRecovery = Cores.calculate_percentage_core_recovery(data['CutLength'],data['RecoveredLength'])
        core.CoreTopStratLithoId = data['CoreTopStratLithoId']
        core.CoreBottomStratLithoId = data['CoreBottomStratLithoId']
        core.CorePictureSoftcopyPath = data['CorePictureSoftcopyPath']
        core.CorePictureHyperlink = data['CorePictureHyperlink']
        core.PictureUploadDate = data['PictureUploadDate']
        core.CoreReportSoftcopyPath = data['CoreReportSoftcopyPath']
        core.CoreReportHyperlink = data['CoreReportHyperlink']
        core.ReportUploadDate = data['ReportUploadDate']
        core.ReportFileFormat = data['ReportFileFormat']
        core.ReportFileSize = data['ReportFileSize']
        core.ReportSecurityGrade = data['ReportSecurityGrade']
        core.ReportOpenDueDate = data['ReportOpenDueDate']
        core.ReportDocumentTitle = data['ReportDocumentTitle']
        core.ReportReceivedDate = data['ReportReceivedDate']
        core.ReportDocumentDate = data['ReportDocumentDate']
        core.ReportDocumentName = data['ReportDocumentName']
        # core.WellboreCoreName = data['WellboreCoreName']
        core.Comments = data['Comments']
        core.ModifiedOn = datetime.datetime.now()
        core.ModifiedBy = user.CraneUserId
        core.update()
        return make_response(jsonify({'message':'Welbore Core updated successfuly.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get single core object
@core_bp.route('/apiv1/get_core/<int:WellboreCoreId>',methods=['GET'])
@jwt_required()
def get_core(WellboreCoreId):
    try:
        # get Core_photographs
        photos = Files.query.filter(Files.CoresId == WellboreCoreId, Files.PhotographPath!=None)
        photo_names = []
        if photos:
            for photo in photos:
                photo_names.append(photo.PhotographPath)
        
        # get Core_analysis_reports
        reports = Files.query.filter(Files.CoresId == WellboreCoreId, Files.ReportPath!=None)
        report_names = []
        if reports:
            for report in reports:
                report_names.append(report.ReportPath)

        core = Cores.query.get(WellboreCoreId)
        new_core_object  = core.serialise()
        new_core_object['CoreAnalysisReports'] = report_names
        new_core_object['CorePhotographs'] = photo_names

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
            photos = Files.query.filter(Files.CoresId == core["WellboreCoreId"], Files.PhotographPath!=None)
            photo_names = []
            if photos:
                for photo in photos:
                    photo_names.append(photo.PhotographPath)
            
            # get Core_analysis_reports
            reports = Files.query.filter(Files.CoresId == core["WellboreCoreId"], Files.ReportPath!=None)
            report_names = []
            if reports:
                for report in reports:
                    report_names.append(report.ReportPath)

            core['CoreAnalysisReports'] = report_names
            core['CorePhotographs'] = photo_names
            new_cores.append(core)

        # cores = [z.serialise() for z in Cores.query.all()]
        return make_response(jsonify(new_cores),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@core_bp.route('/apiv1/delete_core/<int:WellboreCoreId>',methods=['DELETE'])
@jwt_required()
@only_data_admin
def delete_core(WellboreCoreId):
    try:
        core = Cores.query.get(WellboreCoreId)
        core.delete()
        return make_response(jsonify({'message':'Welbore Core successfully deleted.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)
