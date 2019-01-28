'''
Routes for tagging service
'''
from flask import request
from service.tags_service import save_new_tag, get_all_tags, get_a_tag, update_a_tag, delete_tag
from models.network_model import TagsSchema, Tags
from flask_restplus import Resource, Namespace, reqparse, fields
from flask_jwt_extended import jwt_required

api = Namespace('tags', description='Tags related operations')


''' adding models for marshalling '''


class TagsDto:
    tags = api.model('tag_operations', {
        'tag_id': fields.Integer(description='Unique tag id'),
        'name': fields.String(description='Tag name')
    })


@api.route('/')
class GetTags(Resource):
    @jwt_required
    @api.marshal_list_with(TagsDto.tags, envelope='data')
    def get(self):
        return Tags.query.all()

    @jwt_required
    @api.expect(TagsDto.tags)
    def post(self):
        """Creates a new tag """
        data = request.json
        return save_new_tag(data=data)


@api.route('/<id>')
class GetTag(Resource):
    @jwt_required
    @api.marshal_list_with(TagsDto.tags, envelope='data')
    def get(self, id):
        return get_a_tag(id)

    @jwt_required
    @api.expect(TagsDto.tags)
    def put(self, id):
        data = request.json
        return update_a_tag(id, data)

    @jwt_required
    def delete(self, id):
        return delete_tag(id)




