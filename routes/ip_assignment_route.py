from flask_restplus import Resource, Namespace, reqparse, fields
from flask_jwt_extended import jwt_required

api = Namespace('ip_assignment', description='IP assignment related operations')


''' adding models for marshalling '''


class IpAddressDto:
    assignment = api.model('pool_assignments', {
        'id': fields.Integer(description='Assignment unique id'),
        'ipaddress': fields.String(description='Machine IP address', required=True),
        'machinename': fields.String(required=True, description='Machine name'),
        'status': fields.Integer(description='Machine status.  0 - unused, 1 - assigned, 2 - reserved, 3 - gateway'),
        'rangeid': fields.Integer(description='Parent pool id')
    })


@api.route('/')
class GetAssignments(Resource):
    @jwt_required
    def get(self):
        return {'Assignments': 'Get all IP assignments'}

    @jwt_required
    @api.expect(IpAddressDto.assignment)
    def post(self):
        return {'Assignment': 'Add IP assignment'}


@api.route('/<id>')
class GetIpAssignment(Resource):
    @jwt_required
    def get(self, id):
        return {'Assignment': 'Get IP assignment by id'}

    @jwt_required
    @api.expect(IpAddressDto.assignment)
    def put(self,id):
        return {'Assignment': 'Update a IP assignment by id'}





