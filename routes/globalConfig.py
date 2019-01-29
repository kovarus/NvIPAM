from flask_restplus import Resource, Namespace, reqparse, fields
from flask_jwt_extended import jwt_required

api = Namespace('settings', description='System settings related operations')

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

''' adding models for marshalling '''


class SettingsDto:
    settings = api.model('global_settings_operations', {
        'id': fields.Integer(description='Unique id'),
        'dns1': fields.String(required=True, description='DNS 1 IP', default='8.8.8.8'),
        'dns2': fields.String(description='DNS 2 IP', default='8.8.4.4'),
        'domainname': fields.String(required=True, description='Domain name', default='corp.local')
    })


@api.route('/')
class GetSettings(Resource):
    @jwt_required
    def get(self):
        return {'Settings': 'Get system settings'}

    @jwt_required
    @api.expect(SettingsDto.settings)
    def post(self):
        return {'Settings': 'Add new settings'}


@api.route('/<id>')
class GetSettings(Resource):
    @jwt_required
    @api.expect(SettingsDto.settings)
    def put(self,id):
        return {'Settings': 'Update system settings'}





