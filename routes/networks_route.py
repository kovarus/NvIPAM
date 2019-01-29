# from run import api
from flask_restplus import Resource, Namespace, reqparse, fields
from service.networks_service import save_new_network, get_all_networks, get_a_network, update_a_network, \
    get_network_tags, add_network_tag, delete_network_tag
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
        return get_all_networks()

    @jwt_required
    @api.expect(NetworksDto.network)
    def post(self):
        data = request.json
        return save_new_network(data)


@api.route('/<id>')
class GetNetwork(Resource):
    @jwt_required
    def get(self, id):
        return get_a_network(id)

    @jwt_required
    @api.expect(NetworksDto.network)
    def put(self,id):
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




