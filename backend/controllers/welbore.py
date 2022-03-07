from flask import Blueprint, request, make_response, jsonify
from ..models.Wellbore import Wellbore, DevelopmentAreaEnum
from ..models.Core import Cores
from ..models.CraneUser import CraneUser, DeleteStatusEnum, UserCatgoryEnum
from flask_jwt_extended import (
    jwt_required,
    get_jwt
    )
import datetime
import traceback
from ..middleware.permissions import only_data_admin


wellbore_bp = Blueprint('wellbore_bp', __name__)

@wellbore_bp.route('/apiv1/add_wellbore',methods=['POST'])
@jwt_required()
@only_data_admin
def add_wellbore():
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()

    # check for redundancies
    welbore_name = Wellbore.query.filter_by(WellboreOfficialName=data['WellboreOfficialName']).first()
    if welbore_name and welbore_name.WellboreOfficialName != None:
        return make_response(jsonify({'message':'Wellbore name already exists.'}),409)

    welbore_PAUID = Wellbore.query.filter_by(PAUID=data['PAUID']).first()
    if welbore_PAUID and welbore_PAUID.PAUID != None:
        return make_response(jsonify({'message':'PAUID already exists.'}),409)
    try:
        new_wellbore = Wellbore(
                        PAUID = data['PAUID'],
                        WellboreOfficialName = data['WellboreOfficialName'],
                        DevelopmentAreaName = data['DevelopmentAreaName'],
                        OtherDevelopmentArea = data['OtherDevelopmentArea'],
                        WellboreLocalName = data['WellboreLocalName'],
                        WellboreAliasName = data['WellboreAliasName'],
                        WellboreSpudDate = data['WellboreSpudDate'],
                        WellboreTypeId = data['WellboreTypeId'],
                        WellborePurposeId = data['WellborePurposeId'],
                        PurposeChangeDate = data['PurposeChangeDate'],
                        ProspectId = data['ProspectId'], # should come from company
                        Discovery = data['Discovery'],
                        WellboreContentId = data['WellboreContentId'],
                        WellboreStatus = data['WellboreStatus'],
                        LicenseOperatorCompanyId = data['LicenseOperatorCompanyId'], # should come from company
                        DrillingContractorCompanyId = data['DrillingContractorCompanyId'], # should come from company
                        WellBoreRigName = data['WellBoreRigName'],
                        Basin = data['Basin'],
                        InitialWellborePurpose = data['InitialWellborePurpose'],
                        WellboreType = data['WellboreType'],
                        FormerExplAreaName = data['FormerExplAreaName'],
                        SeismicLine = data['SeismicLine'],
                        RotaryTableElavation = data['RotaryTableElavation'],
                        GroundLevelElavation = data['GroundLevelElavation'],
                        TDMD = data['TDMD'],
                        TDTVD = data['TDTVD'],
                        TDDate = data['TDDate'],
                        CoreContractorId = data['CoreContractorId'], # should come from company
                        MDTDoneId = data['MDTDoneId'],
                        FETDoneId = data['FETDoneId'],
                        WFTContractor = data['WFTContractor'],
                        DSTDoneId = data['DSTDoneId'],
                        ManifoldFlowTestedId = data['ManifoldFlowTestedId'],
                        DSTContractorId = data['DSTContractorId'], # should come from company
                        HasPetrophysicalLogsId = data['HasPetrophysicalLogsId'],
                        PetrophysicalContractorId = data['PetrophysicalContractorId'], # should come from company
                        TopBasementMD = data['TopBasementMD'],
                        TopBasementTVD = data['TopBasementTVD'],
                        WellboreTestStatus = data['WellboreTestStatus'],
                        PlannedWellboreCost = data['PlannedWellboreCost'],
                        ActualWellboreCost = data['ActualWellboreCost'],
                        WellboreTestCost = data['WellboreTestCost'],
                        CompletionDate = data['CompletionDate'],
                        What3WordWellboreLocation = data['What3WordWellboreLocation'],
                        Comments = data['Comments'],
                        LocationPictureName = data['LocationPictureName'],
                        LocationPicture = data['LocationPicture'],
                        LocationPictureSoftcopyPath = data['LocationPictureSoftcopyPath'],
                        LocationPictureHyperlink = data['LocationPictureHyperlink'],
                        WellboreMapSoftcopyPath = data['WellboreMapSoftcopyPath'],
                        WellboreMapHyperlink = data['WellboreMapHyperlink'],
                        MapPortalWellboreMapLink = data['MapPortalWellboreMapLink'],
                        WellboreFactsiteUrl = data['WellboreFactsiteUrl'],
                        CreatedById = user.CraneUserId,
                        DateCreated = datetime.datetime.now()
                    )
        new_wellbore.save()
        return make_response(jsonify({'message':'Wellbore added successfuly.'}),201)
    except:
        return make_response(str(traceback.format_exc()),500)


