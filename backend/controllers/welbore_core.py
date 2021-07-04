from flask import Blueprint, request, make_response, jsonify
from ..models.WellboreCore import WellboreCore
from .. models.Wellbore import Wellbore
from ..models.CraneUser import CraneUser, UserCatgoryEnum
from flask_jwt_extended import (
    jwt_required,
    get_jwt
    )
# reference for api changes https://flask-jwt-extended.readthedocs.io/en/stable/v4_upgrade_guide/#api-changes
import datetime


welbore_core_bp = Blueprint('welbore_core_bp', __name__)

@welbore_core_bp.route('/apiv1/add_welbore_core',methods=['POST'])
@jwt_required()
def add_welbore_core():
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()
    try:
        new_welbore_core = WellboreCore(
                        Wellbore_id = data['Wellbore_id'],#comes from welbore
                        CoreNumber = data['CoreNumber'],
                        CoringDate = data['CoringDate'],
                        WBCoringContractor_id = data['WBCoringContractor_id'],
                        CoreTopMDRT = data['CoreTopMDRT'],
                        CoreBtmMDRT = data['CoreBtmMDRT'],
                        CoreTopTVD = data['CoreTopTVD'],
                        CoreBtmTVD = data['CoreBtmTVD'],
                        CutLength = data['CutLength'],
                        CutLengthTVD = data['CutLengthTVD'],
                        RecoveredLength = data['RecoveredLength'],
                        CoreRecovery = data['CoreRecovery'],
                        CoreTopStratLitho_id = data['CoreTopStratLitho_id'],
                        CoreBottomStratLitho_id = data['CoreBottomStratLitho_id'],
                        CorePictureSoftcopyPath = data['CorePictureSoftcopyPath'],
                        CorePictureHyperlink = data['CorePictureHyperlink'],
                        PictureUploadDate = data['PictureUploadDate'],
                        CoreReportSoftcopyPath = data['CoreReportSoftcopyPath'],
                        CoreReportHyperlink = data['CoreReportHyperlink'],
                        ReportUploadDate = data['ReportUploadDate'],
                        ReportFormat_id = data['ReportFormat_id'],#should come from file format
                        ReportFileSize = data['ReportFileSize'],
                        CoreReportSecurityGrade_id = data['CoreReportSecurityGrade_id'],#comes from file security grade
                        ReportOpenDueDate = data['ReportOpenDueDate'],
                        ReportDocumentTitle = data['ReportDocumentTitle'],
                        ReportReceivedDate = data['ReportReceivedDate'],
                        ReportDocumentDate = data['ReportDocumentDate'],
                        ReportDocumentName = data['ReportDocumentName'],
                        WellboreCoreName = data['WellboreCoreName'],
                        Comments = data['Comments'],
                        CreatedBy_id = user.CraneUser_id,
                        DateCreated = datetime.datetime.now()
                    )
        new_welbore_core.save()
        return make_response(jsonify({'message':'Welbore Core added successfuly.'}),201)
    except:
        return make_response(jsonify({'message':'Something went wrong'}),500)


@welbore_core_bp.route('/apiv1/edit_welbore_core/<int:WellboreCore_id>',methods=['PUT'])
@jwt_required()
def edit_welbore_core(WellboreCore_id):
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()
    try:
        welbore_core = WellboreCore.query.get(WellboreCore_id)
        welbore_core.Wellbore_id = data['Wellbore_id']
        welbore_core.CoreNumber = data['CoreNumber']
        welbore_core.CoringDate = data['CoringDate']
        welbore_core.WBCoringContractor_id = data['WBCoringContractor_id']
        welbore_core.CoreTopMDRT = data['CoreTopMDRT']
        welbore_core.CoreBtmMDRT = data['CoreBtmMDRT']
        welbore_core.CoreTopTVD = data['CoreTopTVD']
        welbore_core.CoreBtmTVD = data['CoreBtmTVD']
        welbore_core.CutLength = data['CutLength']
        welbore_core.CutLengthTVD = data['CutLengthTVD']
        welbore_core.RecoveredLength = data['RecoveredLength']
        welbore_core.CoreRecovery = data['CoreRecovery']
        welbore_core.CoreTopStratLitho_id = data['CoreTopStratLitho_id']
        welbore_core.CoreBottomStratLitho_id = data['CoreBottomStratLitho_id']
        welbore_core.CorePictureSoftcopyPath = data['CorePictureSoftcopyPath']
        welbore_core.CorePictureHyperlink = data['CorePictureHyperlink']
        welbore_core.PictureUploadDate = data['PictureUploadDate']
        welbore_core.CoreReportSoftcopyPath = data['CoreReportSoftcopyPath']
        welbore_core.CoreReportHyperlink = data['CoreReportHyperlink']
        welbore_core.ReportUploadDate = data['ReportUploadDate']
        welbore_core.ReportFormat_id = data['ReportFormat_id']
        welbore_core.ReportFileSize = data['ReportFileSize']
        welbore_core.CoreReportSecurityGrade_id = data['CoreReportSecurityGrade_id']
        welbore_core.ReportOpenDueDate = data['ReportOpenDueDate']
        welbore_core.ReportDocumentTitle = data['ReportDocumentTitle']
        welbore_core.ReportReceivedDate = data['ReportReceivedDate']
        welbore_core.ReportDocumentDate = data['ReportDocumentDate']
        welbore_core.ReportDocumentName = data['ReportDocumentName']
        welbore_core.WellboreCoreName = data['WellboreCoreName']
        welbore_core.Comments = data['Comments']
        welbore_core.ModifiedOn = datetime.datetime.today()
        welbore_core.ModifiedBy = user.CraneUser_id
        welbore_core.update()
        return make_response(jsonify({'message':'Welbore Core updated successfuly.'}),200)
    except:
        return make_response(jsonify({'message':'Something went wrong'}),500)


# get single welbore_core object
@welbore_core_bp.route('/apiv1/get_welbore_core/<int:WellboreCore_id>',methods=['GET'])
@jwt_required()
def get_welbore_core(WellboreCore_id):
    try:
        welbore_core = WellboreCore.query.get(WellboreCore_id)
        return make_response(jsonify(welbore_core.serialise()),200)
    except:
       return make_response(jsonify({'message':'Something went wrong'}),500)


@welbore_core_bp.route('/apiv1/get_welbore_cores',methods=['GET'])
@jwt_required()
def get_all_welbore_cores():
    try:
        welbore_cores = [z.serialise() for z in WellboreCore.query.all()]
        return make_response(jsonify(welbore_cores),200)
    except:
       return make_response(jsonify({'message':'Something went wrong'}),500)


@welbore_core_bp.route('/apiv1/delete_welbore_core/<int:WellboreCore_id>',methods=['DELETE'])
@jwt_required()
def delete_welbore_core(WellboreCore_id):
    try:
        welbore_core = WellboreCore.query.get(WellboreCore_id)
        welbore_core.delete()
        return make_response(jsonify({'message':'Welbore Core successfully deleted.'}),200)
    except:
       return make_response(jsonify({'message':'Something went wrong'}),500) 
