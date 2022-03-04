from flask import Blueprint, request, make_response, jsonify
from ..models.Company import Company
from ..models.CraneUser import CraneUser, DeleteStatusEnum, UserCatgoryEnum
from flask_jwt_extended import (
    jwt_required,
    get_jwt
    )
# reference for api changes https://flask-jwt-extended.readthedocs.io/en/stable/v4_upgrade_guide/#api-changes
import datetime
import traceback
from ..middleware.permissions import only_data_admin


company_bp = Blueprint('company_bp', __name__)

@company_bp.route('/apiv1/add_company',methods=['POST'])
@jwt_required()
@only_data_admin
def add_company():
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter(CraneUser.UserEmailAddress==current_user_email['sub']).first()
    # check for redundancies
    pauid = Company.query.filter_by(PAUID=data['PAUID']).first()
    company_name = Company.query.filter_by(CompanyLongName=data['CompanyLongName']).first()
    company_short_name = Company.query.filter_by(CompanyShortName=data['CompanyShortName']).first()
    registration_number = Company.query.filter_by(RegistrationNumber=data['RegistrationNumber']).first()
    tin = Company.query.filter_by(TINNumber=data['TINNumber']).first()
    email = Company.query.filter_by(CompanyEmail=data['CompanyEmail']).first()
    if pauid:
        return make_response(jsonify({'message':'PAUID already exists.'}),409)
    if company_name:
        return make_response(jsonify({'message':'CompanyLongName already exists.'}),409)
    if company_short_name and company_short_name.CompanyShortName != None:
        return make_response(jsonify({'message':'CompanyShortName already exists.'}),409)
    if registration_number:
        return make_response(jsonify({'message':'RegistrationNumber already exists.'}),409)
    if tin:
        return make_response(jsonify({'message':'TINNumber already exists.'}),409)
    if email and email.CompanyEmail != None:
        return make_response(jsonify({'message':'CompanyEmail already exists.'}),409)
        
    try:
        new_company = Company(
                        PAUID = data['PAUID'],
                        CompanyLongName = data['CompanyLongName'],
                        CompanyShortName = data['CompanyShortName'],
                        NSDNumber = data['NSDNumber'],
                        CompanyCategoryId = data['CompanyCategoryId'],
                        Country = data['Country'],
                        RegistrationNumber = data['RegistrationNumber'],
                        TINNumber = data['TINNumber'],
                        CompanyTelephone = data['CompanyTelephone'],
                        CompanyEmail = data['CompanyEmail'],
                        CompanyWebsite = data['CompanyWebsite'],
                        CompanyEntityTypeId = data['CompanyEntityTypeId'],
                        CompanyEntitySubTypeId = data['CompanyEntitySubTypeId'],
                        CompanyMajorActivityId = data['CompanyMajorActivityId'],
                        CompanyActivityDivisionId = data['CompanyActivityDivisionId'],
                        CompanyActivityDivisionClassId = data['CompanyActivityDivisionClassId'],
                        CompanyActivityDivisionClassCategoryId = data['CompanyActivityDivisionClassCategoryId'],
                        BusinessNatureDescription = data['BusinessNatureDescription'],
                        CompanyPostalAddress = data['CompanyPostalAddress'],
                        CompanyPhysicalAddress = data['CompanyPhysicalAddress'],
                        CompanyOtherEmails = data['CompanyOtherEmails'],
                        NSDQualificationDate = data['NSDQualificationDate'],
                        NSDQualificationYear = data['NSDQualificationYear'],
                        PrimaryContactEntity = data['PrimaryContactEntity'],
                        ContactEntityEmail = data['ContactEntityEmail'],
                        ContactEntityTelephone = data['ContactEntityTelephone'],
                        ContactEntityMobile = data['ContactEntityMobile'],
                        ContactDesignation = data['ContactDesignation'],
                        OperatorSortOrder = data['OperatorSortOrder'],
                        ContractorSortOrder = data['ContractorSortOrder'],
                        PAURegistrationDate = data['PAURegistrationDate'],
                        CraneNOGTRID = data['CraneNOGTRID'],
                        TempNOGTRIPwd = data['TempNOGTRIPwd'],
                        RegistrationStatusId = data['RegistrationStatusId'],
                        ClassifyAsUgandanId = data['ClassifyAsUgandanId'],
                        Comments = data['Comments'],
                        PrimaryCompanyKindId = data['PrimaryCompanyKindId'],
                        SecondaryCompanyKindId = data['SecondaryCompanyKindId'],
                        OtherCompanyKindId = data['OtherCompanyKindId'],
                        CompanyGroupId = data['CompanyGroupId'],
                        CompanyMobile = data['CompanyMobile'],
                        CompanyFax = data['CompanyFax'],
                        ContactEntityFax = data['ContactEntityFax'],
                        NSDFromDate = data['NSDFromDate'],
                        NSDToDate = data['NSDToDate'],
                        ImportedFromNSD = data['ImportedFromNSD'],
                        ImportedDate = data['ImportedDate'],
                        ExportedDate = data['ExportedDate'],
                        ExportedToNogtr = data['ExportedToNogtr'],
                        CreatedBy = user.CraneUserId,
                        DateCreated = datetime.datetime.now(),
                        PreviousLegalName = data['PreviousLegalName'],
                    )
        new_company.save()
        return make_response(jsonify({'message':'Company added successfuly.'}),201)
    except:
        return make_response(str(traceback.format_exc()),500)


