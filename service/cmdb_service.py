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
from models.cmdb_model import CmdbData, CmdbSchema
from flask import jsonify


def save_new_ci(data):
    # see if the machine name already exists, add if not.

    ci = CmdbData.query.filter_by(machinename=data['machinename']).first()
    if not ci:
        new_assignment = CmdbData(
            id=None,
            machinename=data['machinename'],
            ipaddress=data['ipaddress'],
            network=data['network'],
            mem=data['mem'],
            cpus=data['cpus'],
            disk=data['disk'],
            os=data['os'],
            datacenter=data['datacenter'],
            owner=data['owner'],
            status=data['status']
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

    if data['owner'] != 'string':
        ci.owner = data['owner']

    if data['cpus'] != 0:
        ci.status = data['status']

    # print(output)
    db.session.commit()
    ci_schema = CmdbSchema()
    output = ci_schema.dump(ci).data
    #
    return output
