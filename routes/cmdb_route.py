from flask_restplus import Resource, Namespace, reqparse, fields
from flask import request
from flask_jwt_extended import jwt_required
from service.cmdb_service import get_all_cis, save_new_ci, get_a_ci, update_a_ci

api = Namespace('cmdb', description='CMDB related operations')

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
# jwt_required


@api.route('/')
class GetCmdbs(Resource):
    @jwt_required
    @api.marshal_list_with(CmdbDto.cmdb, envelope='data')
    def get(self):
        """Get all configuration items"""
        return get_all_cis()

    @jwt_required
    @api.expect(CmdbDto.cmdb)
    def post(self):
        """Add a new configuration item"""
        data = request.json
        return save_new_ci(data=data)


@api.route('/<id>')
class GetCmdb(Resource):
    @jwt_required
    @api.marshal_list_with(CmdbDto.cmdb, envelope='data')
    def get(self, id):
        """Get CI by id"""
        return get_a_ci(id)

    @jwt_required
    @api.expect(CmdbDto.cmdb)
    def put(self,id):
        """Update a CI by id"""
        data = request.json
        # print (data)
        return update_a_ci(id, data)





