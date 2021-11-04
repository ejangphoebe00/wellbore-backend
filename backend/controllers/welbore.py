from flask import Blueprint, request, make_response, jsonify
from ..models.Wellbore import Wellbore, DevelopmentAreaEnum
from ..models.Core import Cores
from ..models.CraneUser import CraneUser, UserCatgoryEnum
from flask_jwt_extended import (
    jwt_required,
    get_jwt
    )
# reference for api changes https://flask-jwt-extended.readthedocs.io/en/stable/v4_upgrade_guide/#api-changes
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
    try:
        new_wellbore = Wellbore(
                        PAUID = data['PAUID'],
                        WellboreOfficialName = data['WellboreOfficialName'],
                        DevelopmentAreaName = data['DevelopmentAreaName'],
                        WellboreLocalName = data['WellboreLocalName'],
                        WellboreAliasName = data['WellboreAliasName'],
                        WellboreSpudDate = data['WellboreSpudDate'],
                        SpudYear = data['SpudYear'],
                        WellboreType_id = data['WellboreType_id'],
                        InitialWellborePurpose_id = data['InitialWellborePurpose_id'],
                        WellborePurpose_id = data['WellborePurpose_id'],
                        PurposeChangeDate = data['PurposeChangeDate'],
                        Well_id = data['Well_id'],
                        Prospect_id = data['Prospect_id'], # should come from company
                        Discovery_id = data['Discovery_id'],
                        WellboreContent_id = data['WellboreContent_id'],
                        WellboreStatus_id = data['WellboreStatus_id'],
                        WellboreResponsibleLicence_id = data['WellboreResponsibleLicence_id'],
                        LicenseOperatorCompany_id = data['LicenseOperatorCompany_id'], # should come from company
                        DrillingContractorCompany_id = data['DrillingContractorCompany_id'], # should come from company
                        WellBoreRigName = data['WellBoreRigName'],
                        Basin_id = data['Basin_id'],
                        FormerExplAreaName = data['FormerExplAreaName'],
                        SeismicLine = data['SeismicLine'],
                        RotaryTableElavation = data['RotaryTableElavation'],
                        GroundLevelElavation = data['GroundLevelElavation'],
                        TD_MD = data['TD_MD'],
                        TD_TVD = data['TD_TVD'],
                        TD_Date = data['TD_Date'],
                        # WellboreCore_id = db.Column(db.Integer)
                        CoreContractor_id = data['CoreContractor_id'], # should come from company
                        RCI_Taken_id = data['RCI_Taken_id'],
                        MDT_Done_id = data['MDT_Done_id'],
                        FET_Done_id = data['FET_Done_id'],
                        WFTContractor = data['WFTContractor'],
                        DST_Done_id = data['DST_Done_id'],
                        ManifoldFlowTested_id = data['ManifoldFlowTested_id'],
                        DST_Contractor_id = data['DST_Contractor_id'], # should come from company
                        HasPetrophysicalLogs_id = data['HasPetrophysicalLogs_id'],
                        PetrophysicalContractor_id = data['PetrophysicalContractor_id'], # should come from company
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
                        CreatedBy_id = user.CraneUser_id,
                        DateCreated = datetime.datetime.now()
                    )
        new_wellbore.save()
        return make_response(jsonify({'message':'Wellbore added successfuly.'}),201)
    except:
        return make_response(str(traceback.format_exc()),500)


