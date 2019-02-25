''' using sqlalchemy.  Will need to modify the queries to get the data.'''
from run import db
from utils import save_changes
from models.pdns_model import Domains, DomainsSchema, Records, RecordsSchema
from flask import jsonify
from sqlalchemy import text


def get_domains():
    # myDomains = Domains.query.all()
    # Above didn't work
    myDomains = db.session.query(Domains).all()
    domains_schema = DomainsSchema(many=True)
    output = domains_schema.dump(myDomains).data
    return output

def find_a_domain(filter_by):
    # return PoolAssignments.query.filter(filter_by).all
    print("Filter_by is" + filter_by)
    domain = db.session.query(Domains).filter_by(name=text(filter_by)).first()
    domain_schema = DomainsSchema()
    output = domain_schema.dump(domain).data
    return output


def get_a_domain(id):
    # domain = Domains.query.get(id)
    # domain = db.session.query(Domains).get(id)
    domain = db.session.query(Domains).filter_by(id=id)
    domains_schema = DomainsSchema(many=True)
    output = domains_schema.dump(domain).data
    return output


def update_a_domain(id, data):
    ''' update an IP assignment item '''
    # domain = db.session.query(Domains).get(id)
    domain = db.session.query(Domains).filter_by(id=id).first()

    if data['name'] != 'string':
        domain.name = data['name']

    ''' apply the changes '''
    db.session.commit()
    net_schema = DomainsSchema()
    output = net_schema.dump(domain).data
    return output


def add_a_domain(data):
    domain = db.session.query(Domains).filter_by(name=data['name']).first()
    if not domain:
        new_assignment = Domains(
            id=None,
            name=data['name'],
            master='not set',
            last_check=1,
            type=data['type'],
            notified_serial=1,
            account='not set'
        )
        save_changes(new_assignment)
        response_object = {
            'status': 'success',
            'message': 'Successfully added.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Domain already already exists.',
        }
        return response_object, 409



def get_records():
    # myRecords = Records.query.all()
    myRecords = db.session.query(Records).all()
    records_schema = RecordsSchema(many=True)
    output = records_schema.dump(myRecords).data
    return output


def get_a_record(id):
    record = db.session.query(Records).filter_by(id=id)
    records_schema = RecordsSchema(many=True)
    output = records_schema.dump(record).data
    return output


def add_a_record(data):
    record = db.session.query(Records).filter_by(name=data['name']).first()
    if not record:
        if data['ttl'] == 0:
            ttl = 3600
        else:
            ttl = data['ttl']

        new_assignment = Records(
            id=None,
            domain_id=data['domain_id'],
            name=data['name'],
            type=data['type'],
            content=data['content'],
            ttl=ttl,
            prio=data['prio'],
            disabled=data['disabled'],
            auth=data['auth']
        )
        save_changes(new_assignment)
        response_object = {
            'status': 'success',
            'message': 'Successfully added.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Record already exists.',
        }
        return response_object, 409


def delete_a_record(id):
    record = db.session.query(Records).get(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({'data': 'Record deleted'})


def update_a_record(id, data):
    # ''' update an IP assignment item '''
    # assignment = PoolAssignments.query.get(id)
    #
    # if data['machinename'] != 'string':
    #     assignment.machinename = data['machinename']
    #
    # ''' 0 - unused, 1 - reserved, 2 - used, 3 - gateway'''
    # if data['status'] == 0:
    #     assignment.status = data['status']
    #     ''' delete the hostname if setting to unused '''
    #     assignment.machinename = 'string'
    # else:
    #     assignment.status = data['status']
    #
    # ''' apply the changes '''
    # db.session.commit()
    # net_schema = PoolAssignmentsSchema()
    # output = net_schema.dump(assignment).data
    # return output
    return jsonify({'Update': 'DNS record in progress'})



def find_a_record(filter_by):
    # return PoolAssignments.query.filter(filter_by).all
    print("Filter_by is" + filter_by)
    record = db.session.query(Records).filter_by(name=text(filter_by)).first()
    record_schema = RecordsSchema()
    output = record_schema.dump(record).data
    return output
