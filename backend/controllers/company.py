from flask import Blueprint, request, make_response, jsonify
from ..models.Company import Company
from ..models.CraneUser import CraneUser, UserCatgoryEnum
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
                        NSD_Number = data['NSD_Number'],
                        CompanyCategory_id = data['CompanyCategory_id'],
                        CountryOfOrigin_id = data['CountryOfOrigin_id'],
                        CountryOfRegistration_id = data['CountryOfRegistration_id'],
                        RegistrationNumber = data['RegistrationNumber'],
                        TINNumber = data['TINNumber'],
                        CompanyTelephone = data['CompanyTelephone'],
                        CompanyEmail = data['CompanyEmail'],
                        CompanyWebsite = data['CompanyWebsite'],
                        CompanyEntityType_id = data['CompanyEntityType_id'],
                        CompanyEntitySubType_id = data['CompanyEntitySubType_id'],
                        CompanyMajorActivity_id = data['CompanyMajorActivity_id'],
                        CompanyActivityDivision_id = data['CompanyActivityDivision_id'],
                        CompanyActivityDivisionClass_id = data['CompanyActivityDivisionClass_id'],
                        CompanyActivityDivisionClassCategory_id = data['CompanyActivityDivisionClassCategory_id'],
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
                        RegistrationStatus_id = data['RegistrationStatus_id'],
                        ClassifyAsUgandan_id = data['ClassifyAsUgandan_id'],
                        Comments = data['Comments'],
                        PrimaryCompanyKind_id = data['PrimaryCompanyKind_id'],
                        SecondaryCompanyKind_id = data['SecondaryCompanyKind_id'],
                        OtherCompanyKind_id = data['OtherCompanyKind_id'],
                        CompanyGroup_id = data['CompanyGroup_id'],
                        CompanyMobile = data['CompanyMobile'],
                        CompanyFax = data['CompanyFax'],
                        ContactEntityFax = data['ContactEntityFax'],
                        NSD_FromDate = data['NSD_FromDate'],
                        NSD_ToDate = data['NSD_ToDate'],
                        ImportedFromNSD = data['ImportedFromNSD'],
                        ImportedDate = data['ImportedDate'],
                        ExportedDate = data['ExportedDate'],
                        ExportedToNogtr = data['ExportedToNogtr'],
                        CreatedBy = user.CraneUser_id,
                        DateCreated = datetime.datetime.now(),
                        PreviousLegalName = data['PreviousLegalName'],
                    )
        new_company.save()
        return make_response(jsonify({'message':'Company added successfuly.'}),201)
    except:
        return make_response(str(traceback.format_exc()),500)


@company_bp.route('/apiv1/edit_company/<int:Company_id>',methods=['PUT'])
@jwt_required()
@only_data_admin
def edit_company(Company_id):
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
        if Company_id != pauid.Company_id:
            return make_response(jsonify({'message':'PAUID already exists.'}),409)
    if company_name:       
        if Company_id != company_name.Company_id:
            return make_response(jsonify({'message':'CompanyLongName already exists.'}),409)
    if company_short_name  and company_short_name.CompanyShortName != None: 
        if Company_id != company_short_name.Company_id:
            return make_response(jsonify({'message':'CompanyShortName already exists.'}),409)
    if registration_number:       
        if Company_id != registration_number.Company_id:
            return make_response(jsonify({'message':'RegistrationNumber already exists.'}),409)
    if tin:       
        if Company_id != tin.Company_id:
            return make_response(jsonify({'message':'TINNumber already exists.'}),409)
    if email and email.CompanyEmail != None:   
        if Company_id != email.Company_id:
            return make_response(jsonify({'message':'CompanyEmail already exists.'}),409)

    try:
        company = Company.query.get(Company_id)
        company.PAUID = data['PAUID']
        company.CompanyLongName = data['CompanyLongName']
        company.CompanyShortName = data['CompanyShortName']
        company.NSD_Number = data['NSD_Number']
        company.CompanyCategory_id = data['CompanyCategory_id']
        company.CountryOfOrigin_id = data['CountryOfOrigin_id']
        company.CountryOfRegistration_id = data['CountryOfRegistration_id']
        company.RegistrationNumber = data['RegistrationNumber']
        company.TINNumber = data['TINNumber']
        company.CompanyTelephone = data['CompanyTelephone']
        company.CompanyEmail = data['CompanyEmail']
        company.CompanyWebsite = data['CompanyWebsite']
        company.CompanyEntityType_id = data['CompanyEntityType_id']
        company.CompanyEntitySubType_id = data['CompanyEntitySubType_id']
        company.CompanyMajorActivity_id = data['CompanyMajorActivity_id']
        company.CompanyActivityDivision_id = data['CompanyActivityDivision_id']
        company.CompanyActivityDivisionClass_id = data['CompanyActivityDivisionClass_id']
        company.CompanyActivityDivisionClassCategory_id = data['CompanyActivityDivisionClassCategory_id']
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
        company.RegistrationStatus_id = data['RegistrationStatus_id']
        company.ClassifyAsUgandan_id = data['ClassifyAsUgandan_id']
        company.Comments = data['Comments']
        company.PrimaryCompanyKind_id = data['PrimaryCompanyKind_id']
        company.SecondaryCompanyKind_id = data['SecondaryCompanyKind_id']
        company.OtherCompanyKind_id = data['OtherCompanyKind_id']
        company.CompanyGroup_id = data['CompanyGroup_id']
        company.CompanyMobile = data['CompanyMobile']
        company.CompanyFax = data['CompanyFax']
        company.ContactEntityFax = data['ContactEntityFax']
        company.NSD_FromDate = data['NSD_FromDate']
        company.NSD_ToDate = data['NSD_ToDate']
        company.ImportedFromNSD = data['ImportedFromNSD']
        company.ImportedDate = data['ImportedDate']
        company.ExportedDate = data['ExportedDate']
        company.ExportedToNogtr = data['ExportedToNogtr']
        company.ModifiedBy = user.CraneUser_id
        company.ModifiedOn = datetime.datetime.now()
        company.PreviousLegalName = data['PreviousLegalName']
        company.RecordChangeStamp = data['RecordChangeStamp']
        company.update()
        return make_response(jsonify({'message':'Company updated successfuly.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)


# get single company object
@company_bp.route('/apiv1/get_company/<int:Company_id>',methods=['GET'])
@jwt_required()
def get_company(Company_id):
    try:
        company = Company.query.get(Company_id)
        return make_response(jsonify(company.serialise()),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@company_bp.route('/apiv1/get_companies',methods=['GET'])
@jwt_required()
def get_all_companies():
    try:
        company = [z.serialise() for z in Company.query.all()]
        return make_response(jsonify(company),200)
    except:
        return make_response(str(traceback.format_exc()),500)


@company_bp.route('/apiv1/delete_company/<int:Company_id>',methods=['DELETE'])
@jwt_required()
@only_data_admin
def delete_company(Company_id):
    try:
        company = Company.query.get(Company_id)
        company.delete()
        return make_response(jsonify({'message':'Company successfully deleted.'}),200)
    except:
        return make_response(str(traceback.format_exc()),500)
