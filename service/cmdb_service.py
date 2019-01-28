from run import db
from utils import save_changes
from models.cmdb_model import CmdbData, CmdbSchema
from flask import jsonify


def save_new_ci(data):
    # see if the machine name already exists, add if not.

    ci = CmdbData.query.filter_by(machinename=data['machinename']).first()
    if not ci:
        new_assignment = CmdbData(
            id=data['id'],
            machinename=data['machinename'],
            ipaddress=data['ipaddress'],
            network=data['network'],
            mem=data['mem'],
            cpus=data['cpus'],
            disk=data['disk'],
            os=data['os'],
            datacenter=data['datacenter']
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
            'message': 'CI already exists.',
        }
        return response_object, 409


def get_all_cis():
    # parser = reqparse.RequestParser()
    # parser.add_argument('filter', help='Filter using sql where commands')
    # args = parser.parse_args()
    # if args['filter']:
    #     print(args['filter'])
    #     filter_by = args['filter']
    #     print(filter_by)
    #     return CmdbData.query.filter(filter_by).all()
    return CmdbData.query.all()


def get_a_ci(id):
    return CmdbData.query.filter_by(id=id).first()


def update_a_ci(id, data):
    ci = CmdbData.query.get(id)
    print(data)

    ''' Only update changed fields '''
    if data['machinename'] != 'string':
        ci.machinename = data['machinename']

    if data['ipaddress'] != 'string':
        ci.ipaddress = data['ipaddress']

    if data['network'] != 'string':
        ci.network = data['network']

    if data['datacenter'] != 'string':
        ci.datacenter = data['datacenter']

    if data['os'] != 'string':
        ci.os = data['os']

    if data['mem'] != 0:
        ci.mem = data['mem']

    if data['disk'] != 0:
        ci.disk = data['disk']

    if data['cpus'] != 0:
        ci.disk = data['disk']

    # print(output)
    db.session.commit()
    ci_schema = CmdbSchema()
    output = ci_schema.dump(ci).data
    #
    return jsonify({'data': output})
