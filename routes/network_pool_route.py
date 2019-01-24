# from run import api
from flask_restplus import Resource, Namespace, reqparse, fields
from models.identity_model import UserModel, RevokedTokenModel
from flask_jwt_extended import jwt_required

api = Namespace('pools', description='Network pool related operations')

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

''' adding models for marshalling '''


class NetworkPoolsDto:
    pool = api.model('network_pools', {
        'id': fields.Integer(description='Pool unique id'),
        'poolname': fields.String(required=True, description='Pool name'),
        'poolrange': fields.String(required=True, description='Network pool range'),
        'subnetmask': fields.String(required=True, description='Network subnet'),
        'gateway': fields.String(description='Gateway'),
        'dns1': fields.String(required=True, description='DNS 1 IP', default='8.8.8.8'),
        'dns2': fields.String(description='DNS 2 IP', default='8.8.4.4'),
        'domainname': fields.String(required=True, description='Domain name', default='corp.local'),
        'owner_id': fields.Integer(description='Parent network name')
    })


@api.route('/')
class GetPools(Resource):
    @jwt_required
    def get(self):
        return {'Pools': 'Get all network pools'}

    @jwt_required
    @api.expect(NetworkPoolsDto.pool)
    def post(self):
        return {'Pool': 'Add pool'}


@api.route('/<id>')
class GetNetworkPool(Resource):
    @jwt_required
    def get(self, id):
        return {'Pool': 'Get network pool by id'}

    @jwt_required
    @api.expect(NetworkPoolsDto.pool)
    def put(self,id):
        return {'Pool': 'Update a network pool by id'}





