from flask import Blueprint, request, make_response, jsonify
from ..models.StratLithoUnit import StratLithoUnit
from ..models.CraneUser import CraneUser, UserCatgoryEnum
from flask_jwt_extended import (
    jwt_required,
    get_jwt
    )
# reference for api changes https://flask-jwt-extended.readthedocs.io/en/stable/v4_upgrade_guide/#api-changes
import datetime


strat_litho_unit_bp = Blueprint('strat_litho_unit_bp', __name__)

@strat_litho_unit_bp.route('/apiv1/add_strat_litho_unit',methods=['POST'])
@jwt_required()
def add_strat_litho_unit():
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()
    try:
        new_strat_litho_unit = StratLithoUnit(
                        PAUID = data['PAUID'],
                        StratLithoName = data['StratLithoName'],
                        ReserviorUnit = data['ReserviorUnit'],  # should be 0 or 1
                        LithoStratAlias = data['LithoStratAlias'],
                        IsReservoirUnit_id = data['IsReservoirUnit_id'],
                        LithoStratAge_id = data['LithoStratAge_id'],
                        LithoStratDescriptionSoftcopyPath = data['LithoStratDescriptionSoftcopyPath'],
                        LithoStratDescriptionHyperlink = data['LithoStratDescriptionHyperlink'],
                        LithoStratMapSoftCopyPath = data['LithoStratMapSoftCopyPath'],
                        LithoStratMapHyperlink = data['LithoStratMapHyperlink'],
                        MapPortalLithoStratMapLink = data['MapPortalLithoStratMapLink'],
                        LithoStratFactsiteUrl = data['LithoStratFactsiteUrl'],
                        Comments = data['Comments'],
                        CreatedBy_id = user.CraneUser_id,
                        DateCreated = datetime.datetime.now(),
                    )
        new_strat_litho_unit.save()
        return make_response(jsonify({'message':'Strat Litho Unit added successfuly.'}),201)
    except Exception as error:
        return make_response(jsonify({'message':error}),500)


@strat_litho_unit_bp.route('/apiv1/edit_strat_litho_unit/<int:StratLitho_id>',methods=['PUT'])
@jwt_required()
def edit_strat_litho_unit(StratLitho_id):
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()
    try:
        strat_litho_unit = StratLithoUnit.query.get(StratLitho_id)
        strat_litho_unit.PAUID = data['PAUID']
        strat_litho_unit.StratLithoName = data['StratLithoName']
        strat_litho_unit.ReserviorUnit = data['ReserviorUnit']
        strat_litho_unit.LithoStratAlias = data['LithoStratAlias']
        strat_litho_unit.IsReservoirUnit_id = data['IsReservoirUnit_id']
        strat_litho_unit.LithoStratAge_id = data['LithoStratAge_id']
        strat_litho_unit.LithoStratDescriptionSoftcopyPath = data['LithoStratDescriptionSoftcopyPath']
        strat_litho_unit.LithoStratDescriptionHyperlink = data['LithoStratDescriptionHyperlink']
        strat_litho_unit.LithoStratMapSoftCopyPath = data['LithoStratMapSoftCopyPath']
        strat_litho_unit.LithoStratMapHyperlink = data['LithoStratMapHyperlink']
        strat_litho_unit.MapPortalLithoStratMapLink = data['MapPortalLithoStratMapLink']
        strat_litho_unit.LithoStratFactsiteUrl = data['LithoStratFactsiteUrl']
        strat_litho_unit.Comments = data['Comments']
        strat_litho_unit.ModifiedOn = datetime.datetime.now()
        strat_litho_unit.ModifiedBy = user.CraneUser_id
        strat_litho_unit.update()
        return make_response(jsonify({'message':'Strat Litho Unit updated successfuly.'}),200)
    except Exception as error:
        return make_response(jsonify({'message':error}),500)


# get single strat_litho_unit object
@strat_litho_unit_bp.route('/apiv1/get_strat_litho_unit/<int:StratLitho_id>',methods=['GET'])
@jwt_required()
def get_strat_litho_unit(StratLitho_id):
    try:
        strat_litho_unit = StratLithoUnit.query.get(StratLitho_id)
        return make_response(jsonify(strat_litho_unit.serialise()),200)
    except Exception as error:
        return make_response(jsonify({'message':error}),500)


@strat_litho_unit_bp.route('/apiv1/get_strat_litho_units',methods=['GET'])
@jwt_required()
def get_all_strat_litho_units():
    try:
        strat_litho_units = [z.serialise() for z in StratLithoUnit.query.all()]
        return make_response(jsonify(strat_litho_units),200)
    except Exception as error:
        return make_response(jsonify({'message':error}),500)


@strat_litho_unit_bp.route('/apiv1/delete_strat_litho_unit/<int:StratLitho_id>',methods=['DELETE'])
@jwt_required()
def delete_strat_litho_unit(StratLitho_id):
    try:
        strat_litho_unit = StratLithoUnit.query.get(StratLitho_id)
        strat_litho_unit.delete()
        return make_response(jsonify({'message':'Strat Litho Unit successfully deleted.'}),200)
    except Exception as error:
        return make_response(jsonify({'message':error}),500)