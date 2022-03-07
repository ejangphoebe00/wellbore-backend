from flask import Blueprint, request, make_response, jsonify
from ..models.StratLithoUnit import StratLithoUnit
from ..models.CraneUser import CraneUser, DeleteStatusEnum
from flask_jwt_extended import (
    jwt_required,
    get_jwt
    )
import datetime
import traceback
from ..middleware.permissions import only_data_admin


strat_litho_unit_bp = Blueprint('strat_litho_unit_bp', __name__)

@strat_litho_unit_bp.route('/apiv1/add_strat_litho_unit',methods=['POST'])
@jwt_required()
@only_data_admin
def add_strat_litho_unit():
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()

    # check for redundancies
    litho_name = StratLithoUnit.query.filter_by(StratLithoName=data['StratLithoName']).first()
    if litho_name:
        return make_response(jsonify({'message':'StratLithoName already exists.'}),409)
    try:
        new_strat_litho_unit = StratLithoUnit(
                        PAUID = data['PAUID'],
                        StratLithoName = data['StratLithoName'],
                        LithoStratAlias = data['LithoStratAlias'],
                        IsReservoirUnitId = data['IsReservoirUnitId'],
                        LithoStratAge = data['LithoStratAge'],
                        LithoStratDescriptionSoftcopyPath = data['LithoStratDescriptionSoftcopyPath'],
                        LithoStratDescriptionHyperlink = data['LithoStratDescriptionHyperlink'],
                        LithoStratMapSoftCopyPath = data['LithoStratMapSoftCopyPath'],
                        LithoStratMapHyperlink = data['LithoStratMapHyperlink'],
                        MapPortalLithoStratMapLink = data['MapPortalLithoStratMapLink'],
                        LithoStratFactsiteUrl = data['LithoStratFactsiteUrl'],
                        Comments = data['Comments'],
                        CreatedById = user.CraneUserId,
                        DateCreated = datetime.datetime.now(),
                    )
        new_strat_litho_unit.save()
        return make_response(jsonify({'message':'Strat Litho Unit added successfuly.'}),201)
    except:
        return make_response(str(traceback.format_exc()),500)


@strat_litho_unit_bp.route('/apiv1/edit_strat_litho_unit/<int:StratLithoId>',methods=['PUT'])
@jwt_required()
@only_data_admin
def edit_strat_litho_unit(StratLithoId):
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()

    # check for redundancies
    litho_name = StratLithoUnit.query.filter_by(StratLithoName=data['StratLithoName']).first()
    if litho_name:
        if StratLithoId != litho_name.StratLithoId:
            return make_response(jsonify({'message':'StratLithoName already exists.'}),409)
    try:
        strat_litho_unit = StratLithoUnit.query.get(StratLithoId)
        strat_litho_unit.PAUID = data['PAUID']
        strat_litho_unit.StratLithoName = data['StratLithoName']
        strat_litho_unit.LithoStratAlias = data['LithoStratAlias']
        strat_litho_unit.IsReservoirUnitId = data['IsReservoirUnitId']
        strat_litho_unit.LithoStratAge = data['LithoStratAge']
        strat_litho_unit.LithoStratDescriptionSoftcopyPath = data['LithoStratDescriptionSoftcopyPath']
        strat_litho_unit.LithoStratDescriptionHyperlink = data['LithoStratDescriptionHyperlink']
        strat_litho_unit.LithoStratMapSoftCopyPath = data['LithoStratMapSoftCopyPath']
        strat_litho_unit.LithoStratMapHyperlink = data['LithoStratMapHyperlink']
        strat_litho_unit.MapPortalLithoStratMapLink = data['MapPortalLithoStratMapLink']
        strat_litho_unit.LithoStratFactsiteUrl = data['LithoStratFactsiteUrl']
        strat_litho_unit.Comments = data['Comments']
        strat_litho_unit.ModifiedOn = datetime.datetime.now()
        strat_litho_unit.ModifiedBy = user.CraneUserId
        strat_litho_unit.update()
        return make_response(jsonify({'message':'Strat Litho Unit updated successfuly.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get single strat_litho_unit object
@strat_litho_unit_bp.route('/apiv1/get_strat_litho_unit/<int:StratLithoId>',methods=['GET'])
@jwt_required()
def get_strat_litho_unit(StratLithoId):
    try:
        strat_litho_unit = StratLithoUnit.query.get(StratLithoId)
        return make_response(jsonify(strat_litho_unit.serialise()),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@strat_litho_unit_bp.route('/apiv1/get_strat_litho_units',methods=['GET'])
@jwt_required()
def get_all_strat_litho_units():
    try:
        strat_litho_units = [z.serialise() for z in StratLithoUnit.query.\
            filter((StratLithoUnit.DeleteStatus==DeleteStatusEnum.Available) | (StratLithoUnit.DeleteStatus==None))]
        return make_response(jsonify(strat_litho_units),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@strat_litho_unit_bp.route('/apiv1/delete_strat_litho_unit/<int:StratLithoId>',methods=['DELETE'])
@jwt_required()
@only_data_admin
def delete_strat_litho_unit(StratLithoId):
    try:
        strat_litho_unit = StratLithoUnit.query.get(StratLithoId)
        strat_litho_unit.DeleteStatus = DeleteStatusEnum.Deleted
        strat_litho_unit.update()
        return make_response(jsonify({'message':'Strat Litho Unit successfully deleted.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)