@wellbore_bp.route('/apiv1/edit_wellbore/<int:Wellbore_id>',methods=['PUT'])
@jwt_required()
@only_data_admin
def edit_wellbore(Wellbore_id):
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()
    # check for redundancies
    welbore_name = Wellbore.query.filter_by(WellboreOfficialName=data['WellboreOfficialName']).first()
    if welbore_name and welbore_name.WellboreOfficialName != None:
        if Wellbore_id != welbore_name.Wellbore_id:
            return make_response(jsonify({'message':'Wellbore name already exists.'}),409)
    try:
        wellbore = Wellbore.query.get(Wellbore_id)
        wellbore.PAUID = data['PAUID']
        wellbore.WellboreOfficialName = data['WellboreOfficialName']
        wellbore.WellboreLocalName = data['WellboreLocalName']
        wellbore.DevelopmentAreaName = data['DevelopmentAreaName']
        wellbore.WellboreAliasName = data['WellboreAliasName']
        wellbore.WellboreSpudDate = data['WellboreSpudDate']
        wellbore.SpudYear = data['SpudYear']
        wellbore.WellboreType_id = data['WellboreType_id']
        wellbore.InitialWellborePurpose_id = data['InitialWellborePurpose_id']
        wellbore.WellborePurpose_id = data['WellborePurpose_id']
        wellbore.PurposeChangeDate = data['PurposeChangeDate']
        wellbore.Well_id = data['Well_id']
        wellbore.Prospect_id = data['Prospect_id']
        wellbore.Discovery_id = data['Discovery_id']
        wellbore.WellboreContent_id = data['WellboreContent_id']
        wellbore.WellboreStatus_id = data['WellboreStatus_id']
        wellbore.WellboreResponsibleLicence_id = data['WellboreResponsibleLicence_id']
        wellbore.LicenseOperatorCompany_id = data['LicenseOperatorCompany_id']
        wellbore.DrillingContractorCompany_id = data['DrillingContractorCompany_id']
        wellbore.WellBoreRigName = data['WellBoreRigName']
        wellbore.Basin_id = data['Basin_id']
        wellbore.FormerExplAreaName = data['FormerExplAreaName']
        wellbore.SeismicLine = data['SeismicLine']
        wellbore.RotaryTableElavation = data['RotaryTableElavation']
        wellbore.GroundLevelElavation = data['GroundLevelElavation']
        wellbore.TD_MD = data['TD_MD']
        wellbore.TD_TVD = data['TD_TVD']
        wellbore.TD_Date = data['TD_Date']
        # WellboreCore_id = db.Column(db.Integer)
        wellbore.CoreContractor_id = data['CoreContractor_id']
        wellbore.RCI_Taken_id = data['RCI_Taken_id']
        wellbore.MDT_Done_id = data['MDT_Done_id']
        wellbore.FET_Done_id = data['FET_Done_id']
        wellbore.WFTContractor = data['WFTContractor']
        wellbore.DST_Done_id = data['DST_Done_id']
        wellbore.ManifoldFlowTested_id = data['ManifoldFlowTested_id']
        wellbore.DST_Contractor_id = data['DST_Contractor_id']
        wellbore.HasPetrophysicalLogs_id = data['HasPetrophysicalLogs_id']
        wellbore.PetrophysicalContractor_id = data['PetrophysicalContractor_id']
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
        wellbore.ModifiedOn = datetime.datetime.today()
        wellbore.ModifiedBy = user.CraneUser_id
        wellbore.update()
        return make_response(jsonify({'message':'Welbore updated successfuly.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get single wellbore object
@wellbore_bp.route('/apiv1/get_wellbore/<int:Wellbore_id>',methods=['GET'])
@jwt_required()
def get_wellbore(Wellbore_id):
    try:
        wellbore = Wellbore.query.get(Wellbore_id)
        return make_response(jsonify(wellbore.serialise()),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@wellbore_bp.route('/apiv1/get_wellbore',methods=['GET'])
@jwt_required()
def get_all_wellbore():
    try:
        wellbore = [z.serialise() for z in Wellbore.query.all()]
        return make_response(jsonify(wellbore),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@wellbore_bp.route('/apiv1/delete_wellbore/<int:Wellbore_id>',methods=['DELETE'])
@jwt_required()
@only_data_admin
def delete_wellbore(Wellbore_id):
    try:
        wellbore = Wellbore.query.get(Wellbore_id)
        wellbore.delete()
        return make_response(jsonify({'message':'Welbore successfully deleted.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get wellbore cores of a specific welbore
@wellbore_bp.route('/apiv1/get_wellbore_cores/<int:Wellbore_id>',methods=['GET'])
@jwt_required()
def get_all_wellbore_cores(Wellbore_id):
    try:
        wellbore_cores = [z.serialise() for z in Cores.query.filter(Cores.Wellbore_id == Wellbore_id)]
        return make_response(jsonify(wellbore_cores),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get wellbores from TDA
@wellbore_bp.route('/apiv1/get_tda_welbores',methods=['GET'])
@jwt_required()
def get_TDA_welbores():
    try:
        wellbores = [z.serialise() for z in Wellbore.query.filter(Wellbore.DevelopmentAreaName == DevelopmentAreaEnum.TDA)]
        return make_response(jsonify(wellbores),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get wellbores from KFDA
@wellbore_bp.route('/apiv1/get_kfda_welbores',methods=['GET'])
@jwt_required()
def get_KFDA_welbores():
    try:
        wellbores = [z.serialise() for z in Wellbore.query.filter(Wellbore.DevelopmentAreaName == DevelopmentAreaEnum.KFDA)]
        return make_response(jsonify(wellbores),200)
    except:
        return make_response(str(traceback.format_exc()),500)        
