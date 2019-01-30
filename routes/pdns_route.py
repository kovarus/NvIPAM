from flask_restplus import Resource, Namespace, reqparse, fields
from service.pdns_service import GetRecords, GetDomains
from flask_jwt_extended import jwt_required

api = Namespace('dns', description='DNS related operations')


''' adding models for marshalling '''


@api.route('/records')
class PdnsRecords(Resource):
    #@ api.expect(AuthDto.user_auth)
    @jwt_required
    def get(self):
        """Get all DNS records"""
        return GetRecords()

    @jwt_required
    def post(self):
        """Add DNS record"""
        return {'DNS': 'Add DNS Record'}


@api.route('/records/<id>')
class PdnsRecord(Resource):
    @jwt_required
    def get(self, id):
        """Get DNS record by id"""
        return {'DNS': 'Get DNS record by id'}

    @jwt_required
    def put(self, id):
        """Update DNS record by id"""
        return {'DNS': 'Update a DNS record by id'}

    @jwt_required
    def delete(self, id):
        """Delete DNS record"""
        return {'DNS': 'Delete a DNS record by id'}

@api.route('/domains')
class PdnsRecords(Resource):
    #@ api.expect(AuthDto.user_auth)
    @jwt_required
    def get(self):
        """Get all DNS records"""
        return GetDomains()

    @jwt_required
    def post(self):
        """Add DNS record"""
        return {'DNS': 'Add DNS Record'}


@api.route('/domains/<id>')
class PdnsRecord(Resource):
    @jwt_required
    def get(self, id):
        """Get DNS record by id"""
        return {'DNS': 'Get DNS record by id'}

    @jwt_required
    def put(self, id):
        """Update DNS record by id"""
        return {'DNS': 'Update a DNS record by id'}

    @jwt_required
    def delete(self, id):
        """Delete DNS record"""
        return {'DNS': 'Delete a DNS record by id'}

