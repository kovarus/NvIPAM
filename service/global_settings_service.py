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
