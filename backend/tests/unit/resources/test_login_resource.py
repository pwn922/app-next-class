import json
from unittest.mock import patch
from responses.login_response import LoginSuccessResponse, LoginErrorResponse
from tests.mocks.user_mock import create_mock_user
from utils.security import generate_secure_password


class TestLoginResource:
    @patch('database.db.db.session')
    @patch('utils.security.verify_password')
    def test_login_success(self, mock_verify_password, mock_db_session, client):
        test_email = "test@example.com"
        test_password = "password123"
        hashed_password = generate_secure_password(test_password)
        
        mock_user = create_mock_user(email=test_email, password=hashed_password)
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_user
        mock_verify_password.return_value = True

        response = client.post(
            '/api/v1/login',
            json={
                "email": test_email,
                "password": test_password
            }
        )
        data = json.loads(response.data.decode())

        assert response.status_code == LoginSuccessResponse.LOGIN_SUCCESS.value.get("status_code")
        assert data['success'] is True
        assert 'access_token' in data['data']
        assert 'refresh_token' in data['data']

    @patch('database.db.db.session')
    def test_login_invalid_credentials(self, mock_db_session, client):
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = None

        response = client.post(
            '/api/v1/login',
            json={
                "email": "wrong@example.com",
                "password": "wrongpassword"
            }
        )
        data = json.loads(response.data.decode())

        assert response.status_code == LoginErrorResponse.INVALID_CREDENTIALS.value.get("status_code")
        assert data['success'] is False
        assert data['error_code'] == LoginErrorResponse.INVALID_CREDENTIALS.name

    
    def test_login_missing_fields(self, client):
        response = client.post(
            '/api/v1/login',
            json={
            }
        )
        data = json.loads(response.data.decode())

        assert response.status_code == LoginErrorResponse.INVALID_CREDENTIALS.value.get("status_code")
        assert data['success'] is False
        assert data['error_code'] == LoginErrorResponse.INVALID_CREDENTIALS.name
    
    def test_login_fields_as_a_list(self, client):
        response = client.post(
            '/api/v1/login',
            json={
                "email": [],
                "password": []
            }
        )
        data = json.loads(response.data.decode())

        assert response.status_code == LoginErrorResponse.INVALID_CREDENTIALS.value.get("status_code")
        assert data['success'] is False
        assert data['error_code'] == LoginErrorResponse.INVALID_CREDENTIALS.name
        assert data['message'] == LoginErrorResponse.INVALID_CREDENTIALS.value.get("message")

    def test_login_fields_empty(self, client):
        response = client.post(
            '/api/v1/login',
            json={
                "email": "",
                "password": ""
            }
        )
        data = json.loads(response.data.decode())

        assert response.status_code == LoginErrorResponse.INVALID_CREDENTIALS.value.get("status_code")
        assert data['success'] is False
        assert data['error_code'] == LoginErrorResponse.INVALID_CREDENTIALS.name
        assert data['message'] == LoginErrorResponse.INVALID_CREDENTIALS.value.get("message")

    @patch('database.db.db.session')
    @patch('utils.security.verify_password')
    def test_login_field_as_a_dict(self, mock_db_session, mock_verify_password, client):
        test_email = "test@example.com"
        test_password = "password123"
        hashed_password = generate_secure_password(test_password)
        mock_user = create_mock_user(email=test_email, password=hashed_password)
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_user
        mock_verify_password.return_value = False
        response = client.post(
            '/api/v1/login',
            json={
                "email": {"email": "test@example.com"},
                "password": {"password": "password123"}
            }
        )
        data = json.loads(response.data.decode())
        
        assert response.status_code == LoginErrorResponse.INVALID_CREDENTIALS.value.get("status_code")
        assert data['success'] is False
        assert data['error_code'] == LoginErrorResponse.INVALID_CREDENTIALS.name
        assert data['message'] == LoginErrorResponse.INVALID_CREDENTIALS.value.get("message")


    @patch('database.db.db.session')
    def test_login_server_error(self, mock_db_session, client):
        mock_db_session.query.side_effect = Exception("Database error")
        response = client.post(
            '/api/v1/login',
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )
        data = json.loads(response.data.decode())
       
        assert response.status_code == LoginErrorResponse.UNEXPECTED_ERROR.value.get("status_code")
        assert data['success'] is False
        assert data['error_code'] == LoginErrorResponse.UNEXPECTED_ERROR.name
        assert data['message'] == LoginErrorResponse.UNEXPECTED_ERROR.value.get("message")

    @patch('database.db.db.session')
    def test_login_invalid_field_as_a_number(self, mock_db_session, client):
        response = client.post(
            '/api/v1/login',
            json={
                "email": 123,
                "password": 456
            }
        )
        data = json.loads(response.data.decode())
        
        assert response.status_code == LoginErrorResponse.INVALID_CREDENTIALS.value.get("status_code")
        assert data['success'] is False
        assert data['error_code'] == LoginErrorResponse.INVALID_CREDENTIALS.name
        assert data['message'] == LoginErrorResponse.INVALID_CREDENTIALS.value.get("message")
