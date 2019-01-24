# from run import api
from flask_restplus import Resource, Namespace, reqparse, fields
from models.identity_model import UserModel, RevokedTokenModel
from flask_jwt_extended import jwt_required

api = Namespace('tags', description='Tags related operations')

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

''' adding models for marshalling '''


class TagsDto:
    tags = api.model('tag_operations', {
        'tag_id': fields.Integer(description='Unique tag id'),
        'name': fields.String(description='Tag name')
    })


@api.route('/')
class GetTags(Resource):
    @jwt_required
    def get(self):
        return {'Tags': 'Get all tags'}

    @jwt_required
    @api.expect(TagsDto.tags)
    def post(self):
        return {'Tags': 'Add Tag'}


@api.route('/<id>')
class GetTag(Resource):
    @jwt_required
    def get(self, id):
        return {'Tag': 'Get tag by id'}

    @jwt_required
    @api.expect(TagsDto.tags)
    def put(self,id):
        return {'Tag': 'Update a tag by id'}

    @jwt_required
    def delete(self,id):
        return {'Tag': 'Delete a tag by id'}




