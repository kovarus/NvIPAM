from run import db
from utils import save_changes
from models.network_model import Networks, NetworksSchema, Tags, TagsSchema
from flask import jsonify

def save_new_network(data):
    network = Networks.query.filter_by(key=data['key']).first()
    if not network:
        new_network = Networks(
            id=None,
            key=data['key'],
            networkname=data['networkname'],
            vlanid=data['vlanid'],
            datacenter=data['datacenter'],
            cluster=data['cluster']
        )
        save_changes(new_network)
        response_object = {
            'status': 'success',
            'message': 'Successfully added.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Network already exists. Please Log in.',
        }
        return response_object, 409


def get_all_networks():
    # parser = reqparse.RequestParser()
    # parser.add_argument('filter', help='Filter using sql where commands')
    # args = parser.parse_args()
    # if args['filter']:
    #     print(args['filter'])
    #     filter_by = args['filter']
    #     print(filter_by)
    #     return Networks.query.filter(filter_by).all()


    # return Networks.query.all()
    # network =  Networks.query.filter_by(id=id).first()
    network = Networks.query.all()
    net_schema = NetworksSchema(many=True)
    output = net_schema.dump(network).data
    # print(output)
    return jsonify({'data': output})


def get_a_network(id):
    network = Networks.query.filter_by(id=id).first()
    net_schema = NetworksSchema()
    output = net_schema.dump(network).data
    print(output)
    return jsonify({'data': output})

    # return Networks.query.filter_by(id=id).first()


def update_a_network(id, data):
    ''' update a network item '''
    net = Networks.query.get(id)
    if data['key'] != 'string':
        net.key = data['key']

    if data['networkname'] != 'string':
        net.networkname = data['networkname']

    if data['vlanid'] != 'string':
        net.vlanid = data['vlanid']

    if data['datacenter'] != 'string':
        net.datacenter = data['datacenter']

    if data['cluster'] != 'string':
        net.cluster = data['cluster']

    ''' apply the changes '''
    db.session.commit()
    net_schema = NetworksSchema()
    output = net_schema.dump(net).data
    return jsonify({'data': output})


def get_network_tags(id):
    network = Networks.query.filter_by(id=id).first()
    tags = network.network_tag
    net_schema = TagsSchema(many=True)
    output = net_schema.dump(tags).data
    return jsonify({'data': output})


def add_network_tag(id, data):
    net = Networks.query.get(id)
    tag = Tags.query.get(data['tag_id'])
    net.network_tag.append(tag)
    net_schema=NetworksSchema()
    output = net_schema.dump(net).data
    db.session.commit()
    return jsonify({'data': output})


def delete_network_tag(id, data):
    net = Networks.query.get(id)
    tag = Tags.query.get(data['tag_id'])
    # net.network_tag.delete(tag, synchronize_session=False)
    net.network_tag.remove(tag)
    net_schema=NetworksSchema()
    output = net_schema.dump(net).data
    db.session.commit()
    return jsonify({'data': output})


def get_first_free(net_id, pool_id):
    ''' need to return ip, mask, gateway, dns1, dns2, and domainname '''
    return jsonify({'in': 'progress'})


def claim_first_free(net_id, pool_id):
    return jsonify({'in': 'progress'})
