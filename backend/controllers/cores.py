from flask import Blueprint, request, make_response, jsonify
from ..models.Cores import Cores
from ..models.CraneUser import CraneUser, UserCatgoryEnum
from flask_jwt_extended import (
    jwt_required,
    get_jwt
    )
# reference for api changes https://flask-jwt-extended.readthedocs.io/en/stable/v4_upgrade_guide/#api-changes
import datetime
import traceback
from .helper_functions import upload_file
from collections.abc import Iterable
from ..models.Files import Files


cores_bp = Blueprint('cores_bp', __name__)

@cores_bp.route('/apiv1/add_core',methods=['POST'])
@jwt_required()
def add_core():
    if request.is_json:
            data = request.get_json(force=True)
    else:
        data = request.form
    file = request.files
    
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()
    
    try:
        new_core = Cores(
                        Coring_contractor = data['Coring_contractor'],
                        Wellbore_id = data['Wellbore_id'],
                        Core_number = data['Core_number'],
                        Coring_date = data['Coring_date'],
                        Top_MD = data['Top_MD'], #depth
                        Bottom_MD = data['Bottom_MD'], #depth
                        Cut_length = data['Cut_length'],
                        Percentage_recovery = data['Percentage_recovery'],
                        Top_formation = data['Top_formation'],
                        Bottom_formation = data['Bottom_formation'],
                        # Core_photograph = data['Core_photograph'],
                        # Core_analysis_reports = data['Core_analysis_reports'],
                        CreatedBy_id = user.CraneUser_id
                    )
        new_core.save()
        return make_response(jsonify({'message':'Core added successfuly.'}),201)
    except:
        return make_response(str(traceback.format_exc()),500)



@cores_bp.route('/apiv1/edit_core/<int:Core_sample_id>',methods=['PUT'])
@jwt_required()
def edit_core(Core_sample_id):
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()

    try:
        core = Cores.query.get(Core_sample_id)
        core.Coring_contractor = data['Coring_contractor']
        core.Wellbore_id = data['Wellbore_id']
        core.Core_number = data['Core_number']
        core.Coring_date = data['Coring_date']
        core.Top_MD = data['Top_MD']
        core.Bottom_MD = data['Bottom_MD']
        core.Cut_length = data['Cut_length']
        core.Percentage_recovery = data['Percentage_recovery']
        core.Top_formation = data['Top_formation']
        core.Bottom_formation = data['Bottom_formation']
        # core.Core_photograph = data['Core_photograph']
        # core.Core_analysis_reports = data['Core_analysis_reports']
        core.Modified_by = user.CraneUser_id
        core.update()
        return make_response(jsonify({'message':'Core updated successfuly.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@cores_bp.route('/apiv1/get_core/<int:Core_sample_id>',methods=['GET'])
@jwt_required()
def get_core(Core_sample_id):
    try:
        core = Cores.query.get(Core_sample_id)
        return make_response(jsonify(core.serialise()),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@cores_bp.route('/apiv1/get_cores',methods=['GET'])
@jwt_required()
def get_all_cores():
    try:
        cores = [z.serialise() for z in Cores.query.all()]
        return make_response(jsonify(cores),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@cores_bp.route('/apiv1/delete_core/<int:Core_sample_id>',methods=['DELETE'])
@jwt_required()
def delete_core(Core_sample_id):
    try:
        core = Cores.query.get(Core_sample_id)
        core.delete()
        return make_response(jsonify({'message':'Core successfully deleted.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)
