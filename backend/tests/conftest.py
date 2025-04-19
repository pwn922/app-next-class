import pytest
from flask import Flask
from flask_restful import Api
from resources.pavilion import PavilionResource, PavilionListResource
from tests.mocks.pavilion_mock import create_mock_pavilion, create_mock_pavilion_list

@pytest.fixture
def app():
    """Create test flask app with test config"""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    api = Api(app)
    api.add_resource(PavilionListResource, '/api/v1/pavilions/')
    api.add_resource(PavilionResource, '/api/v1/pavilions/<uuid:id>')
    return app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()