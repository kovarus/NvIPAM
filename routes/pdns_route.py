from flask_restplus import Resource, Namespace, reqparse, fields
from service.pdns_service import get_a_domain, get_a_record, get_domains, get_records, add_a_domain, add_a_record, \
    update_a_domain, update_a_record, delete_a_record, find_a_domain, find_a_record
from flask_jwt_extended import jwt_required
from flask import request

api = Namespace('dns', description='DNS related operations')

''' adding models for marshalling '''
class DomainsDto:
    domains = api.model('dns_domains', {
        'id': fields.Integer(description='Domain unique id'),
        'name': fields.String(required=True, description='Domain name', default='corp.local'),
        'master': fields.String( description='Domain master'),
        'last_check': fields.Integer(description='Network subnet'),
        'type': fields.String(description='Domains Type'),
        'notified_serial': fields.Integer(description='Notified serial'),
        'account': fields.String(description='Account')
    })


class RecordsDto:
    records = api.model('dns_records', {
        'id': fields.Integer(description='Record unique id'),
        'domain_id': fields.Integer(required=True, description='Parent DNS Domain id'),
        'name': fields.String(required=True, description='Hostname'),
        'type': fields.String(required=True, description='Record type i.e., A, PTR, CNAME'),
        'content': fields.String(description='Content'),
        'ttl': fields.Integer(required=True, description='Record TTL', default=3600),
        'prio': fields.Integer(description='Priority'),
        'disabled': fields.Boolean(description='Is the record disabled?', default=False),
        'ordername': fields.String(description='Parent network name'),
        'auth': fields.Boolean(description='Auth')
    })



@api.route('/records')
class PdnsRecords(Resource):
    @api.marshal_list_with(RecordsDto.records, envelope='data')
    @jwt_required
    def get(self):
        """Get all DNS records"""
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='args', help='Record name')
        args = parser.parse_args()
        if args['name']:
            filter_by = args['name']
            print("Record filter_by " + filter_by)
            return find_a_record(filter_by)
        return get_records()

    @api.expect(RecordsDto.records)
    @jwt_required
    def post(self):
        """Add DNS record"""
        data = request.json
        return add_a_record(data)


@api.route('/records/<id>')
class PdnsRecord(Resource):
    @api.marshal_list_with(RecordsDto.records, envelope='data')
    @jwt_required
    def get(self, id):
        """Get DNS record by id"""
        return get_a_record(id)

    @api.expect(RecordsDto.records)
    @jwt_required
    def put(self, id):
        """Update DNS record by id"""
        data = request.json
        return update_a_record(id, data)

    @jwt_required
    def delete(self, id):
        """Delete DNS record"""
        # return {'DNS': 'Delete a DNS record by id'}
        return delete_a_record(id)

    ''' Commented some domain management out.  All the routes work. '''

@api.route('/domains')
class PdnsRecords(Resource):
    @api.marshal_list_with(DomainsDto.domains, envelope='data')
    # @jwt_required
    def get(self):
        """Get all DNS records"""
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='args', help='Domain name')
        args = parser.parse_args()
        if args['name']:
            filter_by = args['name']
            print("Domain filter_by " + filter_by)
            return find_a_domain(filter_by)
        return get_domains()

@api.route('/domains')
class PdnsRecords(Resource):
    @api.marshal_list_with(DomainsDto.domains, envelope='data')
    @jwt_required
    def get(self):
        """Get all DNS records"""
        return get_domains()

    @api.expect(DomainsDto.domains)
    @jwt_required
    def post(self):
        """Add DNS record"""
        data = request.json
        return add_a_domain(data)


@api.route('/domains/<id>')
class PdnsRecord(Resource):
    @api.marshal_list_with(DomainsDto.domains, envelope='data')
    @jwt_required
    def get(self, id):
        """Get DNS record by id"""
        return get_a_domain(id)

    @api.expect(DomainsDto.domains)
    @jwt_required
    def put(self, id):
        """Update DNS record by id"""
        data = request.json
        return update_a_domain(id, data)

    @jwt_required
    def delete(self, id):
        """Delete DNS record"""
        return {'DNS': 'Delete a DNS record by id'}

