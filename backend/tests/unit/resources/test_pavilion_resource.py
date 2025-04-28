import json
from unittest.mock import patch
from responses.pavilion_response import PavilionSuccessResponse, PavilionErrorResponse
from tests.mocks.pavilion_mock import create_mock_pavilion, create_mock_pavilion_list
import uuid


class TestPavilionResource:
    @patch('database.db.db.session')
    def test_get_pavilion_success(self, mock_db_session, client):
        mock_pavilion = create_mock_pavilion()
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_pavilion

        response = client.get(f'/api/v1/pavilions/{mock_pavilion.id}')
        data = json.loads(response.data.decode())

        assert response.status_code == PavilionSuccessResponse.RETRIEVED.value.get("status_code")
        assert data['success'] is True
        assert data['data']['name'] == mock_pavilion.name
        assert data['data']['x'] == mock_pavilion.x
        assert data['data']['y'] == mock_pavilion.y
        assert data['message'] == PavilionSuccessResponse.RETRIEVED.value.get("message")

    @patch('database.db.db.session')
    def test_get_pavilion_not_found(self, mock_db_session, client):
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = None
        test_id = uuid.uuid4()

        response = client.get(f'/api/v1/pavilions/{test_id}')
        data = json.loads(response.data.decode())

        assert response.status_code == PavilionErrorResponse.NOT_FOUND.value.get("status_code")
        assert data['success'] is False
        assert data['message'] == PavilionErrorResponse.NOT_FOUND.value.get("message")

    @patch('database.db.db.session')
    def test_create_pavilion_success(self, mock_db_session, client):
        pavilion_data = {
            "name": "Aula Test",
            "x": 10,
            "y": 20
        }

        response = client.post('/api/v1/pavilions/', json=pavilion_data)
        data = json.loads(response.data.decode())

        assert data["success"] is True
        assert data["message"] == PavilionSuccessResponse.CREATED.value.get("message")
        assert data["data"]["name"] == pavilion_data["name"].upper()
        assert data["data"]["x"] == pavilion_data["x"]
        assert data["data"]["y"] == pavilion_data["y"]
    
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()

    def test_create_pavilion_missing_fields(self, client):
        pavilion_data = {}

        response = client.post(
            '/api/v1/pavilions/',
            json=pavilion_data,
            content_type='application/json'
        )
        data = json.loads(response.data.decode())

        assert response.status_code == PavilionErrorResponse.MISSING_FIELDS.value.get("status_code")
        assert data['success'] is False
        assert data['message'] == PavilionErrorResponse.MISSING_FIELDS.value.get("message")

    @patch('database.db.db.session')
    def test_update_pavilion_success(self, mock_db_session, client):
        mock_pavilion = create_mock_pavilion()
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_pavilion

        update_pavilion_data = {
            "name": "Updated Pavilion",
            "x": 35.0,
            "y": 45.0
        }

        response = client.put(
            f'/api/v1/pavilions/{mock_pavilion.id}',
            json=update_pavilion_data,
            content_type='application/json'
        )
        data = json.loads(response.data.decode())

        assert response.status_code == 200
        assert data['success'] is True
        assert data['data']['name'] == update_pavilion_data['name']
        assert data['data']['x'] == update_pavilion_data['x']
        assert data['data']['y'] == update_pavilion_data['y']
        mock_db_session.commit.assert_called_once()
        
    @patch('database.db.db.session')
    def test_delete_pavilion_success(self, mock_db_session, app, client):
        mock_pavilion = create_mock_pavilion()
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_pavilion

        response = client.delete(f'/api/v1/pavilions/{mock_pavilion.id}')
        
        assert response.status_code == PavilionSuccessResponse.DELETED.value.get("status_code")
        mock_db_session.delete.assert_called_once()
        mock_db_session.commit.assert_called_once()

    @patch('database.db.db.session')
    def test_get_all_pavilions_success(self, mock_db_session, app, client):
        mock_pavilions = create_mock_pavilion_list()
        mock_db_session.query.return_value.all.return_value = mock_pavilions

        response = client.get('/api/v1/pavilions/')
        data = json.loads(response.data.decode())

        assert response.status_code == PavilionSuccessResponse.LIST_RETRIEVED.value.get("status_code")
        assert data['success'] is True
        assert len(data['data']) == len(mock_pavilions)
        for i, pavilion in enumerate(data['data']):
            assert pavilion['name'] == mock_pavilions[i].name
            assert pavilion['x'] == mock_pavilions[i].x
            assert pavilion['y'] == mock_pavilions[i].y

    @patch('database.db.db.session')
    def test_get_pavilion_by_name_success(self, mock_db_session, client):
        mock_pavilion = create_mock_pavilion(name="xd")
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_pavilion
        
        response = client.get(f'/api/v1/pavilions/{mock_pavilion.name}')
        data = json.loads(response.data.decode())

        assert response.status_code == PavilionSuccessResponse.RETRIEVED.value.get("status_code")
        assert data['success'] is True
        assert data['data']['name'] == mock_pavilion.name
        assert data['data']['x'] == mock_pavilion.x
        assert data['data']['y'] == mock_pavilion.y

    @patch('database.db.db.session')
    def test_get_pavilion_by_name_not_found(self, mock_db_session, client):
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = None

        response = client.get('/api/v1/pavilions/non_existent_pavilion')
        data = json.loads(response.data.decode())

        assert response.status_code == PavilionErrorResponse.NOT_FOUND.value.get("status_code")
        assert data['success'] is False
        assert data['message'] == PavilionErrorResponse.NOT_FOUND.value.get("message")
        assert data['error_code'] == PavilionErrorResponse.NOT_FOUND.name
