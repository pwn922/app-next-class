from flask import Flask
from flasgger import Swagger
from flask_restful import Api
from resources.login import LoginCallbackResource, LoginResource
from resources.user import UserListResource, UserResource
from resources.pavilion import PavilionResource, PavilionListResource
from resources.classroom import ClassroomResource, ClassroomListResource
from resources.subject import SubjectResource, SubjectListResource
from resources.schedules import ScheduleResource, ScheduleListResource
from flask_migrate import Migrate
from config.config import ConfigFlask
from models.base import db

app = Flask(__name__)
app.config.from_object(ConfigFlask)
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app, prefix='/api/v1')

api.add_resource(UserResource, '/users/<uuid:user_id>', endpoint='users')
api.add_resource(UserListResource, '/users/')
api.add_resource(LoginResource, '/login')
api.add_resource(LoginCallbackResource, '/login/callback', endpoint='callback')
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

swagger = Swagger(app, template=app.config.get('SWAGGER_TEMPLATE'))

if __name__ == '__main__':
    print("DEBUG: ", app.config.get('DEBUG'))
    app.run(host='0.0.0.0', debug=app.config.get('DEBUG'))