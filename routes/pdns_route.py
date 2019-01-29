from flask_restplus import Resource, Namespace, reqparse, fields
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
        """Get all DNS records"""
        return {'DNS': 'Get DNS records'}

    @jwt_required
    def post(self):
        """Add DNS record"""
        return {'DNS': 'Add DNS Record'}


@api.route('/dns/<id>')
class PdnsRecord(Resource):
    @jwt_required
    def get(self, id):
        """Get DNS record by id"""
        return {'DNS': 'Get DNS record by id'}

    @jwt_required
    def put(self, id):
        """Update DNS record by id"""
        return {'DNS': 'Update a DNS record by id'}

    @jwt_required
    def delete(self, id):
        """Delete DNS record"""
        return {'DNS': 'Delete a DNS record by id'}

