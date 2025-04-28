import json
from unittest.mock import patch

from responses.register_response import RegisterErrorResponse, RegisterSuccessResponse
from tests.mocks.user_mock import create_mock_user


class TestRegisterResource:
    @patch('database.db.db.session')
    def test_register_success(self, mock_db_session, client):
        register_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = None
        response = client.post(
            '/api/v1/register',
            json=register_data
        )

        data = json.loads(response.data.decode())
        assert response.status_code == RegisterSuccessResponse.REGISTRATION_SUCCESS.value.get("status_code")
        assert data['message'] == RegisterSuccessResponse.REGISTRATION_SUCCESS.value.get("message")
        assert data['success'] is True

    def test_register_missing_credentials(self, client):
        register_data = {}
        response = client.post('/api/v1/register', json=register_data)
        data = json.loads(response.data.decode())
        assert response.status_code == RegisterErrorResponse.MISSING_CREDENTIALS.value.get("status_code")
        assert data['message'] == RegisterErrorResponse.MISSING_CREDENTIALS.value.get("message")
        assert data['success'] is False
    
    @patch('database.db.db.session')
    def test_register_existing_user(self, mock_db_session, client):
        register_data = {
            "email": "test@example.com",
            "password": "password123"
        }

        mock_user = create_mock_user(email=register_data['email'])
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_user
        
        response = client.post('/api/v1/register', json=register_data)
        data = json.loads(response.data.decode())

        assert response.status_code == RegisterErrorResponse.EMAIL_ALREADY_EXISTS.value.get("status_code")
        assert data['message'] == RegisterErrorResponse.EMAIL_ALREADY_EXISTS.value.get("message")
        assert data['success'] is False

    @patch('database.db.db.session')
    def test_register_server_error(self, mock_db_session, client):
        register_data = {
            "email": "test@example.com",
            "password": "password123"
        }

        mock_db_session.query.return_value.filter_by.return_value.first.return_value = None
        mock_db_session.add.side_effect = Exception("Database error")
        response = client.post('/api/v1/register', json=register_data)
        data = json.loads(response.data.decode())
        assert response.status_code == RegisterErrorResponse.UNEXPECTED_ERROR.value.get("status_code")
        assert data['error_code'] == RegisterErrorResponse.UNEXPECTED_ERROR.name
        assert data['message'] == RegisterErrorResponse.UNEXPECTED_ERROR.value.get("message")
        assert data['success'] is False
