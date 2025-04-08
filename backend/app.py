from flask import Flask
from flasgger import Swagger
from flask_restful import Api
from resources.login import LoginCallbackResource, LoginResource
from resources.user import UserListResource, UserResource
from resources.pavilion import PavilionResource, PavilionListResource
from resources.classroom import ClassroomResource, ClassroomListResource
from resources.subject import SubjectResource, SubjectListResource
from resources.schedules import ScheduleResource, ScheduleListResource
from resources.logout import LogoutResource
from resources.user import UserResource
from flask_migrate import Migrate
from config.config import ConfigFlask
from database.db import db, init_db
from flask_cors import CORS
import os

from auth.jwt_auth import init_jwt

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.config.from_object(ConfigFlask)
init_db(app)
init_jwt(app)

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
api.add_resource(UserListResource, '/users/')
api.add_resource(LoginResource, '/login')
api.add_resource(LoginCallbackResource, '/login/callback', endpoint='callback')
api.add_resource(LogoutResource, '/logout')
#api.add_resource(RefreshTokenResource, '/refresh-token')

api.add_resource(PavilionListResource, '/pavilions/')
api.add_resource(PavilionResource, '/pavilions/<uuid:id>', endpoint='pavilions')
api.add_resource(ClassroomListResource, '/classrooms/')
api.add_resource(ClassroomResource, '/classrooms/<uuid:id>', endpoint='classrooms')
api.add_resource(SubjectListResource, '/subjects/')
api.add_resource(SubjectResource, '/subjects/<uuid:id>', endpoint='subjects')
api.add_resource(ScheduleResource, '/schedules/<uuid:schedule_id>', endpoint='schedules')
api.add_resource(ScheduleListResource, '/schedules/')

#api.add_resource(UserListResource, '/users')

from models.pavilion import Pavilion
from models.classroom import Classroom
from models.user import User
from models.schedule import Schedule  
from models.subject import Subject
from models.token_blocklist import TokenBlocklist

swagger = Swagger(app, template=app.config.get('SWAGGER_TEMPLATE'))

if __name__ == '__main__':
    print("DEBUG: ", app.config.get('DEBUG'))
    app.run(host='0.0.0.0', debug=app.config.get('DEBUG'))