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
from flask_restplus import Resource, Namespace, reqparse, fields
from flask import request
from flask_jwt_extended import jwt_required
from service.global_settings_service import get_all_settings, update_a_setting, save_new_settings

api = Namespace('settings', description='Global settings related operations')

''' adding models for marshalling '''


class GlobalSettingsDto:
    settings = api.model('global_settings_operations', {
        'id': fields.Integer(description='Unique id'),
        'dns1': fields.String(required=True, description='DNS 1 IP', default='8.8.8.8'),
        'dns2': fields.String(description='DNS 2 IP', default='8.8.4.4'),
        'domainname': fields.String(required=True, description='Domain name', default='corp.local')
    })


@api.route('/')
class SettingsList(Resource):
    @api.marshal_list_with(GlobalSettingsDto.settings, envelope='data')
    @jwt_required
    def get(self):
        """List all global settings"""
        return get_all_settings()

    @api.expect(GlobalSettingsDto.settings, validate=True)
    @jwt_required
    def post(self):
        """Creates a new global settings """
        data = request.json
        return save_new_settings(data=data)

    @api.expect(GlobalSettingsDto.settings, validate=True)
    @jwt_required
    def put(self, id):
        """Creates a new Configuration Item """
        data = request.json
        return update_a_setting(id=id, data=data)
