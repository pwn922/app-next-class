from flask import Flask
from flasgger import Swagger
from flask_restful import Api
from resources.login import LoginCallbackResource, LoginResource
from resources.user import UserResource
from flask_migrate import Migrate
from config.config import ConfigFlask
from models.base import db

app = Flask(__name__)
app.config.from_object(ConfigFlask)
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app, prefix='/api/v1')

api.add_resource(UserResource, '/users/<uuid:user_id>', endpoint='users')
api.add_resource(LoginResource, '/login')
api.add_resource(LoginCallbackResource, '/login/callback', endpoint='callback')
#api.add_resource(UserListResource, '/users')

from models.user import User
from models.classroom import Classroom

swagger = Swagger(app, template=app.config.get('SWAGGER_TEMPLATE'))

if __name__ == '__main__':
    print("DEBUG: ", app.config.get('DEBUG'))
    app.run(host='0.0.0.0', debug=app.config.get('DEBUG'))