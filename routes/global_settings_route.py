from flask_restplus import Resource, Namespace, reqparse, fields
from flask import request
from flask_jwt_extended import jwt_required
from service.global_settings_service import get_all_settings, update_a_setting, save_new_settings

api = Namespace('settings', description='Global settings related operations')

''' adding models for marshalling '''


class GlobalSettingsDto:
    settings = api.model('global_settings_operations', {
        'id': fields.Integer(description='Unique id'),
        'dns1': fields.String(required=True, description='DNS 1 IP', default='8.8.8.8'),
        'dns2': fields.String(description='DNS 2 IP', default='8.8.4.4'),
        'domainname': fields.String(required=True, description='Domain name', default='corp.local')
    })


@api.route('/')
class SettingsList(Resource):
    @api.marshal_list_with(GlobalSettingsDto.settings, envelope='data')
    @jwt_required
    def get(self):
        """List all global settings"""
        return get_all_settings()

    @api.expect(GlobalSettingsDto.settings, validate=True)
    @jwt_required
    def post(self):
        """Creates a new global settings """
        data = request.json
        return save_new_settings(data=data)

    @api.expect(GlobalSettingsDto.settings, validate=True)
    @jwt_required
    def put(self, id):
        """Creates a new Configuration Item """
        data = request.json
        return update_a_setting(id=id, data=data)
