from flask_jwt_extended import JWTManager
import pytest
from flask import Flask
from flask_restful import Api
from config.config import ConfigFlask
from resources.login import LoginResource
from resources.logout import LogoutResource
from resources.pavilion import PavilionByNameResource, PavilionResource, PavilionListResource
from resources.register import RegisterResource
from resources.schedules import ScheduleListResource, ScheduleResource

@pytest.fixture
def app():
    """Create test flask app with test config"""
    app = Flask(__name__)
    app.config.from_object(ConfigFlask)
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    jwt = JWTManager(app)
    api = Api(app, prefix='/api/v1')
    api.add_resource(LoginResource, '/login')
    api.add_resource(LogoutResource, '/logout')
    api.add_resource(PavilionResource, '/pavilions/<string:id>')
    api.add_resource(PavilionByNameResource, '/pavilions/<string:name>')
    api.add_resource(PavilionListResource, '/pavilions/')
    api.add_resource(RegisterResource, '/register')
    api.add_resource(ScheduleListResource, '/user/schedules/')
    return app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()