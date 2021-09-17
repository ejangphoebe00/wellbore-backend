from flask import Blueprint, request, make_response, jsonify
from ..models.CoreCatalog import CoreCatalog
from ..models.CraneUser import CraneUser, UserCatgoryEnum
from flask_jwt_extended import (
    jwt_required,
    get_jwt
    )
# reference for api changes https://flask-jwt-extended.readthedocs.io/en/stable/v4_upgrade_guide/#api-changes
import datetime
import traceback


core_catalog_bp = Blueprint('core_catalog_bp', __name__)

@core_catalog_bp.route('/apiv1/add_core_catalog',methods=['POST'])
@jwt_required()
def add_core_catalog():
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()

    # check for redundancies
    catalog_name = CoreCatalog.query.filter_by(CoreCatalogName=data['CoreCatalogName']).first()
    if catalog_name:
        return make_response(jsonify({'message':'CoreCatalogName already exists.'}),409)
    try:
        new_core_catalog = CoreCatalog(
                        WellboreCore_id = data['WellboreCore_id'], # comes from welbore core
                        CoreType = data['CoreType'], # comes from core type
                        StoreIdentifier = data['StoreIdentifier'],
                        CatalogCoreFromDepth = data['CatalogCoreFromDepth'],
                        CatalogCoreToDepth = data['CatalogCoreToDepth'],
                        CoreCatalogSecurityFlag_id = data['CoreCatalogSecurityFlag_id'], # comes from catalog security flag
                        WasAnalysed_id = data['WasAnalysed_id'],
                        TopStratLitho_id = data['TopStratLitho_id'], # comes from strat litho
                        BottomStratLitho_id = data['BottomStratLitho_id'], # comes from strat litho
                        CatalogueCorePictureName = data['CatalogueCorePictureName'],
                        CataloguePictureSoftcopyPath = data['CataloguePictureSoftcopyPath'],
                        CataloguePictureHyperlink = data['CataloguePictureHyperlink'],
                        CatPictureUploadDate = data['CatPictureUploadDate'],
                        CatalogueReportSoftcopyPath = data['CatalogueReportSoftcopyPath'],
                        CatalogueReportHyperlink = data['CatalogueReportHyperlink'],
                        CatReportUploadDate = data['CatReportUploadDate'],
                        CatalogReportFormat_id = data['CatalogReportFormat_id'], # comes from file format
                        CatalogReportFileSize = data['CatalogReportFileSize'],
                        CatalogReportSecurityGrade_id = data['CatalogReportSecurityGrade_id'], # comes from file security grade
                        CoreCatalogName = data['CoreCatalogName'],
                        Comments = data['Comments'],
                        CreatedBy_id = user.CraneUser_id,
                        DateCreated = datetime.datetime.now(),
                    )
        new_core_catalog.save()
        return make_response(jsonify({'message':'Core Catalog added successfuly.'}),201)
    except:
        return make_response(str(traceback.format_exc()),500)


@core_catalog_bp.route('/apiv1/edit_core_catalog/<int:CoreCatalog_id>',methods=['PUT'])
@jwt_required()
def edit_core_catalog(CoreCatalog_id):
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()

    # check for redundancies
    catalog_name = CoreCatalog.query.filter_by(CoreCatalogName=data['CoreCatalogName']).first()
    if catalog_name:
        if CoreCatalog_id != catalog_name.CoreCatalog_id:
            return make_response(jsonify({'message':'CoreCatalogName already exists.'}),409)
    try:
        core_catalog = CoreCatalog.query.get(CoreCatalog_id)
        core_catalog.WellboreCore_id = data['WellboreCore_id'] # comes from welbore core
        core_catalog.CoreType = data['CoreType'] # comes from core type
        core_catalog.StoreIdentifier = data['StoreIdentifier']
        core_catalog.CatalogCoreFromDepth = data['CatalogCoreFromDepth']
        core_catalog.CatalogCoreToDepth = data['CatalogCoreToDepth']
        core_catalog.CoreCatalogSecurityFlag_id = data['CoreCatalogSecurityFlag_id'] # comes from catalog security flag
        core_catalog.WasAnalysed_id = data['WasAnalysed_id']
        core_catalog.TopStratLitho_id = data['TopStratLitho_id'] # comes from strat litho
        core_catalog.BottomStratLitho_id = data['BottomStratLitho_id'] # comes from strat litho
        core_catalog.CatalogueCorePictureName = data['CatalogueCorePictureName']
        core_catalog.CataloguePictureSoftcopyPath = data['CataloguePictureSoftcopyPath']
        core_catalog.CataloguePictureHyperlink = data['CataloguePictureHyperlink']
        core_catalog.CatPictureUploadDate = data['CatPictureUploadDate']
        core_catalog.CatalogueReportSoftcopyPath = data['CatalogueReportSoftcopyPath']
        core_catalog.CatalogueReportHyperlink = data['CatalogueReportHyperlink']
        core_catalog.CatReportUploadDate = data['CatReportUploadDate']
        core_catalog.CatalogReportFormat_id = data['CatalogReportFormat_id'] # comes from file format
        core_catalog.CatalogReportFileSize = data['CatalogReportFileSize']
        core_catalog.CatalogReportSecurityGrade_id = data['CatalogReportSecurityGrade_id'] # comes from file security grade
        core_catalog.CoreCatalogName = data['CoreCatalogName']
        core_catalog.ModifiedOn = datetime.datetime.now()
        core_catalog.ModifiedBy = user.CraneUser_id
        core_catalog.update()
        return make_response(jsonify({'message':'Core Catalog updated successfuly.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get single core_catalog object
@core_catalog_bp.route('/apiv1/get_core_catalog/<int:CoreCatalog_id>',methods=['GET'])
@jwt_required()
def get_core_catalog(CoreCatalog_id):
    try:
        core_catalog = CoreCatalog.query.get(CoreCatalog_id)
        return make_response(jsonify(core_catalog.serialise()),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@core_catalog_bp.route('/apiv1/get_core_catalogs',methods=['GET'])
@jwt_required()
def get_all_core_catalogs():
    try:
        core_catalogs = [z.serialise() for z in CoreCatalog.query.all()]
        return make_response(jsonify(core_catalogs),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@core_catalog_bp.route('/apiv1/delete_core_catalog/<int:CoreCatalog_id>',methods=['DELETE'])
@jwt_required()
def delete_core_catalog(CoreCatalog_id):
    try:
        core_catalog = CoreCatalog.query.get(CoreCatalog_id)
        core_catalog.delete()
        return make_response(jsonify({'message':'Core Catalog successfully deleted.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)