@company_bp.route('/apiv1/edit_company/<int:CompanyId>',methods=['PUT'])
@jwt_required()
@only_data_admin
def edit_company(CompanyId):
    data = request.get_json(force=True)
    current_user_email = get_jwt()
    user = CraneUser.query.filter_by(UserEmailAddress=current_user_email['sub']).first()

    # check for redundancies
    pauid = Company.query.filter_by(PAUID=data['PAUID']).first()
    company_name = Company.query.filter_by(CompanyLongName=data['CompanyLongName']).first()
    company_short_name = Company.query.filter_by(CompanyShortName=data['CompanyShortName']).first()
    registration_number = Company.query.filter_by(RegistrationNumber=data['RegistrationNumber']).first()
    tin = Company.query.filter_by(TINNumber=data['TINNumber']).first()
    email = Company.query.filter_by(CompanyEmail=data['CompanyEmail']).first()
    if pauid:
        if CompanyId != pauid.CompanyId:
            return make_response(jsonify({'message':'PAUID already exists.'}),409)
    if company_name:       
        if CompanyId != company_name.CompanyId:
            return make_response(jsonify({'message':'CompanyLongName already exists.'}),409)
    if company_short_name  and company_short_name.CompanyShortName != None: 
        if CompanyId != company_short_name.CompanyId:
            return make_response(jsonify({'message':'CompanyShortName already exists.'}),409)
    if registration_number:       
        if CompanyId != registration_number.CompanyId:
            return make_response(jsonify({'message':'RegistrationNumber already exists.'}),409)
    if tin:       
        if CompanyId != tin.CompanyId:
            return make_response(jsonify({'message':'TINNumber already exists.'}),409)
    if email and email.CompanyEmail != None:   
        if CompanyId != email.CompanyId:
            return make_response(jsonify({'message':'CompanyEmail already exists.'}),409)

    try:
        company = Company.query.get(CompanyId)
        company.PAUID = data['PAUID']
        company.CompanyLongName = data['CompanyLongName']
        company.CompanyShortName = data['CompanyShortName']
        company.NSDNumber = data['NSDNumber']
        company.CompanyCategoryId = data['CompanyCategoryId']
        company.Country = data['Country']
        company.RegistrationNumber = data['RegistrationNumber']
        company.TINNumber = data['TINNumber']
        company.CompanyTelephone = data['CompanyTelephone']
        company.CompanyEmail = data['CompanyEmail']
        company.CompanyWebsite = data['CompanyWebsite']
        company.CompanyEntityTypeId = data['CompanyEntityTypeId']
        company.CompanyEntitySubTypeId = data['CompanyEntitySubTypeId']
        company.CompanyMajorActivityId = data['CompanyMajorActivityId']
        company.CompanyActivityDivisionId = data['CompanyActivityDivisionId']
        company.CompanyActivityDivisionClassId = data['CompanyActivityDivisionClassId']
        company.CompanyActivityDivisionClassCategoryId = data['CompanyActivityDivisionClassCategoryId']
        company.BusinessNatureDescription = data['BusinessNatureDescription']
        company.CompanyPostalAddress = data['CompanyPostalAddress']
        company.CompanyPhysicalAddress = data['CompanyPhysicalAddress']
        company.CompanyOtherEmails = data['CompanyOtherEmails']
        company.NSDQualificationDate = data['NSDQualificationDate']
        company.NSDQualificationYear = data['NSDQualificationYear']
        company.PrimaryContactEntity = data['PrimaryContactEntity']
        company.ContactEntityEmail = data['ContactEntityEmail']
        company.ContactEntityTelephone = data['ContactEntityTelephone']
        company.ContactEntityMobile = data['ContactEntityMobile']
        company.ContactDesignation = data['ContactDesignation']
        company.OperatorSortOrder = data['OperatorSortOrder']
        company.ContractorSortOrder = data['ContractorSortOrder']
        company.PAURegistrationDate = data['PAURegistrationDate']
        company.CraneNOGTRID = data['CraneNOGTRID']
        company.TempNOGTRIPwd = data['TempNOGTRIPwd']
        company.RegistrationStatusId = data['RegistrationStatusId']
        company.ClassifyAsUgandanId = data['ClassifyAsUgandanId']
        company.Comments = data['Comments']
        company.PrimaryCompanyKindId = data['PrimaryCompanyKindId']
        company.SecondaryCompanyKindId = data['SecondaryCompanyKindId']
        company.OtherCompanyKindId = data['OtherCompanyKindId']
        company.CompanyGroupId = data['CompanyGroupId']
        company.CompanyMobile = data['CompanyMobile']
        company.CompanyFax = data['CompanyFax']
        company.ContactEntityFax = data['ContactEntityFax']
        company.NSDFromDate = data['NSDFromDate']
        company.NSDToDate = data['NSDToDate']
        company.ImportedFromNSD = data['ImportedFromNSD']
        company.ImportedDate = data['ImportedDate']
        company.ExportedDate = data['ExportedDate']
        company.ExportedToNogtr = data['ExportedToNogtr']
        company.ModifiedBy = user.CraneUserId
        company.ModifiedOn = datetime.datetime.now()
        company.PreviousLegalName = data['PreviousLegalName']
        company.RecordChangeStamp = data['RecordChangeStamp']
        company.update()
        return make_response(jsonify({'message':'Company updated successfuly.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get single company object
@company_bp.route('/apiv1/get_company/<int:CompanyId>',methods=['GET'])
@jwt_required()
def get_company(CompanyId):
    try:
        company = Company.query.get(CompanyId)
        return make_response(jsonify(company.serialise()),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@company_bp.route('/apiv1/get_companies',methods=['GET'])
@jwt_required()
def get_all_companies():
    try:
        company = [z.serialise() for z in Company.query.\
            filter((Company.DeleteStatus==DeleteStatusEnum.Available) | (Company.DeleteStatus==None))]
        return make_response(jsonify(company),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@company_bp.route('/apiv1/delete_company/<int:CompanyId>',methods=['DELETE'])
@jwt_required()
# @only_data_admin
def delete_company(CompanyId):
    try:
        company = Company.query.get(CompanyId)
        company.DeleteStatus = DeleteStatusEnum.Deleted
        company.update()
        return make_response(jsonify({'message':'Company successfully deleted.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)
