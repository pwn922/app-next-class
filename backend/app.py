from flask import Flask
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_migrate import Migrate
from flask_cors import CORS
import os

from config.config import ConfigFlask
from database.db import db, init_db
from auth.jwt_auth import init_jwt

from resources.login import LoginResource
from resources.register import RegisterResource
from resources.logout import LogoutResource
from resources.schedules import ScheduleResource, ScheduleListResource
from resources.pavilion import PavilionByNameResource, PavilionResource, PavilionListResource
from resources.user import UserListResource, UserResource
# from resources.classroom import ClassroomResource, ClassroomListResource
# from resources.subject import SubjectResource, SubjectListResource

from models.pavilion import Pavilion
# from models.classroom import Classroom
from models.user import User
from models.schedule import Schedule
# from models.subject import Subject
from models.token_blocklist import TokenBlocklist

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

def create_app(testing=False):
    app = Flask(__name__)
    app.config.from_object(ConfigFlask)

    if testing:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['JWT_SECRET_KEY'] = 'testing-secret-key'

    init_db(app)
    init_jwt(app)
    JWTManager(app)

    CORS(app, origins=[
        'https://accounts.google.com',
        'https://accounts.google.com/o/oauth2/v2/auth',
        'https://oauth2.googleapis.com',
        'https://oauth2.googleapis.com/device/code',
        'https://openidconnect.googleapis.com',
        'https://openidconnect.googleapis.com/v1/userinfo',
        'https://www.googleapis.com',
        'https://oauth2.googleapis.com/revoke',
    ])

    Migrate(app, db)

    api = Api(app, prefix='/api/v1')

    api.add_resource(LoginResource, '/login')
    api.add_resource(RegisterResource, '/register')
    api.add_resource(LogoutResource, '/logout')
    api.add_resource(ScheduleResource, '/user/schedules/<uuid:id>')
    api.add_resource(ScheduleListResource, '/user/schedules/')
    api.add_resource(UserResource, '/user')
    api.add_resource(UserListResource, '/users/')
    api.add_resource(PavilionListResource, '/pavilions/')
    api.add_resource(PavilionResource, '/pavilions/<uuid:id>', endpoint='pavilions')
    api.add_resource(PavilionByNameResource, '/pavilions/<string:name>')

    Swagger(app, template=app.config.get('SWAGGER_TEMPLATE'))

    return app

if __name__ == '__main__':
    app = create_app()
    print("DEBUG: ", app.config.get('DEBUG'))
    app.run(host='0.0.0.0', debug=app.config.get('DEBUG'))
