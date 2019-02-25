from run import db
from utils import save_changes
from models.network_model import Tags, TagsSchema, PoolAssignmentsSchema, PoolAssignments
from flask import jsonify
from sqlalchemy import text


def save_new_assignment(data):
    # see if the machine name already exists, add if not.

    assignment = PoolAssignments.query.filter_by(machinename=data['machinename']).first()
    if not assignment:
        new_assignment = PoolAssignments(
            id=data['id'],
            machinename=data['machinename'],
            status=data['status'],
            ipaddress=data['ipaddress']
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
            'message': 'Network pool already exists.',
        }
        return response_object, 409


def get_all_assignments():
    # parser = reqparse.RequestParser()
    # parser.add_argument('filter', help='Filter using sql where commands')
    # args = parser.parse_args()
    # if args['filter']:
    #     print(args['filter'])
    #     filter_by = args['filter']
    #     print(filter_by)
    #     return PoolAssignments.query.filter(filter_by).all()
    ips = PoolAssignments.query.all()
    ip_schema = PoolAssignmentsSchema(many=True)
    output = ip_schema.dump(ips).data
    return output


def get_an_assignment(id):
    pool = PoolAssignments.query.filter_by(id=id).first()
    pool_schema = PoolAssignmentsSchema()
    output = pool_schema.dump(pool).data
    return output

def find_an_assignment(filter_by):
    # return PoolAssignments.query.filter(filter_by).all
    print("Filter_by is" + filter_by)
    machine = PoolAssignments.query.filter_by(ipaddress=text(filter_by)).first()
    machine_schema = PoolAssignmentsSchema()
    output = machine_schema.dump(machine).data
    return output


def update_an_assignent(id, data):
    ''' update an IP assignment item '''
    assignment = PoolAssignments.query.get(id)

    if data['machinename'] != 'string':
        assignment.machinename = data['machinename']

    ''' 0 - unused, 1 - reserved, 2 - used, 3 - gateway'''
    if data['status'] == 0:
        assignment.status = data['status']
        ''' delete the hostname if setting to unused '''
        assignment.machinename = 'string'
    else:
        assignment.status = data['status']

    ''' apply the changes '''
    db.session.commit()
    net_schema = PoolAssignmentsSchema()
    output = net_schema.dump(assignment).data
    return output


def get_assignment_tags(id):
    assignment = PoolAssignments.query.filter_by(id=id).first()
    tags = assignment.assignment_tag
    assignment_schema = TagsSchema(many=True)
    output = assignment_schema.dump(tags).data
    return output


def add_assignment_tag(id, data):
    assignment = PoolAssignments.query.get(id)
    tag = Tags.query.get(data['tag_id'])
    assignment.assignment_tag.append(tag)
    assignment_schema=TagsSchema()
    output = assignment_schema.dump(assignment).data
    db.session.commit()
    return output


def delete_assignment_tag(id, data):
    assignment = PoolAssignments.query.get(id)
    tag = Tags.query.get(data['tag_id'])
    assignment.assignment_tag.remove(tag)
    assignment_schema=PoolAssignmentsSchema()
    output = assignment_schema.dump(assignment).data
    db.session.commit()
    return output

