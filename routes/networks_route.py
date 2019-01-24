# from run import api
from flask_restplus import Resource, Namespace, reqparse, fields
from models.identity_model import UserModel, RevokedTokenModel
from flask_jwt_extended import jwt_required

api = Namespace('networks', description='Networks related operations')

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

''' adding models for marshalling '''


class NetworksDto:
    network = api.model('networks', {
        'id': fields.Integer(description='Network unique di'),
        'key': fields.String(required=True, description='NetworkId'),
        'networkname': fields.String(required=True, description='Network name'),
        'vlanid': fields.String(required=True, description='Network vlanId'),
        'datacenter': fields.String(description='Datacenter'),
        'cluster': fields.String(description='Cluster')
    })


@api.route('/')
class GetNetworks(Resource):
    @jwt_required
    def get(self):
        return {'Networks': 'Get all networks'}

    @jwt_required
    @api.expect(NetworksDto.network)
    def post(self):
        return {'Network': 'Add network'}


@api.route('/<id>')
class GetNetwork(Resource):
    @jwt_required
    def get(self, id):
        return {'Network': 'Get network by id'}

    @jwt_required
    @api.expect(NetworksDto.network)
    def put(self,id):
        return {'Network': 'Update a network by id'}





