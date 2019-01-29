# from run import api
from flask_restplus import Resource, Namespace, reqparse, fields
# from models.identity_model import UserModel, RevokedTokenModel
# from ..models.identity_model import UserModel, RevokedTokenModel
from flask_jwt_extended import jwt_required

api = Namespace('dns', description='DNS related operations')

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

''' adding models for marshalling '''

# class AuthDto:
#     user_auth = api.model('user_details', {
#         'username':fields.String(required=True, description="The username"),
#         'password': fields.String(required=True, description='User password')
#     })


@api.route('/dns')
class PdnsRecords(Resource):
    #@ api.expect(AuthDto.user_auth)
    @jwt_required
    def get(self):
        return {'DNS': 'Get DNS records'}

    @jwt_required
    def post(self):
        return {'DNS': 'Add DNS Record'}


@api.route('/dns/<id>')
class PdnsRecord(Resource):
    @jwt_required
    def get(self, id):
        return {'DNS': 'Get DNS record by id'}

    @jwt_required
    def put(self, id):
        return {'DNS': 'Update a DNS record by id'}

    @jwt_required
    def delete(self, id):
        return {'DNS': 'Delete a DNS record by id'}

