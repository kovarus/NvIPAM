from run import db
from utils import save_changes
from models.network_model import Networks, NetworkPools, PoolAssignmentsSchema, PoolAssignments, PoolsSchema, TagsSchema
from routes.tags_route import TagsDto
from routes.network_pool_route import NetworkPoolsDto

from flask import jsonify
import ipaddress

_pool = NetworkPoolsDto.pool
_tags = TagsDto.tags


''' Automatically populate the pool assignment table when adding the pool '''
class PopulateAssignmentTable:
    def __init__(self, iprange, pool, gateway):

        for n in ipaddress.ip_network(iprange).hosts():
            address = str(n)
            if address == gateway:
                new_host = PoolAssignments(ipaddress=address, machinename='Gateway', status=3, rangeid=pool.id)
            else:
                new_host = PoolAssignments(ipaddress=address, rangeid=pool.id)
            ''' add to db and commit '''
            updateDatabase(new_host)
            # db.session.add(new_host)
            # db.session.commit()

class updateDatabase:
    def __init__(self, item):
        self.item = item
        self.updatedItem = db.session.add(item)
        self.completeUpdate = db.session.commit()


def updatePoolname(owner_id, poolname):
    ''' prepend networkname to poolname '''
    networkname = Networks.query.filter_by(id=owner_id).first().networkname
    # print('update ' + networkname + '~' + poolname)
    return networkname + '~' + poolname


def save_new_pool(data):
    net = Networks.query.filter_by(id=data['owner_id']).first()
    pool = NetworkPools.query.filter_by(poolname=net.networkname + '~' + data['poolname']).first()
    ''' TODO: need to only allow the subnet range to be added to a network one time '''

    ''' could figure out gateway using ipaddress.ip_networks().netmask'''
    print(net.networkname)
    if not pool:
        ''' get global settings '''
        _globalSettings = GlobalSettings.query.first()
        ''' prepend the network to the poolname '''
        newPoolname = updatePoolname(net.id, data['poolname'])
        # print(newPoolname)
        # print(_globalSettings)
        ''' use global defaults if not set in data '''
        if data['dns1'] == 'string':
            dns1 = _globalSettings.dns1
        else:
            dns1 = data['dns1']

        if data['dns2'] == 'string':
            dns2 = _globalSettings.dns2
        else:
            dns2 = data['dns2']

        if data['domainname'] == 'string':
            domainname = _globalSettings.domainname
        else:
            domainname = data['domainname']

        new_pool = NetworkPools(
            id=None,
            poolname=newPoolname,
            poolrange=data['poolrange'],
            subnetmask=data['subnetmask'],
            gateway=data['gateway'],
            dns1=dns1,
            dns2=dns2,
            domainname=domainname,
            owner_id=net.id

        )
        save_changes(new_pool)
        ''' populate the assignments table '''
        result = PopulateAssignmentTable(iprange=data['poolrange'], pool=new_pool, gateway=data['gateway'])

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


def get_all_pools():
    _pool = NetworkPools.query.all()
    # parser = reqparse.RequestParser()
    # parser.add_argument('filter', help='Filter using sql where commands')
    # args = parser.parse_args()
    # if args['filter']:
    #     print(args['filter'])
    #     filter_by = args['filter']
    #     print(filter_by)
    #     return NetworkPools.query.filter(filter_by).all()

    pool_schema = PoolsSchema(many=True)
    output = pool_schema.dump(_pool).data
    # print(output)
    return jsonify({'data': output})


def get_a_pool(id):
    pool = NetworkPools.query.filter_by(id=id).first()
    pool_schema = PoolsSchema()
    output = pool_schema.dump(pool).data
    return jsonify({'data': output})


def update_a_pool(id, data):
    ''' update a pool item '''
    _pool = NetworkPools.query.get(id)
    if data['poolname'] != 'string':
        _pool.poolname = data['poolname']

    ''' apply the changes '''
    db.session.commit()
    pool_schema = PoolsSchema()
    output = pool_schema.dump(_pool).data
    return jsonify({'data': output})


def get_pool_tags(id):
    pool = NetworkPools.query.filter_by(id=id).first()
    tags = pool.pool_tag
    pool_schema = TagsSchema(many=True)
    output = pool_schema.dump(tags).data
    return jsonify({'data': output})


def add_pool_tag(id, data):
    pool = NetworkPools.query.get(id)
    tag = Tags.query.get(data['tag_id'])
    pool.pool_tag.append(tag)
    net_schema=TagsSchema()
    output = net_schema.dump(pool).data
    db.session.commit()
    return jsonify({'data': output})


def delete_pool_tag(id, data):
    pool = NetworkPools.query.get(id)
    tag = Tags.query.get(data['tag_id'])
    pool.pool_tag.remove(tag)
    pool_schema=PoolsSchema()
    output = pool_schema.dump(pool).data
    db.session.commit()
    return jsonify({'data': output})


''' add get first by pool id (rangeid)'''
def get_first_free(rangeid):
    firstFree = PoolAssignments.query.filter_by(rangeid=rangeid, status='0').first()
    firstFreeSchema=PoolAssignmentsSchema()
    output = firstFreeSchema.dump(firstFree).data
    return jsonify({'data': output})


def claim_first_free(rangeid, data):
    firstFree = PoolAssignments.query.filter_by(rangeid=rangeid, status='0').first()
    if data['machinename'] != 'string':
        firstFree.machinename = data['machinename']
        ''' set to assigned '''
        firstFree.status = '1'
    else:
        response_object = {
            'status': 'fail',
            'message': 'Machine name must be set.',
        }
        return response_object, 409

    ''' apply the changes '''
    db.session.commit()
    firstFreeSchema=PoolAssignmentsSchema()
    output = firstFreeSchema.dump(firstFree).data
    return jsonify({'data': output})

