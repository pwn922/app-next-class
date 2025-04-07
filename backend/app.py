from flask import Flask
from flasgger import Swagger
from flask_restful import Api
from resources.login import LoginCallbackResource, LoginResource
from resources.logout import LogoutResource
from resources.user import UserResource
from flask_migrate import Migrate
from config.config import ConfigFlask
from database.db import db
from flask_cors import CORS
import os

from auth import jwt_auth

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.config.from_object(ConfigFlask)
db.init_app(app)
jwt_auth.init_jwt(app)

CORS(app, origins=[
    'https://accounts.google.com',
    'https://accounts.google.com/o/oauth2/v2/auth',
    'https://oauth2.googleapis.com',
    'https://oauth2.googleapis.com/device/code',
    'https://openidconnect.googleapis.com',
    'https://openidconnect.googleapis.com/v1/userinfo',
    'https://www.googleapis.com',
    'https://oauth2.googleapis.com/revoke'
])
migrate = Migrate(app, db)
api = Api(app, prefix='/api/v1')

api.add_resource(UserResource, '/users/<uuid:user_id>', endpoint='users')
api.add_resource(LoginResource, '/login')
api.add_resource(LoginCallbackResource, '/login/callback', endpoint='callback')
api.add_resource(LogoutResource, '/logout')
#api.add_resource(RefreshTokenResource, '/refresh-token')

#api.add_resource(UserListResource, '/users')

from models.user import User
from models.classroom import Classroom
from models.token_blocklist import TokenBlocklist

swagger = Swagger(app, template=app.config.get('SWAGGER_TEMPLATE'))

if __name__ == '__main__':
    print("DEBUG: ", app.config.get('DEBUG'))
    app.run(host='0.0.0.0', debug=app.config.get('DEBUG'))