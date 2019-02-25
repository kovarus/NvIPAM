from flask_restplus import Resource, Namespace, reqparse, fields
from flask_jwt_extended import jwt_required
from service.ip_assignment_service import save_new_assignment, get_assignment_tags, get_an_assignment, get_all_assignments, delete_assignment_tag \
    , add_assignment_tag, update_an_assignent, find_an_assignment
from flask import request
from routes.tags_route import TagsDto

api = Namespace('ip_assignment', description='IP assignment related operations')

_tags = TagsDto.tags


''' adding models for marshalling '''


class IpAddressDto:
    assignment = api.model('pool_assignments', {
        'id': fields.Integer(description='Assignment unique id'),
        'ipaddress': fields.String(description='Machine IP address', required=True),
        'machinename': fields.String(required=True, description='Machine name'),
        'status': fields.Integer(description='Machine status.  0 - unused, 1 - assigned, 2 - reserved, 3 - gateway'),
        'rangeid': fields.Integer(description='Parent pool id')
    })


@api.route('/')
class GetAssignments(Resource):
    @jwt_required
    def get(self):
        """Get all IP assignments"""
        parser = reqparse.RequestParser()
        parser.add_argument('ipaddress', type=str, location='args', help='Machine ipaddress')
        args = parser.parse_args()
        if args['ipaddress']:
            filter_by = args['ipaddress']
            print("Route filter_by " + filter_by)
            return find_an_assignment(filter_by)
        return get_all_assignments()


''' Not sure if this fits.  All addresses automatically added when you create the pool '''
    # @jwt_required
    # @api.expect(IpAddressDto.assignment)
    # def post(self):
    #     """Add new IP assignment"""
    #     data = request.json
    #     return save_new_assignment(data)


@api.route('/<id>')
class GetIpAssignment(Resource):
    @jwt_required
    def get(self, id):
        """Get IP assignment by id"""
        return get_an_assignment(id)

    @jwt_required
    @api.expect(IpAddressDto.assignment)
    def put(self,id):
        """Update ip assignment by ip"""
        data = request.json
        return update_an_assignent(id, data)


@api.route('/<id>/tags')
class AssignmentTags(Resource):
    @jwt_required
    def get(self, id):
        """Get a address tags given its identifier"""
        return get_assignment_tags(id)

    @api.expect(_tags, validate=True)
    @jwt_required
    def post(self, id):
        """Updates a address Tag """
        data = request.json
        return add_assignment_tag(id, data)

    @api.expect(_tags, validate=True)
    @jwt_required
    def delete(self, id):
        """Updates an IP assignment Tag """
        data = request.json
        return delete_assignment_tag(id=id, data=data)



