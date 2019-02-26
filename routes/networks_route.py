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
from service.networks_service import save_new_network, get_all_networks, get_a_network, update_a_network, get_network_tags, add_network_tag, delete_network_tag
from routes.tags_route import TagsDto
from flask_jwt_extended import jwt_required
from flask import request

api = Namespace('networks', description='Networks related operations')

_tags = TagsDto.tags

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
    # @api.marshal_list_with(NetworksDto.network, envelope='data')
    def get(self):
        """Get all networks"""
        return get_all_networks()

    @jwt_required
    @api.expect(NetworksDto.network)
    def post(self):
        """Add new network"""
        data = request.json
        return save_new_network(data)


@api.route('/<id>')
class GetNetwork(Resource):
    @jwt_required
    def get(self, id):
        """Get network by id"""
        return get_a_network(id)

    @jwt_required
    @api.expect(NetworksDto.network)
    def put(self,id):
        """Update a network by id"""
        data = request.json
        return update_a_network(id, data)

@api.route('/<id>/tags')
class NetworkTags(Resource):
    @jwt_required
    @api.expect(_tags)
    def get(self, id):
        """Get a network tags given its identifier"""
        tags = get_network_tags(id)
        if not tags:
            api.abort(404)
        else:
            return get_network_tags(id)

    @api.expect(_tags)
    @jwt_required
    def post(self, id):
        """Updates a Network Tag """
        data = request.json
        return add_network_tag(id, data)

    @jwt_required
    @api.expect(_tags)
    def delete(self, id):
        data = request.json
        return delete_network_tag(id, data)