@wellbore_bp.route('/apiv1/edit_wellbore/<int:WellboreId>',methods=['PUT'])
@jwt_required()
@only_data_admin
def edit_wellbore(WellboreId):
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()
    # check for redundancies
    welbore_name = Wellbore.query.filter_by(WellboreOfficialName=data['WellboreOfficialName']).first()
    if welbore_name and welbore_name.WellboreOfficialName != None:
        if WellboreId != welbore_name.WellboreId:
            return make_response(jsonify({'message':'Wellbore name already exists.'}),409)

    welbore_PAUID = Wellbore.query.filter_by(PAUID=data['PAUID']).first()
    if welbore_PAUID and welbore_PAUID.PAUID != None:
        if WellboreId != welbore_PAUID.WellboreId:
            return make_response(jsonify({'message':'PAUID already exists.'}),409)

    try:
        wellbore = Wellbore.query.get(WellboreId)
        wellbore.PAUID = data['PAUID']
        wellbore.WellboreOfficialName = data['WellboreOfficialName']
        wellbore.WellboreLocalName = data['WellboreLocalName']
        wellbore.DevelopmentAreaName = data['DevelopmentAreaName']
        wellbore.OtherDevelopmentArea = data['OtherDevelopmentArea']
        wellbore.WellboreAliasName = data['WellboreAliasName']
        wellbore.WellboreSpudDate = data['WellboreSpudDate']
        wellbore.WellboreTypeId = data['WellboreTypeId']
        wellbore.WellborePurposeId = data['WellborePurposeId']
        wellbore.PurposeChangeDate = data['PurposeChangeDate']
        wellbore.ProspectId = data['ProspectId']
        wellbore.Discovery = data['Discovery']
        wellbore.WellboreContentId = data['WellboreContentId']
        wellbore.LicenseOperatorCompanyId = data['LicenseOperatorCompanyId']
        wellbore.DrillingContractorCompanyId = data['DrillingContractorCompanyId']
        wellbore.WellBoreRigName = data['WellBoreRigName']
        wellbore.Basin = data['Basin']
        wellbore.InitialWellborePurpose = data['InitialWellborePurpose']
        wellbore.WellboreType = data['WellboreType']
        wellbore.FormerExplAreaName = data['FormerExplAreaName']
        wellbore.SeismicLine = data['SeismicLine']
        wellbore.RotaryTableElavation = data['RotaryTableElavation']
        wellbore.GroundLevelElavation = data['GroundLevelElavation']
        wellbore.TDMD = data['TDMD']
        wellbore.TDTVD = data['TDTVD']
        wellbore.TDDate = data['TDDate']
        wellbore.CoreContractorId = data['CoreContractorId']
        wellbore.MDTDoneId = data['MDTDoneId']
        wellbore.FETDoneId = data['FETDoneId']
        wellbore.WFTContractor = data['WFTContractor']
        wellbore.DSTDoneId = data['DSTDoneId']
        wellbore.ManifoldFlowTestedId = data['ManifoldFlowTestedId']
        wellbore.DSTContractorId = data['DSTContractorId']
        wellbore.HasPetrophysicalLogsId = data['HasPetrophysicalLogsId']
        wellbore.PetrophysicalContractorId = data['PetrophysicalContractorId']
        wellbore.TopBasementMD = data['TopBasementMD']
        wellbore.TopBasementTVD = data['TopBasementTVD']
        wellbore.WellboreTestStatus = data['WellboreTestStatus']
        wellbore.PlannedWellboreCost = data['PlannedWellboreCost']
        wellbore.ActualWellboreCost = data['ActualWellboreCost']
        wellbore.WellboreTestCost = data['WellboreTestCost']
        wellbore.CompletionDate = data['CompletionDate']
        wellbore.What3WordWellboreLocation = data['What3WordWellboreLocation']
        wellbore.Comments = data['Comments']
        wellbore.LocationPictureName = data['LocationPictureName']
        wellbore.LocationPicture = data['LocationPicture']
        wellbore.LocationPictureSoftcopyPath = data['LocationPictureSoftcopyPath']
        wellbore.LocationPictureHyperlink = data['LocationPictureHyperlink']
        wellbore.WellboreMapSoftcopyPath = data['WellboreMapSoftcopyPath']
        wellbore.WellboreMapHyperlink = data['WellboreMapHyperlink']
        wellbore.MapPortalWellboreMapLink = data['MapPortalWellboreMapLink']
        wellbore.WellboreFactsiteUrl = data['WellboreFactsiteUrl']
        wellbore.WellboreStatus = data['WellboreStatus']
        wellbore.ModifiedOn = datetime.datetime.today()
        wellbore.ModifiedBy = user.CraneUserId
        wellbore.update()
        return make_response(jsonify({'message':'Welbore updated successfuly.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get single wellbore object
@wellbore_bp.route('/apiv1/get_wellbore/<int:WellboreId>',methods=['GET'])
@jwt_required()
def get_wellbore(WellboreId):
    try:
        wellbore = Wellbore.query.get(WellboreId)
        return make_response(jsonify(wellbore.serialise()),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@wellbore_bp.route('/apiv1/get_wellbore',methods=['GET'])
@jwt_required()
def get_all_wellbore():
    try:
        wellbore = [z.serialise() for z in Wellbore.query.\
            filter((Wellbore.DeleteStatus==DeleteStatusEnum.Available) | (Wellbore.DeleteStatus==None))]
        return make_response(jsonify(wellbore),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@wellbore_bp.route('/apiv1/delete_wellbore/<int:WellboreId>',methods=['DELETE'])
@jwt_required()
@only_data_admin
def delete_wellbore(WellboreId):
    try:
        wellbore = Wellbore.query.get(WellboreId)
        wellbore.DeleteStatus = DeleteStatusEnum.Deleted
        wellbore.updated()
        return make_response(jsonify({'message':'Welbore successfully deleted.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get wellbores from TDA
@wellbore_bp.route('/apiv1/get_tda_welbores',methods=['GET'])
@jwt_required()
def get_TDA_welbores():
    try:
        wellbores = [z.serialise() for z in Wellbore.query.filter(Wellbore.DevelopmentAreaName == DevelopmentAreaEnum.TDA,\
            (Wellbore.DeleteStatus==DeleteStatusEnum.Available) | (Wellbore.DeleteStatus==None))]
        return make_response(jsonify(wellbores),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get wellbores from KFDA
@wellbore_bp.route('/apiv1/get_kfda_welbores',methods=['GET'])
@jwt_required()
def get_KFDA_welbores():
    try:
        wellbores = [z.serialise() for z in Wellbore.query.filter(Wellbore.DevelopmentAreaName == DevelopmentAreaEnum.KFDA,\
            (Wellbore.DeleteStatus==DeleteStatusEnum.Available) | (Wellbore.DeleteStatus==None))]
        return make_response(jsonify(wellbores),200)
    except:
        return make_response(str(traceback.format_exc()),500)        
