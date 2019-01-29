from flask_restplus import Resource, Namespace, reqparse, fields
from service.network_pools_service import save_new_pool, get_all_pools, get_a_pool, update_a_pool, get_pool_tags, add_pool_tag, delete_pool_tag, get_first_free, claim_first_free
from routes.tags_route import TagsDto
from routes.ip_assignment_route import IpAddressDto
from routes.network_pool_route import NetworkPoolsDto
from flask_jwt_extended import jwt_required
from flask import request

api = Namespace('pools', description='Network pool related operations')

# api = NetworkPoolsDto.api

_pool = NetworkPoolsDto.pool
_tags = TagsDto.tags
_assignments = IpAddressDto.assignment

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
#
#
# # api = NetworkPoolsDto.api
#
# _pool = NetworkPoolsDto.pool
# _tags = TagsDto.tags
# _assignments = IpAddressDto.assignment
#
#
# @api.route('/')
# class PoolsList(Resource):
#     @api.doc('list_of_pools')
#     @jwt_required
#     # @api.marshal_list_with(_pool, envelope='data')
#     # @api.response(401, 'Provide a valid token')
#     # @token_required
#     def get(self):
#         """List all pools"""
#         return get_all_pools()
#
#     @api.doc('create a new pool')
#     @api.expect(_pool, validate=True)
#     # @token_required
#     def post(self):
#         """Creates a new network pool """
#         data = request.json
#         return save_new_pool(data=data)
#
#
# @api.route('/<id>')
# class PoolDetails(Resource):
#     @jwt_required
#     @api.doc('get a pool')
#     def get(self, id):
#         """Get a network pool given its identifier"""
#         pool = get_a_pool(id)
#         if not pool:
#             api.abort(404)
#         else:
#             return pool
#
#     @api.doc('update a Network')
#     @api.expect(_pool, validate=True)
#     @jwt_required
#     def put(self, id):
#         """Creates a new Configuration Item """
#         data = request.json
#         return update_a_pool(id=id, data=data)
#
#
# @api.route('/<id>/tags')
# @api.param('id', 'The Pool identifier')
# class PoolTags(Resource):
#     @api.doc('get pool tags')
#     @jwt_required
#     def get(self, id):
#         """Get a pool tags given its identifier"""
#         tags = get_pool_tags(id)
#         if not tags:
#             api.abort(404)
#         else:
#             return get_pool_tags(id)
#
#     @api.doc('update a pool tag')
#     @api.expect(_tags, validate=True)
#     @jwt_required
#     def post(self, id):
#         """Updates a Pool Tag """
#         data = request.json
#         return add_pool_tag(id, data)
#
#     @api.doc('update a Pool')
#     @api.expect(_tags, validate=True)
#     @api.response(401, 'Provide a valid token')
#     @jwt_required
#     def delete(self, id):
#         """Updates a Network Tag """
#         data = request.json
#         return delete_pool_tag(id, data)
#
#
# @api.route('/getfirstfree/<pool_id>')
# class GetFirstFree(Resource):
#     @api.doc('get first free based on pool id')
#     @jwt_required
#     def get(self, pool_id):
#         """Get a first free from pool by id"""
#         firstFree = get_first_free(pool_id)
#         if not firstFree:
#             api.abort(404)
#         else:
#             return get_first_free(pool_id)
#
#     @api.expect(_assignments, validate=True)
#     @jwt_required
#     def post(self, pool_id):
#         """Claim the first free from the pool by pool id"""
#         data = request.json
#         firstFree = get_first_free(pool_id)
#         if not firstFree:
#             api.abort(404)
#         else:
#             return claim_first_free(pool_id, data)
#
