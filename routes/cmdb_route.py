'''

BSD 3-Clause License

Copyright (c) 2019, Kovarus
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



'''

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
        'datacenter': fields.String(description='Datacenter serving machine'),
        'owner' : fields.String(description='Machine owner, AKA requestedBy'),
        'status' : fields.Integer(description='Machine status, active = 1, retired = 2')
    })



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





