'''

BSD 3-Clause License

Copyright (c) 2019, Kovarus
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''

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


