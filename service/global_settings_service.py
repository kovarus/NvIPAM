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
from models.global_settings_model import GlobalSettings, GlobalSettingsSchema


def save_new_settings(data):
    _settings = GlobalSettings.query.first()

    if not _settings:
        new_settings = GlobalSettings(
            id=None,
            dns1=data['dns1'],
            dns2=data['dns2'],
            domainname=data['domainname']
        )
        save_changes(new_settings)

        response_object = {
            'status': 'success',
            'message': 'Successfully added.'
        }
        return response_object, 201

    else:
        response_object = {
            'status': 'fail',
            'message': 'Global settings not added.',
        }
        return response_object, 409


def get_all_settings():
    _settings = GlobalSettings.query.first()
    pool_schema = GlobalSettingsSchema()
    output = pool_schema.dump(_settings).data
    return output
    # return NetworkPools.query.all()


def update_a_setting(id, data):
    ''' update a setting '''
    _settings = GlobalSettings.query.first()
    if data['dns1'] != 'string':
        _settings.poolname = data['dns1']

    if data['dns2'] != 'string':
        _settings.poolname = data['dns2']

    if data['domainname'] != 'string':
        _settings.poolname = data['domainname']

    ''' apply the changes '''
    db.session.commit()
    setting_schema = GlobalSettingsSchema()
    output = setting_schema.dump(_settings).data
    return output
