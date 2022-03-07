from flask import Blueprint, request, make_response, jsonify
from ..models.CoreCatalog import CoreCatalog
from ..models.CraneUser import CraneUser, DeleteStatusEnum, UserCatgoryEnum
from flask_jwt_extended import (
    jwt_required,
    get_jwt
    )
import datetime
import traceback
from ..middleware.permissions import only_data_admin


core_catalog_bp = Blueprint('core_catalog_bp', __name__)

@core_catalog_bp.route('/apiv1/add_core_catalog',methods=['POST'])
@jwt_required()
@only_data_admin
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
                        WellboreCoreId = data['WellboreCoreId'], # comes from welbore core
                        StoreIdentifier = data['StoreIdentifier'],
                        CatalogCoreFromDepth = data['CatalogCoreFromDepth'],
                        CatalogCoreToDepth = data['CatalogCoreToDepth'],
                        WasAnalysedId = data['WasAnalysedId'],
                        TopStratLithoId = data['TopStratLithoId'], # comes from strat litho
                        BottomStratLithoId = data['BottomStratLithoId'], # comes from strat litho
                        CatalogueCorePictureName = data['CatalogueCorePictureName'],
                        CataloguePictureSoftcopyPath = data['CataloguePictureSoftcopyPath'],
                        CataloguePictureHyperlink = data['CataloguePictureHyperlink'],
                        CatPictureUploadDate = data['CatPictureUploadDate'],
                        CatalogueReportSoftcopyPath = data['CatalogueReportSoftcopyPath'],
                        CatalogueReportHyperlink = data['CatalogueReportHyperlink'],
                        CatReportUploadDate = data['CatReportUploadDate'],
                        CatalogReportFileSize = data['CatalogReportFileSize'],
                        CoreCatalogName = data['CoreCatalogName'],
                        Comments = data['Comments'],
                        CreatedById = user.CraneUserId,
                        DateCreated = datetime.datetime.now(),
                    )
        new_core_catalog.save()
        return make_response(jsonify({'message':'Core Catalog added successfuly.'}),201)
    except:
        return make_response(str(traceback.format_exc()),500)


@core_catalog_bp.route('/apiv1/edit_core_catalog/<int:CoreCatalogId>',methods=['PUT'])
@jwt_required()
@only_data_admin
def edit_core_catalog(CoreCatalogId):
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()

    # check for redundancies
    catalog_name = CoreCatalog.query.filter_by(CoreCatalogName=data['CoreCatalogName']).first()
    if catalog_name:
        if CoreCatalogId != catalog_name.CoreCatalogId:
            return make_response(jsonify({'message':'CoreCatalogName already exists.'}),409)
    try:
        core_catalog = CoreCatalog.query.get(CoreCatalogId)
        core_catalog.WellboreCoreId = data['WellboreCoreId'] # comes from welbore core
        core_catalog.StoreIdentifier = data['StoreIdentifier']
        core_catalog.CatalogCoreFromDepth = data['CatalogCoreFromDepth']
        core_catalog.CatalogCoreToDepth = data['CatalogCoreToDepth']
        core_catalog.WasAnalysedId = data['WasAnalysedId']
        core_catalog.TopStratLithoId = data['TopStratLithoId'] # comes from strat litho
        core_catalog.BottomStratLithoId = data['BottomStratLithoId'] # comes from strat litho
        core_catalog.CatalogueCorePictureName = data['CatalogueCorePictureName']
        core_catalog.CataloguePictureSoftcopyPath = data['CataloguePictureSoftcopyPath']
        core_catalog.CataloguePictureHyperlink = data['CataloguePictureHyperlink']
        core_catalog.CatPictureUploadDate = data['CatPictureUploadDate']
        core_catalog.CatalogueReportSoftcopyPath = data['CatalogueReportSoftcopyPath']
        core_catalog.CatalogueReportHyperlink = data['CatalogueReportHyperlink']
        core_catalog.CatReportUploadDate = data['CatReportUploadDate']
        core_catalog.CatalogReportFileSize = data['CatalogReportFileSize']
        core_catalog.CoreCatalogName = data['CoreCatalogName']
        core_catalog.ModifiedOn = datetime.datetime.now()
        core_catalog.ModifiedBy = user.CraneUserId
        core_catalog.update()
        return make_response(jsonify({'message':'Core Catalog updated successfuly.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get single core_catalog object
@core_catalog_bp.route('/apiv1/get_core_catalog/<int:CoreCatalogId>',methods=['GET'])
@jwt_required()
def get_core_catalog(CoreCatalogId):
    try:
        core_catalog = CoreCatalog.query.get(CoreCatalogId)
        return make_response(jsonify(core_catalog.serialise()),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@core_catalog_bp.route('/apiv1/get_core_catalogs',methods=['GET'])
@jwt_required()
def get_all_core_catalogs():
    try:
        core_catalogs = [z.serialise() for z in CoreCatalog.query.\
        filter((CoreCatalog.DeleteStatus==DeleteStatusEnum.Available) | (CoreCatalog.DeleteStatus==None))]
        return make_response(jsonify(core_catalogs),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@core_catalog_bp.route('/apiv1/delete_core_catalog/<int:CoreCatalogId>',methods=['DELETE'])
@jwt_required()
@only_data_admin
def delete_core_catalog(CoreCatalogId):
    try:
        core_catalog = CoreCatalog.query.get(CoreCatalogId)
        core_catalog.DeleteStatus = DeleteStatusEnum.Deleted
        core_catalog.updated()
        return make_response(jsonify({'message':'Core Catalog successfully deleted.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)
