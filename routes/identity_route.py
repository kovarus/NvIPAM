# from run import api
from flask_restplus import Resource, Namespace, reqparse, fields
from models.identity_model import UserModel, RevokedTokenModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

api = Namespace('identity', description='identity related operations')

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

''' adding models for marshalling '''

class AuthDto:
    user_auth = api.model('user_details', {
        'username':fields.String(required=True, description="The username"),
        'password': fields.String(required=True, description='User password')
    })


''' 
Update - added default user in run.py (admin/VMware1!)
'''


@api.route('/login')
class UserLogin(Resource):
    @api.expect(AuthDto.user_auth)
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Wrong credentials'}


@api.route('/logout/access')
class UserLogoutAccess(Resource):
        @jwt_required
        def post(self):
            jti = get_raw_jwt()['jti']
            try:
                revoked_token = RevokedTokenModel(jti = jti)
                revoked_token.add()
                return {'message': 'Access token has been revoked'}
            except:
                return {'message': 'Something went wrong'}, 500


@api.route('/logout/refresh')
class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


@api.route('/token/refresh')
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}


''' sample protected route'''
#
#
# @api.route('/secret')
# class SecretResource(Resource):
#     @jwt_required
#     def get(self):
#         return {
#             'answer': 42
#         }
