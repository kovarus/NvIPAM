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
    app.run(debug=True)
