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

from flask import Flask, Blueprint
from flask_restplus import Api, Namespace
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
# import time
import datetime

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api/1.0')
api = Api(blueprint)
app.register_blueprint(blueprint)


''' Will need to use Postgres if you want to save arrays (disks, nics, etc) '''

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nvipam:VMware1!@localhost/nvipam'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'
app.config['ADMIN_PASSWORD'] = 'VMware1!'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

app.url_map.strict_slashes = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


jwt = JWTManager(app)

jwt._set_error_handler_callbacks(api)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return identity_ns.RevokedTokenModel.is_jti_blacklisted(jti)


@app.before_first_request
def create_tables():
    db.create_all()
    ''' Add default user account'''
    existingUser = identity_model.UserModel.find_by_username('admin')
    if not existingUser:
        new_user = identity_model.UserModel(
            username = 'admin',
            password = identity_model.UserModel.generate_hash('VMware1!')
        )
        new_user.save_to_db()
    '''
            new_user = UserModel(
            username = data['username'],
            password = UserModel.generate_hash(data['password'])
        )

        try:
            new_user.save_to_db()
    '''


from models import identity_model
from routes.pdns_route import api as pdns_ns
from routes.cmdb_route import api as cmdb_ns
from routes.ip_assignment_route import api as assignment_ns
from routes.identity_route import api as identity_ns
from routes.global_settings_route import api as settings_ns
from routes.tags_route import api as tags_ns
from routes.networks_route import api as networks_ns
from routes.networks_pools_route import api as network_pools_ns


api.add_namespace(cmdb_ns)
api.add_namespace(pdns_ns)
api.add_namespace(identity_ns)
api.add_namespace(assignment_ns)
api.add_namespace(networks_ns)
api.add_namespace(network_pools_ns)
api.add_namespace(settings_ns)
api.add_namespace(tags_ns)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
