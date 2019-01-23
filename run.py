from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


app = Flask(__name__)
api = Api(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'
app.config['ADMIN_PASSWORD'] = 'VMware1!'

db = SQLAlchemy(app)

jwt = JWTManager(app)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return identity_ns.RevokedTokenModel.is_jti_blacklisted(jti)


@app.before_first_request
def create_tables():
    db.create_all()
    ''' Add default user account'''
    existingUser = models.UserModel.find_by_username('admin')
    if not existingUser:
        new_user = models.UserModel(
            username = 'admin',
            password = models.UserModel.generate_hash('VMware1!')
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

import models
from apis.identity import api as identity_ns

api.add_namespace(identity_ns)


if __name__ == '__main__':
    app.run(debug=True)
