# from run import api
from flask_restplus import Resource, Namespace, reqparse, fields
from models.identity_model import UserModel, RevokedTokenModel
from flask_jwt_extended import jwt_required

api = Namespace('cmdb', description='CMDB related operations')

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

''' adding models for marshalling '''


class CmdbDto:
    cmdb = api.model('cmdb_operations', {
        'id': fields.Integer(description='Pool unique id'),
        'machinename': fields.String(required=True, description='Machine name'),
        'ipaddress': fields.String(required=True, description='Machine IP Address'),
        'network': fields.String(required=True, description='NIC 0 network name'),
        'mem': fields.Integer(description='Machine memory in GB.'),
        'cpus': fields.Integer(description='Number of CPUs'),
        'disk': fields.Integer(description='HD size in GB'),
        'os': fields.String(description='Operating System'),
        'datacenter': fields.String(description='Datacenter serving machine')
    })


@api.route('/')
class GetCmdbs(Resource):
    @jwt_required
    def get(self):
        return {'Assignments': 'Get all configuration items'}

    @jwt_required
    @api.expect(CmdbDto.cmdb)
    def post(self):
        return {'Assignment': 'Add IP assignment'}


@api.route('/<id>')
class GetCmdb(Resource):
    @jwt_required
    def get(self, id):
        return {'Assignment': 'Get configuration item by id'}

    @jwt_required
    @api.expect(CmdbDto.cmdb)
    def put(self,id):
        return {'Assignment': 'Update a configuration item by id'}





