from flask import Blueprint, request, make_response, jsonify
from flask.globals import g
from ..models.CraneUser import DeleteStatusEnum, UserCatgoryEnum, CraneUser
from ..models.FluidSamples import FluidCategoryEnum, FluidSamples
from ..models.Cuttings import Cuttings, CuttingsCategoryEnum
from flask_jwt_extended import (
    jwt_required,
    get_jwt
)
import traceback

dashboard_bp = Blueprint('dashboard_bp', __name__)

# get data admins  
@dashboard_bp.route('/apiv1/get_data_admins',methods=['GET'])
@jwt_required()
def get_data_admins():
    try:
        data_admins = CraneUser.query.filter(CraneUser.UserCategory == UserCatgoryEnum.Data_Admin)
        data_admins = [admin.serialise() for admin in data_admins]
        return make_response(jsonify(data_admins),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get app admins  
@dashboard_bp.route('/apiv1/get_app_admins',methods=['GET'])
@jwt_required()
def get_app_admins():
    try:
        app_admins = CraneUser.query.filter(CraneUser.UserCategory == UserCatgoryEnum.App_Admin)
        app_admins = [admin.serialise() for admin in app_admins]
        return make_response(jsonify(app_admins),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get staff
@dashboard_bp.route('/apiv1/get_staff',methods=['GET'])
@jwt_required()
def get_staff():
    try:
        staff = CraneUser.query.filter(CraneUser.UserCategory == UserCatgoryEnum.Staff)
        staff = [member.serialise() for member in staff]
        return make_response(jsonify(staff),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get oils
@dashboard_bp.route('/apiv1/get_oil_samples',methods=['GET'])
@jwt_required()
def get_oil_samples():
    try:
        oils = FluidSamples.query.filter(FluidSamples.FluidCategory == FluidCategoryEnum.Oil,\
            (FluidSamples.DeleteStatus==DeleteStatusEnum.Available) | (FluidSamples.DeleteStatus==None))
        oils = [sample.serialise() for sample in oils]
        return make_response(jsonify(oils),200)
    except:
        return make_response(str(traceback.format_exc()),500)

    
# get gas
@dashboard_bp.route('/apiv1/get_gas_samples',methods=['GET'])
@jwt_required()
def get_gas_samples():
    try:
        gas = FluidSamples.query.filter(FluidSamples.FluidCategory == FluidCategoryEnum.Gas,\
            (FluidSamples.DeleteStatus==DeleteStatusEnum.Available) | (FluidSamples.DeleteStatus==None))
        gas = [sample.serialise() for sample in gas]
        return make_response(jsonify(gas),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get water
@dashboard_bp.route('/apiv1/get_water_samples',methods=['GET'])
@jwt_required()
def get_water_samples():
    try:
        water = FluidSamples.query.filter(FluidSamples.FluidCategory == FluidCategoryEnum.Water,\
            (FluidSamples.DeleteStatus==DeleteStatusEnum.Available) | (FluidSamples.DeleteStatus==None))
        water = [sample.serialise() for sample in water]
        return make_response(jsonify(water),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get washed dried cutting
@dashboard_bp.route('/apiv1/get_washed_dried',methods=['GET'])
@jwt_required()
def get_washed_dried():
    try:
        cuttings = Cuttings.query.filter(Cuttings.CuttingCategory == CuttingsCategoryEnum.Washed_Dried,\
            (Cuttings.DeleteStatus==DeleteStatusEnum.Available) | (Cuttings.DeleteStatus==None))
        cuttings = [sample.serialise() for sample in cuttings]
        return make_response(jsonify(cuttings),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get washed wet cutting
@dashboard_bp.route('/apiv1/get_washed_wet',methods=['GET'])
@jwt_required()
def get_washed_wet():
    try:
        cuttings = Cuttings.query.filter(Cuttings.CuttingCategory == CuttingsCategoryEnum.Washed_Wet,\
            (Cuttings.DeleteStatus==DeleteStatusEnum.Available) | (Cuttings.DeleteStatus==None))
        cuttings = [sample.serialise() for sample in cuttings]
        return make_response(jsonify(cuttings),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get wet unwashed cutting
@dashboard_bp.route('/apiv1/get_wet_unwashed',methods=['GET'])
@jwt_required()
def get_wet_unwashed():
    try:
        cuttings = Cuttings.query.filter(Cuttings.CuttingCategory == CuttingsCategoryEnum.Wet_Unwashed,\
            (Cuttings.DeleteStatus==DeleteStatusEnum.Available) | (Cuttings.DeleteStatus==None))
        cuttings = [sample.serialise() for sample in cuttings]
        return make_response(jsonify(cuttings),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get dry unwashed cutting
@dashboard_bp.route('/apiv1/get_dry_unwashed',methods=['GET'])
@jwt_required()
def get_dry_unwashed():
    try:
        cuttings = Cuttings.query.filter(Cuttings.CuttingCategory == CuttingsCategoryEnum.Dry_Unwashed,\
            (Cuttings.DeleteStatus==DeleteStatusEnum.Available) | (Cuttings.DeleteStatus==None))
        cuttings = [sample.serialise() for sample in cuttings]
        return make_response(jsonify(cuttings),200)
    except:
        return make_response(str(traceback.format_exc()),500)
